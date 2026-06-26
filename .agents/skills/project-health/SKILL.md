---
name: project-health
description: Analizar la salud de un proyecto de software. Usar cuando se pida evaluar la calidad del proyecto, el estado de las pruebas o la salud del repositorio.
---

Ejecuta el script desde el directorio del skill y pasa el directorio de trabajo actual (el proyecto del usuario) como primer argumento:

```bash
node ./scripts/project-health.js "$PWD"
```

Analiza la salida JSON y proporciona:

1. Una puntuación de salud de 0 a 100.
2. Fortalezas.
3. Riesgos.
4. Próximas acciones recomendadas.
