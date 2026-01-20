"""Request and response schemas for the chatbot API."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single chat message."""

    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str = Field(..., description="User message to send to the chatbot")
    conversation_id: Optional[str] = Field(
        None, description="Optional conversation ID for context"
    )


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""

    message: str = Field(..., description="Assistant response")
    conversation_id: str = Field(..., description="Conversation ID for follow-up")
    sources: Optional[List[str]] = Field(
        None, description="Sources used in the response"
    )


class ConversationHistory(BaseModel):
    """Conversation history response."""

    conversation_id: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    version: str = "0.1.0"
