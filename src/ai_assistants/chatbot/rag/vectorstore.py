"""Vector store setup and management."""

from typing import List, Optional

from ai_assistants.shared.config import settings
from ai_assistants.shared.logging import get_logger

logger = get_logger(__name__)

# Global vectorstore instance
_vectorstore = None


def get_vectorstore():
    """Get the vectorstore instance.

    Returns:
        The vectorstore instance, or None if not initialized.
    """
    return _vectorstore


def initialize_vectorstore(documents: Optional[List] = None):
    """Initialize the ChromaDB vectorstore.

    Args:
        documents: Optional list of documents to add to the vectorstore.

    Returns:
        The initialized vectorstore.
    """
    global _vectorstore

    try:
        from langchain_anthropic import ChatAnthropic
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma

        # Use HuggingFace embeddings (free, no API key needed)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Create or load the vectorstore
        _vectorstore = Chroma(
            persist_directory=settings.chroma_persist_directory,
            embedding_function=embeddings,
            collection_name="financial_docs",
        )

        if documents:
            _vectorstore.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to vectorstore")

        logger.info("Vectorstore initialized successfully")
        return _vectorstore

    except ImportError as e:
        logger.warning(f"Could not initialize vectorstore: {e}")
        return None
    except Exception as e:
        logger.error(f"Error initializing vectorstore: {e}")
        return None
