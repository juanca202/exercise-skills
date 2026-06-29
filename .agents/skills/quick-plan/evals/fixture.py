#!/usr/bin/env python3
"""Prepara/limpia un git worktree aislado para correr un eval con su fixture.

Por qué: varios evals de roll-dice dependen de un MEMORY.md con contenidos
OPUESTOS (con regla de "8 caras por defecto" vs. sin regla). Si corrieran en la
misma raíz se pisarían. Cada run se ejecuta en su propio worktree, donde sembramos
el MEMORY.md que ese eval necesita y VERIFICAMOS la precondición antes de lanzar
el run, para que un fixture mal puesto falle ruidosamente en vez de dar un pase falso.

Subcomandos:
  prepare  Crea el worktree, escribe setup.files, verifica setup.verify.
           Imprime la ruta del worktree por stdout (úsala como cwd del run).
  cleanup  Elimina el worktree.

Ejemplos:
  python fixture.py prepare --evals evals.json --eval-id 1 \
      --repo-root /ruta/al/repo --worktree /tmp/eval-wt/eval-1
  # ... lanza el run con cwd = /tmp/eval-wt/eval-1, califica, y luego:
  python fixture.py cleanup --repo-root /ruta/al/repo --worktree /tmp/eval-wt/eval-1
"""
import argparse
import json
import os
import subprocess
import sys


def _git(repo_root, *args):
    subprocess.run(["git", "-C", repo_root, *args], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def _load_eval(evals_path, eval_id):
    data = json.load(open(evals_path, encoding="utf-8"))
    ev = next((e for e in data["evals"] if e.get("id") == eval_id), None)
    if ev is None:
        sys.exit(f"No existe eval con id={eval_id} en {evals_path}")
    return ev


def cmd_prepare(args):
    ev = _load_eval(args.evals, args.eval_id)
    setup = ev.get("setup") or {}

    # worktree limpio en HEAD; --detach para no crear ramas.
    os.makedirs(os.path.dirname(os.path.abspath(args.worktree)), exist_ok=True)
    _git(args.repo_root, "worktree", "add", "--detach", "--force", args.worktree, "HEAD")

    # Sembrar los archivos del fixture dentro del worktree.
    for rel, content in (setup.get("files") or {}).items():
        dest = os.path.join(args.worktree, rel)
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(content)

    # Verificar la precondición ANTES de lanzar el run.
    verify = setup.get("verify")
    if verify:
        target = os.path.join(args.worktree, verify["file"])
        text = open(target, encoding="utf-8").read() if os.path.exists(target) else ""
        if "must_contain" in verify and verify["must_contain"] not in text:
            _git(args.repo_root, "worktree", "remove", "--force", args.worktree)
            sys.exit(f"PRECONDICIÓN FALLIDA: {verify['file']} no contiene "
                     f"{verify['must_contain']!r}. Run abortado.")
        if "must_not_contain" in verify and verify["must_not_contain"] in text:
            _git(args.repo_root, "worktree", "remove", "--force", args.worktree)
            sys.exit(f"PRECONDICIÓN FALLIDA: {verify['file']} contiene "
                     f"{verify['must_not_contain']!r} y no debería. Run abortado.")

    print(os.path.abspath(args.worktree))


def cmd_cleanup(args):
    _git(args.repo_root, "worktree", "remove", "--force", args.worktree)
    print(f"worktree eliminado: {args.worktree}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prepare")
    p.add_argument("--evals", required=True)
    p.add_argument("--eval-id", type=int, required=True)
    p.add_argument("--repo-root", required=True)
    p.add_argument("--worktree", required=True)
    p.set_defaults(func=cmd_prepare)

    c = sub.add_parser("cleanup")
    c.add_argument("--repo-root", required=True)
    c.add_argument("--worktree", required=True)
    c.set_defaults(func=cmd_cleanup)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
