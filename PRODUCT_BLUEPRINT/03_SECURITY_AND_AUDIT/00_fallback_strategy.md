# Fallback & Error Handling Strategy

## 1. Fallback a nivel de Orquestación (Límite de Rondas)
Aunque el `ApprovalGroupChatManager` detiene la conversación en la ronda 2, se configuró un `max_rounds=10` como red de seguridad. Si por algún motivo el `Reviewer` no aprueba el contenido (ej. el `Writer` entra en un bucle de errores), la orquestación se detendrá a las 10 rondas para evitar consumir tokens infinitamente.

## 2. Fallback a nivel de LLM (API Key)
Si la API Key de OpenRouter falla o expira, el sistema capturará la excepción en `run_multi_agent_task` y devolverá un mensaje controlado:
*"Error en la orquestación y sin respuesta del Writer."*

## 3. Guardrails (Controles de Calidad)
- **Validación de Respuesta:** El callback `_agent_response_callback` solo guarda la **primera** respuesta del `Writer`. Esto garantiza que, incluso si el sistema falla y devuelve el último mensaje, el resultado final sea el contenido sustancial y no una cortesía.
- **Prompt Engineering:** El `Reviewer` tiene instrucciones estrictas de no aprobar contenido que no cumpla con los requisitos técnicos.