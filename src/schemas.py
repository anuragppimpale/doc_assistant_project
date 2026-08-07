from datetime import datetime, timezone
from pydantic import BaseModel, Field
from enum import Enum


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