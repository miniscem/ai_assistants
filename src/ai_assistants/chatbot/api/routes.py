"""API routes for the chatbot."""

import uuid
from typing import Dict

from fastapi import APIRouter, HTTPException
from langgraph.graph import StateGraph

from ai_assistants.chatbot.api.schemas import (
    ChatRequest,
    ChatResponse,
    ConversationHistory,
    HealthResponse,
)
from ai_assistants.chatbot.core.graph import create_graph
from ai_assistants.shared.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["chat"])

# In-memory conversation store (replace with persistent storage in production)
conversations: Dict[str, list] = {}

# Create the LangGraph workflow
graph: StateGraph = create_graph()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message and return a response."""
    conversation_id = request.conversation_id or str(uuid.uuid4())

    # Get or create conversation history
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    # Add user message to history
    conversations[conversation_id].append(
        {"role": "user", "content": request.message}
    )

    try:
        # Run the graph
        result = await graph.ainvoke(
            {
                "messages": conversations[conversation_id],
                "conversation_id": conversation_id,
            }
        )

        # Extract response
        response_message = result.get("response", "I apologize, but I couldn't generate a response.")
        sources = result.get("sources", [])

        # Add assistant response to history
        conversations[conversation_id].append(
            {"role": "assistant", "content": response_message}
        )

        return ChatResponse(
            message=response_message,
            conversation_id=conversation_id,
            sources=sources if sources else None,
        )

    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}", response_model=ConversationHistory)
async def get_conversation(conversation_id: str) -> ConversationHistory:
    """Get conversation history by ID."""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    from datetime import datetime

    messages = [
        {"role": msg["role"], "content": msg["content"], "timestamp": datetime.utcnow()}
        for msg in conversations[conversation_id]
    ]

    return ConversationHistory(
        conversation_id=conversation_id,
        messages=messages,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str) -> Dict[str, str]:
    """Delete a conversation."""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    del conversations[conversation_id]
    return {"status": "deleted", "conversation_id": conversation_id}
