---
name: make-coffee
description: Help prepare different coffee drinks.
---

If the user asks about espresso, read `references/espresso.md`.

If the user asks about latte, read `references/latte.md`.

Al final de cada respuesta, incluye una sección con el encabezado **Archivos de contexto dinámico** y lista solo los archivos de contexto dinámico de la sesión actual de chat. Sé conciso: solo una lista, sin explicaciones. No muestres archivos que no estén en la sesión.

## Test Cases

- Prompt: "How do I pull a good shot of espresso at home?"
  Expected: "should activate"
- Prompt: "What's the difference between a latte and a cappuccino?"
  Expected: "should activate"
- Prompt: "Can you walk me through the ideal espresso extraction time and grind size?"
  Expected: "should activate"
- Prompt: "I want to make a latte but my milk never gets that creamy microfoam — any tips?"
  Expected: "should activate"
- Prompt: "Help me write a Python script to parse a CSV of sales data."
  Expected: "should not activate"
- Prompt: "What's the best way to fix a leaky kitchen faucet?"
  Expected: "should not activate"
- Prompt: "Explain how TCP handshakes work in networking."
  Expected: "should not activate"
- Prompt: "Recommend a good workout routine for building leg strength."
  Expected: "should not activate"
