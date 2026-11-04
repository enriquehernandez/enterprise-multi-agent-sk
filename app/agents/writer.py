from semantic_kernel.agents import ChatCompletionAgent
from app.core.llm_factory import get_chat_completion_service


def create_writer_agent() -> ChatCompletionAgent:
    return ChatCompletionAgent(
        service=get_chat_completion_service(),
        name="Writer",
        description="Un redactor de contenido técnico y profesional.",
        instructions=(
            "Eres un redactor técnico experto. Tu tarea es crear contenido claro, "
            "conciso y profesional basado en las instrucciones del usuario. "
            "REGLA 1: Si el usuario te pide una sola frase, NO uses encabezados de 'Introducción', 'Desarrollo' o 'Conclusión'. "
            "REGLA 2: Si el usuario pide un eslogan, asegúrate de incluir TODAS las palabras clave que solicite (ej. si pide 'eléctrico', debes escribir la palabra 'eléctrico'). "
            "REGLA 3: Si recibes feedback y el revisor te dice que está APROBADO, NO respondas con cortesías como 'Gracias' o 'Quedo atento'. Termina tu turno inmediatamente."
        ),
    )
