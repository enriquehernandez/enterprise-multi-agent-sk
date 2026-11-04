from app.core.config import settings
from app.agents.manager import run_multi_agent_task
from openai import AsyncOpenAI
import asyncio
import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


async def evaluate_with_judge(task: str, reference: str, agent_response: str) -> dict:
    """
    Usa OpenRouter como LLM juez para evaluar si la respuesta del agente cumple con el objetivo de referencia.
    Devuelve un diccionario con puntuación (0 o 1), razón y veredicto.
    """
    client = AsyncOpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
    )

    prompt = f"""Eres un evaluador imparcial. Tu tarea es determinar si la respuesta de un agente de IA logró cumplir con el objetivo solicitado.

**Tarea del usuario:**
{task}

**Respuesta del agente:**
{agent_response}

**Criterio de referencia (qué se esperaba lograr):**
{reference}

Evalúa si la respuesta del agente cumple con el criterio de referencia. Responde ÚNICAMENTE con un objeto JSON válido con esta estructura:
{{
  "score": 1 o 0,
  "reason": "explicación breve en español de por qué asignaste esa puntuación"
}}

- score = 1 si el agente logró el objetivo descrito en la referencia.
- score = 0 si no lo logró o la respuesta es irrelevante/incorrecta.
"""

    try:
        response = await client.chat.completions.create(
            model=settings.OPENROUTER_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        result = json.loads(content)
        # Validación mínima
        if "score" not in result or result["score"] not in (0, 1):
            result = {"score": 0,
                      "reason": "Formato de respuesta del juez inválido."}
        return result
    except Exception as e:
        return {"score": 0, "reason": f"Error al invocar al juez: {str(e)}"}


async def main():
    # Casos de prueba: tarea + referencia del objetivo esperado
    test_cases = [
        {
            "task": "Escribe un eslogan corto para un SUV eléctrico familiar.",
            "reference": "El eslogan debe ser corto (máximo 10 palabras), mencionar que es eléctrico y familiar, y tener un tono positivo."
        },
        {
            "task": "Explica en una frase qué es Semantic Kernel.",
            "reference": "Debe mencionar que es un SDK de Microsoft para integrar LLMs en aplicaciones de software, y que permite orquestar agentes."
        }
    ]

    print("⚖️  Iniciando evaluación LLM-as-a-Judge (sin Ragas)...\n")

    for i, case in enumerate(test_cases, 1):
        print(f"--- Caso {i}: {case['task']} ---")

        # 1. Ejecutar el sistema multi-agente real
        try:
            agent_result = await run_multi_agent_task(case["task"])
            print(f"🤖 Respuesta del Agente:\n{agent_result}\n")
        except Exception as e:
            print(f"❌ Error ejecutando el agente: {e}\n")
            continue

        # 2. Evaluar con el juez
        verdict = await evaluate_with_judge(
            task=case["task"],
            reference=case["reference"],
            agent_response=agent_result
        )

        print(f"⚖️  Puntuación del Juez: {verdict['score']}")
        print(f"📝 Razón: {verdict['reason']}\n")

        if verdict["score"] == 1:
            print("✅ APROBADO: El agente logró el objetivo.\n")
        else:
            print("⚠️  REVISAR: El agente no logró cumplir con la referencia.\n")


if __name__ == "__main__":
    asyncio.run(main())
