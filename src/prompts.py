
from langchain_core.prompts import FewShotPromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, PromptTemplate, SystemMessagePromptTemplate


def get_intent_classification_prompt() -> FewShotPromptTemplate:
    """
    Get the intent classification prompt template.
    """
    intent_examples = [
        {
            "user_input": "What's the total amount in invoice INV-001?",
            "intent": "qa",
            "confidence": "0.98",
            "reasoning": (
                "The user is asking for a specific factual value from the document and no calculation is required."
            ),
        },
        {
            "user_input": "Who is the client on INV-002?",
            "intent": "qa",
            "confidence": "0.98",
            "reasoning": (
                "The user is asking for a specific piece of information contained in the document."
            ),
        },
        {
            "user_input": "Give me the key points of CON-001",
            "intent": "summarization",
            "confidence": "0.88",
            "reasoning": (
                "The user is asking to identify and extract the main points from the document."
            ),
        },
        {
            "user_input": "Summarize all contracts",
            "intent": "summarization",
            "confidence": "0.80",
            "reasoning": (
                "The user explicitly asks for a summary of the document rather than a specific fact or calculation."
            ),
        },
        {
            "user_input": "What was the percentage increase in revenue from 2024 to 2025?",
            "intent": "calculation",
            "confidence": "0.99",
            "reasoning": (
                "The user is asking for a percentage change, which requires a mathematical calculation using values from the document."
            ),
        },
        {
            "user_input": "What is the combined total of all invoices?",
            "intent": "calculation",
            "confidence": "0.99",
            "reasoning": (
                "The user explicitly requests a mathematical calculation using numerical information from the document."
            ),
        },
        {
            "user_input": "Tell me something interesting.",
            "intent": "unknown",
            "confidence": "0.15",
            "reasoning": (
                "The request is too vague to determine whether the user wants a document question, summary, or calculation."
            ),
        },
    ]
    example_prompt = PromptTemplate(
        input_variables=[
            "user_input",
            "intent",
            "confidence",
            "reasoning",
        ],
        template="""User Input: {user_input}
    Intent: {intent}
    Confidence: {confidence}
    Reasoning: {reasoning}""",
    )
    return FewShotPromptTemplate(
    examples=intent_examples,
    example_prompt=example_prompt,

    prefix="""You are an intent classifier for a document processing assistant.

Your task is to classify the user's request into exactly one of these
intent categories:

- qa: Questions about documents or records that do not require calculations. Retrieving a fact, figure, date, or party that is already stated in a document, including totals printed on the document.
- summarization: Requests to summarize or extract key points from documents that do not require calculations. Condensing one or more documents into key points.
- calculation: Mathematical operations or numerical computations, OR questions about documents that require calculations. The answer requires arithmetic that is not already printed — sums across multiple documents, percentages, differences, or standalone math.
- unknown: The intent cannot be reliably determined. Greetings, small talk, or requests where no category applies.

Classification rules:

1. Choose "calculation" whenever answering the request requires a
   mathematical calculation, even if the request also involves
   document questions or summarization.

2. Choose "qa" when the user wants a specific fact, value, entity,
   or piece of information from the document and no calculation
   is required.

3. Choose "summarization" when the user wants a summary, overview,
   key points, findings, risks, or other condensed representation
   of document content and no calculation is required.

4. Choose "unknown" when the request is too vague, ambiguous, or
   does not clearly fit any of the above categories.

Confidence scoring:

Confidence represents your certainty that the selected INTENT is correct,
given the user input and available conversation history.

It does NOT represent confidence that the eventual answer will be correct.

Use the following scale:

- 0.90-1.00: Very high confidence. The intent is explicit and there is
  little or no plausible alternative.

- 0.75-0.89: High confidence. The intent is clear, with only minor
  ambiguity.

- 0.50-0.74: Moderate confidence. The selected intent is plausible,
  but another intent is reasonably possible.

- 0.25-0.49: Low confidence. The request is significantly ambiguous
  and multiple intents are plausible.

- 0.00-0.24: Very low confidence. There is insufficient information
  to reliably determine the intent.

When the intent cannot be reliably determined, use "unknown".
When intent is "unknown", confidence should normally be below 0.50.

Use the conversation history to resolve references such as "it",
"that report", "the previous document", or "calculate that".

Here are examples of correctly classified requests:

""",

    suffix="""

Now classify the following user request.

User Input:
{user_input}

Recent Conversation History:
{conversation_history}

Determine the single best intent category.

Return:
- intent_type: qa, summarization, calculation, or unknown
- confidence: a value between 0.0 and 1.0 following the confidence
  scoring guidelines above
- reasoning: a brief explanation supporting the classification
""",

    input_variables=[
        "user_input",
        "conversation_history",
    ],
)

# Q&A System Prompt
QA_SYSTEM_PROMPT = """You are a helpful document assistant specializing in answering questions about financial and healthcare documents.

Your capabilities:
- Answer specific questions about document content
- Cite sources accurately
- Provide clear, concise answers
- Use available tools to search and read documents

Guidelines:
1. Always search for relevant documents before answering
2. Cite specific document IDs when referencing information
3. If information is not found, say so clearly
4. Be precise with numbers and dates
5. Maintain professional tone

"""

# Summarization System Prompt
SUMMARIZATION_SYSTEM_PROMPT = """You are an expert document summarizer specializing in financial and healthcare documents.

Your approach:
- Extract key information and main points
- Organize summaries logically
- Highlight important numbers, dates, and parties
- Keep summaries concise but comprehensive

Guidelines:
1. First search for and read the relevant documents
2. Structure summaries with clear sections
3. Include document IDs in your summary
4. Focus on actionable information
"""

# Calculation System Prompt
CALCULATION_SYSTEM_PROMPT = """You are an expert calculation assistant for financial and healthcare documents.

Your approach:
- Determine which document contains the information needed for the calculation.
- Retrieve the relevant document using the document reader tool before calculating.
- Identify the mathematical expression required by the user's request.
- Use the calculator tool to perform every calculation, no matter how simple.

Guidelines:
1. Do not calculate values yourself; always use the calculator tool.
2. Use only information retrieved from the relevant documents when a calculation depends on document content.
3. Clearly explain the inputs, formula, and result.
4. Cite the relevant document IDs in your response.
5. If the required information is unavailable, say so clearly.
"""


def get_chat_prompt_template(intent_type: str) -> ChatPromptTemplate:
    """
    Get the appropriate chat prompt template based on intent.
    """
    if intent_type == "qa":
        system_prompt = QA_SYSTEM_PROMPT
    elif intent_type ==  "summarization":
        system_prompt =  SUMMARIZATION_SYSTEM_PROMPT
    elif intent_type ==  "calculation":
        system_prompt = CALCULATION_SYSTEM_PROMPT
    else:
        system_prompt = QA_SYSTEM_PROMPT  # Default fallback

    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        MessagesPlaceholder("chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])


# Memory Summary Prompt
MEMORY_SUMMARY_PROMPT = """Summarize the following conversation history into a concise summary:

Focus on:
- Key topics discussed
- Documents referenced
- Important findings or calculations
- Any unresolved questions
"""
