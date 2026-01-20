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


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
