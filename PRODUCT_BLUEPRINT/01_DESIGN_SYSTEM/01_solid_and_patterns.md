# Principios SOLID y Patrones de Diseño

Este documento detalla las decisiones arquitectónicas tomadas para garantizar que el sistema sea mantenible y escalable.

## 1. Principios SOLID

*   **S - Single Responsibility Principle (SRP):**
    *   `writer.py` y `reviewer.py` solo se encargan de la creación de sus respectivos agentes.
    *   `llm_factory.py` solo se encarga de instanciar el LLM.
    *   `manager.py` solo se encarga de la orquestación.
*   **O - Open/Closed Principle (OCP):**
    *   El sistema está abierto a nuevos proveedores de IA (gracias al `_PROVIDER_REGISTRY` en `llm_factory.py`) sin modificar el código existente.
    *   El sistema está abierto a nuevos agentes (ej. un futuro "Traductor") sin modificar el `Manager`.
*   **D - Dependency Inversion Principle (DIP):**
    *   Los agentes dependen de la abstracción `ChatCompletionAgent` y del servicio retornado por `get_chat_completion_service()`, no de implementaciones concretas (como OpenAI directamente).

## 2. Patrones de Diseño Implementados

### A. Registry Pattern (LLM Factory)
**Ubicación:** `app/core/llm_factory.py`
**Problema:** Evitar bloques `if/elif` al instanciar diferentes proveedores de IA.
**Solución:** Un diccionario que mapea el nombre del proveedor (string) a su función constructora. Esto permite agregar nuevos proveedores (ej. Anthropic) añadiendo una sola línea al diccionario.

### B. Strategy Pattern (Orquestación)
**Ubicación:** `app/agents/manager.py`
**Problema:** El comportamiento por defecto de `RoundRobinGroupChatManager` es hablar indefinidamente hasta alcanzar `max_rounds`.
**Solución:** Se heredó de `RoundRobinGroupChatManager` creando `ApprovalGroupChatManager`. Este sobrescribe el método `should_terminate` para inyectar una lógica de negocio (detenerse si el Reviewer dice "APROBADO").

### C. Provider-Agnostic (OpenRouter)
**Ubicación:** `app/core/llm_factory.py`
**Problema:** Acoplamiento a un solo proveedor de LLM.
**Solución:** Uso de `AsyncOpenAI` con `base_url` apuntando a OpenRouter. Esto permite cambiar entre GPT-4o, Claude o Gemini simplemente cambiando la variable de entorno `OPENROUTER_MODEL`.