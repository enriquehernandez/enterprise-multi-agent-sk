# Architecture Design - Multi-Agent SK

## 1. Flujo de Orquestación (Group Chat)

```mermaid
graph TD
    A[Usuario: Tarea] --> B[GroupChatOrchestration]
    B --> C[Writer Agent]
    C -->|Propuesta Inicial| D[Reviewer Agent]
    D -->|Feedback / Aprobado?| E{ApprovalGroupChatManager}
    E -->|No Aprobado| C
    E -->|Aprobado| F[Fin de la Orquestación]
    F --> G[Resultado Final]
    H[RoundRobinManager] -->|Controla turnos| C
    H -->|Controla turnos| D
```

## 2. Flujo de una Petición HTTP (FastAPI)

```mermaid
sequenceDiagram
    participant U as Usuario (Cliente)
    participant API as FastAPI (/orchestrate)
    participant M as Manager (SK)
    participant W as Writer Agent
    participant R as Reviewer Agent

    U->>API: POST /orchestrate (task)
    API->>M: run_multi_agent_task(task)
    M->>W: Inicia conversación
    W-->>M: "Eslogan propuesto..."
    M->>R: Envía a revisión
    R-->>M: "APROBADO"
    M->>M: should_terminate() = True
    M-->>API: Retorna respuesta del Writer
    API-->>U: JSON { "result": "..." }
```

3. Componentes de Software

- **API Layer** (`app/main.py`): FastAPI. Expone los endpoints y maneja la concurrencia.
- **Agent Engine** (`app/agents/manager.py`): Configura la orquestación, los agentes y el manager de control.
- **Agents** (`writer.py`, `reviewer.py`): Definen la personalidad, instrucciones y el servicio de LLM a utilizar.
- **LLM Factory** (`app/core/llm_factory.py`): Patrón Registry para instanciar el proveedor de IA (OpenRouter).