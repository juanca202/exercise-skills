---
name: system-info
description: Mostrar información básica del sistema operativo. Usar cuando se pida mostrar detalles del sistema, información de la máquina, versión del SO, nombre de host o usuario actual.
---

Determinar el sistema operativo antes de ejecutar un script.

Ejecutar los comandos desde el directorio del skill (la carpeta que contiene este `SKILL.md`). Obtener esa ruta desde la ubicación del skill en el contexto, luego hacer `cd` a ese directorio antes de ejecutar cualquier script.

Para macOS o Linux:

```bash
bash ./scripts/system-info.sh
```

Para Windows:

```powershell
powershell -ExecutionPolicy Bypass -File ./scripts/system-info.ps1
```
