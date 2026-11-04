# 🧠 Enterprise Multi-Agent System with Semantic Kernel

Sistema multi-agente de nivel empresarial construido con **Microsoft Semantic Kernel** y **OpenRouter** como proveedor de IA agnóstico. Implementa el patrón **Group Chat** para orquestar la colaboración entre un agente **Writer** y un **Reviewer**.

## ✨ Características

- **Orquestación Multi-Agente:** Uso de `GroupChatOrchestration` y `RoundRobinGroupChatManager` de Semantic Kernel.
- **Provider-Agnostic:** OpenRouter como puerta de entrada a cualquier modelo (GPT-4o, Gemini, Claude, etc.) con una sola API Key.
- **Patrón Registry:** Fábrica de LLMs que respeta el principio Open/Closed de SOLID.
- **Arquitectura Documentada:** Incluye `PRODUCT_BLUEPRINT` con diagramas y decisiones de diseño.
- **API REST:** FastAPI con endpoints documentados automáticamente.

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.11
- **Framework de Agentes:** Semantic Kernel (Microsoft)
- **Proveedor IA:** OpenRouter (OpenAI-compatible)
- **Backend:** FastAPI + Uvicorn

## 🚀 Quick Start

1. **Clonar e instalar dependencias:**
```bash
git clone https://github.com/enriquehernandez/enterprise-multi-agent-sk.git
cd enterprise-multi-agent-sk
uv sync
```

2. Variables de Entorno
Copia el archivo de ejemplo y configura tu API Key de OpenRouter:

```bash
cp .env.example .env
```

Edita el archivo .env:

```env
LLM_PROVIDER=OPENROUTER
OPENROUTER_MODEL=openai/gpt-4o
OPENROUTER_API_KEY=sk-or-v1-tu_api_key_aqui
```


3. Levantar el Servidor

```bash
uv run uvicorn app.main:app --reload --port 8003
```

Accede a la documentación interactiva (Swagger UI) en: http://127.0.0.1:8003/docs

## 📡 Ejemplo de Uso

### API REST

Haz un `POST` al endpoint `/orchestrate`:

```bash
curl -X POST http://localhost:8003/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"task": "Escribe un eslogan corto para un SUV eléctrico familiar."}'
```

**Respuesta esperada:**

```json
{
  "result": "Espacio familiar, energía eléctrica."
}
```

**Evaluación con LLM-as-a-Judge**

El proyecto incluye un script que ejecuta casos de prueba y usa un LLM como juez para evaluar si el agente cumplió con los objetivos:

```bash
uv run python scripts/evaluate_judge.py
```

**Salida esperada:**

```text
⚖️  Iniciando evaluación LLM-as-a-Judge...

--- Caso 1: Escribe un eslogan corto para un SUV eléctrico familiar. ---
🚀 Iniciando tarea...
--- 🔄 Ronda 1 ---
**Writer**
Espacio familiar, energía eléctrica.
--- 🔄 Ronda 2 ---
**Reviewer**
... APROBADO
🏁 Tarea finalizada en 2 rondas.

⚖️  Puntuación del Juez: 1
📝 Razón: El eslogan tiene 4 palabras, menciona familiar y eléctrico, y tiene tono positivo.
✅ APROBADO: El agente logró el objetivo.
```

## 🧪 Testing y Calidad

El proyecto cuenta con una suite de pruebas unitarias y de integración. Se ha alcanzado un **100% de cobertura de código** en la carpeta `app/`.

Para ejecutar los tests:

```bash
uv run pytest tests/ --cov=app --cov-report=term-missing
```

**Herramientas utilizadas:**

- pytest y pytest-asyncio para pruebas síncronas y asíncronas.
- unittest.mock para simular APIs externas (OpenRouter) y evitar costos durante los tests.

## 🧠 Decisiones de Arquitectura Destacadas

1. Control de Bucles (Anti-Chatter)

En los sistemas multi-agente, es común que los agentes caigan en bucles infinitos de cortesía (ej. "Gracias", "De nada"). Para evitarlo, se implementó un `ApprovalGroupChatManager` **personalizado** que hereda de `RoundRobinGroupChatManager`.

- **Lógica**: El manager evalúa el historial en cada turno. Si el `Reviewer` emite la palabra clave `APROBADO`, la orquestación se detiene inmediatamente.
- **Impacto**: Reduce el consumo de tokens y la latencia, garantizando que las tareas finalicen en un mínimo de 2 rondas.

2. Registry Pattern (Fábrica de LLMs)Ubicación: `app/core/llm_factory.py`.
Se utiliza un diccionario (`_PROVIDER_REGISTRY`) para mapear el nombre del proveedor a su función constructora. Esto respeta el principio **Open/Closed de SOLID**, permitiendo añadir nuevos proveedores sin modificar la lógica central.

3. Provider-Agnostic con OpenRouter

El conector `OpenAIChatCompletion` de Semantic Kernel se configura con un cliente `AsyncOpenAI` que tiene una `base_url` personalizada (apuntando a OpenRouter). Esto permite usar cualquier modelo (GPT-4o, Gemini, Claude, etc.) sin cambiar el código.

🗺️ Roadmap
☑ Soporte para OpenRouter (Provider-Agnostic).
☑ Orquestación Multi-Agente con Semantic Kernel.
☑ Control de Bucles con Manager Personalizado.
☑ Evaluación LLM-as-a-Judge.
☑ Tests con mocks y 100% de cobertura.
□ Integración con Azure OpenAI directo (sin OpenRouter).
□ Streaming de respuestas (SSE) en la API.
□ Docker + CI/CD (GitHub Actions).


## 🧑‍💻 Autor
Enrique Hernández Leiva
* [LinkedIn](https://www.linkedin.com/in/enrique-hernandez-leiva/)
* [GitHub](https://github.com/enriquehernandez)