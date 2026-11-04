# Problem Statement (Planteamiento del Problema)

## Contexto de Negocio
En entornos empresariales (banca, consultoría, marketing), la generación de contenido técnico o creativo mediante un solo LLM (Large Language Model) presenta dos problemas críticos:
1.  **Alucinaciones:** El modelo puede inventar datos o ignorar restricciones técnicas.
2.  **Falta de revisión:** Un solo paso de generación no garantiza la calidad ni el cumplimiento de normativas (ej. publicidad engañosa).

## Solución Propuesta
Implementar un **Sistema Multi-Agente** donde el trabajo se divide en roles especializados, imitando un equipo humano:
*   **Agente `Writer`:** Encargado de la generación creativa y técnica.
*   **Agente `Reviewer`:** Actúa como auditor, verificando precisión, tono y restricciones. Tiene poder de veto (solicita correcciones).
*   **Orquestador (`Manager`):** Gestiona el flujo de conversación y decide cuándo el trabajo está terminado.

## Valor Diferencial
A diferencia de un chatbot tradicional, este sistema es **autónomo y auto-correctivo**. Si el `Reviewer` detecta un error, el `Writer` recibe el feedback y genera una nueva versión, repitiendo el ciclo hasta que el contenido sea aprobado.