#  Doc Assistent

DocDacity Intelligent Document Assistant

## Architecture
![Document Assistant Architecture](docs/images/langgraph_agent_architecture.png)

## Getting Started

Instructions for how to get a copy of the project running on your local machine.

Use Python version 3.13.14
Install libraries specified in requirements.txt

### Dependencies

langgraph
langgraph-prebuilt
langgraph-sdk
langgraph-checkpoint-sqlite
langsmith>=0.7.31
langchain-community
langchain-core>=1.2.28
langchain-openai>=1.1.14
langchain-ollama
langchain-text-splitters>=1.1.2
notebook
langchain-tavily
wikipedia
trustcall
langgraph-cli[inmem]

aiohttp>=3.13.4
Pygments>=2.20.0
cryptography>=46.0.7
grandalf
print-color>=0.4.6

### Installation

Run uv venv command to create a virtual envirnment.
Activate the virtual environment.
Run uv sync command to install dependencies from pyproject.toml file OR run pip install -r requirements.txt
Create and edit env using .env.example and set OPENAI_API_KEY
Run this command to start the assistent - python main.py

## Testing
### Break Down Tests

Following are the terminal logs of running the project:
Command to run the project followed by the logs:

 PS C:\data\technology\workspaces\langchain\doc_assistant_project>  c:; cd 'c:\data\technology\workspaces\langchain\doc_assistant_project'; & 'C:\data\technology\anaconda\anaconda3\envs\ai313\python.exe' 'c:\Users\anurag\.vscode\extensions\ms-python.debugpy-2026.6.0-win32-x64\bundled\libs\debugpy\launcher' '56264' '--' 'c:\data\technology\workspaces\langchain\doc_assistant_project\main.py' 

============================================================
DocDacity Intelligent Document Assistant
============================================================

 INITIALIZING ASSISTANT...
Enter your user ID (or press Enter for 'demo_user'): 
Started new session 7e15b3cc-a046-482c-9b56-8de4caef1822
Session started: 7e15b3cc-a046-482c-9b56-8de4caef1822

AVAILABLE COMMANDS:
  /help     - Show this help message
  /docs     - List available documents
  /quit     - Exit the assistant

Example queries:
  - What's the total amount in invoice INV-001?
  - Summarize all contracts
  - Calculate the sum of all invoice totals
  - Find documents with amounts over $50,000


#### Following test demonstrates IntentType=QA and tool=document_reader

Enter Message: Who is the client on INV-002?

Processing...

🤖 Assistant: The client on INV-002 is TechStart Inc.

INTENT: IntentType.QA

SOURCES: INV-002

TOOLS USED: document_reader

CONVERSATION SUMMARY: The client on invoice INV-002 is TechStart Inc. The invoice details include a total amount of $69,300, with products listed as EnterpriseLicense, Implementation Services, and Training Package. A discount and tax are applied to the subtotal.

#### Following test demonstrates IntentType=SUMMARIZATION and tool=document_search, document_reader
Enter Message: Summarize all contracts

Processing...

🤖 Assistant: The Service Agreement (Document ID: CON-001) is a contract between DocDacity Solutions Inc. and Healthcare Partners LLC, effective from January 1, 2024. It includes services such as access to a document processing platform, 24/7 technical support, monthly data analytics reports, and compliance monitoring. The contract is valued at $180,000 over a 12-month period, with a monthly fee of $15,000. Either party can terminate the agreement with a 60-day written notice.

INTENT: IntentType.SUMMARIZATION

SOURCES: INV-002, CON-001

TOOLS USED: document_reader, document_search, document_reader

CONVERSATION SUMMARY: The conversation involved identifying the client on invoice INV-002, which is TechStart Inc. The invoice details a total amount due of $69,300 for services including an enterprise license, implementation services, and a training package. Additionally, a service contract (CON-001) was summarized, which is between DocDacity Solutions Inc. and Healthcare Partners LLC, effective January 1, 2024. The contract covers document processing, technical support, data analytics, and compliance monitoring, valued at $180,000 over 12 months, with a monthly fee of $15,000. Termination requires a 60-day notice.

