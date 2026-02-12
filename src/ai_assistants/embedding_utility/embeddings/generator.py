"""Sentence-transformers wrapper with lazy model loading."""

import logging

from sentence_transformers import SentenceTransformer

from ai_assistants.embedding_utility.config import get_model_cache_dir
from ai_assistants.shared.config import settings

logger = logging.getLogger(__name__)

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Load and cache the sentence-transformers model."""
    global _model
    if _model is None:
        cache_dir = get_model_cache_dir()
        logger.info(
            "Loading embedding model: %s (cache: %s)",
            settings.embedding_model_name,
            cache_dir or "HuggingFace default",
        )
        _model = SentenceTransformer(
            settings.embedding_model_name,
            cache_folder=cache_dir,
        )
    return _model


def generate_embeddings(texts: list[str], batch_size: int = 64) -> list[list[float]]:
    """Generate embeddings for a batch of texts."""
    model = get_model()
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=False)
    return [embedding.tolist() for embedding in embeddings]


def generate_embedding(text: str) -> list[float]:
    """Generate an embedding for a single text."""
    return generate_embeddings([text])[0]
