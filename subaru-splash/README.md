# Subaru boot screens

The two Subaru boot images for this unit, kept together so they don't get lost. The unit shows
**two** screens at boot, in this order, and each is a different file in a different place.

| File | Which screen | Where it goes | How to write it |
|---|---|---|---|
| `1_uboot_logo_subaru.bmp` | **First** screen (the earliest one, replaces the "Android hifi" u-boot logo). Text-only white SUBARU wordmark + outlined emblem. | `logo` partition = `/dev/block/by-name/logo` = `mmcblk0p12` | root: `dd if=1_uboot_logo_subaru.bmp of=/dev/block/by-name/logo` |
| `2_bootanimation_subaru.zip` | **Second** screen (the one you actually watch while it boots). Graphical blue Subaru emblem. | `/oem/media/bootanimation.zip` (via the `/fem` alias) | either put it on the FAT32 flash-stick as `bootanimation.zip` (the updater copies it in during a flash), or root-copy it to `/fem/media/bootanimation.zip` |
| `source_subaru_emblem.png` | source art for the emblem (reference only, not flashed) | — | — |
| `stock_uboot_logo_backup.img` | the **stock** first-screen logo, to revert | `logo` partition | root: `dd if=stock_uboot_logo_backup.img of=/dev/block/by-name/logo` |

## Format notes for `1_uboot_logo_subaru.bmp`

The u-boot logo partition wants a raw **768x1024, 32-bit, bottom-up BMP at offset 0**, and the image is
stored **rotated 180 degrees** because the panel is mounted upside-down (`ro.sf.swrotation=180`). So the
file looks upside-down when you open it but displays upright on the unit. It is built from an upright
source with `scripts/make_logo_bmp.py` (rotate + repack to match the stock header). If you re-make it,
render it back and confirm it looks upside-down in the file.

`2_bootanimation_subaru.zip` is a **STORED** (uncompressed) zip: `desc.txt` (`768 1024 30` + `p 0 0 part0`)
plus a single `part0/0000.png` frame, displayed upright (no rotation).
