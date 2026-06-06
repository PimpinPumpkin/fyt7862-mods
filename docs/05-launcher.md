# 05 — Launcher (Lawnchair, single full‑width home)

The stock launcher is `com.android.launcher6`. This unit runs **Lawnchair 15** instead. The one real
problem to fix: Lawnchair rendered the home as **two half‑width panels**.

## The two‑panel bug

Launcher3's `DisplayController$Info.getDeviceType()` classifies **each rotation's** window bounds against
`MIN_TABLET_WIDTH = 600dp` and OR‑s them:
- portrait 768×880dp → tablet
- (theoretical) landscape 1024×**564**dp → phone (564 < 600, because of the taller bar insets)
- mixed → `TYPE_MULTI_DISPLAY` → **two‑panel home**

The unit never rotates, but Launcher3 evaluates all rotations anyway. There is **no flag/pref** for it —
it's purely computed (the 7870 avoids it because A13 inset handling lands landscape at exactly 600dp).

## The fix (one‑instruction smali patch)

In `DisplayController$Info.smali` `getDeviceType()`, the mixed‑bounds branch returns
`MULTI_DISPLAY` (`v3`, value 1). Change it to return **`PHONE`** (`v4`, value 0):

```smali
# mixed-bounds branch:
- return v3      # MULTI_DISPLAY
+ return v4      # PHONE   → single full-width 4×5 page
```

## Build/install (user app, so different from the SYU apps)

`apktool b` fails at the aapt2 resource‑link for this Compose app, **but it still emits the patched
`classes3.dex`** under `dec/build/apk/`. **Dex‑swap** it into the *original* APK (resources stay
byte‑identical), `zipalign`, re‑sign with **any** key (debug is fine — it's a user app on a locked A10),
then `uninstall`→`install` preserving data:

```
tar /data/data/app.lawnchair  → backup
adb uninstall app.lawnchair
adb install lc_patched.apk
# restore: tar -x back  + chown -R <NEW-uid> + restorecon -R   (uid is reassigned on reinstall!)
cmd package set-home-activity app.lawnchair/...
```

Re‑add the clock widget by hand afterward (widget bindings don't survive the reinstall). The patched APK
is in `artifacts/launcher/`.

## Icon accent color (Material You / themed icons)

Home icons are **Lawnicons** (themed monochrome) tinted by the system. On the **7870 (A13)** that tint is
Material You (monet) from the wallpaper → purple. The **7862 is A10 — no Material You** — so themed icons fall
back to **white**, and Lawnchair's `accent_color` does **not** drive that tint.

- Lawnchair's `accent_color` (DataStore `files/datastore/preferences.preferences_pb`) serializes a custom
  color as **`custom|#aarrggbb`** (e.g. `custom|#ffb69df8`); sentinels are `wallpaper_primary` /
  `system_accent` / `default`. (Found in the obfuscated `s9/d$a`+`d$b` `ColorOption` classes — `%08x`.)
  Setting it colors Lawnchair's **own UI**, not the themed app icons on A10.
- Hand‑editing the proto: it's a `PreferenceMap` — each entry is `0a<len> 0a 0c<key> 12<len> 2a<slen><value>`.
  **Update the outer entry length too**, or it won't parse and Lawnchair crashes to the fallback launcher
  (`Unable to parse preferences proto`). Force‑stop Lawnchair, `cat` the new file in, back up first.
- Net: purple icons on A10 would need a framework monet backport or a patched Lawnchair — left white.
