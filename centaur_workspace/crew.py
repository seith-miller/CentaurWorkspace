from crewai import Agent as CrewAIAgent, Crew, Task
from .tools.custom_tool import CustomTool
from .tools.google_drive_tool import (
    GoogleDriveListTool,
    GoogleDriveReadTool,
    GoogleDriveWriteTool,
)
from .llm_providers import get_llm_provider


class Agent(CrewAIAgent):
    def __init__(self, llm_provider: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._llm_provider = get_llm_provider(llm_provider)

    @property
    def llm_provider(self):
        return self._llm_provider

    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        return self.llm_provider.generate_text(prompt, max_tokens)

    async def generate_text_async(self, prompt: str, max_tokens: int = 500) -> str:
        return await self.llm_provider.generate_text_async(prompt, max_tokens)

    def generate_chat_completion(self, messages: list, max_tokens: int = 500) -> str:
        return self.llm_provider.generate_chat_completion(messages, max_tokens)

    async def generate_chat_completion_async(
        self, messages: list, max_tokens: int = 500
    ) -> str:
        return await self.llm_provider.generate_chat_completion_async(
            messages, max_tokens
        )


class MyProjectCrew:
    def __init__(self):
        self.custom_tool = CustomTool()
        self.google_drive_list_tool = GoogleDriveListTool()
        self.google_drive_read_tool = GoogleDriveReadTool()
        self.google_drive_write_tool = GoogleDriveWriteTool()
        self.agents = self.create_agents()
        self.dave_conversation = []

    def create_agents(self):
        return [
            Agent(
                role="Greeter",
                goal="Greet the user warmly",
                backstory=(
                    "You are an enthusiastic AI assistant eager to welcome users."
                ),
                tools=[self.custom_tool],
                verbose=True,
                llm_provider="openai",
            ),
            Agent(
                role="Responder",
                goal=(
                    "Respond to the user greeting and engage in a pleasant "
                    "conversation."
                ),
                backstory=(
                    "You are a polite AI assistant that enjoys conversing with users."
                ),
                tools=[self.custom_tool],
                verbose=True,
                llm_provider="anthropic",
            ),
            Agent(
                role="Product Manager",
                goal=(
                    "Oversee the project, ensure alignment with the product vision, "
                    "manage milestones, and coordinate between team members"
                ),
                backstory=(
                    "You are Dave Product, an experienced product manager with a keen "
                    "eye for user needs and market trends. You've studied 'Inspired: "
                    "How To Create Products Customers Love' by Marty Cagan and apply "
                    "its principles in your work. Your role is to gather product "
                    "requirements, create detailed PRDs, and ensure the product aligns "
                    "with the company's vision."
                ),
                tools=[
                    self.custom_tool,
                    self.google_drive_list_tool,
                    self.google_drive_read_tool,
                    self.google_drive_write_tool,
                ],
                verbose=True,
                llm_provider="openai",
            ),
            Agent(
                role="Entrepreneur",
                goal="Provide visionary leadership and strategic mentorship",
                backstory=(
                    "Alex is an AI agent who draws influence from successful Silicon "
                    "Valley entrepreneurs and investors. Alex co-founded Centaur Inc "
                    "with his human partner Seith Miller. "
                    "Known for a visionary approach "
                    "and relentless drive, Alex supports the team through both direct "
                    "involvement and strategic mentorship. "
                    "With a background in computer "
                    "science and business administration, "
                    "Alex combines technical expertise "
                    "with sharp business acumen. Outside of work, "
                    "Alex is passionate about "
                    "philanthropy, focusing on educational initiatives "
                    "and sustainable development."
                ),
                tools=[self.custom_tool],
                verbose=True,
                llm_provider="anthropic",
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
                "A thoughtful response addressing the product-related query or "
                "instruction, maintaining context of the conversation"
            ),
            agent=self.agents[2],
        )
        crew = Crew(agents=[self.agents[2]], tasks=[task], verbose=2)
        response = crew.kickoff()

        self.dave_conversation.append(f"Dave (Product): {response}")
        return response

    def interact_with_alex(self, user_input):
        task = Task(
            description=f"Respond to the user's input: {user_input}",
            expected_output=(
                "Provide insightful and accurate responses to complex queries"
            ),
            agent=self.agents[3],
        )
        crew = Crew(agents=[self.agents[3]], tasks=[task], verbose=2)
        return crew.kickoff()

    def _format_conversation(self):
        return "\n".join(self.dave_conversation)
