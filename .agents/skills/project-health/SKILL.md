---
name: project-health
description: Analyze the health of a software project. Use when asked to evaluate project quality, testing status, or repository health.
---

The script is located in the same skill directory under `scripts/project-health.js`.

Execute the script from the skill directory and pass the current working directory (the user's project) as the first argument:

```bash
node scripts/project-health.js "$PWD"
```

Analyze the JSON output and provide:

1. A health score from 0 to 100.
2. Strengths.
3. Risks.
4. Recommended next actions.