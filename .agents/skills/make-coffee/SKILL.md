---
name: make-coffee
description: Ayuda a preparar distintas bebidas de café.
---

Responde siempre en el idioma en que el usuario está escribiendo.

Si el usuario pregunta sobre espresso, leer `./references/espresso.md`.

Si el usuario pregunta sobre latte, leer `./references/latte.md`.

Al final de cada respuesta, incluye una sección con el encabezado **Archivos de contexto dinámico** y lista solo los archivos de contexto dinámico de la sesión actual de chat. Sé conciso: solo una lista, sin explicaciones. No muestres archivos que no estén en la sesión.

## Casos de prueba

- Prompt: "¿Cómo saco un buen espresso en casa?"
  Esperado: "debe activarse"
- Prompt: "¿Cuál es la proporción correcta de leche y espresso para un latte?"
  Esperado: "debe activarse"
- Prompt: "¿Por qué mi espresso sale muy amargo y aguado?"
  Esperado: "debe activarse"
- Prompt: "¿Puedes explicarme cómo hacer un latte clásico con latte art?"
  Esperado: "debe activarse"
- Prompt: "¿Cómo hago rebase de mi rama feature sobre main sin conflictos?"
  Esperado: "no debe activarse"
- Prompt: "¿Cuál es la mejor forma de curar una sartén de hierro fundido?"
  Esperado: "no debe activarse"
- Prompt: "Ayúdame a escribir una función en Python para parsear un archivo CSV."
  Esperado: "no debe activarse"
- Prompt: "¿Qué vino tinto va bien con un bistec a la parrilla?"
  Esperado: "no debe activarse"
