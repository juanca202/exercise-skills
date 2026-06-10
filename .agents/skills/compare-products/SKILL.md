---
name: compare-products
description: Compara dos productos en formato vs extrayendo especificaciones y comentarios de fuentes web y sintetiza una tabla comparativa con puntuación por reseñas. Usar cuando se pida comparar productos, hacer un vs, tabla comparativa, análisis de alternativas, pros/contras entre dos herramientas o servicios, o cuando el usuario mencione "compare products", "/compare-products" o quiera evaluar un producto contra otro.
---

# Comparador de productos (vs)

Comparar **exactamente dos productos** extrayendo especificaciones y comentarios de la web, y entregar una **tabla comparativa** con los nombres de los productos en columnas.

## Regla principal

Este skill **siempre** es un comparador **Producto 1 vs Producto 2**. No comparar más de dos productos en una sola ejecución.

## Paso 1 — Identificar los productos

Extraer del mensaje del usuario los dos productos a comparar. Aceptar formatos como:

- «Notion vs Obsidian»
- «compara iPhone 15 y Samsung S24»
- «Producto A contra Producto B»

**Si falta alguno de los dos productos**, pedirlos antes de investigar (usar `AskQuestion` si está disponible):

1. **Producto 1** — nombre exacto o descripción clara.
2. **Producto 2** — nombre exacto o descripción clara.

No iniciar búsquedas ni lanzar subagentes hasta tener ambos nombres confirmados.

Opcional: si el usuario aporta URLs concretas (web oficial, G2, Capterra, etc.), incluirlas en el prompt del subagente correspondiente.

## Paso 2 — Investigación en paralelo con Task

En **una sola respuesta**, lanzar **exactamente 2** subagentes `Task` con:

- `subagent_type: "generalPurpose"`
- `run_in_background: true`

Un subagente por producto. Esperar a que ambos terminen antes de consolidar.

### Plantilla de prompt por subagente

```
Investiga el producto: [NOMBRE DEL PRODUCTO]

Objetivo: recopilar especificaciones técnicas/comerciales y comentarios o reseñas de usuarios.

Fuentes sugeridas (usar las que el usuario haya indicado; si no, buscar):
- Web oficial del producto
- Una fuente de reseñas (G2, Capterra, Trustpilot, Amazon, etc.)

Herramientas: usa WebSearch para encontrar URLs relevantes y WebFetch para extraer contenido verificable.

Devuelve JSON con esta estructura:

{
  "productName": "[NOMBRE DEL PRODUCTO]",
  "specifications": {
    "precio": "...",
    "categoria": "...",
    "[nombre de spec]": "..."
  },
  "comments": [
    {
      "author": "...",
      "date": "...",
      "text": "...",
      "sentiment": "positive|neutral|negative",
      "source": "URL"
    }
  ],
  "aggregateRating": "...",
  "sources": ["URL1", "URL2"],
  "notes": "datos no encontrados, ambiguos o errores de fetch"
}

Reglas:
- Solo incluir datos que aparezcan en las fuentes consultadas.
- Si WebFetch falla, documentar el error en "notes" y probar otra URL.
- Recopilar al menos 3 comentarios cuando existan en las fuentes.
- No inventar precios, ratings ni citas.
```

## Paso 3 — Consolidación (agente principal)

1. Recibir los JSON de ambos subagentes.
2. Unificar el conjunto de especificaciones: unión de todas las claves de `specifications` de ambos productos.
3. Calcular **puntuación por comentarios** para cada producto (primera fila de la tabla):
   - Si hay `aggregateRating` numérico en la fuente, usarlo y normalizar a escala **0–10** (p. ej. 4.5/5 → 9.0).
   - Si no hay rating agregado, derivar puntuación de los comentarios recopilados:
     - `positive` = 1, `neutral` = 0.5, `negative` = 0
     - Puntuación = promedio × 10, redondeado a 1 decimal
   - Indicar en nota al pie el método usado y el número de comentarios analizados.
4. Marcar celdas sin dato con «—» y anotar gaps en notas al pie.

## Paso 4 — Formato de salida

Entregar en este orden:

### 1. Tabla comparativa (especificaciones en filas, productos en columnas)

```markdown
## [Producto 1] vs [Producto 2]

| Especificación | [Producto 1] | [Producto 2] |
|----------------|--------------|--------------|
| **Puntuación (comentarios)** | 8.4/10 | 7.1/10 |
| Precio | ... | ... |
| ... | ... | ... |
```

Reglas de la tabla:

- **Primera fila de datos:** siempre **Puntuación (comentarios)** con escala 0–10.
- **Primera columna:** nombres de especificaciones (filas).
- **Columnas 2 y 3:** valores de cada producto, usando los nombres exactos confirmados en el Paso 1.
- Orden sugerido tras la puntuación: precio, categoría, specs técnicas relevantes, integraciones, soporte, etc.
- Valores ambiguos o inferidos: marcar con asterisco (*) y explicar en notas al pie.

### 2. Comentarios destacados

```markdown
## Comentarios y reseñas

### [Producto 1]
- **positivo** — @autor (fecha): "texto" — [fuente](url)

### [Producto 2]
- **negativo** — @autor (fecha): "texto" — [fuente](url)
```

Agrupar por producto. Si no hay comentarios en las fuentes, indicarlo explícitamente.

### 3. Resumen (3–5 viñetas)

- Ventaja clara de cada producto según specs y comentarios.
- Gaps de información detectados.
- Fuentes que fallaron o devolvieron datos parciales.

## Calidad y límites

- **No inventar** datos: solo lo extraído por los subagentes desde fuentes web.
- Preferir fuente oficial + una fuente de reseñas por producto.
- Responder en el idioma del usuario.
- Si el usuario pide comparar más de dos productos, explicar el límite de dos y ofrecer ejecutar comparaciones vs adicionales en invocaciones separadas.

## Ejemplos de activación

- «Compara Notion vs Obsidian»
- `/compare-products iPhone 15 vs Samsung Galaxy S24`
- «Quiero un vs entre HubSpot y Pipedrive» (sin nombres claros → pedir Producto 1 y Producto 2)
