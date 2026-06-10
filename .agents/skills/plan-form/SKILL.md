---
name: plan-form
description: Planifica formularios web antes de implementar — campos, validación, arquitectura y pasos de implementación. Usar cuando se pida diseñar, planificar o definir un formulario web, campos de entrada, validación o flujo de captura de datos, o cuando el usuario mencione "planificar formulario", "plan form", "/plan-form" o quiera un plan antes de codificar un form.
---

# Plan de formularios web

Elaborar un **plan de implementación** sin escribir código. Permanecer en modo Plan hasta aprobación o petición explícita de implementar.

## Paso 0 — Modo Plan

Al activarse, invocar `SwitchMode` con `target_mode_id: "plan"` **antes de cualquier otra acción**. Explicar brevemente que se elaborará el plan sin código.

## Paso 1 — Contexto mínimo

Confirmar solo lo que falte. Si el usuario ya lo dio, **no repetir preguntas**.

| Dato | Obligatorio |
|------|-------------|
| Propósito del formulario (qué captura y para qué) | Sí |
| Campos: nombre, tipo, obligatorio | Sí |
| Stack del proyecto (framework, lib de forms/validación) | Sí |
| Envío: endpoint, acción local o solo UI | Sí |
| Restricciones: diseño, a11y, i18n, reglas de negocio | Si aplica |

Usar `AskQuestion` cuando esté disponible; si no, preguntar en prosa con opciones enumeradas.

**Inspeccionar el repo** antes de proponer arquitectura: buscar formularios existentes, librerías de validación (`react-hook-form`, `zod`, `@angular/forms`, etc.) y componentes reutilizables.

## Paso 2 — Redactar el plan

Entregar en el idioma del usuario con esta estructura:

```markdown
# Plan: [nombre del formulario]

## Objetivo
[Qué resuelve y criterio de éxito]

## Campos
| Campo | Tipo | Obligatorio | Validación | Notas |
|-------|------|-------------|------------|-------|
| ...   | ...  | Sí/No       | ...        | ...   |

## Arquitectura
- Componentes a crear o reutilizar
- Estado del formulario (local, contexto, store)
- Librerías / APIs del proyecto

## Validación y errores
- Reglas por campo
- Mensajes y momento de mostrarlos (onBlur, onSubmit, etc.)

## UX y accesibilidad
- Labels, `aria-*`, orden de tabulación
- Estados: loading, disabled, éxito, error global

## Flujo de envío
- Submit: validación → request → feedback
- Errores de red o servidor

## Pasos de implementación
1. [ ] Paso concreto y verificable
2. [ ] ...

## Pruebas sugeridas
- Casos felices y de error por campo
- Accesibilidad básica (teclado, lectores de pantalla)

## Riesgos y decisiones abiertas
- [Puntos que requieran confirmación]
```

**Reglas del plan:**
- Pasos de implementación: verbos imperativos, verificables, ordenados por dependencia.
- Marcar supuestos con asterisco (*) y listarlos en «Riesgos y decisiones abiertas».
- Si el repo tiene convención de specs (p. ej. `docs/specs/`), ofrecer guardar como `[nombre].plan.md`.

## Paso 3 — Cierre

1. Preguntar si aprueba el plan o quiere ajustes.
2. **No implementar código** en modo Plan salvo petición explícita.
3. Si aprueba implementación: invocar `SwitchMode` con `target_mode_id: "agent"` y ejecutar los pasos en orden.

## Límites

- No generar código ni tests durante la planificación.
- No asumir stack: inferirlo del repo o preguntar.
- Responder en el idioma del usuario.
