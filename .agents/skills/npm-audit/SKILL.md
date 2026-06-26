---
name: npm-audit
description: "Activar cuando el usuario tenga un paquete npm vacío o incompleto y quiera saber qué le falta. Observa el estado real del repo, razona qué falta y guarda un reporte en results/."
version: "1.0.0"
---

# NPM Audit

Loop ReAct: **Observar → Razonar → Actuar**. Nunca asumas el estado del repo; siempre lee primero.

## PASO 1 — Observar

```bash
ls -la
cat package.json 2>/dev/null || echo "NO_PACKAGE_JSON"
```

Evalúa presencia de:

| Archivo       | Requerido |
|---------------|-----------|
| `package.json`| ✅        |
| `README.md`   | ✅        |
| `.gitignore`  | ✅        |
| `index.js`    | ✅        |
| `.npmignore`  | opcional  |

## PASO 2 — Razonar

Declara en voz alta antes de actuar:
Existe:  [lista]

Falta:   [lista]

Acción:  Guardar reporte en results/{NNN}-{slug}.md

Donde `{slug}` viene del campo `name` en `package.json`, o `paquete-sin-nombre` si no existe.

Para el secuencial:
```bash
ls results/ 2>/dev/null | grep -E '^[0-9]{3}-' | sort | tail -1
```

## PASO 3 — Actuar

Crea `results/{NNN}-{slug}.md`:

```markdown
# Reporte npm: {nombre del paquete}

## Estado del repositorio
| Archivo        | Estado  |
|----------------|---------|
| `package.json` | ✅ / ❌ |
| `README.md`    | ✅ / ❌ |
| `.gitignore`   | ✅ / ❌ |
| `index.js`     | ✅ / ❌ |
| `.npmignore`   | ✅ / ❌ |

## Diagnóstico
[Una línea por archivo faltante explicando qué impacto tiene]

## Recomendaciones
- [ ] [acción concreta 1]
- [ ] [acción concreta 2]
```

Confirma con:
✅ Reporte guardado en results/{NNN}-{slug}.md

## Reglas
- Observar siempre antes de razonar; razonar siempre antes de actuar.
- Si `results/` no existe, crearlo.
- Secuencial: basarse en el número más alto existente, no en el conteo.
- Si no hay `package.json`, usar slug `paquete-sin-nombre` y marcarlo como hallazgo crítico.