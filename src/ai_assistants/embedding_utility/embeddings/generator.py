"""Sentence-transformers wrapper with lazy model loading."""

import logging

from sentence_transformers import SentenceTransformer

from ai_assistants.embedding_utility.config import get_model_cache_dir
from ai_assistants.shared.config import settings

logger = logging.getLogger(__name__)

_model: SentenceTransformer | None = None
_model_name: str | None = None


def get_model(model_name: str | None = None) -> SentenceTransformer:
    """Load and cache the sentence-transformers model."""
    global _model, _model_name
    effective_name = model_name or settings.embedding_model_name
    if _model is None or _model_name != effective_name:
        cache_dir = get_model_cache_dir()
        logger.info(
            "Loading embedding model: %s (cache: %s)",
            effective_name,
            cache_dir or "HuggingFace default",
        )
        _model = SentenceTransformer(
            effective_name,
            cache_folder=cache_dir,
        )
        _model_name = effective_name

        logger.info(f'Model {effective_name} loaded successfully and will be used in embeddings.')
    return _model


def generate_embeddings(texts: list[str], batch_size: int = 64, model_name: str = None) -> list[list[float]]:
    """Generate embeddings for a batch of texts."""
    logger.info(f"Generating embeddings for {len(texts)} texts...")
    model = get_model(model_name)
    logger.info(f"Generating embeddings for {len(texts)} texts using model {model}...")
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=True)
    return [embedding.tolist() for embedding in embeddings]


def generate_embedding(text: str, model_name: str = "") -> list[float]:
    """Generate an embedding for a single text."""
    logger.info(f"Generating embedding for single text...")
    return generate_embeddings([text], model_name=model_name)[0]
