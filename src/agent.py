import operator
from typing import TypedDict, Annotated, List, Dict, Any, Optional, Literal
from langgraph.graph.message import add_messages
from langchain.agents import create_agent
from prompt_toolkit import prompt
from schemas import UserIntent, AnswerResponse, UpdateMemoryResponse
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from prompts import get_intent_classification_prompt, get_chat_prompt_template, MEMORY_SUMMARY_PROMPT
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver

class AgentState(TypedDict):
    """
    The agent state object
    """
    # Current conversation
    user_input: Optional[str]
    messages: Annotated[List[BaseMessage], add_messages]

    # Intent and routing
    intent: Optional[UserIntent]
    next_step: str

    # Memory and context
    conversation_summary: str
    active_documents: Optional[List[str]]

    # Current task state
    current_response: Optional[Dict[str, Any]]
    tools_used: List[str]

    # Session management
    session_id: Optional[str]
    user_id: Optional[str]

    actions_taken: Annotated[List[str], operator.add]

def classify_intent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Classify user intent and update next_step. Also records that this
    function executed by appending "classify_intent" to actions_taken.
    """

    llm = config.get("configurable").get("llm")
    history = state.get("messages", [])
 
    llm = llm.with_structured_output(UserIntent)

    prompt_template = get_intent_classification_prompt()
    conversation_history = "\n".join(
        f"{message.type}: {message.content}" for message in history
    )
    prompt = prompt_template.format(
        user_input=state.get("user_input", ""),
        conversation_history=conversation_history,
    )

    intent = llm.invoke(prompt)

    if intent.intent_type == "summarization":
        next_step = "summarization"
    elif intent.intent_type == "calculation":
        next_step = "calculation"
    else:
        next_step = "qa"

    return {
        "actions_taken": ["classify_intent"],
        "intent": intent,
        "next_step": next_step
    }

def qa_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Handle Q&A tasks and record the action.
    """
    llm = config.get("configurable").get("llm")
    tools = config.get("configurable").get("tools")

    prompt_template = get_chat_prompt_template("qa")

    messages = prompt_template.invoke({
        "input": state["user_input"],
        "chat_history": state.get("messages", []),
    }).to_messages()

    result, tools_used = invoke_agent(AnswerResponse, messages, llm, tools)

    return {
        "messages": result.get("messages", []),
        "actions_taken": ["qa_agent"],
        "current_response": result,
        "tools_used": tools_used,
        "next_step": "update_memory",
    }


def summarization_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Handle summarization tasks and record the action.
    """

    llm = config.get("configurable").get("llm")
    tools = config.get("configurable").get("tools")

    prompt_template = get_chat_prompt_template("summarization")

    messages = prompt_template.invoke({
        "input": state["user_input"],
        "chat_history": state.get("messages", []),
    }).to_messages()

    result, tools_used = invoke_agent(AnswerResponse, messages, llm, tools)

    return {
        "messages": result.get("messages", []),
        "actions_taken": ["summarization_agent"],
        "current_response": result,
        "tools_used": tools_used,
        "next_step": "update_memory",
    }


def calculation_agent(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Handle calculation tasks and record the action.
    """

    llm = config.get("configurable").get("llm")
    tools = config.get("configurable").get("tools")

    prompt_template = get_chat_prompt_template("calculation")

    messages = prompt_template.invoke({
        "input": state["user_input"],
        "chat_history": state.get("messages", []),
    }).to_messages()

    result, tools_used = invoke_agent(AnswerResponse, messages, llm, tools)

    return {
        "messages": result.get("messages", []),
        "actions_taken": ["calculation_agent"],
        "current_response": result,
        "tools_used": tools_used,
        "next_step": "update_memory",
    }
    

def invoke_agent(response_schema: type[BaseModel], messages: List[BaseMessage], llm, tools) -> tuple[
Dict[str, Any], List[str]]:
    llm_with_tools = llm.bind_tools(
        tools
    )

    agent = create_agent(
        model=llm_with_tools,  # Use the bound model
        tools=tools,
        response_format=response_schema,
    )

    result = agent.invoke({"messages": messages})
    tools_used = [t.name for t in result.get("messages", []) if isinstance(t, ToolMessage)]

    return result, tools_used

def update_memory(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Update conversation memory and record the action.
    """

    llm = config.get("configurable").get("llm")
    # tools = config.get("configurable").get("tools")

    prompt_with_history = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(MEMORY_SUMMARY_PROMPT),
        MessagesPlaceholder("chat_history"),
    ]).invoke({
        "chat_history": state.get("messages", []),
    })

    structured_llm = llm.with_structured_output(
        UpdateMemoryResponse
    )

    response = structured_llm.invoke(prompt_with_history)
    return {
        "conversation_summary":  response.summary,
        "active_documents":  response.document_ids,
        "next_step":  "end"
    }

def should_continue(state: AgentState) -> str:
    """Router function"""
    return state.get("next_step", "end")

# TODO: Complete the create_workflow function. Refer to README.md Task 2.5
def create_workflow(llm, tools):
    """
    Creates the LangGraph agents.
    Compiles the workflow with an InMemorySaver checkpointer to persist state.
    """
    workflow = StateGraph(AgentState)

    # TODO: Add all the nodes to the workflow by calling workflow.add_node(...)
    workflow.add_node("classify_intent", classify_intent, config={"configurable": {"llm": llm}})
    workflow.add_node("qa_agent", qa_agent, config={"configurable": {"llm": llm, "tools": tools}})
    workflow.add_node("summarization_agent", summarization_agent, config={"configurable": {"llm": llm, "tools": tools}})
    workflow.add_node("calculation_agent", calculation_agent, config={"configurable": {"llm": llm, "tools": tools}})
    workflow.add_node("update_memory", update_memory, config={"configurable": {"llm": llm}})


    workflow.set_entry_point("classify_intent")
    workflow.add_conditional_edges(
        "classify_intent",
        should_continue,
        {
            "qa": "qa_agent",
            "summarization": "summarization_agent",
            "calculation": "calculation_agent",
            "unknown": "qa_agent",
            "end": END
        }
    )


    # qa_agent -> update_memory
    workflow.add_edge("qa_agent", "update_memory")
    # summarization_agent -> update_memory
    workflow.add_edge("summarization_agent", "update_memory")
    # calculation_agent -> update_memory
    workflow.add_edge("calculation_agent", "update_memory")

    workflow.add_edge("update_memory", END)

    checkpointer = InMemorySaver()
    return workflow.compile(checkpointer=checkpointer)
