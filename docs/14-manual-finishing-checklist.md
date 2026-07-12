# 14 - Manual finishing checklist (the on-screen stuff)

Everything that can be scripted is in the other docs. These are the last steps that have to be done by
hand on the unit's touchscreen (widget bindings, per-app icons, and a couple of settings that live behind
account/name fields). Run through this after a fresh clone.

## Must-do

- [ ] **Change the Bluetooth name.** Stock ships as `LEHX-L6Pro`. Bluetooth app -> gear/BT Set tab ->
      **Device Name** -> set your own. (Do this per unit so two units in the same car/phone list are not
      both "LEHX-L6Pro".) The BT name is stored separately (`settings get secure bluetooth_name`) and is
      NOT changed by the device name below.
- [ ] **Change the Android device name** (shown for USB / cast / Nearby, defaults to `ums512_1h10_Natv`).
      This is separate from the Bluetooth name. Set it with root adb:
      `adb shell settings put global device_name Outback`
      (or Settings -> About device -> Device name). "Outback" is the one used on this car.
- [ ] **Add the clock widget.** Long-press the home -> Widgets -> **FYT Clock** -> drop it, pick a color.
      (Widget bindings do not survive the Lawnchair reinstall, so this is always by hand.)
- [ ] **Arrange the home icons** how you want them. The restored layout only brings over apps that are
      actually installed on this unit, so expect gaps.
- [ ] **Set the quiet BT incoming-call chime.** The stock tone is loud over music. This is NOT part of the
      BT reskin APK - it is a separate file at `/sdcard/.btring/ring.mp3`. It takes TWO things (traced in
      `com.syu.bt`): the file at that fixed path, AND a non-empty `name_ring` pref in the app's
      `bt_data.xml` (empty `name_ring` = stock ring; the BT ring picker sets both when you pick a tone, and
      a BT-reset clears `name_ring` back to `""`). To apply without the picker:
      ```
      adb shell 'mkdir -p /sdcard/.btring'
      adb push artifacts/bt_incoming_chime.mp3 /sdcard/.btring/ring.mp3
      # then, BT app stopped so it doesn't overwrite, add name_ring to bt_data.xml (owner stays 1000:1000):
      adb shell 'su -c "am force-stop com.syu.bt;
        sed -i \"s#</map>#    <string name=\\\"name_ring\\\">ring.mp3</string>\n</map>#\" \
          /data/data/com.syu.bt/shared_prefs/bt_data.xml;
        restorecon /data/data/com.syu.bt/shared_prefs/bt_data.xml"'
      ```
      Or just use the **Bluetooth app -> ring picker** on the unit (does both). The actual ring playback is
      a layer below the app (MCU/system reads `ring.mp3`), so confirm on a real incoming call. Persists
      across reboots.

## Icons (Lawnchair per-app custom icon)

Dark mode + Themed Icons already gives the purple Lawnicons look (see
[12-newer-builds-and-second-units.md](12-newer-builds-and-second-units.md)). To override a single app's
icon: long-press the app -> **Edit** -> tap the icon -> pick from the Lawnicons pack.

Most are obvious - **search the app's name** and pick it (search `settings` -> the gear, etc.). The one
that is not obvious:

- **Car Link** - there is no "car link" icon. **Search `android`** and pick the (Android Auto) logo that
  comes up.

## Ignore updates for the modded launcher apps

The patched **Lawnchair** and the recolored **Lawnicons** are both re-signed with the **Android Debug key**
(`CN=Android Debug`, SHA-256 `24467432e91370be2bcba5a3e07650fa0bec1b6158708403f9adc4db9e5fc452`), which
is a different signature from the official releases. So an official update **cannot** install over them - it
fails with `INSTALL_FAILED_UPDATE_INCOMPATIBLE`. You are protected from a silent overwrite.

Still, in whatever store tracks them (**Droid-ify** if you added the Lawnchair/Lawnicons repos; Obtainium if
you added them there) set **"Ignore all updates"** on both. Not because an update would succeed, but to stop
the repeated failed-update nagging AND - the real risk - to avoid an updater's "the update failed, uninstall
and reinstall?" prompt, which would wipe the modded Lawnchair and all its layout/config. Aurora / Play do
not track these (not Play apps, and the sig would not match anyway).

## Apps that work well on this unit

- **Calculator: Unitto** (F-Droid). Installed and works with no UI glitches on this 768x1024 A10 panel
  (the stock `com.android.calculator2` is hidden). Use this instead of hunting for a calculator.

## Optional

- [ ] **Themed Icons** should read "Home screen" (Lawnchair -> Settings -> General -> Themed Icons). It is
      on from the restore, just confirm.
- [ ] **Grid / size** are restored (drawer 4 columns, home icons 150%) - confirm in Lawnchair settings if
      you want (see [../artifacts/launcher/lawnchair-settings.md](../artifacts/launcher/lawnchair-settings.md)).
- [ ] **Obtainium silent installs** need Shizuku (Obtainium has no native root installer). Flash the **Sui**
      Magisk module (or Shizuku app -> "Start via root"), then Obtainium -> Settings -> **Use Shizuku**.
      Droidify/Aurora already have their own root installers, so this is only for Obtainium's GitHub sources.
