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
- **Bottom bar** `radio_menu_bk` (768×100): flat `#15171f`; the 154×100 `radio_menu_*` cells redrawn as
  **labeled Material glyphs** (`scripts/mkradio.py`): icon on top + a text label below — `BAND SCAN ST TA
  AF PTY LOC NOTES SAVE SET` — white `#d7dbe2`, slider‑blue `_p` (active), dim `#5a5e66` `_u`. The bar's
  functions are non‑obvious (1st cycles FM bands + AM, one scans, ST locks mono, NOTES is per‑station
  notes; swipe for more) so the labels disambiguate.
- **Font → Inter**: radio text is code‑drawn by `com.syu.ctrl.{JText,JButton,JCheckBox}` (extend TextView,
  no typeface). Inject `setTypeface(Typeface.createFromAsset(getAssets(),"Inter.ttf"))` into each
  `<init>(Context,MyUi)` (smali, `.locals 2` → v0/v1 free) and bundle `assets/Inter.ttf`.

## Bluetooth (`com.syu.bt`, activity `.BtAct` → runs as `com.syu.air`‑style uid system)

Uses the **encrypted skin pack** → modernize via the override ([07-skin-system.md](07-skin-system.md)):
- Background: drop a flat dark `bt_bk` into app res.
- Tab bar: flat `bt_menu_bk`.
- **Icon set** (`scripts/mkbticons.py`): clean Material glyphs for `bt_menu{dial,contact,history,av,pair,set}`
  (white normal `#d2d6dd`, slider‑blue `#71b5ff` active) + `bt_dialdial` (green circle + phone) /
  `bt_dialhang` (red circle + rotated phone) + `bt_diallinkcut` (link) + `bt_dialdel` (backspace).
- **Player transport** `btav_{pre,playpause,stop,next}` (+ `bt_navi_av_*`): flat dark `#243049` rounded
  cards, slider‑blue glyphs (pressed `#4a72b8` + white), matching the dialer.
- **Album‑art placeholder**: the stock "Bluetooth 5.1" gradient badge + vinyl record were two layers —
  **`bt_av`** (the shown 38 KB composite) → a flat dark `#243049` rounded card with a centered slider‑blue
  music note; **`bt_navi_btav`(+`_p`)** (the badge overlay) → transparent. (Find which layer is actually
  drawn empirically — the badge is hidden when idle.)
- Drop all into app res, rebuild — the skin zip is bypassed.
- **Incoming‑call ring**: `Page_PopBtRing` plays **`/mnt/sdcard/.btring/ring.mp3`** via `MyMediaPlayer`
  (`STREAM_RING`); the app has a built‑in ring picker (copies a chosen file there + saves `name_ring`). The
  stock tone is loud — drop a quiet local mp3 at that path (a soft 2‑note chime via `ffmpeg sine`,
  `artifacts/bt_incoming_chime.mp3`) so it's calm and not ear‑splitting over music. Persists across reboots.
- **In-call OSD**: the active-call bar + DTMF keypad are `com.syu.bt` skin drawables, override via app
  res (07-skin-system). Keypad numbers `bt_dial0..9`, `*`=`bt_dialx`, `#`=`bt_dialj` (each a full grey glossy
  button); bar = `bt_dialtxt_bk` (call-info box), `bt_dialsound` (headset/audio), `bt_dial_showkey` /
  `bt_keyboardshow` / `bt_dial_keyboard_show` / `bt_keyboardhide` (keypad toggle), `bt_navihang` (end-call).
  Re-rendered all flat: dark `#21242e` rounded buttons + white digits/glyphs, slider-blue `_p`; the call-info
  box flat `#1a1c24`; `bt_navihang` a flat red `#c0392b` button + white Material call-end glyph. Drop into app
  res, rebuild, reboot.

## FYT Settings (`com.syu.settings`)

**Tab glyphs → modern Material** (`scripts/mksetbt.py`): the bottom tabs `rotate_set_menu_{wifi,device,
system,factory,people,common}`(+`_p`) are 128×80 cells — redraw as centered Material glyphs (wifi /
monitor / gear / wrench / person / tune), white `#d7dbe2`, slider‑blue `#71b5ff` active, to match the BT
set.
- **Dark background**: the grey skeuomorphic bg is `rotate_light_bk` (768×1024, portrait/day) / `rotate_dark_bk`
  (night) — replace both (+ `set_bk`, `rotate_bk`) with a flat `#0e0f13` image. (Recoloring `bk`/`rotate_bk`
  alone is inert — those aren't the active bg; the SetBkView per‑view setter + these full‑screen bgs are.)
- **PIN keypad** (`scripts/mksetbt.py`): `set_pin_0..9`(+`_p`), `set_pin_confirm`(+`_p`), `set_pin_delete`(+`_p`)
  are compiled `R.drawable` refs → overwrite the files with flat dark rounded buttons + white digits/glyphs
  (Material check / backspace), slider‑blue for pressed + confirm.
- **Toggles**: the on/off switch is `JSwitchButton`; its drawables come from the markup **`drawableExtra`**
  attr (comma-split: `MyUi` -> `Markup.GetAttr("drawableExtra")` -> `setStrDrawableExtra`), NOT `sw_*`/`set_sw_*`
  (those aren't the switch -- why the earlier overrides were inert). A 2-element `drawableExtra` -> 2-state image
  (`bIsCheckBox`; `setIconName` loads `[0]`=off / `[1]`=on); a single `drawable=` attr -> bg toggle
  (`updateBackground`: `base` off, `base+"_p"` on). The portrait slide switch is **`rotate_set_bottom`/`_p`**
  (86x42, glossy silver knob); landscape twin **`set_bottom`/`_p`** (95x53). Overwrote all four flat: dark
  `#30333b` track + grey `#9aa0ab` knob (off, knob-left); slider-blue `#4a72b8` track + white knob (on,
  knob-right). (`check_sevenlight1..7` glossy boxes are the 7-colour-pick **checkboxes** -- left as-is.)

**Android
Settings** (`com.android.settings`): the visible teal is the *framework* `?android:colorAccent`
(`#80cbc4`), not an app color — matching it needs a platform‑signed framework RRO overlay (root). Left
teal by choice.
