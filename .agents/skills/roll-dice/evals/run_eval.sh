#!/usr/bin/env bash
# Orquesta el ciclo completo de evals de roll-dice de forma autónoma:
#   prepare (worktree + fixture verificado) -> run (claude -p headless) -> grade -> cleanup
#
# Cada eval corre en su propio git worktree con su MEMORY.md sembrado, así los
# estados opuestos (con/sin regla) no se pisan y se pueden lanzar en paralelo.
# El run se ejecuta con claude -p --output-format stream-json, cuyos eventos traen
# los tool_use en el mismo formato que parsea grade_usage.py (no hace falta buscar
# el transcript por ruta).
#
# Uso:
#   bash run_eval.sh                 # corre todos los evals
#   bash run_eval.sh 1               # corre solo el eval con id=1
#   MODEL=sonnet bash run_eval.sh    # fija el modelo del run
#
# Salidas por eval en: <evals>/runs/eval-<id>/
#   events.jsonl   -> stream de eventos del run (transcript para grading)
#   result.txt     -> texto final del run
#   grading.json   -> resultado de las usage_assertions (formato del visor)
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$HERE" rev-parse --show-toplevel)"
EVALS="$HERE/evals.json"
RUNS_DIR="$HERE/runs"
WT_BASE="${WT_BASE:-$RUNS_DIR/.worktrees}"
MODEL="${MODEL:-}"            # vacío = modelo por defecto del CLI
ALLOWED="Bash Read Glob Grep" # herramientas que el run puede usar sin prompts

# IDs a correr: argumentos, o todos los del evals.json
if [ "$#" -gt 0 ]; then
  IDS=("$@")
else
  mapfile -t IDS < <(python3 -c "import json;print('\n'.join(str(e['id']) for e in json.load(open('$EVALS'))['evals']))")
fi

mkdir -p "$RUNS_DIR" "$WT_BASE"

run_one() {
  local id="$1"
  local rundir="$RUNS_DIR/eval-$id"
  local wt="$WT_BASE/eval-$id"
  mkdir -p "$rundir"

  echo "[$id] prepare worktree + fixture"
  local wtpath
  if ! wtpath="$(python3 "$HERE/fixture.py" prepare --evals "$EVALS" --eval-id "$id" --repo-root "$REPO_ROOT" --worktree "$wt" 2>"$rundir/prepare.err")"; then
    echo "[$id] PRECONDICIÓN FALLIDA (run abortado):"; cat "$rundir/prepare.err"
    return 1
  fi

  local prompt skill
  prompt="$(python3 -c "import json;print(next(e['prompt'] for e in json.load(open('$EVALS'))['evals'] if e['id']==$id))")"
  skill="$(cat "$wtpath/.agents/skills/roll-dice/SKILL.md")"

  echo "[$id] run: claude -p \"$prompt\" (cwd=worktree)"
  ( cd "$wtpath" && claude -p "$prompt" \
      --output-format stream-json --verbose \
      --allowedTools $ALLOWED \
      ${MODEL:+--model "$MODEL"} \
      --append-system-prompt "Tienes disponible el skill roll-dice. Síguelo al pie de la letra para esta tarea:

$skill" \
    ) > "$rundir/events.jsonl" 2>"$rundir/run.err"

  # Texto final del run (último evento type=result, campo result)
  python3 -c "
import json
res=''
for line in open('$rundir/events.jsonl'):
    line=line.strip()
    if not line: continue
    try:o=json.loads(line)
    except:continue
    if o.get('type')=='result' and 'result' in o: res=o['result']
open('$rundir/result.txt','w').write(res)
print('[%s] result:'%'$id', (res[:160].replace(chr(10),' ') or '(sin texto)'))
"

  echo "[$id] grade usage_assertions"
  python3 "$HERE/grade_usage.py" --transcript "$rundir/events.jsonl" \
    --evals "$EVALS" --eval-id "$id" --out "$rundir/grading.json" >/dev/null
  python3 -c "
import json
g=json.load(open('$rundir/grading.json'))
s=g['summary']
print('[%s] usage: %d/%d'%('$id', s['passed'], s['total']))
for e in g['expectations']:
    print('      ', 'PASS' if e['passed'] else 'FAIL', '-', e['text'])
"

  echo "[$id] cleanup"
  python3 "$HERE/fixture.py" cleanup --repo-root "$REPO_ROOT" --worktree "$wtpath" >/dev/null
}

for id in "${IDS[@]}"; do
  echo "==================== eval $id ===================="
  run_one "$id"
  echo
done

echo "Listo. Resultados en: $RUNS_DIR/eval-<id>/"
