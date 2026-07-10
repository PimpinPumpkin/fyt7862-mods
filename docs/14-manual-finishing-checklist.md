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

## Icons (Lawnchair per-app custom icon)

Dark mode + Themed Icons already gives the purple Lawnicons look (see
[12-newer-builds-and-second-units.md](12-newer-builds-and-second-units.md)). To override a single app's
icon: long-press the app -> **Edit** -> tap the icon -> pick from the Lawnicons pack.

Most are obvious - **search the app's name** and pick it (search `settings` -> the gear, etc.). The one
that is not obvious:

- **Car Link** - there is no "car link" icon. **Search `android`** and pick the (Android Auto) logo that
  comes up.

## Optional

- [ ] **Themed Icons** should read "Home screen" (Lawnchair -> Settings -> General -> Themed Icons). It is
      on from the restore, just confirm.
- [ ] **Grid / size** are restored (drawer 4 columns, home icons 150%) - confirm in Lawnchair settings if
      you want (see [../artifacts/launcher/lawnchair-settings.md](../artifacts/launcher/lawnchair-settings.md)).
- [ ] **Obtainium silent installs** need Shizuku (Obtainium has no native root installer). Flash the **Sui**
      Magisk module (or Shizuku app -> "Start via root"), then Obtainium -> Settings -> **Use Shizuku**.
      Droidify/Aurora already have their own root installers, so this is only for Obtainium's GitHub sources.
