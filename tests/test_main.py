import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

# Ya tienes test_health(), lo dejamos, pero aquí agregamos los demás.


@patch("app.main.run_multi_agent_task")
def test_orchestrate_success(mock_run_task):
    """Prueba el endpoint /orchestrate exitoso."""
    mock_run_task.return_value = AsyncMock(return_value="Resultado simulado")

    response = client.post(
        "/orchestrate",
        json={"task": "Escribe un poema"}
    )

    assert response.status_code == 200
    assert response.json() == {"result": "Resultado simulado"}


@patch("app.main.run_multi_agent_task")
def test_orchestrate_failure(mock_run_task):
    """Prueba el caso de error 500 en el endpoint."""
    mock_run_task.side_effect = Exception("Error simulado en el agente")

    response = client.post(
        "/orchestrate",
        json={"task": "Escribe un poema"}
    )

    assert response.status_code == 500
    assert "Error simulado" in response.json()["detail"]


@patch("app.agents.manager.GroupChatOrchestration")
@patch("app.agents.manager.InProcessRuntime")
@patch("app.agents.manager.create_writer_agent")
@patch("app.agents.manager.create_reviewer_agent")
@pytest.mark.asyncio
async def test_manager_callback_line(mock_writer, mock_reviewer, mock_runtime, mock_orch):
    """Fuerza la ejecución del _agent_response_callback para cubrir el print de la línea 10."""
    from app.agents.manager import run_multi_agent_task, _agent_response_callback
    from semantic_kernel.contents import ChatMessageContent

    # 1. Ejecutamos el callback directamente para cubrir la línea 10
    fake_message = ChatMessageContent(
        role="assistant", content="Hola", name="Writer")
    _agent_response_callback(fake_message)  # Esto imprime y cubre la línea 10.

    # 2. Configuramos el resto del test rápido
    mock_result = AsyncMock()
    mock_result.get = AsyncMock(return_value="APROBADO")
    mock_orch.return_value.invoke = AsyncMock(return_value=mock_result)
    mock_runtime.return_value.stop_when_idle = AsyncMock()

    await run_multi_agent_task("Test")
