from unittest.mock import patch, MagicMock
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from app.agents.writer import create_writer_agent
from app.agents.reviewer import create_reviewer_agent


def test_create_writer_agent():
    with patch("app.agents.writer.get_chat_completion_service") as mock_get:
        # Usamos MagicMock pero asignando un service_id y ai_model_id string
        # para que Pydantic no falle al validar.
        mock_service = MagicMock(spec=OpenAIChatCompletion)
        mock_service.service_id = "default"
        mock_service.ai_model_id = "gpt-4o"
        mock_get.return_value = mock_service

        agent = create_writer_agent()
        assert agent.name == "Writer"


def test_create_reviewer_agent():
    with patch("app.agents.reviewer.get_chat_completion_service") as mock_get:
        mock_service = MagicMock(spec=OpenAIChatCompletion)
        mock_service.service_id = "default"
        mock_service.ai_model_id = "gpt-4o"
        mock_get.return_value = mock_service

        agent = create_reviewer_agent()
        assert agent.name == "Reviewer"
