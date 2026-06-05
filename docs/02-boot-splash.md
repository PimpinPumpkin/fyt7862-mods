# 02 — Boot splash & wallpaper

Three boot screens; you usually only care about the first two.

## 1. uboot logo (earliest)

- Partition **`mmcblk0p12`** = `/dev/block/by-name/logo` (8 MB).
- Format: a raw **768×1024 32‑bpp BMP at offset 0**, stored **180°‑rotated** (panel is mounted
  upside‑down, matching `swrotation=180`). Author your image upright → rotate 180° → write.
  Render it back to confirm it *looks* upside‑down in the file.
- macOS `sips` writes top‑down 24‑bit BMPs, so build the final 32‑bit bottom‑up BMP in Python and match
  the stock header (`scripts/make_logo_bmp.py`). Backup: `artifacts/splash/logo_backup.img`.
- Write (root): `dd if=subaru_logo.bmp of=/dev/block/by-name/logo`.

## 2. bootanimation (the one you actually watch)

- File: **`/oem/media/bootanimation.zip`** — a **STORED** (uncompressed) zip,
  `desc.txt` = `768 1024 30` + `p 0 0 part0` and `part0/0000.png` (single frame here).
- Swap it via `/fem` (no re‑sign needed). Backup: `artifacts/splash/bootanimation_current.zip`.

## 3. fbootlogo

- Partition `mmcblk0p13`, 1024×600 "Powered by android". **Never displayed on this unit — leave it.**

## Wallpaper (as root)

```
cat img.png > /data/system/users/0/wallpaper        # (+ wallpaper_orig if same dims)
killall system_server   # or reboot to reload
```
