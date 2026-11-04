import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.agents.manager import run_multi_agent_task


@pytest.mark.asyncio
async def test_run_multi_agent_task_mocked(monkeypatch):
    """
    Prueba la orquestación mockeando los agentes y la orquestación.
    Verifica que se llame a invoke y se devuelva el resultado.
    """
    # 1. Mockear los agentes (no queremos que llamen a OpenRouter)
    mock_writer = MagicMock()
    mock_reviewer = MagicMock()
    monkeypatch.setattr(
        "app.agents.manager.create_writer_agent", lambda: mock_writer)
    monkeypatch.setattr(
        "app.agents.manager.create_reviewer_agent", lambda: mock_reviewer)

    # 2. Mockear la orquestación y el runtime
    with patch("app.agents.manager.GroupChatOrchestration") as MockOrch, \
            patch("app.agents.manager.InProcessRuntime") as MockRuntime:

        # 3. Configurar el resultado simulado
        mock_result = AsyncMock()
        mock_result.get = AsyncMock(
            return_value="APROBADO. Contenido de prueba final.")

        # 4. Configurar invoke como AsyncMock (¡esto es clave!)
        MockOrch.return_value.invoke = AsyncMock(return_value=mock_result)

        # 5. Configurar el runtime (start es síncrono, stop_when_idle es asíncrono)
        MockRuntime.return_value.start = MagicMock()
        MockRuntime.return_value.stop_when_idle = AsyncMock()

        # 6. Ejecutar
        resultado = await run_multi_agent_task("Escribe un eslogan.")

        # 7. Verificar
        assert "APROBADO" in resultado
        MockOrch.return_value.invoke.assert_called_once()
        MockRuntime.return_value.start.assert_called_once()
        MockRuntime.return_value.stop_when_idle.assert_called_once()
