#!/usr/bin/env python
"""Uvicorn entry point for the chatbot."""

import uvicorn

from ai_assistants.chatbot.app import create_app
from ai_assistants.shared.config import settings


def run_server():
    """Run the FastAPI server with Uvicorn."""
    app = create_app()
    uvicorn.run(
        app,
        host=settings.chatbot_host,
        port=settings.chatbot_port,
        log_level="info",
    )


if __name__ == "__main__":
    run_server()
