# 00 — Overview, connection & ground rules

## Connecting ADB

USB is flaky on these. The reliable path:
1. **Rear 4‑pin port, USB‑A ↔ A cable** (a host port, not the front).
2. Developer options → **USB role = Device**, then **reboot** (a runtime toggle alone often won't enumerate).
3. `adb devices` → it shows up (this unit's USB serial: `ae9c2360f77258a06c4f453e44e79674`).
4. After root, **persistent wireless ADB**: `adb shell su -c "setprop persist.adb.tcp.port 5555"`,
   then `adb connect <ip>:5555` (survives reboot). This unit used `192.168.158.150:5555`.

## Key facts to know before you touch anything

- **Version is faked.** `ro.build.version.release` says 16, but SDK = **29 / Android 10** (set in
  `config.txt`). Treat API 29 as the hard ceiling.
- **Panel is upside‑down.** `ro.sf.swrotation=180`; the uboot logo BMP is stored 180°‑rotated.
- **`/oem` is read‑only**; write via **`/fem`** (the rw alias of `mmcblk0p42`). Files are **immutable**
  (`chattr +i`) → clear with Magisk busybox `chattr -i` before overwriting.
- **`su` quoting trap.** Always `adb shell 'su -c "…"'` (blob form) or root work silently runs as uid 2000.
- **Three different bars are three different apps:** status bar = `com.android.systemui`;
  nav bar (home/volume/back) = `com.syu.air`; the orange volume popup = `com.syu.ms`.
- **Reskins need a full reboot** to show (cached resources survive a process kill).

## What's reversible

- App reskins: keep a copy of each stock APK; `cat` the original back via `/fem` + reboot.
- Root: only `boot` is touched; reflash stock boot (or full firmware) to undo.
- Splash/wallpaper: backups in `artifacts/splash/`.

## Tooling used to build all this (host = macOS)

`adb`, **apktool 3.x**, Android **build‑tools 35** (`apksigner`/`zipalign`/`aapt2`), Java 17, `openssl`,
`ffmpeg` (recolors), **`rsvg-convert`** (`brew install librsvg`, for icons), Python 3 stdlib
(raw‑PNG generation — no PIL on macOS). Get the platform + testkey signing keys with `scripts/fetch_keys.sh` — they're public AOSP keys, **not**
committed to this repo.
