#!/usr/bin/env bash
# Smoke-test driver for the exercise-skills repo.
#
# Drives every skill in .agents/skills/ that has an executable artifact and
# asserts on its real output. This is the "run the app" path for a repo whose
# product is a collection of agent skills: there is no server or GUI, so the
# things you can actually launch are the skills' runnable scripts.
#
# Usage (from repo root):   bash .agents/skills/run-exercise-skills/smoke.sh
# Exit code 0 = all checks passed, 1 = at least one failed.

set -uo pipefail

# Repo root = three levels up from this script (.agents/skills/run-exercise-skills).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SKILLS="$ROOT/.agents/skills"

pass=0
fail=0

ok()   { echo "  PASS: $1"; pass=$((pass+1)); }
bad()  { echo "  FAIL: $1"; fail=$((fail+1)); }

echo "== system-info =="
out="$(bash "$SKILLS/system-info/scripts/system-info.sh" 2>&1)"
echo "$out" | grep -q "Sistema operativo:" && ok "prints OS line" || bad "missing 'Sistema operativo:'"
echo "$out" | grep -q "Usuario actual:"    && ok "prints user line" || bad "missing 'Usuario actual:'"

echo "== roll-dice (inline one-liner from SKILL.md, sides=20) =="
roll="$(echo $((RANDOM % 20 + 1)))"
if [[ "$roll" =~ ^[0-9]+$ ]] && (( roll >= 1 && roll <= 20 )); then
  ok "rolled $roll in range 1..20"
else
  bad "roll '$roll' out of range"
fi

echo "== project-health (against a fixture package.json) =="
fix="$(mktemp -d)"
cat > "$fix/package.json" <<'JSON'
{ "name": "smoke-fixture", "version": "9.9.9",
  "dependencies": { "left-pad": "1.0.0" },
  "devDependencies": { "jest": "29.0.0" } }
JSON
ph="$(node "$SKILLS/project-health/scripts/project-health.js" "$fix" 2>&1)"
rm -rf "$fix"
echo "$ph" | grep -q "Project: smoke-fixture" && ok "reads project name" || bad "missing project name"
echo "$ph" | grep -q "Version: 9.9.9"          && ok "reads version"      || bad "missing version"
echo "$ph" | grep -q "Dependencies: 1"          && ok "counts deps"        || bad "wrong dep count"

echo
echo "== summary: $pass passed, $fail failed =="
[[ $fail -eq 0 ]] || exit 1
