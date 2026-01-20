"""LangGraph state definitions."""

from typing import Annotated, List, Optional, TypedDict

from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    """State for the chat workflow.

    Attributes:
        messages: List of conversation messages with automatic accumulation.
        conversation_id: Unique identifier for the conversation.
        response: The final response to return to the user.
        sources: List of sources used in generating the response.
        should_search_web: Whether to perform web search.
        should_use_rag: Whether to use RAG for document retrieval.
        context: Retrieved context from RAG or web search.
    """

    messages: Annotated[list, add_messages]
    conversation_id: str
    response: Optional[str]
    sources: Optional[List[str]]
    should_search_web: bool
    should_use_rag: bool
    context: Optional[str]
