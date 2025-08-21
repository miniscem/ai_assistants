from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class BlogWriterCrew():
    """AiAssistants crew"""

    agents: List[BaseAgent]
    tasks: List[Task]     
    
    ########################################################## 
    ### personal blog writing agent and task configuration ### 
    ##########################################################
    @agent
    def blog_planner(self) -> Agent:
        return Agent(
            config = self.agents_config['blog_planner'],
            verbose=True,
            allow_delegation=False
        )
        
    @agent
    def blog_writer(self) -> Agent:
        return Agent(
            config = self.agents_config['blog_writer'],
            verbose=True,
            allow_delegation=False
        )
        
    @agent
    def blog_editor(self) -> Agent:
        return Agent(
            config = self.agents_config['blog_editor'],
            verbose=True,
            allow_delegation=False
        )

    @task
    def blog_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_plan_task'], # type: ignore[index]
        )

    @task
    def blog_write_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_write_task'], # type: ignore[index]
        )
        
    @task
    def blog_edit_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_edit_task'], # type: ignore[index]
        )        
    

    @crew
    def crew(self) -> Crew:
        """Creates the AiAssistants crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