#### Following test demonstrates IntentType=QA and tool=document_search, document_reader
Enter Message: Find documents with amounts over $50,000

Processing...

🤖 Assistant: The document with an amount over $50,000 is Invoice #12346 (Document ID: INV-002) with a total amount of $69,300.00.

INTENT: IntentType.QA

SOURCES: INV-002, CON-001

TOOLS USED: document_reader, document_search, document_reader, document_search

CONVERSATION SUMMARY: The conversation involved inquiries about specific financial documents. The client on Invoice #12346 (Document ID: INV-002) is TechStart Inc., with a total amount of $69,300.00. Additionally, a Service Agreement (Document ID: CON-001) was summarized, detailing a contract between DocDacity Solutions Inc. and Healthcare Partners LLC, valued at $180,000 over 12 months. The user also requested documents with amounts over $50,000, and Invoice #12346 was identified as such a document.

#### Following test demonstrates IntentType=QA and tool=document_search, document_reader, document_statistics
Enter Message: Show me collection statistics

Processing...

🤖 Assistant: The document collection contains a total of 5 documents, with 4 of them having associated amounts. The breakdown by document type is as follows:
- Invoices: 3
- Contracts: 1
- Claims: 1

Financial Summary:
- Total Amount: $466,250.00
- Average Amount: $116,562.50
- Minimum Amount: $2,450.00
- Maximum Amount: $214,500.00

INTENT: IntentType.QA

SOURCES: INV-002, CON-001

TOOLS USED: document_reader, document_search, document_reader, document_search, document_statistics

CONVERSATION SUMMARY: The conversation involved inquiries about specific documents and their details. The client on Invoice #12346 (Document ID: INV-002) is TechStart Inc. A Service Agreement (Document ID: CON-001) was summarized, detailing a contract between DocDacity Solutions Inc. and Healthcare Partners LLC, valued at $180,000 over 12 months. A search for documents with amounts over $50,000 identified Invoice #12346 with a total of $69,300. Collection statistics revealed5 documents in total, with 4 having amounts, including 3 invoices, 1 contract, and 1 claim, with a total financial amount of $466,250.00.

#### Following test demonstrates IntentType=CALCULATION and tool=document_search, document_reader, document_statistics, calculator
Enter Message: What is the combined total of INV-002 and INV-003?

Processing...

🤖 Assistant: 283800.0

INTENT: IntentType.CALCULATION

SOURCES: INV-002, CON-001, INV-003

TOOLS USED: document_reader, document_search, document_reader, document_search, document_statistics, document_reader, document_reader, calculator

CONVERSATION SUMMARY: The conversation involved inquiries about specific financial documents and their details. The client on Invoice INV-002 is TechStart Inc.A Service Agreement (Document ID: CON-001) was summarized, detailing a contract between DocDacity Solutions Inc. and Healthcare Partners LLC, valued at $180,000 over 12 months. The user requested documents with amounts over $50,000, identifying Invoice INV-002 with an amount of $69,300. Collection statistics were provided, showing a total of 5 documents with a combined financial total of $466,250. Finally, the combined total of INV-002 and INV-003 was calculated to be $283,800.

#### Following test demonstrates Memory and IntentType=CALCULATION and tool=document_search, document_reader, document_statistics, calculator
Enter Message: And what was the tax on the first one?

Processing...

🤖 Assistant: The tax on INV-002 was $6,300.00.

INTENT: IntentType.QA

SOURCES: INV-002, CON-001, INV-003

TOOLS USED: document_reader, document_search, document_reader, document_search, document_statistics, document_reader, document_reader, calculator

