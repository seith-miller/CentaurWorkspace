from crewai import Agent as CrewAIAgent, Crew, Task
from .tools.custom_tool import CustomTool
from .tools.google_drive.navigate import GoogleDriveNavigationTool
from .tools.google_drive.read import GoogleDriveReadTool
from .tools.google_drive.write import GoogleDriveWriteTool
from .llm_providers import get_llm_provider
from .tools.timestamp_tool import TimestampTool
from .config_loader import load_agent_config


class Agent(CrewAIAgent):
    def __init__(self, llm_provider: str, model: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._llm_provider = get_llm_provider(llm_provider, model)
        self._llm_name = f"{llm_provider}-{model}"

    @property
    def llm_provider(self):
        return self._llm_provider

    def get_llm_name(self) -> str:
        return self._llm_name


class Worker(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def report_llm(self) -> str:
        return f"I'm running on {self.get_llm_name()}"


class GenericTester(Agent):
    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        llm_provider: str,
        model: str,
        *args,
        **kwargs,
    ):
        super().__init__(
            role=role,
            goal=goal,
            backstory=backstory,
            llm_provider=llm_provider,
            model=model,
            *args,
            **kwargs,
        )


class MyProjectCrew:
    def __init__(self):
        self.tools = {
            "custom_tool": CustomTool(),
            "google_drive_navigation_tool": GoogleDriveNavigationTool(),
            "google_drive_read_tool": GoogleDriveReadTool(),
            "google_drive_write_tool": GoogleDriveWriteTool(),
            "timestamp_tool": TimestampTool(),
        }
        self.agents = self.create_agents()
        self.dave_conversation = []

    def create_agents(self):
        agents = []
        for agent_config in [
            "product_manager",
            "entrepreneur",
            "tester_gpt35",
            "tester_gpt4",
        ]:
            config = load_agent_config(agent_config)
            if "tools" in config:
                config["tools"] = [self.tools[tool["name"]] for tool in config["tools"]]
            if agent_config in ["product_manager", "entrepreneur"]:
                agents.append(Worker(**config))
            else:
                agents.append(GenericTester(**config))
        return agents

    def interact_with_dave_product_manager(self, user_input):
        self.dave_conversation.append(f"User: {user_input}")

        if "llm" in user_input.lower():
            response = self.agents[0].report_llm()
        else:
            task = Task(
                description=(
                    f"As the Product Manager, respond to: {user_input}\n\n"
                    f"Conversation history:\n{self._format_conversation()}\n\n"
                    f"To navigate Google Drive, use these actions:\n"
                ),
                expected_output=(
                    "A thoughtful response addressing the product-related query or "
                    "instruction, maintaining context of the conversation"
                ),
                agent=self.agents[0],
            )
            crew = Crew(agents=[self.agents[0]], tasks=[task], verbose=2)
            response = crew.kickoff()

        self.dave_conversation.append(f"Dave (Product): {response}")
        return response

    def interact_with_alex_entrepreneur(self, user_input):
        if "llm" in user_input.lower():
            return self.agents[1].report_llm()

        task = Task(
            description=f"Respond to the user's input: {user_input}",
            expected_output=(
                "Provide insightful and accurate responses to complex queries"
            ),
            agent=self.agents[1],
        )
        crew = Crew(agents=[self.agents[1]], tasks=[task], verbose=2)
        response = crew.kickoff()
        return response

    def _format_conversation(self):
        return "\n".join(self.dave_conversation)
