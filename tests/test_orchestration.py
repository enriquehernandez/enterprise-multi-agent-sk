import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from semantic_kernel.agents.orchestration.group_chat import BooleanResult
from semantic_kernel.contents import ChatHistory, ChatMessageContent
from app.agents.manager import ApprovalGroupChatManager, run_multi_agent_task


@pytest.mark.asyncio
async def test_run_multi_agent_task_mocked():
    with patch("app.agents.manager.create_writer_agent") as mock_writer, \
            patch("app.agents.manager.create_reviewer_agent") as mock_reviewer, \
            patch("app.agents.manager.GroupChatOrchestration") as mock_orch, \
            patch("app.agents.manager.InProcessRuntime") as mock_runtime:

        # Simulamos el resultado de la orquestación
        mock_result = AsyncMock()
        mock_result.get = AsyncMock(return_value="APROBADO")
        mock_orch.return_value.invoke = AsyncMock(return_value=mock_result)

        # Simulamos el runtime
        mock_runtime.return_value.start = MagicMock()
        mock_runtime.return_value.stop_when_idle = AsyncMock()

        # TRUCO: Hacemos que al crear la orquestación, se llame al callback del Writer
        def side_effect_orch(*args, **kwargs):
            callback = kwargs.get("agent_response_callback")
            if callback:
                # Simulamos el mensaje del Writer
                msg = ChatMessageContent(
                    role="assistant", content="Eslogan de prueba", name="Writer")
                callback(msg)
            return mock_orch.return_value

        mock_orch.side_effect = side_effect_orch

        result = await run_multi_agent_task("Tarea de prueba")

        assert "Eslogan de prueba" in result


@pytest.mark.asyncio
async def test_approval_manager_terminates():
    """Cubre la lógica de should_terminate de nuestro Manager."""
    manager = ApprovalGroupChatManager(max_rounds=5)

    # Caso 1: Historial vacío
    history = ChatHistory()
    assert (await manager.should_terminate(history)).result is False

    # Caso 2: Último mensaje del Writer (No termina)
    history.add_message(ChatMessageContent(
        role="assistant", content="Hola", name="Writer"))
    assert (await manager.should_terminate(history)).result is False

    # Caso 3: Último mensaje del Reviewer con APROBADO (Termina)
    history.add_message(ChatMessageContent(
        role="assistant", content="APROBADO", name="Reviewer"))
    assert (await manager.should_terminate(history)).result is True


@pytest.mark.asyncio
async def test_run_multi_agent_task_exception():
    """Cubre el bloque except del manager."""
    with patch("app.agents.manager.create_writer_agent") as mock_writer, \
            patch("app.agents.manager.create_reviewer_agent") as mock_reviewer, \
            patch("app.agents.manager.GroupChatOrchestration") as mock_orch, \
            patch("app.agents.manager.InProcessRuntime") as mock_runtime:

        # Hacemos que la orquestación lance una excepción
        mock_orch.return_value.invoke = AsyncMock(
            side_effect=Exception("Error simulado"))
        mock_runtime.return_value.start = MagicMock()
        mock_runtime.return_value.stop_when_idle = AsyncMock()

        result = await run_multi_agent_task("Tarea de prueba")
        # Debe capturar la excepción y retornar el mensaje de error
        assert "Error en la orquestación y sin respuesta del Writer." in result


@pytest.mark.asyncio
async def test_run_multi_agent_task_no_writer_response():
    """Cubre la línea 71: Orquestación exitosa pero sin respuesta del Writer."""
    with patch("app.agents.manager.create_writer_agent") as mock_writer, \
            patch("app.agents.manager.create_reviewer_agent") as mock_reviewer, \
            patch("app.agents.manager.GroupChatOrchestration") as mock_orch, \
            patch("app.agents.manager.InProcessRuntime") as mock_runtime:

        # Simulamos una orquestación exitosa
        mock_result = AsyncMock()
        mock_result.get = AsyncMock(return_value="APROBADO")
        mock_orch.return_value.invoke = AsyncMock(return_value=mock_result)

        mock_runtime.return_value.start = MagicMock()
        mock_runtime.return_value.stop_when_idle = AsyncMock()

        # IMPORTANTE: NO ejecutamos el callback del Writer (simulando que no hubo respuesta)
        def side_effect_orch(*args, **kwargs):
            return mock_orch.return_value
        mock_orch.side_effect = side_effect_orch

        result = await run_multi_agent_task("Tarea de prueba")

        # Verificamos que entró al if/else de la línea 70-71
        assert result == "No se generó respuesta por parte del Writer."


@pytest.mark.asyncio
async def test_run_multi_agent_task_exception_without_writer():
    """Cubre la línea 76: Ocurre una excepción y tampoco hay respuesta del Writer."""
    with patch("app.agents.manager.create_writer_agent") as mock_writer, \
            patch("app.agents.manager.create_reviewer_agent") as mock_reviewer, \
            patch("app.agents.manager.GroupChatOrchestration") as mock_orch, \
            patch("app.agents.manager.InProcessRuntime") as mock_runtime:

        # Hacemos que la orquestación lance una excepción
        mock_orch.return_value.invoke = AsyncMock(
            side_effect=Exception("Error simulado"))
        mock_runtime.return_value.start = MagicMock()
        mock_runtime.return_value.stop_when_idle = AsyncMock()

        # IMPORTANTE: NO llenamos writer_responses (el Writer nunca habló)
        result = await run_multi_agent_task("Tarea de prueba")

        # Verificamos que entró al except y al if/else de la línea 75-76
        assert result == "Error en la orquestación y sin respuesta del Writer."


@pytest.mark.asyncio
async def test_run_multi_agent_task_exception_with_writer_response():
    """Cubre la línea 75: Ocurre una excepción PERO el Writer ya había respondido."""
    with patch("app.agents.manager.create_writer_agent") as mock_writer, \
            patch("app.agents.manager.create_reviewer_agent") as mock_reviewer, \
            patch("app.agents.manager.GroupChatOrchestration") as mock_orch, \
            patch("app.agents.manager.InProcessRuntime") as mock_runtime:

        # 1. Simulamos que la orquestación lanza una excepción
        mock_orch.return_value.invoke = AsyncMock(
            side_effect=Exception("Error simulado"))
        mock_runtime.return_value.start = MagicMock()
        mock_runtime.return_value.stop_when_idle = AsyncMock()

        # 2. TRUCO: Hacemos que al crear la orquestación, se ejecute el callback del Writer
        def side_effect_orch(*args, **kwargs):
            callback = kwargs.get("agent_response_callback")
            if callback:
                # Simulamos el mensaje del Writer ANTES de que ocurra el error
                msg = ChatMessageContent(
                    role="assistant", content="Eslogan de prueba", name="Writer")
                callback(msg)
            return mock_orch.return_value

        mock_orch.side_effect = side_effect_orch

        # 3. Ejecutamos (fallará, pero debe entrar al except con la lista llena)
        result = await run_multi_agent_task("Tarea de prueba")

        # 4. Verificamos que entró a la línea 75 y retornó el eslogan, no el mensaje de error
        assert result == "Eslogan de prueba"
