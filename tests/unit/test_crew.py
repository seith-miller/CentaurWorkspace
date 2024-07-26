import pytest
from unittest.mock import patch, MagicMock
from centaur_workspace.crew import MyProjectCrew, Worker, GenericTester


@pytest.mark.unit
class TestMyProjectCrew:
    @patch("centaur_workspace.crew.Agent")
    def test_create_agents(self, MockAgent):
        mock_agents = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        MockAgent.side_effect = mock_agents

        crew = MyProjectCrew()
        assert len(crew.agents) == 4
        assert isinstance(crew.agents[0], Worker)
        assert isinstance(crew.agents[1], Worker)
        assert isinstance(crew.agents[2], GenericTester)
        assert isinstance(crew.agents[3], GenericTester)

    @patch("centaur_workspace.crew.Agent")
    @patch("centaur_workspace.crew.Task")
    @patch("centaur_workspace.crew.Crew")
    def test_interact_with_dave_product_manager(self, MockCrew, MockTask, MockAgent):
        mock_crew_instance = MagicMock()
        MockCrew.return_value = mock_crew_instance
        mock_task_instance = MagicMock()
        MockTask.return_value = mock_task_instance
        mock_crew_instance.kickoff.return_value = "Product Manager Response"

        crew = MyProjectCrew()
        response = crew.interact_with_dave_product_manager("Test input")

        assert "Product Manager Response" in response
        MockTask.assert_called_once()
        MockCrew.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()

    @patch("centaur_workspace.crew.Agent")
    @patch("centaur_workspace.crew.Task")
    @patch("centaur_workspace.crew.Crew")
    def test_interact_with_alex_entrepreneur(self, MockCrew, MockTask, MockAgent):
        mock_crew_instance = MagicMock()
        MockCrew.return_value = mock_crew_instance
        mock_task_instance = MagicMock()
        MockTask.return_value = mock_task_instance
        mock_crew_instance.kickoff.return_value = "Entrepreneur Response"

        crew = MyProjectCrew()
        response = crew.interact_with_alex_entrepreneur("Test input")

        assert response == "Entrepreneur Response"
        MockTask.assert_called_once()
        MockCrew.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()
