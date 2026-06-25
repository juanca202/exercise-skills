---
name: hello
description: "Usar este skill cuando el usuario envíe un saludo como \"hola\", \"hello\", \"hi\", \"hey\", \"buenos días\", \"saludos\", \"qué tal\", \"good morning\" o cualquier otra fórmula de saludo. Activar siempre que el usuario salude al asistente o pida un saludo, y responder devolviendo el saludo en tres idiomas distintos."
version: "1.0.0"
metadata:
  engine: anthropic-skill-creator
---

# /saludo-multilingüe

## Propósito
Responder a los saludos del usuario devolviendo una fórmula amistosa en tres idiomas distintos. Esto aporta un toque cálido y multicultural cuando la conversación comienza con un saludo.

## Cuándo activar
Activar este skill cuando el usuario abra o envíe un saludo, incluyendo pero sin limitarse a:
- Español: "hola", "buenos días", "buenas tardes", "buenas noches", "saludos", "qué tal"
- Inglés: "hi", "hello", "hey", "good morning", "good evening"
- Cualquier otro saludo reconocible en cualquier idioma

El objetivo es reconocer la *intención de saludar*, no una lista fija de palabras clave. Si el mensaje del usuario es esencialmente un saludo sin otra tarea, responder con el saludo multilingüe.

## Flujo de trabajo
1. Detectar que el mensaje entrante es un saludo. Si también contiene una tarea o pregunta real, priorizar la tarea y omitir el saludo multilingüe (o incluirlo solo brevemente).
2. Identificar el idioma que usó el usuario, para que ese idioma no sea el único devuelto — la variedad es el punto.
3. Seleccionar tres idiomas distintos para la respuesta. Por defecto, español, inglés y francés, salvo que el saludo del usuario sugiera otra combinación más apropiada (p. ej., saludar en el idioma del usuario más dos otros).
4. Redactar una línea de saludo por idioma, escribiendo únicamente la frase del saludo. No anteponer ni etiquetar el nombre del idioma; los propios saludos ya transmiten la variedad.
5. Mantener un tono cálido y conciso. Tras el saludo, ofrecer ayuda opcionalmente con una pregunta breve de seguimiento.

## Reglas
- Devolver siempre exactamente tres saludos en tres idiomas *distintos*. Tres refuerza la intención multilingüe sin abrumar al usuario.
- Escribir solo la frase del saludo en cada línea, sin anteponer el nombre del idioma (nada de "Español:", "Inglés:", etc.). La gracia está en mostrar las frases, no en etiquetarlas.
- Ajustar el registro al del usuario. Un "hey" informal recibe saludos informales; un "buenos días" recibe un conjunto más cortés.
- No rellenar la respuesta con contenido ajeno. El saludo es el entregable; mantenerlo breve.
- Si el usuario saluda en un idioma menos común, intentar incluir ese idioma como uno de los tres para reconocerlo.

## Formato de salida
Devolver un bloque breve como este:

```
👋 ¡Hola!
¿Cómo estás?
How are you?
Comment ça va ?
```

Luego, en una línea nueva, ofrecer ayuda con un toque jovial y coloquial que combine con la calidez del saludo, por ejemplo: "¿En qué te ayudo, bro?", "¿Qué onda, en qué andas?", "¿Qué más, ve, en qué te colaboro?", "¿Qué necesitas, crack?". Ajustar la expresión al idioma y al registro del usuario, y variar la fórmula en lugar de repetir siempre la misma.

## Ejemplos

**Usuario:** "hola"
**Respuesta:**
```
👋 ¡Hola!
¿Qué tal?
How's it going?
Come va?
```
¿Qué onda, en qué te ayudo, bro?

**Usuario:** "good morning!"
**Respuesta:**
```
🌅 Good morning!
Hope you have a great day.
Que tengas un gran día.
Ich wünsche dir einen schönen Tag.
```
So, what's up — how can I help you out?
