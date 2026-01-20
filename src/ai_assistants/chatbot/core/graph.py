"""LangGraph workflow definition."""

from langgraph.graph import END, StateGraph

from ai_assistants.chatbot.core.nodes import (
    generate_response,
    retrieve_context,
    route_query,
)
from ai_assistants.chatbot.core.state import ChatState


def should_retrieve(state: ChatState) -> str:
    """Determine if we should retrieve context."""
    if state.get("should_search_web") or state.get("should_use_rag"):
        return "retrieve"
    return "generate"


def create_graph() -> StateGraph:
    """Create the LangGraph workflow for the chatbot.

    The workflow:
    1. Route the query to determine what tools to use
    2. Optionally retrieve context from RAG/web search
    3. Generate the final response

    Returns:
        Compiled StateGraph workflow.
    """
    # Create the graph
    workflow = StateGraph(ChatState)

    # Add nodes
    workflow.add_node("route", route_query)
    workflow.add_node("retrieve", retrieve_context)
    workflow.add_node("generate", generate_response)

    # Define edges
    workflow.set_entry_point("route")

    # Conditional edge from route
    workflow.add_conditional_edges(
        "route",
        should_retrieve,
        {
            "retrieve": "retrieve",
            "generate": "generate",
        },
    )

    # Retrieve always goes to generate
    workflow.add_edge("retrieve", "generate")

    # Generate goes to END
    workflow.add_edge("generate", END)

    # Compile and return
    return workflow.compile()
