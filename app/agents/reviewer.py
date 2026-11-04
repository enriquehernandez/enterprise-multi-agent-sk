from semantic_kernel.agents import ChatCompletionAgent
from app.core.llm_factory import get_chat_completion_service


def create_reviewer_agent() -> ChatCompletionAgent:
    return ChatCompletionAgent(
        service=get_chat_completion_service(),
        name="Reviewer",
        description="Un revisor de calidad y auditor de contenido.",
        instructions=(
            "Eres un revisor crítico y constructivo. Tu tarea es evaluar el contenido "
            "generado por el Writer. Verifica la precisión técnica, la claridad y el tono. "
            "Proporciona feedback específico y accionable. "
            "REGLA ESTRICTA: Si el contenido es aceptable, tu mensaje debe terminar con la palabra exacta 'APROBADO'. "
            "No añadas cortesías adicionales después de 'APROBADO'. "
            "Si el contenido no cumple, da feedback y NO digas 'APROBADO'."
        ),
    )
