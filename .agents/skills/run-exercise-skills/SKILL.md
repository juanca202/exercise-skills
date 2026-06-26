---
name: run-exercise-skills
description: Run, smoke-test, and evaluate the agent skills in this repo. Use when asked to run the exercise-skills project, smoke-test the skills, check that the skill scripts work, or evaluate a skill's agent behavior with skillgrade.
---

# Run exercise-skills

This repo is **not an app** — it is a collection of Claude/agent skills under
`.agents/skills/` (`make-coffee`, `roll-dice`, `system-info`, `project-health`,
`plan-form`, `compare-products`, …). There is no server, GUI, or build step.
"Running" it means two things:

1. **Smoke-test the runnable skill artifacts** — the skills that ship an
   executable script. This is the fast, deterministic, no-network path and the
   one you want by default. Driver: `.agents/skills/run-exercise-skills/smoke.sh`.
2. **Evaluate a skill's agent behavior** — does an agent discover and use the
   skill correctly. Driver: `scripts/skillgrade.sh` (wraps the `skillgrade` CLI
   and loads the repo-root `.env`).

> Paths below are relative to the repo root (`<unit>/`). The driver lives at
> `.agents/skills/run-exercise-skills/`. Note `.claude/skills` is a **symlink**
> to `.agents/skills`, so the same skills are discoverable under both paths.

## Prerequisites

- **Node.js** (repo verified on v26; anything 20+ is fine) and **bash**.
- For the eval path only: `skillgrade` (`npm i -g skillgrade`, v0.1.5 verified)
  and the `claude` CLI logged in (subscription). **Docker is NOT required** for
  the verified path — it uses `--provider=local`.

## Run (agent path) — smoke-test the skill scripts

```bash
bash .agents/skills/run-exercise-skills/smoke.sh
```

Drives every skill that has an executable artifact and asserts on real output:

- **system-info** → runs `system-info/scripts/system-info.sh`, checks the OS and
  user lines.
- **roll-dice** → runs the inline one-liner from its `SKILL.md`
  (`echo $((RANDOM % 20 + 1))`), checks the result is in range.
- **project-health** → runs `project-health/scripts/project-health.js` against a
  throwaway `package.json` fixture, checks name/version/dep count.

Prints `PASS`/`FAIL` per check and exits non-zero if any fail. Verified output:

```
== summary: 6 passed, 0 failed ==
```

The other skills (`make-coffee`, `plan-form`, `compare-products`, `roll-dice-tools`)
are prose-only — they have no script to execute. Drive those by invoking the
skill in a Claude session (`/make-coffee`, etc.) or with the eval path below.

## Run (eval path) — drive a skill's agent behavior with skillgrade

`skillgrade` spins up an agent, gives it a task, and grades the result. Use the
repo wrapper so it loads `.env` from the repo root and runs inside the target
skill directory (the one containing `SKILL.md`). It needs an `eval.yaml`; this
repo's existing `evals/*.json` files are from a different (web) evaluator and
skillgrade does **not** read them.

```bash
# From repo root — <skill-dir> is relative to the repo root:
bash scripts/skillgrade.sh .agents/skills/<skill-name> [skillgrade args...]

# From inside a skill directory (omit <skill-dir>):
cd .agents/skills/<skill-name>
bash ../../../scripts/skillgrade.sh init --force
```

The wrapper sources `exercise-skills/.env` (e.g. `GEMINI_API_KEY`) and `cd`s
into the skill before calling `skillgrade`. Without it, `skillgrade` only looks
for `.env` in the skill directory.

A verified, ready eval lives next to this skill. To reproduce the run that was
confirmed in this container (PASS, 100%):

```bash
# 1. Work on a copy so you don't touch the tracked skill:
cp -R .agents/skills/system-info /tmp/sg-system-info
cp .agents/skills/run-exercise-skills/example-eval.yaml /tmp/sg-system-info/eval.yaml

# 2. Run one trial with the local provider + claude CLI (no Docker, no API key):
bash scripts/skillgrade.sh /tmp/sg-system-info \
  --eval=show-system-info --agent=claude --provider=local --trials=1 --parallel=1

# 3. Review:
bash scripts/skillgrade.sh /tmp/sg-system-info preview   # CLI report
```

Verified result:

```
1/1   PASS  1.00  15.9s  2 cmds
Pass Rate  100.0%
```

Reports are written to `$TMPDIR/skillgrade/<skill-name>/results/*.json`.

To scaffold an eval for a skill that has none:

```bash
bash scripts/skillgrade.sh .agents/skills/<skill-name> init
```

With `GEMINI_API_KEY` (or similar) in the repo-root `.env`, `init` uses AI to
generate tasks. Without an API key it produces a **TODO template** — its grader is
a stub that always scores 0. Replace the `tasks:` block with a real instruction
and grader (see `example-eval.yaml`) before running.

## Gotchas

- **`.claude/skills` is a symlink** to `.agents/skills`. Edit/inspect skills via
  `.agents/skills/`; both paths point at the same files.
- **`skillgrade`'s default provider is `docker`**, and Docker is not running in
  this environment. Always pass `--provider=local` for the verified path.
- **`--agent=claude` uses the logged-in `claude` CLI subscription** — no
  `ANTHROPIC_API_KEY` required. (The README implies an API key; the local+claude
  path works off the subscription, matching `billingMode: subscription` in the
  repo's history files.)
- **macOS has no `timeout` command.** Don't wrap skillgrade in `timeout`; use the
  `timeout:` field inside `eval.yaml` (skillgrade enforces it internally).
- **The repo's `evals/*.json` and `benchmark.json` are NOT skillgrade's format.**
  They come from a separate evaluator (`provider: claude-cli`). skillgrade uses
  `eval.yaml` and writes to `$TMPDIR/skillgrade/...`, not back into the repo.
- **Use `scripts/skillgrade.sh` instead of calling `skillgrade` directly** so the
  repo-root `.env` is loaded. The wrapper `cd`s into the skill dir; running bare
  `skillgrade` at the repo root finds many skills.
- **Run evals on a copy when experimenting.** It auto-detects the skill from the
  nearest `SKILL.md`.

## Troubleshooting

- `command not found: timeout` — you wrapped a command in `timeout` on macOS.
  Drop it (see Gotchas).
- skillgrade exits immediately complaining about Docker / image build — you left
  the default provider. Add `--provider=local`.
- skillgrade grades every trial 0.00 right after `init` — the template grader is
  a `{"score": 0.0, "details": "TODO"}` stub. Write a real grader.
- `project-health.js` prints `package.json not found` — pass a directory that
  contains a `package.json` as the first argument; the smoke driver builds a
  fixture for this automatically.
