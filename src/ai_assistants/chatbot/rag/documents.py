"""Document loading utilities."""

from pathlib import Path
from typing import List, Optional

from ai_assistants.shared.logging import get_logger

logger = get_logger(__name__)


def load_documents_from_directory(
    directory: str,
    glob_pattern: str = "**/*.txt",
) -> List:
    """Load documents from a directory.

    Args:
        directory: Path to the directory containing documents.
        glob_pattern: Glob pattern to match files.

    Returns:
        List of loaded documents.
    """
    try:
        from langchain_community.document_loaders import DirectoryLoader, TextLoader

        loader = DirectoryLoader(
            directory,
            glob=glob_pattern,
            loader_cls=TextLoader,
        )
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents from {directory}")
        return documents

    except ImportError:
        logger.warning("langchain-community not installed")
        return []
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        return []


def load_pdf(file_path: str) -> List:
    """Load a PDF document.

    Args:
        file_path: Path to the PDF file.

    Returns:
        List of document pages.
    """
    try:
        from langchain_community.document_loaders import PyPDFLoader

        loader = PyPDFLoader(file_path)
        pages = loader.load()
        logger.info(f"Loaded {len(pages)} pages from {file_path}")
        return pages

    except ImportError:
        logger.warning("pypdf not installed")
        return []
    except Exception as e:
        logger.error(f"Error loading PDF: {e}")
        return []


def split_documents(
    documents: List,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List:
    """Split documents into chunks.

    Args:
        documents: List of documents to split.
        chunk_size: Size of each chunk.
        chunk_overlap: Overlap between chunks.

    Returns:
        List of document chunks.
    """
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        chunks = splitter.split_documents(documents)
        logger.info(f"Split into {len(chunks)} chunks")
        return chunks

    except ImportError:
        logger.warning("langchain not installed")
        return documents
    except Exception as e:
        logger.error(f"Error splitting documents: {e}")
        return documents
