# Kalyeah promo page

One-page promotional site for **Kalyeah**, a 3v3 Filipino street-game brawler for Android.

- `index.html`: the page, ready to open (all art is in `img/`, the game font is inlined).
- `index.src.html`: the template it is built from.
- `build.py`: fills the template with the weapon cards, kids and font from the game repo.

## Rebuild

This folder lives at `promo/` inside the game repo (`earl-gh/kalyeah`), because `build.py` reads `data/` and `assets/` from there:

```sh
python3 promo/build.py
```

The art in `img/` is copied from the game's `assets/`; the screenshots are captured from the game in Godot 4.6.2.

Made by Den Earl De Dios, Jayvee Salcedo and Richard Ace Vallo.
