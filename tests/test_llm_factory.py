import pytest
from unittest.mock import patch, MagicMock
from app.core import llm_factory
from app.core.config import settings


# ==========================================
# 1. TESTS DE INTEGRACIÓN (Cubren las líneas rojas)
# Aquí probamos que las funciones _build_... funcionan
# ==========================================

@patch("app.core.llm_factory.OpenAIChatCompletion")
@patch("app.core.llm_factory.AsyncOpenAI")
def test_build_openrouter_integration(mock_async_openai, mock_chat_completion):
    """Prueba la creación real del cliente de OpenRouter."""
    # Asignamos valores string reales a los settings para que no fallen
    settings.LLM_PROVIDER = "OPENROUTER"
    settings.OPENROUTER_API_KEY = "test-key"
    settings.OPENROUTER_BASE_URL = "https://test.url/v1"
    settings.OPENROUTER_MODEL = "test-model"

    # Al llamar a get_chat_completion_service, entrará en _build_openrouter
    # y usará las clases mockeadas.
    llm_factory.get_chat_completion_service()

    mock_async_openai.assert_called_once()
    mock_chat_completion.assert_called_once()


@patch("app.core.llm_factory.OpenAIChatCompletion")
def test_build_openai_integration(mock_chat_completion):
    """Prueba la creación real del cliente de OpenAI."""
    settings.LLM_PROVIDER = "OPENAI"
    settings.OPENAI_API_KEY = "test-key"
    settings.OPENAI_MODEL = "test-model"

    llm_factory.get_chat_completion_service()

    mock_chat_completion.assert_called_once()


# ==========================================
# 2. TESTS DEL REGISTRY (Lógica del diccionario)
# Verifican que get_chat_completion_service busca bien en el diccionario
# ==========================================

@patch("app.core.llm_factory._PROVIDER_REGISTRY")
def test_get_chat_completion_service_uses_registry(mock_registry):
    """Simula el diccionario y verifica que se busque la llave correcta."""
    mock_registry.get.return_value = MagicMock()

    settings.LLM_PROVIDER = "OPENROUTER"
    llm_factory.get_chat_completion_service()

    mock_registry.get.assert_called_once_with("OPENROUTER")


# ==========================================
# 3. TEST DE ERROR (Cubre el raise ValueError)
# ==========================================

def test_get_chat_completion_service_invalid_provider():
    """Prueba que lance ValueError si el proveedor no existe."""
    settings.LLM_PROVIDER = "INVALID_PROVIDER"

    with pytest.raises(ValueError, match="Proveedor no soportado"):
        llm_factory.get_chat_completion_service()
