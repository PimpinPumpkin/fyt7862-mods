# SystemUI — Quick Settings

Two stock blues (`#41A4F7`), both recolored to the theme accent (`#7176FA`, the volume‑slider purple):

- **Brightness slider** — `brightness_progress_drawable.xml`: the stock fill was a baked PNG
  (`brightness_progress_drawable_p_default.png`, solid `#41A4F7`). Replaced with an inline purple→cyan
  gradient (`#7176FA → #6CDDFA`). File is here.
- **Active tile circle** — the active QS tiles are **baked `_p` / `_lsec` PNGs** with `#41A4F7` rendered in
  (NOT a runtime tint — `colorAccent` / `QSTileBaseView.mColorActive` are dead ends). Recolored 27 of them
  to `#7176FA` with `../../scripts/recolor_qs_active.py` — pure resource edit, no smali/framework/bootloop.

Both ship inside `artifacts/SystemUI.apk`. Full trace: `docs/03-systemui.md` → "Quick Settings accent".
