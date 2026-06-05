#!/usr/bin/env bash
# Install a signed APK into /oem via the read-write /fem alias, then reboot.
# The app must already be signed (SYU/system apps: AOSP platform key — see fetch_keys.sh).
#
#   ./install_fem.sh com.syu.bt.apk 190000002_yx_com.syu.bt
#
set -e
APK="$1"; DIR="$2"
[ -f "$APK" ] && [ -n "$DIR" ] || { echo "usage: $0 <signed.apk> <oem_dir_name>"; exit 1; }

adb push "$APK" /sdcard/_install.apk
# NOTE the blob form: adb shell 'su -c "…"'  — otherwise the body runs as uid 2000, not root.
adb shell 'su -c "
  BB=/data/adb/magisk/busybox
  D=/fem/app/'"$DIR"'
  A=\$D/\$(ls \$D | grep -m1 .apk)
  mount -o remount,rw /fem
  blockdev --setrw /dev/block/mmcblk0p42
  \$BB chattr -i \$A                 # FYT marks files immutable; toybox has no chattr
  cat /sdcard/_install.apk > \$A     # cat preserves the SELinux context
  \$BB chattr +i \$A
  echo installed: \$A
"'
echo "rebooting to apply (resource changes need a full reboot)…"
adb reboot
