from crewai import Agent, Crew, Task
from .tools.custom_tool import CustomTool


class MyProjectCrew:
    def __init__(self):
        self.custom_tool = CustomTool()
        self.agents = self.create_agents()
        self.dave_conversation = []

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
                goal=(
                    "Respond to the user greeting and engage in a pleasant "
                    "conversation."
                ),
                backstory=(
                    "You are a polite AI assistant that enjoys conversing with "
                    "users."
                ),
                tools=[self.custom_tool],
                verbose=True,
            ),
            Agent(
                role="Product Manager",
                goal=(
                    "Oversee the project, ensure alignment with the product "
                    "vision, manage milestones, and coordinate between team "
                    "members"
                ),
                backstory=(
                    "You are Dave Product, an experienced product manager with "
                    "a keen eye for user needs and market trends. You've "
                    "studied 'Inspired: How To Create Products Customers Love' "
                    "by Marty Cagan and apply its principles in your work. "
                    "Your role is to gather product requirements, create "
                    "detailed PRDs, and ensure the product aligns with the "
                    "company's vision."
                ),
                tools=[self.custom_tool],
                verbose=True,
            ),
        ]

    def chat(self, user_input):
        task = Task(
            description=f"Respond to the user's input: {user_input}",
            expected_output=("A friendly and engaging response to the user's input"),
            agent=self.agents[1],
        )
        crew = Crew(agents=self.agents, tasks=[task], verbose=2)
        return crew.kickoff()

    def interact_with_product_manager(self, user_input):
        self.dave_conversation.append(f"User: {user_input}")

        task = Task(
            description=(
                f"As the Product Manager, respond to: {user_input}\n\n"
                f"Conversation history:\n{self._format_conversation()}"
            ),
            expected_output=(
                "A thoughtful response addressing the product-related query "
                "or instruction, maintaining context of the conversation"
            ),
            agent=self.agents[-1],
        )
        crew = Crew(agents=[self.agents[-1]], tasks=[task], verbose=2)
        response = crew.kickoff()

        self.dave_conversation.append(f"Dave (Product): {response}")
        return response

    def _format_conversation(self):
        return "\n".join(self.dave_conversation)
