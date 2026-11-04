import logging
from typing import Callable
from openai import AsyncOpenAI
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from app.core.config import settings

# Configurar el logger para este módulo
logger = logging.getLogger(__name__)


def _build_openrouter() -> OpenAIChatCompletion:
    """
    Construye un servicio de chat apuntando a OpenRouter.
    Usa el cliente asíncrono de OpenAI con base_url personalizada.
    """
    client = AsyncOpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
    )
    return OpenAIChatCompletion(
        ai_model_id=settings.OPENROUTER_MODEL,
        async_client=client,
        service_id="default"
    )


def _build_openai() -> OpenAIChatCompletion:
    """Construye un servicio de chat para OpenAI directo."""
    return OpenAIChatCompletion(
        ai_model_id=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        service_id="default"
    )


# El registro de proveedores
_PROVIDER_REGISTRY: dict[str, Callable[[], OpenAIChatCompletion]] = {
    "OPENROUTER": _build_openrouter,
    "OPENAI": _build_openai,
}


def get_chat_completion_service() -> OpenAIChatCompletion:
    """
    Factory (Registry Pattern): Retorna el servicio de chat según LLM_PROVIDER.
    """
    provider = settings.LLM_PROVIDER.upper()
    # print(f"🤖 [LLM FACTORY] Inicializando proveedor: {provider}")
    logger.info(f"🤖 [LLM FACTORY] Inicializando proveedor: {provider}")

    builder = _PROVIDER_REGISTRY.get(provider)
    if not builder:
        raise ValueError(
            f"Proveedor no soportado: {provider}. Usa OPENROUTER u OPENAI."
        )
    return builder()
