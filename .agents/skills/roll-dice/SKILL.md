---
name: roll-dice
description: Tirar dados usando un generador de números aleatorios. Usar cuando se pida tirar un dado (d6, d20, etc.), tirar dados o generar una tirada aleatoria.
---

Para tirar un dado, usar el siguiente comando que genera un número aleatorio del 1 al número de caras indicado:

```bash
echo $((RANDOM % <sides> + 1))
```

```powershell
Get-Random -Minimum 1 -Maximum (<sides> + 1)
```

Reemplazar `<sides>` por el número de caras del dado (p. ej., 6 para un dado estándar, 20 para un d20).
