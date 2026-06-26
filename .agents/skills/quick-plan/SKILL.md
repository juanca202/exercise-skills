---
name: quick-plan
description: "Activar cuando el usuario pida planificar, descomponer o estructurar una tarea técnica simple. Guía al asistente por tres pasos secuenciales: entender la tarea, definir subtareas y estimar esfuerzo."
version: "1.0.0"
---

# Quick plan

Ejecuta estos pasos **en orden**, uno a la vez. No saltes ni combines pasos.

## Pasos

### PASO 1 — Entender la tarea
Pregunta al usuario:
- ¿Qué hay que hacer? (una línea basta)
- ¿Hay alguna restricción importante? (tecnología, tiempo, etc.)

Espera la respuesta antes de continuar.

### PASO 2 — Descomponer en subtareas
Con la información recibida, lista entre 3 y 5 subtareas concretas y accionables en formato:

 Subtarea 1
 Subtarea 2
 Subtarea 3

Confirma con el usuario si la descomposición tiene sentido.

### PASO 3 — Estimar esfuerzo
Para cada subtarea asigna una estimación simple: `S` (< 1h), `M` (1–4h), `L` (> 4h).
Muestra un resumen final:
SubtareaEsfuerzoSubtarea 1SSubtarea 2M
Cierra con el esfuerzo total estimado en horas.

## Reglas
- Respetar el orden: 1 → 2 → 3. Nunca anticipar información de un paso posterior.
- Ser concreto y breve en cada paso; sin relleno.
- Si el usuario da la info del paso 1 en el mensaje inicial, úsala directamente y pasa al paso 2.