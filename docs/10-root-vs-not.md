# 10 — What needs root, what doesn't

If you want to apply these mods to *another* FYT (Topway/SYU) unit, here's the split.
The deciding factor is simple: **does it drop into the app drawer, or does it replace
something the device shipped with?**

## No root needed — any FYT, plain `adb` / sideload

These are ordinary user apps or settings any user can change:

| Mod | How | Notes |
|---|---|---|
| **Clock widget** (`com.fyt7862.clock`) | `adb install clockwidget.apk` (or sideload) | Self-contained. Add via the launcher's widget picker; colors/opacity/**hex** via the "FYT Clock" drawer app. |
| **Lawnchair launcher** + **Lawnicons (purple)** | install both APKs, set Lawnchair as default launcher, select the icon pack | `artifacts/launcher/`. The recolored pack is a normal icon-pack APK — Lawnchair doesn't verify its signature. |
| **Home wallpaper** | Settings → wallpaper | The *boot splash* (below) needs root; the home wallpaper does not. |
| **Dark mode** | `adb shell cmd uimode night yes` (or `settings put secure ui_night_mode 2`) | Uses WRITE_SECURE_SETTINGS, which the adb shell already holds — no root. Persists across reboots. |
| **Wireless ADB (per boot)** | `adb tcpip 5555` | Works without root but resets on reboot; see below to make it survive a reboot. |

## Root needed — Magisk + write to `/system` / `/oem` (via the `/fem` alias)

Anything that replaces a system/OEM app or a system image. These partitions are
mounted read-only and the files are `chattr +i` (immutable), so you need root to
remount rw, clear the immutable bit, and overwrite:

| Mod | Why root |
|---|---|
| **SystemUI** — status bar, nav bar, **wifi icon**, clock | `SystemUI.apk` is a priv-app on a read-only partition |
| **SYU app reskins** — Settings, EQ, BT dialer, Steering-wheel, Radio | They live in `/oem` (`/fem`) — read-only + immutable |
| **Boot splash** | written to the splash partition |
| **Skin drawable overrides** | the SYU skin lives in `/oem` |
| **Persistent ADB across reboot** | `setprop persist.adb.tcp.port 5555` needs root |

## Rule of thumb

- **Installs into the drawer / launcher / Settings** → no root.
- **Replaces something pre-installed** (a system app, an `/oem` app, the splash) → root,
  because those partitions are read-only and the files are immutable.

So on a **non-rooted** FYT you can still get: the clock widget, the Lawnchair + purple-icon
home, dark mode, and a wallpaper. The status-bar / wifi look and the de-skeuomorphized SYU
apps (Settings/EQ/BT/Steering/Radio) require root.

> Caveat: `/oem` partition names and SYU app IDs can differ slightly between FYT models /
> SoCs. The *method* is identical; double-check the `by-name/oem` device path and the
> `190000xxx_*` app folder names on the target unit before flashing (see
> [08-applying.md](08-applying.md)).
