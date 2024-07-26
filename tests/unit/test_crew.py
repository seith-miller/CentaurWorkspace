import pytest
from unittest.mock import patch, MagicMock
from centaur_workspace.crew import Agent, MyProjectCrew


@pytest.mark.unit
class TestAgent:
    def test_agent_initialization_with_llm_provider(self):
        with patch("centaur_workspace.crew.get_llm_provider") as mock_get_llm_provider:
            mock_get_llm_provider.return_value = MagicMock()
            agent = Agent(
                role="Test Agent",
                goal="Test Goal",
                backstory="Test Backstory",
                llm_provider="openai",
            )
            mock_get_llm_provider.assert_called_once_with("openai")
            assert agent.llm_provider == mock_get_llm_provider.return_value


@pytest.mark.unit
class TestMyProjectCrew:
    @patch("centaur_workspace.crew.Agent")
    def test_create_agents(self, MockAgent):
        mock_agents = [MagicMock(), MagicMock()]
        MockAgent.side_effect = mock_agents

        crew = MyProjectCrew()
        assert len(crew.agents) == 2
        for call in MockAgent.call_args_list:
            assert call.kwargs["llm_provider"] in ["openai", "anthropic"]

    @patch("centaur_workspace.crew.Agent")
    @patch("centaur_workspace.crew.Task")
    @patch("centaur_workspace.crew.Crew")
    def test_interact_with_product_manager(self, MockCrew, MockTask, MockAgent):
        mock_crew_instance = MagicMock()
        MockCrew.return_value = mock_crew_instance
        mock_task_instance = MagicMock()
        MockTask.return_value = mock_task_instance
        mock_crew_instance.kickoff.return_value = "Product Manager Response"

        crew = MyProjectCrew()
        crew.interact_with_product_manager("Product question")

        assert "Product Manager Response" in crew.dave_conversation[-1]
        MockTask.assert_called_once()
        MockCrew.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()
