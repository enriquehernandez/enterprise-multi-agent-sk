# Orchestration Contract (Contrato de Orquestación)

## El `ApprovalGroupChatManager`
Para evitar el "Agent Chatter", se implementó un manager personalizado.

### Contrato de `should_terminate`
- **Entrada:** El historial de la conversación (`ChatHistory`).
- **Lógica:**
  1. Se obtiene el último mensaje del historial.
  2. Si el mensaje proviene del `Reviewer` y su contenido (en mayúsculas) contiene la palabra `"APROBADO"`.
  3. Retorna `BooleanResult(result=True)`.
  4. En caso contrario, retorna `BooleanResult(result=False)`.
- **Efecto:** Cuando retorna `True`, el framework de Semantic Kernel detiene inmediatamente la orquestación y no permite que el `Writer` responda con "Gracias".

## Flujo de Datos
1. `run_multi_agent_task(task)` inicializa el `runtime`.
2. La orquestación invoca al `Writer`.
3. El `Writer` genera una respuesta.
4. El manager verifica si el `Writer` aprobó (No).
5. La orquestación invoca al `Reviewer`.
6. El `Reviewer` responde "APROBADO".
7. El manager verifica si el `Reviewer` aprobó (Sí).
8. La orquestación termina y se extrae la respuesta guardada en el callback.