# tests/test_agents.py
from unittest.mock import patch, create_autospec
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from app.agents.writer import create_writer_agent
from app.agents.reviewer import create_reviewer_agent


def test_create_writer_agent():
    """Prueba la creación del agente Writer con un mock tipado."""
    with patch("app.agents.writer.get_chat_completion_service") as mock_service:
        # create_autospec hace que el mock herede de la clase real
        mock_service.return_value = create_autospec(
            OpenAIChatCompletion, instance=True)

        agent = create_writer_agent()

        assert agent.name == "Writer"
        assert agent.description == "Un redactor de contenido técnico y profesional."


def test_create_reviewer_agent():
    """Prueba la creación del agente Reviewer con un mock tipado."""
    with patch("app.agents.reviewer.get_chat_completion_service") as mock_service:
        mock_service.return_value = create_autospec(
            OpenAIChatCompletion, instance=True)

        agent = create_reviewer_agent()

        assert agent.name == "Reviewer"
        assert agent.description == "Un revisor de calidad y auditor de contenido."
