---

## name: task-lifecycle
description: "Activar cuando el usuario quiera crear, avanzar, bloquear o cerrar una tarea. Gestiona el ciclo de vida backlog → in-progress → done con reglas de transición estrictas. Persiste el estado en tasks/TASKS.md."
version: "1.0.0"

# Task lifecycle

Cada tarea tiene un estado. Las transiciones solo ocurren si se cumplen las condiciones. El estado persiste en `tasks/TASKS.md`.

## Estados y transiciones

backlog → in-progress → done

↓

blocked → in-progress


| Desde         | Hacia         | Condición                           |
| ------------- | ------------- | ----------------------------------- |
| `backlog`     | `in-progress` | Sin restricción                     |
| `in-progress` | `done`        | El usuario confirma que está lista  |
| `in-progress` | `blocked`     | El usuario indica un impedimento    |
| `blocked`     | `in-progress` | El usuario indica que se desbloqueó |
| cualquiera    | `backlog`     | ❌ No permitido                      |
| `done`        | cualquiera    | ❌ No permitido                      |


## Comandos reconocidos


| Intención del usuario      | Acción             |
| -------------------------- | ------------------ |
| "crear tarea X"            | Agregar en backlog |
| "empezar / trabajar en X"  | → in-progress      |
| "X está bloqueada por Y"   | → blocked          |
| "se desbloqueó X"          | → in-progress      |
| "X está lista / terminé X" | → done             |
| "ver tareas / estado"      | Mostrar TASKS.md   |


## Formato de TASKS.md

```markdown
# Tasks

| ID  | Tarea        | Estado      | Nota                  |
|-----|-------------|-------------|-----------------------|
| 001 | Nombre tarea | in-progress | bloqueada por: X      |
```

## Por cada transición

1. Leer `tasks/TASKS.md`
2. Verificar que la transición es válida. Si no lo es, responder:
  > "⚠️ No es posible pasar de `{estado actual}` a `{estado pedido}`."
3. Actualizar el estado en la fila correspondiente
4. Confirmar:

✅ Tarea 001 → in-progress

## Reglas

- Si `tasks/` o `TASKS.md` no existen, crearlos al registrar la primera tarea.
- ID secuencial: basarse en el ID más alto existente, no en el conteo.
- Una tarea `done` es inmutable; nunca se modifica.
- Si el usuario intenta una transición inválida, explicar qué transiciones sí son posibles desde ese estado.

