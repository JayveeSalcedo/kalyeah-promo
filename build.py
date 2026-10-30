"""Builds promo/index.html from index.src.html, the weapon and kid data and the game font.

Run from the repo root: python3 promo/build.py
"""
import base64
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROMO = ROOT / "promo"
KINDS = {0: ("Attack", "k-attack"), 1: ("Control", "k-control"), 2: ("Block", "k-block"), 3: ("Heal", "k-heal")}
KID_ORDER = ["junjun", "ligaya", "migo", "toni", "popoy", "inday"]
GAME_ORDER = ["Tumbang preso", "Bato-bato-pik", "Jackstone", "Trumpo", "Langit Lupa"]


def fields(path: pathlib.Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r'^(\w+) = &?"?(.*?)"?$', line)
        if m and m.group(1) not in out:
            out[m.group(1)] = m.group(2)
    return out


def cards() -> str:
    weapons = [fields(p) for p in sorted((ROOT / "data/weapons").glob("*.tres"))]
    weapons.sort(key=lambda w: (GAME_ORDER.index(w["street_game"]), int(w["kind"]), w["display_name"]))
    rows = []
    for w in weapons:
        kind, cls = KINDS[int(w["kind"])]
        rows.append(
            f'<div class="card"><div class="art"><img src="img/cards/{w["id"]}.webp" alt="{html.escape(w["display_name"])} card art" '
            f'width="512" height="677" loading="lazy"><span class="cost" title="Ice water cost">{w["elixir_cost"]}</span></div>'
            f'<h3>{html.escape(w["display_name"])}</h3><span class="kind {cls}">{kind} · {html.escape(w["street_game"])}</span>'
            f'<p>{html.escape(w["description"])}</p></div>'
        )
    return "\n      ".join(rows)


def deck() -> str:
    weapons = [fields(p) for p in sorted((ROOT / "data/weapons").glob("*.tres"))]
    return json.dumps([{"id": w["id"], "name": w["display_name"], "cost": int(w["elixir_cost"])} for w in weapons])


def kids() -> str:
    rows = []
    for kid_id in KID_ORDER:
        k = fields(ROOT / f"data/characters/{kid_id}.tres")
        rows.append(
            f'<div class="kid"><img src="img/kids/{kid_id}.webp" alt="{html.escape(k["display_name"])} character card" '
            f'width="480" height="737" loading="lazy"><h3>{html.escape(k["display_name"])}</h3>'
            f'<p>{html.escape(k["description"])}</p></div>'
        )
    return "\n      ".join(rows)


def main() -> None:
    font = base64.b64encode((ROOT / "assets/fonts/clash/Clash-Regular.otf").read_bytes()).decode()
    page = (PROMO / "index.src.html").read_text(encoding="utf-8")
    page = page.replace("__CLASH__", font).replace("__CARDS__", cards()).replace("__KIDS__", kids()).replace("__DECK__", deck())
    (PROMO / "index.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
