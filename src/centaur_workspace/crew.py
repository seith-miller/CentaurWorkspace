from crewai import Agent, Crew, Task

from .tools.custom_tool import CustomTool


class MyProjectCrew:
    def __init__(self):
        self.custom_tool = CustomTool()
        self.agents = self.create_agents()

    def create_agents(self):
        return [
            Agent(
                role="Greeter",
                goal="Greet the user warmly",
                backstory=(
                    "You are an enthusiastic AI assistant eager to welcome " "users."
                ),
                tools=[self.custom_tool],
                verbose=True,
            ),
            Agent(
                role="Responder",
                goal="Respond to the user greeting and engage in a pleasant "
                "conversation.",
                backstory=(
                    "You are a polite AI assistant that enjoys conversing with "
                    "users."
                ),
                tools=[self.custom_tool],
                verbose=True,
            ),
        ]

    def chat(self, user_input):
        task = Task(
            description=f"Respond to the user's input: {user_input}",
            expected_output="A friendly and engaging response to the user's input",
            agent=self.agents[1],
        )
        crew = Crew(agents=self.agents, tasks=[task], verbose=2)
        return crew.kickoff()
