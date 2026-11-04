import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.agents.manager import run_multi_agent_task


@pytest.mark.asyncio
async def test_run_multi_agent_task_mocked():
    with patch("app.agents.manager.create_writer_agent") as mock_writer, \
            patch("app.agents.manager.create_reviewer_agent") as mock_reviewer, \
            patch("app.agents.manager.GroupChatOrchestration") as mock_orch, \
            patch("app.agents.manager.InProcessRuntime") as mock_runtime:

        # 1. Configurar el resultado final de la orquestación
        mock_result = AsyncMock()
        mock_result.get = AsyncMock(
            return_value="APROBADO. Contenido de prueba.")

        # 2. Configurar invoke como AsyncMock (¡esto es clave!)
        mock_orch.return_value.invoke = AsyncMock(return_value=mock_result)

        # 3. Configurar el runtime
        mock_runtime.return_value.start = MagicMock()
        mock_runtime.return_value.stop_when_idle = AsyncMock()

        # 4. Ejecutar
        result = await run_multi_agent_task("Tarea de prueba")

        # 5. Verificar
        assert "APROBADO" in result
        mock_orch.return_value.invoke.assert_called_once()
        mock_runtime.return_value.start.assert_called_once()
        mock_runtime.return_value.stop_when_idle.assert_called_once()
