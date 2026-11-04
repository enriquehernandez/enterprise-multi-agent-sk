# Glosario Técnico de Agentes y Semantic Kernel

### ¿Qué es un Sistema Multi-Agente (Multi-Agent System o MAS)?
Es una arquitectura de software en la que múltiples agentes autónomos (cada uno con un rol, objetivos y capacidades específicas) colaboran para resolver un problema complejo. En lugar de tener un solo agente "todopoderoso", el trabajo se divide en especialidades (ej. Escritor, Revisor, Traductor). Estos agentes se comunican entre sí (generalmente mediante mensajes) y un **Orquestador** coordina sus interacciones hasta alcanzar un objetivo común. 
*En este proyecto, el MAS está compuesto por el `Writer`, el `Reviewer` y el `ApprovalGroupChatManager` que los coordina.*

### ¿Qué es Semantic Kernel?
Es un SDK de código abierto de Microsoft que permite integrar modelos de lenguaje (LLMs) con código tradicional (C#, Python, Java). Su objetivo es actuar como un "kernel" (núcleo) que orquesta funciones (plugins) y agentes para automatizar tareas complejas.

### ¿Qué es un Agente Autónomo?
Es una entidad de software impulsada por un LLM que tiene un rol, un conjunto de instrucciones y la capacidad de tomar decisiones (como pedir una revisión o aprobar un contenido) de forma independiente.

### ¿Qué es `ChatCompletionAgent`?
Es la clase de Semantic Kernel que nos permite instanciar un agente. Recibe tres parámetros clave: 
1. `service`: El modelo de lenguaje a usar (a través de nuestra fábrica `llm_factory`).
2. `name`: El nombre del agente (ej. "Writer").
3. `instructions`: El "System Prompt" o conjunto de reglas que definen su personalidad y comportamiento.

### ¿Qué es `GroupChatOrchestration`?
Es un patrón de orquestación de Semantic Kernel donde múltiples agentes trabajan juntos en un "chat grupal". Un `Manager` decide qué agente debe hablar a continuación basándose en el historial de la conversación.

### ¿Qué es un `RoundRobinGroupChatManager`?
Es el manager por defecto que asigna turnos de forma circular (Agente A -> Agente B -> Agente A). Es predecible y fácil de depurar, pero tiene el riesgo de permitir bucles infinitos si no se configura un límite de rondas.

### ¿Qué es el "Agent Chatter" (Bucle de Cortesía)?
Es un fenómeno común en sistemas multi-agente donde los agentes, tras completar una tarea, continúan conversando con cortesías (ej. "Gracias", "De nada"). Esto consume tokens innecesariamente y retrasa la respuesta final. En este proyecto, lo resolvemos con un manager personalizado (`ApprovalGroupChatManager`) que corta el flujo al detectar la palabra clave.

### ¿Qué es `BooleanResult` en el contexto de Semantic Kernel?
Es el objeto que retorna el método `should_terminate`. Contiene un valor booleano (`result=True/False`) y una razón (`reason`). Si es `True`, el framework detiene la orquestación inmediatamente y pasa al estado final.

### ¿Qué es LLM-as-a-Judge?
Es una técnica de evaluación donde se utiliza un LLM (con temperatura baja) para actuar como "juez" y calificar la calidad de la respuesta de otro LLM, comparándola con un criterio de referencia o "ground truth". En este proyecto, el script `evaluate_judge.py` implementa esta técnica para auditar el resultado final de la orquestación.