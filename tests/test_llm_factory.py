# tests/test_llm_factory.py
import pytest
from unittest.mock import patch
from app.core import llm_factory
from app.core.config import settings


@patch("app.core.llm_factory._build_openrouter")
def test_get_chat_completion_service_openrouter(mock_build_openrouter, monkeypatch):
    """Prueba que devuelva OpenRouter si está configurado."""
    # Solo modificamos la propiedad LLM_PROVIDER, el resto de settings queda real
    monkeypatch.setattr(settings, "LLM_PROVIDER", "OPENROUTER")

    llm_factory.get_chat_completion_service()
    mock_build_openrouter.assert_called_once()


@patch("app.core.llm_factory._build_openai")
def test_get_chat_completion_service_openai(mock_build_openai, monkeypatch):
    """Prueba que devuelva OpenAI si está configurado."""
    monkeypatch.setattr(settings, "LLM_PROVIDER", "OPENAI")

    llm_factory.get_chat_completion_service()
    mock_build_openai.assert_called_once()


def test_get_chat_completion_service_invalid(monkeypatch):
    """Prueba que lance ValueError si el proveedor no existe."""
    monkeypatch.setattr(settings, "LLM_PROVIDER", "INVALID_PROVIDER")

    with pytest.raises(ValueError, match="Proveedor no soportado"):
        llm_factory.get_chat_completion_service()


@patch("app.core.llm_factory.AsyncOpenAI")
@patch("app.core.llm_factory.OpenAIChatCompletion")
def test_build_openrouter_real(mock_completion, mock_async_openai):
    """Ejecuta la función real _build_openrouter para cubrir las líneas de creación."""
    llm_factory._build_openrouter()
    mock_async_openai.assert_called_once()
    mock_completion.assert_called_once()


@patch("app.core.llm_factory.OpenAIChatCompletion")
def test_build_openai_real(mock_completion):
    """Ejecuta la función real _build_openai."""
    llm_factory._build_openai()
    mock_completion.assert_called_once()
