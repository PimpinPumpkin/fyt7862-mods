# 01 — Rooting (locked bootloader, no PC)

The UIS7862 ships with a **locked bootloader** (`ro.boot.flash.locked=1`,
`ro.boot.verifiedbootstate=green`). You can't `fastboot flash`. But you don't need to.

## Why this works

FYT's updater `lsec6315update` is a repackaged **AOSP recovery `updater`**: it whole‑file‑verifies an
OTA's signature against the keys the device trusts, and **these units trust the public AOSP testkey.**
So a testkey‑signed OTA that flashes *only* a Magisk‑patched `boot.img` is accepted — it never touches
the bootloader, TZ, or verified partitions, so AVB stays happy. A bad signature or a too‑old timestamp
is **refused with nothing written** (fails safe).

> **Why not just flash Mario Dantas' MD‑EDITION kernel?** The usual FYT root path is to flash his
> Magisk‑EDITION (MD‑EDITION) kernel and then enable root by **registering in the FYT app**. *At the time
> of writing, that registration / root‑enable step is broken* — the kernel flashes fine but root is never
> granted afterward. So this kit takes the self‑contained route instead: a testkey‑signed **boot‑only OTA
> that flashes a Magisk‑patched boot directly** — no kernel swap, no FYT‑app registration.

## Prerequisites

- ADB to the unit (see [00-overview.md](00-overview.md) for the USB‑A↔A + Device‑role + reboot dance).
- The **Magisk app** installed on the unit (the Manager; e.g. v27+).
- A **FAT32** USB stick, cleanly formatted + safe‑ejected (bad sticks throw red‑error sig fails).
- The boot‑only OTA package: `artifacts/root/6315_1.zip` (+ the build scripts in `artifacts/root/`).

> The bundled `6315_1.zip` embeds a Magisk‑patched boot for **this exact build**
> (`QP1A.190711.020`). If your unit reports a different `ro.build.fingerprint`, **rebuild** the
> package against *your* boot (steps below) — flashing a foreign boot can bootloop.

## A. Patch the boot image (only if rebuilding)

1. Pull your current boot:
   `adb shell su -c "dd if=/dev/block/by-name/boot of=/sdcard/boot.img"` then `adb pull /sdcard/boot.img`.
   (Partition: `/dev/block/platform/soc/soc:ap-apb/71400000.sdio/by-name/boot`.)
2. Copy `boot.img` to the unit, open **Magisk app → Install → Patch a File**, pick it → get
   `magisk_patched.img` (no root needed for patching).
3. `adb pull` the patched image back.

## B. Build the boot‑only OTA

`artifacts/root/build_bootonly.py` produces a signed `6315_1.zip` with:
- `META-INF/com/google/android/update-binary` (the OEM lsec binary, unchanged)
- a minimal `updater-script` doing only
  `package_extract_file("boot.img", "/dev/block/.../by-name/boot")`
- `META-INF/com/android/metadata` with `post-timestamp` bumped **above** the device's
  `ro.build.date.utc` (use `1800000000`) to clear the anti‑downgrade floor
- whole‑file signature with the **AOSP testkey**, via
  `openssl smime -sign -binary -noattr -md sha1 -inkey testkey.key.pem -signer testkey.x509.pem -outform DER`
  (byte‑identical to `signapk -w`; the unit signs with **SHA‑1**).

```
cd artifacts/root && python3 build_bootonly.py    # embeds magisk_patched.img → 6315_1.zip
```

## C. Flash

1. Copy to the **FAT32 stick root**: `6315_1.zip`, `lsec6315update`, the `lsec_updatesh/` helpers,
   and `config.txt` (see [config](../artifacts/config/)). Safe‑eject.
2. Insert the stick into a **HOST‑mode USB port** and **reboot the unit**.
   The updater scans for `6315_1.zip` *at boot* — it does **not** fire on hot‑insert into a running system.
3. Wait for the green "success", give it +5s, remove the stick, reboot.

## D. Verify + lock in

```
adb shell su -c id          # → uid=0 ... u:r:magisk:s0
```
- Magisk app shows **Installed**.
- **Persist wireless ADB**: `adb shell su -c "setprop persist.adb.tcp.port 5555"` (survives reboot).
- Magisk → Settings → Superuser → **Automatic response = Grant** (so headless `su` doesn't drop to uid 2000).

## Recovery

If the patched boot bootloops: rebuild `6315_1.zip` with the **stock** `boot.img` and reflash, or flash a
full variant‑matched (`768×1024 / normal7862 / 6315`) firmware. Because only `boot` was touched, this is
low‑risk. (A slot‑switch AVB brick from mixing an old rooted boot with a newer build is recoverable
natively via `spd_dump set_active` on macOS — see the FYT 7870 recovery notes.)

## References

- Testkey: googlesource `platform/build` → `target/product/security/testkey.{pk8,x509.pem}`
  (serial `936EACBE07F201DF` = the device otacert).
- Magisk‑EDITION kernels: Mario Dantas (`fytfactory.mariodantas.com/kernels/`), XDA 4610985.
