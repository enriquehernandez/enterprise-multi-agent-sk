import asyncio
from app.agents.manager import run_multi_agent_task


async def main():
    task = "Escribe un artículo corto sobre los beneficios de los agentes autónomos en la banca."
    print(f"📝 Tarea: {task}\n")
    result = await run_multi_agent_task(task)
    print(f"\n✅ Resultado Final:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())
