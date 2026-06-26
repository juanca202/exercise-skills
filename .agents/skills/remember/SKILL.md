---
name: remember
description: "Activar SOLO cuando el usuario pida explícitamente recordar, guardar o anotar algo para futuras sesiones: 'recuerda que...', 'anota esto', 'no olvides que...', 'guarda en memoria'. NO activar para conversación general."
version: "1.1.0"
---

# Remember

Persiste en `MEMORY.md` solo lo que el usuario pide explícitamente recordar.

## PASO 1 — Verificar intención

Si el mensaje no contiene una intención clara de persistir información, responder:
> "¿Quieres que recuerde esto para futuras sesiones?"

Solo continuar si la intención es explícita o el usuario confirma.

## PASO 2 — Leer estado actual

```bash
cat MEMORY.md 2>/dev/null || echo "NO_MEMORY"
cat AGENTS.md 2>/dev/null || echo "NO_AGENTS"
```

## PASO 3 — Actualizar MEMORY.md

Si no existe, créalo. Agrega la nueva entrada arriba:

```markdown
# Memory

## {YYYY-MM-DD}
- {lo que el usuario pidió recordar}
```

## PASO 4 — Asegurar referencia en AGENTS.md

Solo si `AGENTS.md` no menciona `MEMORY.md`, agregar al final:

```markdown
## Contexto estático
- [MEMORY.md](./MEMORY.md) — memoria persistente del proyecto
```

## PASO 5 — Confirmar
✅ Guardado en MEMORY.md

📎 Referenciado en AGENTS.md

## Reglas
- Nunca guardar sin intención explícita del usuario.
- Nunca sobreescribir entradas anteriores; solo agregar arriba.
- Si el usuario pide **olvidar** algo, eliminar solo esa línea.
- No modificar nada más en `AGENTS.md` fuera de la referencia a `MEMORY.md`.