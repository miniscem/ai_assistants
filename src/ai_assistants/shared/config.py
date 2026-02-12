"""Centralized configuration using Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API Keys
    anthropic_api_key: str = ""
    tavily_api_key: str = ""

    # Chatbot settings
    chatbot_host: str = "0.0.0.0"
    chatbot_port: int = 8000
    chatbot_model: str = "claude-sonnet-4-20250514"

    # RAG settings
    chroma_persist_directory: str = "./chroma_db"

    # CrewAI settings
    crew_verbose: bool = True

    # Embedding utility settings
    azure_search_endpoint: str = ""
    azure_search_api_key: str = ""
    azure_search_index_name: str = "document-chunks"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_model_cache_dir: str = ""
    embedding_chunk_size: int = 1000
    embedding_input_dir: str = "./data/embedding_input"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
