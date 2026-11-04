# Evaluación Automatizada (LLM-as-a-Judge)

La oferta de Coderio exige "diseñar mecanismos de evaluación de modelos". Para cumplir con esto, el proyecto incluye un pipeline de evaluación en `scripts/evaluate_judge.py`.

## ¿Cómo funciona?
1. **Definición de Casos de Prueba:** Se definen tareas (ej. "Escribe un eslogan") y una **referencia** (criterio de éxito).
2. **Ejecución del Agente:** El script llama a `run_multi_agent_task()` y obtiene la respuesta final.
3. **Evaluación (Judge):** Se invoca a un segundo LLM (usando OpenRouter) con un prompt que le pide actuar como juez imparcial. El juez compara la respuesta del agente con la referencia y devuelve un JSON con:
   - `score`: 1 si cumple, 0 si no.
   - `reason`: Explicación en español de la decisión.

## Ventajas
- **Evita Alucinaciones:** Si el agente se desvía del objetivo, el juez lo detecta y le asigna un 0.
- **Automatización:** No requiere revisión humana para validar la calidad del sistema.
- **Integrable en CI/CD:** Este script puede ejecutarse en un pipeline de GitHub Actions. Si la puntuación promedio baja de un umbral (ej. 0.8), el pipeline falla, alertando que un cambio en los prompts ha roto la calidad.