import os
from openai import OpenAI
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from .tools.custom_tool import CustomTool

load_dotenv()

class MyProjectCrew:
    def __init__(self):
        self.custom_tool = CustomTool()
        self.agents = self.create_agents()

    def create_agents(self):
        return [
            Agent(
                role='Greeter',
                goal='Greet the user warmly',
                backstory='You are an enthusiastic AI assistant eager to welcome users.',
                tools=[self.custom_tool],
                verbose=True
            ),
            Agent(
                role='Responder',
                goal='Respond to the user greeting and engage in a pleasant conversation.',
                backstory='You are a polite AI assistant that enjoys conversing with users.',
                tools=[self.custom_tool],
                verbose=True
            )
        ]

    def chat(self, user_input):
        # Use the responder agent to handle the user input
        result = self.agents[1].execute_task(user_input)
        return result
