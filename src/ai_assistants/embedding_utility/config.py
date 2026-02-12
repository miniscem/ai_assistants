"""Computed configuration helpers for the embedding utility."""

from pathlib import Path

from ai_assistants.shared.config import settings


def get_chunk_overlap() -> int:
    """Return 10% of chunk size as overlap."""
    return int(settings.embedding_chunk_size * 0.1)


def get_input_directory() -> Path:
    """Return resolved input directory path."""
    return Path(settings.embedding_input_dir).resolve()


def get_model_cache_dir() -> str | None:
    """Return model cache directory, or None to use HuggingFace default."""
    if settings.embedding_model_cache_dir:
        return str(Path(settings.embedding_model_cache_dir).resolve())
    return None