CONVERSATION SUMMARY: The conversation involved inquiries about specific financial documents, including invoices and contracts. Key topics included identifyingthe client on Invoice INV-002, which was TechStart Inc., and summarizing a service agreement contract (CON-001) between DocDacity Solutions Inc. and HealthcarePartners LLC. The user also requested documents with amounts over $50,000, resulting in the identification of Invoice INV-002. Collection statistics were provided, showing a total of 5 documents with a combined financial total of $466,250.00. The user asked for the combined total of INV-002 and INV-003, which was calculated to be $283,800.00. Additionally, the tax on INV-002 was confirmed to be $6,300.00.

#### Following test demonstrates IntentType=UNKNOWN
Enter Message: tell me a joke about python

Processing...

🤖 Assistant: Why do Python programmers prefer dark mode?

Because light attracts bugs!

INTENT: IntentType.UNKNOWN

SOURCES: INV-002, CON-001, INV-003

TOOLS USED: document_reader, document_search, document_reader, document_search, document_statistics, document_reader, document_reader, calculator

CONVERSATION SUMMARY: The conversation involved inquiries about specific financial documents, particularly invoices and contracts. The user asked about the client on Invoice INV-002, which was identified as TechStart Inc. The user also requested a summary of all contracts, leading to the retrieval of a Service Agreement (CON-001) between DocDacity Solutions Inc. and Healthcare Partners LLC, valued at $180,000 over 12 months. Additionally, the user inquired about documents with amounts over $50,000, resulting in the identification of Invoice INV-002 with a total of $69,300. The user also asked for collection statistics, which revealed a total of 5 documents with a combined amount of $466,250. Finally, the user requested the combined total of INV-002 and INV-003, calculated to be $283,800, and the tax on INV-002, which was $6,300.

Enter Message: /quit

Goodbye!


## Project Instructions

## Built With

* langgraph
* langgraph-prebuilt
* langgraph-sdk
* langgraph-checkpoint-sqlite
* langsmith>=0.7.31
* langchain-community
* langchain-core>=1.2.28
* langchain-openai>=1.1.14
* langchain-ollama
* langchain-text-splitters>=1.1.2
* notebook
* langchain-tavily
* wikipedia
* trustcall
* langgraph-cli[inmem]
* aiohttp>=3.13.4
* Pygments>=2.20.0
* cryptography>=46.0.7
* grandalf
* print-color>=0.4.6

## Implementation Decisions
First of all, UserIntent is determined by passing UserInput to LLM. This is done so that our classify_intent function in agent.py can effectively classify agent along with structured responses for next steps.

LLM uses following structured responses.:
* AnswerResponse - Used for QA and UKNOWN intent
* SummarizationResponse - Used for Summarization intent
* CalculationResponse - Used for Calculation intent

SimulatedRetriever uses in-memory sample documents instead of a vector store to avoid additional complexity of integrating with the Vector DB.

Calculator tool uses regex to confirm if its a valid mathematical expression. This is to avoid runtime errors in case LLM produces incorrect mathematical expression for the calculator tool

UKNOWN intent fallback on QA. 

LLM - gpt-4o is used because it is sufficient for the usecase. Consise responses are required from LLM, so the temperature is set to 0.1

## State and Memory
The Document Assistant uses two layers of state and memory:

* AgentState and checkpointer — maintains the state of an active conversation while the application is running.
* Session JSON files — provide persistent session storage that survives application/process restarts.

AgentState uses the following fields
* user_input: Current user input
* messages: List of HumanMessage, AIMessage, ToolMessage. It uses the add_messages reducer.
* intent: UserIntent determined by LLM based on UserInput
* next_step: Used for routing request to the correct agent based on the intent
* conversation_summary: Summary of all messages exchanged in the session.
* active_documents: List of documents in the current execution
* current_response: Response to the cuurent request
* tools_used: List of tools used by current execution
* session_id: Current session id
* user_id: Current user id
* actions_taken: Action taken by the current execution. It uses operator.add reducer.
  



