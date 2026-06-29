#!/usr/bin/env bash
# Orquesta el ciclo completo de evals de quick-plan de forma autónoma:
#   prepare (worktree + fixture verificado) -> run (claude -p headless) -> grade -> cleanup
#
# Cada eval corre en su propio git worktree con su MEMORY.md sembrado, así los
# estados opuestos (con/sin regla) no se pisan y se pueden lanzar en paralelo.
# El run se ejecuta con claude -p --output-format stream-json, cuyos eventos traen
# los tool_use en el mismo formato que parsea grade_usage.py (no hace falta buscar
# el transcript por ruta).
#
# Uso:
#   bash run_eval.sh                 # corre todos los evals (1 vez c/u)
#   bash run_eval.sh 1               # corre solo el eval con id=1
#   MODEL=sonnet bash run_eval.sh    # fija el modelo del run
#   REPS=3 bash run_eval.sh          # corre cada eval 3 veces y reporta tasa de acierto
#                                    # (detecta assertions inestables entre corridas)
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
REPS="${REPS:-1}"            # nº de repeticiones por eval (>1 = mide tasa de acierto)
ALLOWED="Bash Read Glob Grep" # herramientas que el run puede usar sin prompts

# IDs a correr: argumentos, o todos los del evals.json
# (sin mapfile: el bash de macOS es 3.2 y no lo trae)
IDS=()
if [ "$#" -gt 0 ]; then
  for a in "$@"; do IDS+=("$a"); done
else
  while IFS= read -r line; do
    [ -n "$line" ] && IDS+=("$line")
  done < <(python3 -c "import json;print('\n'.join(str(e['id']) for e in json.load(open('$EVALS'))['evals']))")
fi

mkdir -p "$RUNS_DIR" "$WT_BASE"

run_one() {
  local id="$1"
  local rundir="$2"   # dónde escribir events/result/grading de ESTA corrida
  local wt="$3"       # ruta del worktree a usar (única por corrida)
  mkdir -p "$rundir"

  echo "[$id] prepare worktree + fixture"
  local wtpath
  if ! wtpath="$(python3 "$HERE/fixture.py" prepare --evals "$EVALS" --eval-id "$id" --repo-root "$REPO_ROOT" --worktree "$wt" 2>"$rundir/prepare.err")"; then
    echo "[$id] PRECONDICIÓN FALLIDA (run abortado):"; cat "$rundir/prepare.err"
    return 1
  fi

  local prompt skill
  prompt="$(python3 -c "import json;print(next(e['prompt'] for e in json.load(open('$EVALS'))['evals'] if e['id']==$id))")"
  skill="$(cat "$wtpath/.agents/skills/quick-plan/SKILL.md")"

  echo "[$id] run: claude -p \"$prompt\" (cwd=worktree)"
  ( cd "$wtpath" && claude -p "$prompt" \
      --output-format stream-json --verbose \
      --allowedTools $ALLOWED \
      ${MODEL:+--model "$MODEL"} \
      --append-system-prompt "Tienes disponible el skill quick-plan. Síguelo al pie de la letra para esta tarea:

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

# Agrega la tasa de acierto de un eval a partir de los grading.json de sus reps.
aggregate_eval() {
  local id="$1"; shift
  python3 - "$id" "$@" <<'PY'
import json, sys
eid, dirs = sys.argv[1], sys.argv[2:]
runs, pass_runs = 0, 0
per_assert = {}  # text -> [passed_count, total_count]
for d in dirs:
    try:
        g = json.load(open(f"{d}/grading.json", encoding="utf-8"))
    except Exception:
        continue
    runs += 1
    s = g["summary"]
    if s["passed"] == s["total"]:
        pass_runs += 1
    for e in g["expectations"]:
        st = per_assert.setdefault(e["text"], [0, 0])
        st[1] += 1
        if e["passed"]:
            st[0] += 1
print(f"[{eid}] AGREGADO: {pass_runs}/{runs} corridas perfectas "
      f"({(100*pass_runs/runs if runs else 0):.0f}%)")
for text, (p, t) in per_assert.items():
    flag = "" if p == t else "   <-- inestable"
    print(f"      {p}/{t}  {text}{flag}")
PY
}

for id in "${IDS[@]}"; do
  echo "==================== eval $id ===================="
  rep_dirs=()
  for rep in $(seq 1 "$REPS"); do
    if [ "$REPS" -gt 1 ]; then
      rundir="$RUNS_DIR/eval-$id/rep-$rep"
      wt="$WT_BASE/eval-$id-rep-$rep"
      echo "-------- rep $rep/$REPS --------"
    else
      rundir="$RUNS_DIR/eval-$id"
      wt="$WT_BASE/eval-$id"
    fi
    run_one "$id" "$rundir" "$wt"
    rep_dirs+=("$rundir")
  done
  [ "$REPS" -gt 1 ] && aggregate_eval "$id" "${rep_dirs[@]}"
  echo
done

if [ "$REPS" -gt 1 ]; then
  echo "Listo. Resultados en: $RUNS_DIR/eval-<id>/rep-<k>/ (con tasa de acierto agregada)"
else
  echo "Listo. Resultados en: $RUNS_DIR/eval-<id>/"
fi
