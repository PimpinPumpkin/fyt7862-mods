# 08 — Applying changes (the `/fem` install pipeline)

All the reskinned apps live in `/oem/app/<NNNN>_<pkg>/`. **`/oem` is a read‑only view of `mmcblk0p42`** —
write through its read‑write alias **`/fem`**. Resource changes only show after a **full reboot**
(a process kill reuses cached resources).

## Build → sign → install

```bash
SDK=~/Library/Android/sdk/build-tools/35.0.0
KEY=path/to/keys          # platform.pk8 + platform.x509.pem (AOSP platform key)

# 1. build (apktool 3.x; decode the device framework first: apktool if framework-res_7862.apk)
apktool b -f <dec_dir> -o app.apk

# 2. align + sign. SYU apps + anything uid 1000/priv-app are signed with the AOSP PLATFORM key
#    (SHA-256 c8a2e9bc…). Platform-signing keeps their system UID.
$SDK/zipalign -p -f 4 app.apk app_aligned.apk
$SDK/apksigner sign --key $KEY/platform.pk8 --cert $KEY/platform.x509.pem --out app_signed.apk app_aligned.apk

# 3. push + install in place via /fem (preserves SELinux ctx)
adb push app_signed.apk /sdcard/app_signed.apk
adb shell 'su -c "
  BB=/data/adb/magisk/busybox
  DIR=/fem/app/<NNNN>_<pkg>
  APK=\$DIR/\$(ls \$DIR | grep -m1 .apk)
  mount -o remount,rw /fem
  blockdev --setrw /dev/block/mmcblk0p42
  \$BB chattr -i \$APK          # FYT marks files immutable; toybox lacks chattr → use Magisk busybox
  cat /sdcard/app_signed.apk > \$APK
  \$BB chattr +i \$APK
"'

# 4. REBOOT (resource changes need a full reboot)
adb reboot
```

`scripts/install_fem.sh` wraps steps 3–4.

## Critical gotchas

- **adb+su quoting.** `adb shell su -c '<multiline>'` silently runs the body as **uid 2000**, not root
  (and a plain `su -c id` still elevates, masking it). Always use the **blob form**:
  `adb shell 'su -c "cmd; cmd"'` — whole device command single‑quoted to adb, inner double‑quoted to su.
- **uid changes on reinstall** (user apps only). If you ever `uninstall`/`install` a *user* app (e.g. the
  patched Lawnchair) instead of `cat`‑replacing in place, restore its data with
  `chown -R <NEW-uid>` + `restorecon -R` (the uid is reassigned) and re‑set the home activity.
- **SystemUI / priv‑app** (`/system` or `/odm` priv‑app, e.g. `SystemUI.apk`) installs the same way but to
  the priv‑app path; keep a stock backup to restore if the UI breaks.
- **aapt2 segfault** on huge SYU resource tables (e.g. `com.syu.air`, 266 layouts): don't recompile —
  swap the *compiled* binary XML/PNG at the zip level, or do smali‑only edits via dex‑swap. See
  [03-systemui.md](03-systemui.md) / [06-app-reskins.md](06-app-reskins.md).

## Which apps go where

| App | `/oem` dir | Key | Notes |
|---|---|---|---|
| EQ | `190000000_com.syu.eq` | platform | recolored in apk |
| FM radio (UI) | `190000005_yx_com.syu.radio` | platform | UI is `com.syu.radio/.act.ActRadio`, **not** carradio |
| Bluetooth | `190000002_yx_com.syu.bt` | platform | icons via skin override ([07](07-skin-system.md)) |
| FYT Settings | `190001001_com.syu.settings` | platform | thin wrapper, low impact |
| Nav bar | `190000000_com.syu.air` | platform | blob‑swap layout (aapt2 segfaults) |
| SystemUI | `/system/priv-app/SystemUI` (via `/fem/priv-app`) | platform | status bar |
