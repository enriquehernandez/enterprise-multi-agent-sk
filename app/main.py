from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agents.manager import run_multi_agent_task

app = FastAPI(
    title="Enterprise Multi-Agent System",
    description="Sistema multi-agente con Semantic Kernel y OpenRouter",
    version="0.1.0"
)


class TaskRequest(BaseModel):
    task: str


class TaskResponse(BaseModel):
    result: str


@app.post("/orchestrate", response_model=TaskResponse)
async def orchestrate(request: TaskRequest):
    """
    Recibe una tarea en lenguaje natural y la procesa con el sistema multi-agente.
    """
    try:
        result = await run_multi_agent_task(request.task)
        return TaskResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}
