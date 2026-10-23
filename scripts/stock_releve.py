#!/usr/bin/env python3
"""Relevé quotidien du stock des machines BoosterStop → _data/stock.json

Lancé chaque matin par .github/workflows/stock-releve.yml. Interroge le même
Worker que la page Stock Live, pour chaque machine de _data/machines.yml qui a
un « worker ». Les pages (machines et Stock Live) affichent ce relevé en texte,
lisible par Google ; le stock en direct reste chargé par le navigateur.

Si une machine ne répond pas, son dernier relevé est gardé. Si aucune ne répond,
le fichier n'est pas modifié et le script échoue (GitHub envoie un e-mail).
"""
import datetime, json, os, sys, urllib.request
from zoneinfo import ZoneInfo
import yaml

WORKER = os.environ.get("BS_WORKER", "https://boosterstop-stock.cold-water-7039.workers.dev")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "_data", "stock.json")


def prix(v):
    if v in (None, "", 0, "0"):
        return None
    try:
        return f"{float(str(v).replace(',', '.')):.2f}"
    except ValueError:
        return str(v)


def main():
    machines = yaml.safe_load(open(os.path.join(ROOT, "_data", "machines.yml"), encoding="utf-8"))
    try:
        prev = json.load(open(OUT, encoding="utf-8"))
    except Exception:
        prev = {}
    prev_m = prev.get("machines") or {}
    now = datetime.datetime.now(ZoneInfo("Europe/Zurich")).replace(microsecond=0).isoformat()
    result, seen, tried, ok = {}, {}, 0, 0
    for m in machines:
        w = m.get("worker")
        if w is None or w == "":
            continue
        tried += 1
        req = urllib.request.Request(
            f"{WORKER}/stock?machine={w}",
            headers={"User-Agent": "BoosterStop-releve/1.0 (+https://boosterstop.com)",
                     "Accept": "application/json",
                     "Origin": "https://boosterstop.com",
                     "Referer": "https://boosterstop.com/stock.html"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
            if not data or not data.get("ok"):
                raise ValueError("réponse sans ok")
            mid = data.get("machine_id")
            if mid and mid in seen:
                raise ValueError(f"même machine_id que {seen[mid]}")
            if mid:
                seen[mid] = m["id"]
            par_nom = {}
            for s in data.get("slots") or []:
                if not s.get("configured"):
                    continue
                q = int(s.get("stock") or 0)
                nom = (s.get("goods_name") or "").strip()
                if q <= 0 or not nom:
                    continue
                e = par_nom.setdefault(nom, {"nom": nom, "qte": 0, "prix": None})
                e["qte"] += q
                e["prix"] = e["prix"] or prix(s.get("price"))
            produits = sorted(par_nom.values(), key=lambda x: (-x["qte"], x["nom"].lower()))
            result[m["id"]] = {"ok": True, "maj": now, "produits": produits}
            ok += 1
            print(f"{m['id']}: {len(produits)} produits")
        except Exception as e:
            print(f"[!] {m['id']} (worker {w}) : {e}", file=sys.stderr)
            if m["id"] in prev_m:
                result[m["id"]] = prev_m[m["id"]]
    if tried and not ok:
        print("Aucune machine n'a répondu : relevé précédent conservé.", file=sys.stderr)
        sys.exit(1)
    out = {"maj": now, "machines": result}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(f"Relevé écrit : {ok}/{tried} machines")


if __name__ == "__main__":
    main()
