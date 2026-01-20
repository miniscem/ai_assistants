"""Blog Writer Crew implementation."""

from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class BlogWriterCrew:
    """Blog Writer crew for content creation pipeline.

    Pipeline:
    1. blog_planner - Creates content plan with outline, audience analysis, SEO keywords
    2. blog_writer - Writes the blog post based on the plan
    3. blog_editor - Proofreads and aligns with brand voice
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def blog_planner(self) -> Agent:
        """Content planning agent."""
        return Agent(
            config=self.agents_config["blog_planner"],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def blog_writer(self) -> Agent:
        """Content writing agent."""
        return Agent(
            config=self.agents_config["blog_writer"],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def blog_editor(self) -> Agent:
        """Content editing agent."""
        return Agent(
            config=self.agents_config["blog_editor"],
            verbose=True,
            allow_delegation=False,
        )

    @task
    def blog_plan_task(self) -> Task:
        """Create content plan task."""
        return Task(
            config=self.tasks_config["blog_plan_task"],
        )

    @task
    def blog_write_task(self) -> Task:
        """Write blog post task."""
        return Task(
            config=self.tasks_config["blog_write_task"],
        )

    @task
    def blog_edit_task(self) -> Task:
        """Edit blog post task."""
        return Task(
            config=self.tasks_config["blog_edit_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Create the Blog Writer crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
