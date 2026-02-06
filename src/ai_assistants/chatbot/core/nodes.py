"""LangGraph node functions."""

import json
from typing import Any, Dict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from ai_assistants.chatbot.core.prompts import (
    FINANCIAL_ADVISOR_SYSTEM_PROMPT,
    ROUTER_PROMPT,
)
from ai_assistants.chatbot.core.state import ChatState
from ai_assistants.chatbot.rag.vectorstore import get_vectorstore
from ai_assistants.chatbot.tools.web_search import search_web
from ai_assistants.shared.config import settings
from ai_assistants.shared.logging import get_logger

logger = get_logger(__name__)


def get_anthropic_llm() -> ChatAnthropic:
    """Get the LLM instance."""
    return ChatAnthropic(
        model=settings.chatbot_model,
        api_key=settings.anthropic_api_key,
    )


async def route_query(state: ChatState) -> Dict[str, Any]:
    """Route the query to determine what tools to use."""
    llm = get_anthropic_llm()

    # Get the last user message
    messages = state.get("messages", [])
    if not messages:
        return {
            "should_search_web": False,
            "should_use_rag": False,
        }

    last_message = messages[-1]
    if isinstance(last_message, dict):
        user_message = last_message.get("content", "")
    else:
        user_message = getattr(last_message, "content", "")
        test_message:SystemMessage = SystemMessage(content="test")
        test_message.content

    try:
        response = await llm.ainvoke(
            [
                SystemMessage(content=ROUTER_PROMPT),
                HumanMessage(content=user_message),
            ]
        )

        # Parse the response
        response_content = response.content
        if isinstance(response_content, str):
            # Try to extract JSON from the response
            try:
                result = json.loads(response_content)
                return {
                    "should_search_web": result.get("should_search_web", False),
                    "should_use_rag": result.get("should_use_rag", False),
                }
            except json.JSONDecodeError:
                logger.warning("Could not parse router response as JSON")

    except Exception as e:
        logger.error(f"Error in route_query: {e}")

    return {
        "should_search_web": False,
        "should_use_rag": False,
    }


async def retrieve_context(state: ChatState) -> Dict[str, Any]:
    """Retrieve context from RAG and/or web search."""
    context_parts = []
    sources = []

    messages = state.get("messages", [])
    if not messages:
        return {"context": None, "sources": []}

    last_message = messages[-1]
    if isinstance(last_message, dict):
        query = last_message.get("content", "")
    else:
        query = getattr(last_message, "content", "")

    # RAG retrieval
    if state.get("should_use_rag", False):
        try:
            vectorstore = get_vectorstore()
            if vectorstore:
                docs = vectorstore.similarity_search(query, k=3)
                for doc in docs:
                    context_parts.append(doc.page_content)
                    if doc.metadata.get("source"):
                        sources.append(doc.metadata["source"])
        except Exception as e:
            logger.warning(f"RAG retrieval failed: {e}")

    # Web search
    if state.get("should_search_web", False):
        try:
            web_results = await search_web(query)
            if web_results:
                context_parts.append(f"Web search results:\n{web_results['content']}")
                sources.extend(web_results.get("sources", []))
        except Exception as e:
            logger.warning(f"Web search failed: {e}")

    context = "\n\n".join(context_parts) if context_parts else None

    return {
        "context": context,
        "sources": sources,
    }


async def generate_response(state: ChatState) -> Dict[str, Any]:
    """Generate the final response."""
    llm = get_anthropic_llm()

    messages = state.get("messages", [])
    context = state.get("context")

    # Build the system message
    system_content = FINANCIAL_ADVISOR_SYSTEM_PROMPT
    if context:
        system_content += f"\n\nRelevant context:\n{context}"

    # Convert messages to LangChain format
    lc_messages = [SystemMessage(content=system_content)]
    for msg in messages:
        if isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
        else:
            role = getattr(msg, "role", "user")
            content = getattr(msg, "content", "")

        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        # Skip assistant messages for now to avoid duplication

    try:
        response = await llm.ainvoke(lc_messages)
        response_text = response.content if hasattr(response, "content") else str(response)

        return {
            "response": response_text,
            "sources": state.get("sources", []),
        }

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return {
            "response": "I apologize, but I encountered an error generating a response. Please try again.",
            "sources": [],
        }
