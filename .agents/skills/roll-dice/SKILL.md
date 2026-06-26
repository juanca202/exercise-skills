---
name: roll-dice
description: Tirar dados usando un generador de números aleatorios. Usar cuando se pida tirar un dado (d6, d20, etc.), tirar dados o generar una tirada aleatoria.
---

**Antes de cualquier otra acción**, leer el archivo `MEMORY.md` en la raíz del repositorio actual para conocer las preferencias persistentes del usuario.

Una vez leído, determinar el número de caras siguiendo este orden de prioridad:

1. Si el usuario lo indicó explícitamente en el mensaje → usar ese valor.
2. Si en `MEMORY.md` hay una regla sobre el número de caras por defecto → aplicarla **sin preguntar**.
3. Solo si ninguna de las dos anteriores aplica → preguntarle al usuario cuántas caras tiene el dado (p. ej., 6 para un dado estándar, 20 para un d20).

Una vez conocido el número de caras, usar el siguiente comando que genera un número aleatorio del 1 al número de caras indicado: 

```bash
echo $((RANDOM % <sides> + 1))
```

```powershell
Get-Random -Minimum 1 -Maximum (<sides> + 1)
```

Reemplazar `<sides>` por el número de caras del dado (p. ej., 6 para un dado estándar, 20 para un d20).
