# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Claude Usage Best Practices

When referencing or answering questions about Claude usage, capabilities, or implementation patterns, always consult and reference:
- Official Claude developer documentation (docs.anthropic.com)
- Anthropic GitHub repositories
- Published best practice guides and cookbook examples

Use these authoritative sources rather than making assumptions about Claude's capabilities or recommended usage patterns.

## Build and Run Commands

```bash
uv sync                 # Install dependencies

# Chatbot (LangGraph + FastAPI)
chatbot                 # Start the FastAPI server on port 8000

# CrewAI - Blog Writer
blog_writer             # Run the blog writer crew
crewai run              # Alternative: run via crewai CLI
crewai train <n> <file> # Train crew for n iterations, save to file
crewai replay <task_id> # Replay from specific task
crewai test <n> <llm>   # Test crew with n iterations using specified LLM
```

## Architecture

This project supports two AI capabilities:

### 1. LangChain/LangGraph Chatbot (`src/ai_assistants/chatbot/`)

A FastAPI-based financial advisor with RAG and web search capabilities.

**Structure:**
- `app.py` - FastAPI application factory
- `main.py` - Uvicorn entry point
- `api/routes.py` - REST endpoints (/chat, /conversations)
- `api/schemas.py` - Pydantic request/response models
- `core/graph.py` - LangGraph workflow definition
- `core/nodes.py` - Graph node functions (route, retrieve, generate)
- `core/state.py` - TypedDict state definition
- `tools/web_search.py` - Tavily web search integration
- `rag/vectorstore.py` - ChromaDB vector store setup

**Endpoints:**
- `POST /api/v1/chat` - Send message and get response
- `GET /api/v1/conversations/{id}` - Get conversation history
- `DELETE /api/v1/conversations/{id}` - Delete conversation
- `GET /api/v1/health` - Health check

### 2. CrewAI Crews (`src/ai_assistants/crews/`)

Multi-agent systems for experimentation using crewAI.

**Blog Writer Pipeline:**
1. `blog_planner` - Creates content plan with outline, audience analysis, SEO keywords
2. `blog_writer` - Writes the blog post based on the plan
3. `blog_editor` - Proofreads and aligns with brand voice

**Structure:**
- `main.py` - CLI entry points for all crews
- `blog_writer/crew.py` - Crew class with `@CrewBase` decorator
- `blog_writer/config/agents.yaml` - Agent configurations (role, goal, backstory, llm)
- `blog_writer/config/tasks.yaml` - Task configurations
- `tools/custom_tool.py` - Shared custom tools

### 3. Shared Utilities (`src/ai_assistants/shared/`)

- `config.py` - Pydantic Settings for environment variables
- `logging.py` - Centralized logging configuration

## Environment Variables

Required in `.env`:
```
ANTHROPIC_API_KEY=your-api-key
TAVILY_API_KEY=your-tavily-key  # Optional, for web search
```

Optional settings:
```
CHATBOT_HOST=0.0.0.0
CHATBOT_PORT=8000
CHATBOT_MODEL=claude-sonnet-4-20250514
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## Adding New Crews

1. Create new directory under `crews/` (e.g., `crews/my_crew/`)
2. Add `crew.py` with `@CrewBase` decorator
3. Add `config/agents.yaml` and `config/tasks.yaml`
4. Add entry point in `crews/main.py`
5. Register in `pyproject.toml` under `[project.scripts]`
