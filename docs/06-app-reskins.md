# 06 — App reskins (EQ · FM radio · Bluetooth · Settings)

Shared design: **dark near‑neutral surfaces + one accent = the volume‑slider blue→cyan gradient**
(`#7176FA → #6CDDFA`, mid `#71B5FF`); no skeuomorphism; keep functional colors (red dial needle,
green/red call buttons). Build/sign/install per [08-applying.md](08-applying.md).

## Recolor techniques (ffmpeg, no Photoshop)

- **Alpha‑preserving fill** (a single‑color glyph on transparency → accent):
  `ffmpeg -i in.png -vf "format=rgba,geq=r=R:g=G:b=B:a=alpha(X\,Y)" out.png`
- **Whiteness‑preserving blend** (a colored button with a *white label baked on* → accent bg, white kept):
  `t=clip((min(r,g,b)-45)/190,0,1)`, `out_chan = accent*(1-t) + 255*t` (b pinned 255). Works for any bg
  hue, so blue + orange states collapse to one accent.
- **Gradient accent** = the blend with `accent_chan(Y)=lerp(top,bottom,Y/H)` (each element reads blue→cyan
  top→bottom; white labels stay white).
- **Pick what to recolor by saturation** of the mean opaque color (`max-min > 90`) → hits colored accents,
  skips gray inactive states and dark backgrounds. Exclude `*bk*`/launcher/`*.9.png` by name; then
  **hand‑restore functional non‑accent colors** the filter caught (the red `radio_ruler_mark` dial needle).
- **Backgrounds / flat cards / rounded buttons**: hand‑write raw 8‑bit‑RGB PNGs (macOS has no PIL →
  `zlib`+`struct`, see `scripts/mkbg.py`) or render with `rsvg-convert` (`<rect rx=14>` for rounded cards).
- **Icons**: render Material SVG paths to PNG with `rsvg-convert` (`scripts/mkbticons.py`).

## EQ (`com.syu.eq`)

Already dark. Accent was cyan `#00FFFF` named colors (`cyan`/`aqua`/`menu_text_enable`/`speciale_line_color`)
+ 21 hardcoded `*_p.png` active‑state icons (the 4 bottom tabs, arrows, mode‑select, progress). Recolor the
colors + alpha‑fill the icons → slider blue. Ignore `akm_*` (an AKM‑DAC variant this unit never draws).
Build note: bump `minSdkVersion`→26 in `apktool.yml` for the `<adaptive-icon>` aapt2 error.

## FM radio (`com.syu.radio`, UI activity `.act.ActRadio` — *not* `com.syu.carradio`)

No skin pack — APK drawables. Final look:
- **Background** `radio_bk` (768×880): dropped the "earth horizon" for a dark near‑neutral gradient
  (`#131620`→`#0a0b10`).
- **Presets** `radio_ch` (196×96): flat dark card `#243049`; `radio_ch_p` (selected) flat slider‑blue
  `#4a72b8`, rounded corners via rsvg. (Dropped an earlier loud blue→cyan gradient.)
- **Bottom bar** `radio_menu_bk` (768×100): flat `#15171f`; **reflections stripped** from the 154×100
  `radio_menu_*` icon cells with `geq` alpha=0 below y=60.

## Bluetooth (`com.syu.bt`, activity `.BtAct` → runs as `com.syu.air`‑style uid system)

Uses the **encrypted skin pack** → modernize via the override ([07-skin-system.md](07-skin-system.md)):
- Background: drop a flat dark `bt_bk` into app res.
- Tab bar: flat `bt_menu_bk`.
- **Icon set** (`scripts/mkbticons.py`): clean Material glyphs for `bt_menu{dial,contact,history,av,pair,set}`
  (white normal `#d2d6dd`, slider‑blue `#71b5ff` active) + `bt_dialdial` (green circle + phone) /
  `bt_dialhang` (red circle + rotated phone) + `bt_diallinkcut` (link) + `bt_dialdel` (backspace). Drop all
  into app res, rebuild — the skin zip is bypassed.

## FYT Settings (`com.syu.settings`)

Recolored to slider blue, but it's a thin wrapper (low impact). **Android Settings** (`com.android.settings`):
the visible teal is the *framework* `?android:colorAccent` (`#80cbc4`), not an app color — matching it needs a
platform‑signed framework RRO overlay (root). Left teal by choice.
