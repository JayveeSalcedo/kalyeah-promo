"""Builds promo/index.html from index.src.html, the kid data and the game font.

Run from the repo root: python3 promo/build.py
"""
import base64
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROMO = ROOT / "promo"
KID_ORDER = ["junjun", "ligaya", "migo", "toni", "popoy", "inday"]


def fields(path: pathlib.Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r'^(\w+) = &?"?(.*?)"?$', line)
        if m and m.group(1) not in out:
            out[m.group(1)] = m.group(2)
    return out


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
    page = page.replace("__CLASH__", font).replace("__KIDS__", kids())
    (PROMO / "index.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
