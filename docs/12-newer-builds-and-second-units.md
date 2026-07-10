# 12 - Rooting a newer build / a second unit

Notes from rooting a **second, identical UIS7862** that shipped on a newer firmware than the one this
kit was originally built against. The short version: you almost never need to flash Mario Dantas'
firmware. Root the build that is already on the unit.

## Do you need Mario Dantas' firmware? Usually no.

The first unit got MD's firmware flashed only because (a) it was a higher build date than the faked
"Android 16" string it shipped with, and (b) the boot-only root method had not been worked out yet, and
(c) it was the only package that could be found. None of that is a reason to flash a whole firmware just
to root.

This head unit is not going to get real OEM updates. So going forward:

- **Root the build that is on the unit.** The boot-only testkey OTA (see [01-rooting.md](01-rooting.md))
  flashes only `boot`, off a FAT32 stick, no PC and no download mode. It does not care what build you are
  on.
- Flash MD's full firmware only if you actually want to **change the whole system** (his debloat, his
  config), not to root. And if you do, compare it to what is on the unit first (see the kernel check
  below) so you are not downgrading.
- The fake Android-version string is set in `config.txt` (`ro.build.version.release`), so if you ever care
  about it, edit that, not the firmware.

## Rooting a build the kit's boot was NOT built for (cross-build safety)

The kit's `artifacts/root/*.zip` embeds a Magisk-patched boot for build `08310`. A second unit was on a
newer build (`24210`). Flashing an old boot onto a newer system can bootloop **if the kernel differs**, so
check the kernel before flashing:

```bash
# the kernel the packaged boot carries:
strings artifacts/root/boot.img | grep -m1 'Linux version'
# the kernel the unit is actually running (no root needed):
adb shell cat /proc/version
```

If the `Linux version 4.14.133 ... SMP PREEMPT` string matches (the build counter `#2` vs `#11` and the
date can differ, that is just a rebuild), the packaged boot is safe to flash. If the kernel version
differs, rebuild the OTA against the unit's own boot instead.

Same idea for the **app reskins**: before dropping a reskinned SYU app on a different build, compare
versions. On the second unit, `com.syu.eq` / `com.syu.radio` / `com.syu.bt` had **identical** versionCodes
across the two builds, so those reskins applied with zero risk. Settings / steering / air / ms differed,
so those were backed up first (`adb pull` the stock `/oem/app/<dir>/*.apk`) before replacing. All the SYU
apps and SystemUI are signed with the **public AOSP platform key** (`c8a2e9bc...`), the same on every unit,
so a platform-signed reskin always passes the shared-system-UID signature check. The point: even if a
future build changes an app's look, the patching instructions in [06-app-reskins.md](06-app-reskins.md) /
[07-skin-system.md](07-skin-system.md) / [08-applying.md](08-applying.md) still tell you how to redo the
look, because they work off the app that is on the unit.

## Magisk on newer builds (30.7)

- The unit auto-installs a Magisk **stub** manager on first boot after flashing a patched boot. **The stub
  denies `su`.** Install the **full** Magisk app over it, then Superuser -> **Automatic response = Grant**
  and **Superuser access = Apps and ADB**. Only then does headless `adb shell su` work.
- After you install the full Magisk, it may pop a prompt to **reboot / finish setup ("additional setup
  required")**. If the unit already booted a patched boot and `su` works, you can **decline that** - it is
  already rooted; the prompt is Magisk offering to patch/install itself, which is not needed here.
- On the newer build, **`toybox` has `chattr`**, and Magisk 30.7 no longer ships busybox at the old
  `/data/adb/magisk/busybox` path. So the `/fem` immutable-file dance uses `toybox chattr -i` / `+i`
  instead of the magisk busybox (`install_fem.sh` note).

## USB, ports, and the Device-mode toggle (this unit)

- **Wired adb** goes on the **rear 4-pin USB connector** (USB-A to USB-A). The **flash stick** for the
  update goes on **either port of the 6-pin dual-USB head** (port 2 was used, it does not matter which).
  The flash-stick port is not picky; the adb port is.
- Every reboot resets the USB role to **host**, so adb drops until you set it back to **Device**. On this
  unit that toggle is: **Developer options -> the hamburger menu, top-right -> a little menu appears (it is
  in Chinese) -> two radio buttons, one already selected, pick the other one.** That flips host -> device
  and adb reconnects.
- Best fix: right after root, turn on **persistent wireless adb** so you stop doing that dance:
  `adb shell su -c "setprop persist.adb.tcp.port 5555"`, then `adb connect <unit-ip>:5555`. It survives
  reboots.

## Mario's FYT Management Center

His firmware bakes in `com.mariodantas.fytmanagementcenter` (FMC), which auto-launches on boot and is how
his account-gated root is supposed to work (it is broken, which is why we root with the testkey OTA
instead). Once you are rooted it is just noise. Disable it:

```
adb shell su -c "pm disable-user --user 0 com.mariodantas.fytmanagementcenter"
```

## Dark mode (and why it makes the purple Lawnicons appear)

FYT **locks** Android's night mode off (`dumpsys uimode` -> `mNightModeLocked=true`), so "follow system"
apps stay light and the themed icons do not go purple. Root overrides the lock:

```
adb shell su -c "cmd uimode night yes"     # mCurUiMode -> 0x21, dark
```

FYT re-locks it at every boot, so **persist it** with a Magisk service script
`/data/adb/service.d/darkmode.sh` (root, `chmod 0755`):

```sh
#!/system/bin/sh
while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 2; done
sleep 6
cmd uimode night yes
```

**This is also what makes the purple Lawnicons show up.** The purple is NOT Material You (this is A10, it
has none). The `lawnicons-purple` pack's `color/primaryForeground` is **night-qualified** - black in light
mode, `#ffc8bfff` (light purple) in `-night`. So the themed icons only render purple **once the unit is in
dark mode**. Toggling Lawnchair's Themed Icons while night is off does nothing. Order of operations:

1. force dark mode (above),
2. Lawnchair -> Settings -> General -> **Themed Icons -> Home screen**,
3. clear the icon cache so it re-renders: `su -c "rm /data/data/app.lawnchair/databases/app_icons.db*"`
   then restart Lawnchair.

**To get purple on the AUTO-matched apps, turn Themed Icons OFF (not on).** This is the counter-intuitive
part. With **Themed Icons ON**, Lawnchair draws apps that have a Lawnicons match as the monochrome layer
tinted with the **blue system accent** (measured glyph `~(140,151,198)`, green channel > red = blue). With
**Themed Icons OFF** (Settings -> General -> Themed Icons -> Off) and Icon Pack = Lawnicons, those same apps
fall back to the pack's own **purple** adaptive icon (`~(145,138,186)`, red > green = purple), which is
identical to what the custom-icon picker gives. So: **Icon Pack = Lawnicons, Themed Icons = OFF, "use
tinted accent color" = OFF.** Apps not in Lawnicons then show their normal icon unless you custom-set one.

**Gotcha - a Lawnchair restart does NOT re-render cached icons.** Lawnchair caches rendered icons in
`app_icons.db`, so after you change any icon setting (themed on/off, tinted-accent, pack) the already-cached
icons keep their old look and only newly-rendered ones update - which is why the custom-icon picker shows
the right (purple) icon but the auto-applied ones stayed stuck (blue) even after toggling Themed Icons off.
Always finish with: `su -c "rm /data/data/app.lawnchair/databases/app_icons.db*"` then force-stop + reopen
Lawnchair.
