# Vision and Goals (Visión y Objetivos)

## Visión
Crear un motor de generación de contenido de nivel producción que garantice la calidad del resultado final mediante la colaboración de múltiples agentes de IA, con la capacidad de ser auditado y evaluado de forma automatizada.

## Objetivos Técnicos (Goals)
1.  **Orquestación Robusta:** Utilizar `GroupChatOrchestration` de Semantic Kernel para coordinar roles.
2.  **Provider-Agnostic:** Desacoplar la lógica del agente del proveedor de IA, utilizando **OpenRouter** como puerta de enlace universal (acceso a GPT-4o, Gemini, Claude, etc.).
3.  **Eficiencia (Anti-Chatter):** Implementar mecanismos de terminación temprana para evitar que los agentes caigan en bucles infinitos de cortesía (ahorrando costos de tokens).
4.  **Evaluación Automatizada:** Incluir un pipeline (LLM-as-a-Judge) que audite la respuesta final contra un criterio de referencia.
5.  **Observabilidad:** Loguear el número de rondas, los agentes involucrados y las decisiones tomadas durante la conversación.