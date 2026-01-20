#!/usr/bin/env python
"""CLI entry points for CrewAI crews."""

import sys
import warnings
from datetime import datetime

from ai_assistants.crews.blog_writer.crew import BlogWriterCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run_blog_writer():
    """Run the blog writer crew."""
    inputs = {"topic": "Leader election on distributed databases"}

    try:
        BlogWriterCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train_blog_writer():
    """Train the blog writer crew for a given number of iterations."""
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year),
    }
    try:
        BlogWriterCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay_blog_writer():
    """Replay the blog writer crew execution from a specific task."""
    try:
        BlogWriterCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test_blog_writer():
    """Test the blog writer crew execution and return results."""
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year),
    }

    try:
        BlogWriterCrew().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


# Aliases for backwards compatibility
run_crew = run_blog_writer
run = run_blog_writer
train = train_blog_writer
replay = replay_blog_writer
test = test_blog_writer
