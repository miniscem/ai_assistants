"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_assistants.chatbot.api.routes import router
from ai_assistants.shared.logging import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="AI Financial Advisor",
        description="A LangGraph-powered financial advisor chatbot with RAG and web search capabilities.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(router)

    @app.on_event("startup")
    async def startup_event():
        """Initialize resources on startup."""
        logger.info("Starting AI Financial Advisor chatbot...")

        # Optionally initialize vectorstore
        # from ai_assistants.chatbot.rag.vectorstore import initialize_vectorstore
        # initialize_vectorstore()

    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup resources on shutdown."""
        logger.info("Shutting down AI Financial Advisor chatbot...")

    return app
