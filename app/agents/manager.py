from semantic_kernel.agents import GroupChatOrchestration, RoundRobinGroupChatManager
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.contents import ChatMessageContent, ChatHistory
from semantic_kernel.agents.orchestration.group_chat import BooleanResult
from app.agents.writer import create_writer_agent
from app.agents.reviewer import create_reviewer_agent


class ApprovalGroupChatManager(RoundRobinGroupChatManager):
    """
    Manager personalizado que detiene la orquestación en cuanto 
    el Reviewer dice 'APROBADO'. Evita el bucle infinito de cortesías.
    """

    async def should_terminate(self, chat_history: ChatHistory) -> BooleanResult:
        if not chat_history.messages:
            return BooleanResult(result=False, reason="Sin mensajes aún.")

        last_message = chat_history.messages[-1]

        # Solo el Reviewer puede aprobar
        if last_message.name == "Reviewer" and "APROBADO" in last_message.content.upper():
            return BooleanResult(result=True, reason="Reviewer aprobó el contenido.")

        return BooleanResult(result=False, reason="No hay aprobación aún.")


async def run_multi_agent_task(task: str) -> str:
    """
    Ejecuta una tarea usando orquestación GroupChat.
    Devuelve la PRIMERA respuesta del Writer (que es el contenido real).
    """
    writer_responses = []
    current_round = [0]

    def _agent_response_callback(message: ChatMessageContent) -> None:
        current_round[0] += 1
        print(f"\n--- 🔄 Ronda {current_round[0]} ---")
        print(f"**{message.name}**\n{message.content}")

        # Guardamos solo la primera respuesta del Writer
        if message.name == "Writer" and not writer_responses:
            writer_responses.append(message.content)

    # 1. Crear agentes
    writer = create_writer_agent()
    reviewer = create_reviewer_agent()

    # 2. Configurar orquestación con nuestro Manager personalizado
    orchestration = GroupChatOrchestration(
        members=[writer, reviewer],
        manager=ApprovalGroupChatManager(max_rounds=10),  # Red de seguridad
        agent_response_callback=_agent_response_callback,
    )

    # 3. Ejecutar en runtime
    runtime = InProcessRuntime()
    runtime.start()

    try:
        print(f"🚀 Iniciando tarea: {task}")

        # Ejecutamos la orquestación (el Manager la detendrá si hay aprobación)
        orchestration_result = await orchestration.invoke(task=task, runtime=runtime)
        await orchestration_result.get()

        # 4. Retornar la respuesta guardada
        if writer_responses:
            return writer_responses[0]

        return "No se generó respuesta por parte del Writer."

    except Exception as e:
        print(f"❌ Error en la orquestación: {e}")
        if writer_responses:
            return writer_responses[0]
        return "Error en la orquestación y sin respuesta del Writer."

    finally:
        await runtime.stop_when_idle()
        print(f"🏁 Tarea finalizada en {current_round[0]} rondas.")
