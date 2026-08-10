from datetime import datetime, timezone
from pydantic import BaseModel, Field
from enum import Enum
from langchain_core.messages import BaseMessage
from typing import List, Optional, Dict, Any, Literal, TypedDict


class DocumentChunk(BaseModel):
    """Represents a chunk of document content"""
    doc_id: str = Field(description="Document identifier")
    content: str = Field(description="The actual text content")
    metadata: Dict[str, Any] = Field(default_factory=lambda: dict, description="Additional metadata")
    relevance_score: float = Field(default=0.0, description="Relevance score for retrieval")

class SummarizationResponse(BaseModel):
    """Structured response for summarization tasks"""
    original_length: int = Field(description="Length of original text")
    summary: str = Field(description="The generated summary")
    key_points: List[str] = Field(description="List of key points extracted")
    document_ids: List[str] = Field(default_factory=lambda: list, description="Documents summarized")
    timestamp: datetime = Field(default_factory=datetime.now)


class CalculationResponse(BaseModel):
    """Structured response for calculation tasks"""
    expression: str = Field(description="The mathematical expression")
    result: float = Field(description="The calculated result")
    explanation: str = Field(description="Step-by-step explanation")
    units: Optional[str] = Field(default=None, description="Units if applicable")
    timestamp: datetime = Field(default_factory=datetime.now)


class UpdateMemoryResponse(BaseModel):
    """Response after updating memory"""
    summary: str = Field(description="Summary of the conversation up to this point")
    document_ids: List[str] = Field(default_factory=lambda: list, description="List of documents ids that are relevant to the users last message")


class AnswerResponse(BaseModel):
    """
    Structured response schema for document Q&A.

    Ensures consistent formatting of answers and tracks
    referenced source documents.
    """

    question: str = Field(
        description="The original user question"
    )

    answer: str = Field(
        description="The generated answer"
    )

    sources: list[str] = Field(
        default_factory=list,
        description="List of source document IDs used to generate the answer"
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the response was generated"
    )

class IntentType(str, Enum):
    QA = "qa"
    SUMMARIZATION = "summarization"
    CALCULATION = "calculation"
    UNKNOWN = "unknown"


class UserIntent(BaseModel):
    """
    Represents the classified intent of a user request.
    
    Used by the LangGraph router to determine
    which agent should handle the request.
    """

    intent_type: IntentType = Field(
        description=(
            "The classified user intent: "
            "qa, summarization, calculation, or unknown"
        )
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score for the intent classification between 0 and 1"
    )

    reasoning: str = Field(
        description="Explanation for why this intent was selected"
    )

class SessionState(BaseModel):
    """Session state"""
    session_id: str
    user_id: str
    # conversation_history: List[TypedDict] = Field(default_factory=lambda: list)
    # document_context: List[str] = Field(default_factory=lambda: list, description="Active document IDs")
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    document_context: List[str] = Field(default_factory=list, description="Active document IDs")
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
