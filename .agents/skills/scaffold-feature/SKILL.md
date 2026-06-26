---
name: scaffold-feature
description: "Activar cuando el usuario pida crear o scaffoldear una nueva feature, módulo o componente. Crea un plan en plan/, espera aprobación y genera el archivo resultado en results/."
version: "2.0.0"
---

# Scaffold feature

Dos fases: **PLANEAR** → aprobación → **EJECUTAR**. Nunca ejecutes sin aprobación.

## FASE 1 — Plan

Con el nombre/descripción recibida, determina el slug (kebab-case) y el siguiente secuencial:

```bash
ls results/ 2>/dev/null | grep -E '^[0-9]{3}-' | sort | tail -1
```

- Si hay archivos: toma el número del último y suma 1.
- Si no hay archivos: empieza en `001`.

Crea `plan/{slug}.md`:

```markdown
# Plan: {nombre}

## Archivo destino
results/{NNN}-{slug}.md

## Secciones a generar
- Descripción general
- Componentes principales
- Consideraciones técnicas
```

Luego muestra el plan al usuario y pregunta: **"¿Arrancamos o ajustamos algo?"**

## FASE 2 — Ejecución

Solo si el usuario aprueba:

1. Genera el contenido según el plan
2. Guarda en `results/{NNN}-{slug}.md`
3. Confirma con:
✅ Listo.

📄 results/{NNN}-{slug}.md

## Reglas
- Slug: lowercase, guiones, sin espacios ni caracteres especiales.
- Secuencial: siempre basarse en el archivo más alto existente en `results/`, no en el conteo total.
- Si `plan/` o `results/` no existen, crearlos.
- Si el usuario pide cambios al plan, actualizar `plan/{slug}.md` antes de ejecutar.