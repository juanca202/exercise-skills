#!/usr/bin/env bash
# Wrapper for skillgrade — loads the repo-root .env and runs from a skill directory.
#
# skillgrade only reads .env from the current working directory. This script
# sources exercise-skills/.env and cds into the target skill before invoking it.
#
# Usage:
#   bash scripts/skillgrade.sh <skill-dir> [skillgrade args...]   # from repo root
#   bash scripts/skillgrade.sh [skillgrade args...]               # from inside a skill dir
#
# Examples:
#   bash scripts/skillgrade.sh .agents/skills/hello init --force
#   cd .agents/skills/hello && bash ../../../scripts/skillgrade.sh init --force
#   bash scripts/skillgrade.sh .agents/skills/hello --provider=local --smoke

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

usage() {
  echo "Uso:" >&2
  echo "  $(basename "$0") <skill-dir> [skillgrade args...]   # desde la raíz del repo" >&2
  echo "  $(basename "$0") [skillgrade args...]               # desde un directorio con SKILL.md" >&2
  echo "Ejemplos:" >&2
  echo "  $(basename "$0") .agents/skills/hello init --force" >&2
  echo "  cd .agents/skills/hello && $(basename "$0") init --force" >&2
}

resolve_skill_dir() {
  local candidate="$1"
  if [[ -f "$candidate/SKILL.md" ]]; then
    (cd "$candidate" && pwd)
    return 0
  fi
  if [[ -f "$ROOT/$candidate/SKILL.md" ]]; then
    echo "$ROOT/$candidate"
    return 0
  fi
  return 1
}

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

SKILL_DIR=""

if [[ $# -gt 0 ]] && resolved="$(resolve_skill_dir "$1" 2>/dev/null || true)" && [[ -n "$resolved" ]]; then
  SKILL_DIR="$resolved"
  shift
elif [[ -f "$(pwd)/SKILL.md" ]]; then
  SKILL_DIR="$(pwd)"
else
  usage
  echo >&2
  if [[ $# -gt 0 ]]; then
    echo "Error: '$1' no es un directorio de skill (falta SKILL.md)." >&2
    echo "       Si ya estás dentro del skill, omite la ruta: $(basename "$0") $*" >&2
  else
    echo "Error: indica un directorio de skill o ejecuta desde uno que contenga SKILL.md." >&2
  fi
  exit 1
fi

if ! command -v skillgrade >/dev/null 2>&1; then
  echo "Error: skillgrade no está instalado (npm i -g skillgrade)" >&2
  exit 1
fi

cd "$SKILL_DIR"
exec skillgrade "$@"
