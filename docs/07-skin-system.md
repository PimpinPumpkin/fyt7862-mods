# 07 — The FYT/lsec skin system (and the no‑decrypt override)

Some SYU apps (the **Bluetooth dialer** is the clear case) don't draw their UI from app resources —
they load it from an **external, AES‑encrypted skin pack**. Understanding this is the difference between
"can't touch the brushed‑metal bar" and "flatten any of it in one rebuild."

## How it works

- The skin pack lives at `/oem/app/<appdir>/assets/core_ogg/res_<x>.ogg`
  (BT: `/oem/app/190000002_yx_com.syu.bt/assets/core_ogg/res_bt.ogg`).
- Despite the `.ogg` extension it's a **ZIP** (store‑compressed entries) holding the real drawables:
  `bt_dial0..9`, `bt_dialdial` (call), `bt_dialhang` (hangup), `bt_menu{dial,contact,history,av,pair,set}`
  (the 6 tabs, `+_p` active), `bt_menu_bk` (tab‑bar bg), `bt_bk`/`bk_day` (backgrounds), …
- It's loaded by the bundled framework `com.lsec.core.frame.app.MyUi.getDrawableFromPath(name, …)`.
- The ZIP is **AES‑encrypted** (Zip4j). `unzip` and `7zz` both fail to extract (0‑byte output); the
  MD5‑looking `3c6e0b8a9c15224a8228b9a98ca1531d` in `Zip4jUtilFunc` is **not** a usable password.
  You **cannot** cleanly decrypt/repack it.

## The override (this is the whole trick)

You don't need to. `getDrawableFromPath` resolves a name in this order:

```
1. mResources.getIdentifier(name, "drawable", appPkg)   ← the APP's own resources, checked FIRST
2. only if that returns 0 → the encrypted skin zip
```

So **add a drawable with the exact skin name to the app's own `res/` and rebuild** — `getIdentifier`
finds it, returns it, and the skin zip is never consulted for that name. No decryption, ever.

```bash
# example: flatten the brushed-metal tab bar
#   bt_menu_bk is the tab-bar bg in the skin → make our own flat one
cp flat_dark_768x96.png stock_bt/res/drawable-nodpi-v4/bt_menu_bk.png
apktool b -f stock_bt -o bt.apk     # then sign + /fem install + reboot (docs/08)
```

That single drop turned the iOS‑era brushed‑metal bar flat. The full icon‑set modernization
(`scripts/mkbticons.py`) is the same move ×20: render clean Material SVGs to PNGs named exactly like the
skin assets, drop them in `res/`, rebuild.

## Finding the names

`unzip -l res_<x>.ogg` lists every entry's **name** — the central directory isn't encrypted even though
the entries are. Match names to on‑screen elements (e.g. `bt_menu_history` = the call‑log tab) and
override the ones you want.

## When an app does NOT use a skin pack

The **FM radio** (`com.syu.radio`) has no `assets/core_ogg/` — its drawables are in the APK, so you edit
them directly (recolor/replace `radio_ch`, `radio_menu_bk`, etc.) and rebuild. Same end result, simpler.
(Editing the app's own `radio_bk` worked precisely because app‑res beats any skin lookup.)

> Low‑risk: overriding a name that isn't actually used simply has no effect — it can't break the app.
