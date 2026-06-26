---
name: roll-dice-tools
description: Tirar dados usando un generador de números aleatorios. Usar cuando se pida tirar un dado (d6, d20, etc.), tirar dados o generar una tirada aleatoria.
---

## Plan de ejecución

Al iniciar la tirada, usar la **herramienta de to-do** para mostrar las tareas a ejecutar y actualizar su estado a medida que se completen. Crear al menos estas tareas:

1. **Confirmar número de caras** — leer `MEMORY.md`; si hay preferencia guardada o el usuario lo indicó, marcar como completada sin preguntar.
2. **Ejecutar tirada** — generar el valor aleatorio con el comando correspondiente.
3. **Generar visualización** — crear la imagen del dado con el resultado.

Marcar cada tarea como `completed` al terminarla y dejar `in_progress` solo en la que se esté ejecutando.

## Número de caras

**Antes de cualquier otra acción**, leer el archivo `MEMORY.md` en la raíz del repositorio actual para conocer las preferencias persistentes del usuario. Este paso es **obligatorio** aunque el número de caras parezca obvio o el usuario no lo haya mencionado.

Determinar el número de caras siguiendo este orden de prioridad:

1. Si el usuario lo indicó explícitamente en el mensaje → usar ese valor.
2. Si en `MEMORY.md` hay una regla sobre el número de caras por defecto → aplicarla **sin preguntar** y marcar la tarea "Confirmar número de caras" como completada directamente.
3. Solo si ninguna de las dos anteriores aplica → preguntar mediante la **herramienta de preguntas estructuradas** del cliente (opciones tappables).

Reglas para cuando sí hay que preguntar:

- **Una pregunta** con hasta **3 opciones** mutuamente excluyentes, por ejemplo: `d6 (6 caras)` / `d20 (20 caras)` / `d10 (10 caras)`.
- **Fallback**: si el cliente no expone la herramienta, preguntar en prosa con opciones enumeradas (1, 2, 3…).
- No tirar el dado hasta tener el número de caras confirmado.

## Tirada

Para tirar un dado, usar el siguiente comando que genera un número aleatorio del 1 al número de caras indicado:

```bash
echo $((RANDOM % <sides> + 1))
```

```powershell
Get-Random -Minimum 1 -Maximum (<sides> + 1)
```

Reemplazar `<sides>` por el número de caras del dado (p. ej., 6 para un dado estándar, 20 para un d20).

## Visualización

Tras obtener el resultado, usar la **herramienta de generación de imágenes** para mostrar un dado con el número de caras indicado y el valor obtenido en la tirada. La imagen debe:

- Representar visualmente un dado de `<sides>` caras (p. ej., forma de d6, d10 o d20 según corresponda).
- Mostrar de forma clara y legible el **resultado** de la tirada.
- Incluir en la descripción el tipo de dado y el valor (p. ej., «d20 mostrando el número 7»).
