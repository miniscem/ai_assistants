# AiAssistants

> **Purpose:** This repository is for exploring [crewAI](https://crewai.com) and hands-on AI application development with a focus on multi-agent systems. It serves as a sandbox for experimenting with collaborative AI agents, workflows, and automation.

Welcome to the AiAssistants project, powered by [crewAI](https://crewai.com). This project is used to setup multi-agent AI system with ease, leveraging crewAI. The goal of this project is to illustrate working examples of agentic workflows and use cases you can use to automate common tasks performed in your personal life. The goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## 🚀 What is This?

This repository is a series of examples for creating and orchestrating multiple AI agents, each with their own roles and skills. The agents can:

- **Write and edit blog posts**
- **Research topics and summarize findings**
- **Automate repetitive personal tasks**
- **Collaborate to solve complex problems**

All powered by [crewAI](https://crewai.com), making it easy to define, extend, and run your own agent workflows.

---

## 🛠️ Quickstart

1. **Install Python (>=3.10, <3.14)**
2. **Install [uv](https://docs.astral.sh/uv/):**
   ```bash
   pip install uv
   ```
3. **Install dependencies:**
   ```bash
   crewai install
   ```
4. **Add your `OPENAI_API_KEY` to a `.env` file**
5. **Run your agents:**
   ```bash
   crewai run
   ```

---

## 🧩 How It Works

- **Agents** are defined in `src/ai_assistants/config/agents.yaml`.
- **Tasks** are defined in `src/ai_assistants/config/tasks.yaml`.
- **Logic, tools, and customizations** go in `src/ai_assistants/crew.py` and `src/ai_assistants/main.py`.

You can easily add new agents, define new tasks, or plug in your own tools. The default setup includes a blog-writing workflow, but you can extend it to automate anything you want.

---

## 🧑‍💻 Why Use This?

- **Save time**: Let AI handle your routine writing and research.
- **Flexible**: Add, remove, or customize agents and tasks as you wish.
- **Collaborative**: Agents work together, not in isolation.
- **Open source & extensible**: Build your own automations on top.

---

## 📂 Project Structure

- `src/ai_assistants/` – Core logic, agent definitions, and tools
- `src/ai_assistants/config/` – YAML files for agents and tasks

---

## 🤝 Contributing

Ideas, issues, and pull requests are welcome! If you have a personal automation you want to add, open an issue or PR.

---

## 📚 Resources

- [crewAI Documentation](https://docs.crewai.com)
- [crewAI GitHub](https://github.com/joaomdmoura/crewai)
