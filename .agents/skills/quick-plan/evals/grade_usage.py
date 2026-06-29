#!/usr/bin/env python3
"""Verifica assertions de USO (qué tools, skills o agentes usó un run) leyendo
el transcript .jsonl de un subagente y emite grading en el formato del visor.

Por qué existe: las assertions normales se evalúan contra el OUTPUT del run, pero
"¿usó la herramienta X?", "¿leyó MEMORY.md?", "¿NO lanzó subagentes?" solo se
pueden comprobar mirando la traza real de tool calls. Esto lo hace de forma
programática (más fiable que a ojo) y reutilizable entre iteraciones.

Tipos de check soportados (campo "type" en cada usage_assertion):
  tool_used / tool_not_used   -> ¿hubo un tool_use? Filtra por "tool" (nombre,
                                 opcional; None = cualquiera) y "input_contains"
                                 (substring dentro del input serializado, opcional).
  skill_invoked / skill_not_invoked  -> tool_use name=Skill; filtra por "skill".
  agent_spawned / agent_not_spawned  -> tool_use name=Agent; filtra por "agent_type".

Uso:
  # Lee usage_assertions de evals.json para un eval concreto:
  python grade_usage.py --transcript <run.jsonl> --evals evals.json --eval-id 0

  # O pasa las assertions inline:
  python grade_usage.py --transcript <run.jsonl> --assertions '[{...}]'

Salida: imprime el JSON de grading por stdout y, si se pasa --out, lo escribe ahí.
"""
import argparse
import json
import sys


def load_tool_calls(transcript_path):
    """Devuelve [(name, input_dict), ...] en orden para todos los tool_use del transcript."""
    calls = []
    with open(transcript_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = obj.get("message")
            content = msg.get("content") if isinstance(msg, dict) else None
            if not isinstance(content, list):
                continue
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    calls.append((block.get("name"), block.get("input") or {}))
    return calls


def _input_text(inp):
    return json.dumps(inp, ensure_ascii=False)


def _find_tool(calls, tool=None, input_contains=None):
    """Primer tool_use que casa (name y substring). Devuelve (name, input) o None."""
    for name, inp in calls:
        if tool is not None and name != tool:
            continue
        if input_contains is not None and input_contains not in _input_text(inp):
            continue
        return (name, inp)
    return None


def check(assertion, calls):
    t = assertion.get("type")
    text = assertion.get("text", f"(sin texto) [{t}]")

    if t in ("tool_used", "tool_not_used"):
        hit = _find_tool(calls, assertion.get("tool"), assertion.get("input_contains"))
        used = hit is not None
        passed = used if t == "tool_used" else (not used)
        evidence = (f"Encontrado tool_use {hit[0]} input={_input_text(hit[1])[:200]}"
                    if hit else "No se encontró ningún tool_use que coincida")
        return {"text": text, "passed": passed, "evidence": evidence}

    if t in ("skill_invoked", "skill_not_invoked"):
        want = assertion.get("skill")
        hit = next(((n, i) for n, i in calls
                    if n == "Skill" and (want is None or i.get("skill") == want)), None)
        inv = hit is not None
        passed = inv if t == "skill_invoked" else (not inv)
        evidence = (f"Skill invocado: {hit[1].get('skill')}" if hit
                    else "No se invocó ningún Skill que coincida")
        return {"text": text, "passed": passed, "evidence": evidence}

    if t in ("agent_spawned", "agent_not_spawned"):
        want = assertion.get("agent_type")
        hit = next(((n, i) for n, i in calls
                    if n == "Agent" and (want is None or i.get("subagent_type") == want)), None)
        spawned = hit is not None
        passed = spawned if t == "agent_spawned" else (not spawned)
        evidence = (f"Agent lanzado: {hit[1].get('subagent_type')}" if hit
                    else "No se lanzó ningún subagente que coincida")
        return {"text": text, "passed": passed, "evidence": evidence}

    return {"text": text, "passed": False,
            "evidence": f"Tipo de check desconocido: {t!r}"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True, help="Ruta al .jsonl del run")
    ap.add_argument("--assertions", help="JSON inline con la lista de usage_assertions")
    ap.add_argument("--evals", help="Ruta a evals.json")
    ap.add_argument("--eval-id", type=int, help="id del eval dentro de evals.json")
    ap.add_argument("--out", help="Ruta donde escribir el grading (opcional)")
    args = ap.parse_args()

    if args.assertions:
        assertions = json.loads(args.assertions)
    elif args.evals is not None and args.eval_id is not None:
        data = json.load(open(args.evals, encoding="utf-8"))
        ev = next((e for e in data["evals"] if e.get("id") == args.eval_id), None)
        if ev is None:
            sys.exit(f"No existe eval con id={args.eval_id} en {args.evals}")
        assertions = ev.get("usage_assertions", [])
    else:
        sys.exit("Pasa --assertions, o bien --evals y --eval-id")

    calls = load_tool_calls(args.transcript)
    expectations = [check(a, calls) for a in assertions]
    result = {
        "expectations": expectations,
        "summary": {
            "passed": sum(1 for e in expectations if e["passed"]),
            "total": len(expectations),
        },
    }
    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out)
    print(out)


if __name__ == "__main__":
    main()
