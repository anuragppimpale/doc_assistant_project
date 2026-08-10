# README Template

Below is a template provided for use when building your README file for students.

# Project Title

Document Assistant Project - Udacity

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

Run uv venv command to create a virtual environment.
Activate the virtual environment.
Run uv sync command to install dependencies from pyproject.toml file OR run pip install -r requirements.txt
Create and edit .env using .env.example and set OPENAI_API_KEY
Run this command to start the assistent - python main.py

## Testing

Explain the steps needed to run any automated tests

### Break Down Tests

Following are the terminal logs of running the project:

(ai313) PS C:\data\technology\workspaces\langchain\doc_assistant_project> & C:\data\technology\anaconda\anaconda3\envs\ai313\python.exe c:/data/technology/workspaces/langchain/doc_assistant_project/main.py

============================================================
DocDacity Intelligent Document Assistant
============================================================

 INITIALIZING ASSISTANT...
Enter your user ID (or press Enter for 'demo_user'): 
Started new session dcf22bb0-5deb-4ddf-b2af-40762c5c7ee0
Session started: dcf22bb0-5deb-4ddf-b2af-40762c5c7ee0

AVAILABLE COMMANDS:
  /help     - Show this help message
  /docs     - List available documents
  /quit     - Exit the assistant

Example queries:
  - What's the total amount in invoice INV-001?
  - Summarize all contracts
  - Calculate the sum of all invoice totals
  - Find documents with amounts over $50,000


Enter Message: hello

Processing...

🤖 Assistant: Returning structured response: question='hello' answer='Hello! How can I assist you today with your financial or healthcare documents?' sources=[] confidence=1.0 timestamp=datetime.datetime(2026, 8, 10, 21, 39, 35, 635980, tzinfo=datetime.timezone.utc)

INTENT: IntentType.UNKNOWN

TOOLS USED: AnswerResponse

CONVERSATION SUMMARY: The assistant greeted the user and offered help with financial or healthcare documents.

Enter Message: calculate 3 + 5 + 9

Processing...
Deserializing unregistered type schemas.IntentType from checkpoint. This will be blocked in a future version. Set LANGGRAPH_STRICT_MSGPACK=true to block now, or add to allowed_msgpack_modules to allow explicitly: [('schemas', 'IntentType')]
Deserializing unregistered type schemas.UserIntent from checkpoint. This will be blocked in a future version. Set LANGGRAPH_STRICT_MSGPACK=true to block now, or add to allowed_msgpack_modules to allow explicitly: [('schemas', 'UserIntent')]
Deserializing unregistered type schemas.AnswerResponse from checkpoint. This will be blocked in a future version. Set LANGGRAPH_STRICT_MSGPACK=true to block now, or add to allowed_msgpack_modules to allow explicitly: [('schemas', 'AnswerResponse')]

🤖 Assistant: Returning structured response: question='calculate 3 + 5 + 9' answer='The result of the calculation 3 + 5 + 9 is 17.' sources=[] confidence=1.0 timestamp=datetime.datetime(2026, 8, 10, 21, 43, 53, 62137, tzinfo=datetime.timezone.utc)

INTENT: IntentType.CALCULATION

TOOLS USED: AnswerResponse, calculator, AnswerResponse

CONVERSATION SUMMARY: The user greeted the assistant and requested a simple arithmetic calculation of 3 + 5 + 9, which was calculated tobe 17.

Enter Message: What's the total amount in invoice INV-001?

Processing...

🤖 Assistant: Returning structured response: question="What's the total amount in invoice INV-001?" answer='The total amount in invoice INV-001 is $22,000, which includes a subtotal of $20,000 and a tax of $2,000.' sources=['INV-001'] confidence=1.0 timestamp=datetime.datetime(2026, 8, 10, 21, 44, 43, 44527, tzinfo=datetime.timezone.utc)

INTENT: IntentType.CALCULATION

TOOLS USED: AnswerResponse, calculator, AnswerResponse, document_reader, AnswerResponse

CONVERSATION SUMMARY: The user greeted the assistant and requested a simple arithmetic calculation of 3 + 5 + 9, which resulted in 17. The user then asked for the total amount in invoice INV-001. The assistant retrieved the document and found that the total amount is $22,000, including a subtotal of $20,000 and a tax of $2,000.

Enter Message: /quit

Goodbye!
(ai313) PS C:\data\technology\workspaces\langchain\doc_assistant_project> 


## Project Instructions

This section should contain all the student deliverables for this project.

## Built With

* [Item1](www.item1.com) - Description of item
* [Item2](www.item2.com) - Description of item
* [Item3](www.item3.com) - Description of item

Include all items used to build project.

## License
[License](../LICENSE.md)
