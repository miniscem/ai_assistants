# AI Assistants

> **Purpose:** This repository is for exploring AI application development with a focus on multi-agent systems (CrewAI) and LangGraph-based chatbots. It serves as a sandbox for experimenting with collaborative AI agents, workflows, and automation.

## Features

- **Financial Advisor Chatbot** - LangGraph-powered chatbot with RAG and web search
- **Blog Writer Crew** - Multi-agent content creation pipeline
- **Extensible Architecture** - Easy to add new crews and capabilities

---

## Quickstart

### Prerequisites

1. **Install Python 3.12**
2. **Install [uv](https://docs.astral.sh/uv/):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Installation

```bash
# Clone and install dependencies
git clone <repo-url>
cd ai_assistants
uv sync
```

### Configuration

Create a `.env` file with your API keys:

```bash
ANTHROPIC_API_KEY=your-anthropic-key
TAVILY_API_KEY=your-tavily-key  # Optional, for web search
```

### Running the Chatbot

```bash
chatbot
```

The FastAPI server starts at `http://localhost:8000`. Try it:

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the basics of investing?"}'
```

API docs available at `http://localhost:8000/docs`

### Running the Blog Writer Crew

```bash
blog_writer
# or
crewai run
```

---

## Project Structure

```
src/ai_assistants/
├── shared/                      # Shared utilities
│   ├── config.py                # Pydantic settings, env loading
│   └── logging.py               # Centralized logging
│
├── chatbot/                     # LangChain/LangGraph + FastAPI
│   ├── app.py                   # FastAPI app factory
│   ├── main.py                  # Uvicorn entry point
│   ├── api/                     # REST API layer
│   ├── core/                    # LangGraph workflow
│   ├── tools/                   # Web search, etc.
│   └── rag/                     # Document retrieval
│
└── crews/                       # CrewAI multi-agent systems
    ├── main.py                  # CLI entry points
    ├── blog_writer/             # Blog writing crew
    │   ├── crew.py
    │   └── config/
    └── tools/                   # Shared CrewAI tools
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `chatbot` | Start the FastAPI chatbot server |
| `blog_writer` | Run the blog writer crew |
| `crewai run` | Run the default crew |
| `crewai train <n> <file>` | Train crew for n iterations |
| `crewai replay <task_id>` | Replay from a specific task |
| `crewai test <n> <llm>` | Test crew with specified LLM |

---

## Adding New Crews

1. Create a new directory under `src/ai_assistants/crews/`
2. Add `crew.py` with `@CrewBase` decorator
3. Add `config/agents.yaml` and `config/tasks.yaml`
4. Add entry point in `crews/main.py`
5. Register command in `pyproject.toml`

---

## Resources

- [crewAI Documentation](https://docs.crewai.com)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
