#!/usr/bin/env python3
"""Genera un reporte HTML autónomo a partir de los resultados en runs/.

Lee runs/eval-<id>/rep-<k>/ (o runs/eval-<id>/ si REPS=1) y produce un HTML con:
  - resumen por eval (tasa de corridas perfectas)
  - por cada repetición: el texto final del run y el detalle de assertions
  - marca de assertions inestables (no pasan en todas las repeticiones)

Uso:
  python make_report.py                 # escribe runs/report.html
  python make_report.py --out ruta.html
"""
import argparse
import glob
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_eval_meta():
    data = json.load(open(os.path.join(HERE, "evals.json"), encoding="utf-8"))
    return {e["id"]: e for e in data["evals"]}


def rep_dirs(eid):
    multi = sorted(glob.glob(os.path.join(HERE, "runs", f"eval-{eid}", "rep-*")))
    if multi:
        return multi
    flat = os.path.join(HERE, "runs", f"eval-{eid}")
    return [flat] if os.path.exists(os.path.join(flat, "grading.json")) else []


def read(path):
    try:
        return open(path, encoding="utf-8").read()
    except OSError:
        return ""


def collect():
    metas = load_eval_meta()
    evals = []
    for eid in sorted(metas):
        m = metas[eid]
        reps = []
        per_assert = {}
        perfect = 0
        for d in rep_dirs(eid):
            try:
                g = json.load(open(os.path.join(d, "grading.json"), encoding="utf-8"))
            except OSError:
                continue
            s = g["summary"]
            if s["passed"] == s["total"]:
                perfect += 1
            for e in g["expectations"]:
                st = per_assert.setdefault(e["text"], [0, 0])
                st[1] += 1
                if e["passed"]:
                    st[0] += 1
            reps.append({"result": read(os.path.join(d, "result.txt")).strip(),
                         "summary": s, "expectations": g["expectations"]})
        evals.append({"id": eid, "name": m.get("name", str(eid)),
                      "prompt": m.get("prompt", ""), "expected": m.get("expected_output", ""),
                      "reps": reps, "perfect": perfect, "total": len(reps),
                      "per_assert": per_assert})
    return evals


CSS = """
:root{--bg:#0f1117;--card:#1a1d27;--ink:#e6e8ef;--mut:#9aa0b4;--ok:#3fb950;--bad:#f85149;--warn:#d29922;--line:#2a2e3d;--accent:#6e9bff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:32px 20px 80px}
h1{font-size:24px;margin:0 0 4px}.sub{color:var(--mut);margin:0 0 28px}
.summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:32px}
.scard{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.scard .nm{font-weight:600}.scard .pr{font-size:28px;font-weight:700;margin:6px 0}
.scard .meta{color:var(--mut);font-size:13px}
.pill{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12px;font-weight:600}
.pill.ok{background:rgba(63,185,80,.15);color:var(--ok)}
.pill.bad{background:rgba(248,81,73,.15);color:var(--bad)}
.pill.warn{background:rgba(210,153,34,.15);color:var(--warn)}
.eval{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px;margin-bottom:20px}
.eval h2{margin:0 0 2px;font-size:18px}.prompt{color:var(--accent);font-family:ui-monospace,Menlo,monospace;font-size:13px;margin:0 0 4px}
.exp{color:var(--mut);font-size:13px;margin:0 0 16px}
.assertbar{margin:14px 0 6px;border-top:1px solid var(--line);padding-top:14px}
.assertrow{display:flex;align-items:center;gap:10px;padding:5px 0;font-size:14px}
.assertrow .frac{font-family:ui-monospace,Menlo,monospace;color:var(--mut);min-width:42px}
.reps{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-top:14px}
.rep{border:1px solid var(--line);border-radius:10px;padding:12px;background:#13161f}
.rep .rh{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-size:13px;color:var(--mut)}
.rep .res{font-size:13px;white-space:pre-wrap;border-left:3px solid var(--line);padding-left:10px;color:var(--ink)}
.rep ul{margin:10px 0 0;padding-left:0;list-style:none;font-size:12.5px}
.rep li{padding:3px 0;display:flex;gap:7px}
.tick{font-weight:700}.tick.ok{color:var(--ok)}.tick.bad{color:var(--bad)}
.foot{color:var(--mut);font-size:12px;text-align:center;margin-top:24px}
"""


def pill(perfect, total):
    if total == 0:
        return '<span class="pill warn">sin datos</span>'
    cls = "ok" if perfect == total else ("warn" if perfect else "bad")
    return f'<span class="pill {cls}">{perfect}/{total} perfectas</span>'


def render(evals):
    rows = []
    # tarjetas resumen
    cards = []
    for e in evals:
        pct = (100 * e["perfect"] / e["total"]) if e["total"] else 0
        cards.append(f"""<div class="scard"><div class="nm">#{e['id']} · {html.escape(e['name'])}</div>
        <div class="pr">{pct:.0f}%</div>
        <div class="meta">{e['perfect']}/{e['total']} corridas perfectas</div></div>""")
    rows.append('<div class="summary">' + "".join(cards) + "</div>")

    for e in evals:
        ab = []
        for text, (p, n) in e["per_assert"].items():
            stable = p == n
            mark = ('<span class="pill ok">estable</span>' if stable
                    else '<span class="pill bad">inestable</span>')
            ab.append(f'<div class="assertrow"><span class="frac">{p}/{n}</span>'
                      f'<span>{html.escape(text)}</span>{mark}</div>')
        reps_html = []
        for i, r in enumerate(e["reps"], 1):
            s = r["summary"]
            items = []
            for x in r["expectations"]:
                t = "ok" if x["passed"] else "bad"
                g = "✓" if x["passed"] else "✗"
                items.append(f'<li><span class="tick {t}">{g}</span>'
                             f'<span>{html.escape(x["text"])}</span></li>')
            res = html.escape(r["result"]) or "<em>(sin texto)</em>"
            reps_html.append(f"""<div class="rep"><div class="rh"><span>rep {i}</span>
            {pill(1 if s['passed']==s['total'] else 0,1)}</div>
            <div class="res">{res}</div><ul>{''.join(items)}</ul></div>""")
        rows.append(f"""<div class="eval"><h2>#{e['id']} · {html.escape(e['name'])} {pill(e['perfect'],e['total'])}</h2>
        <p class="prompt">prompt: "{html.escape(e['prompt'])}"</p>
        <p class="exp">{html.escape(e['expected'])}</p>
        <div class="assertbar">{''.join(ab)}</div>
        <div class="reps">{''.join(reps_html)}</div></div>""")

    n_eval = len(evals)
    n_perfect = sum(1 for e in evals if e["total"] and e["perfect"] == e["total"])
    return f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>roll-dice · reporte de evals</title><style>{CSS}</style></head><body><div class="wrap">
<h1>🎲 roll-dice — reporte de evaluación</h1>
<p class="sub">{n_perfect}/{n_eval} evals perfectos en todas sus repeticiones · grading programático del uso de herramientas</p>
{''.join(rows)}
<p class="foot">Generado desde runs/eval-&lt;id&gt;/rep-&lt;k&gt;/grading.json</p>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "runs", "report.html"))
    args = ap.parse_args()
    html_doc = render(collect())
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(html_doc)
    print(args.out)


if __name__ == "__main__":
    main()
