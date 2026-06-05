# 04 — Nav bar (com.syu.air)

The bottom **HOME / volume‑slider / BACK bar is `com.syu.air`, NOT SystemUI** — confirm with
`dumpsys window windows` (the `NavigationBar` window's `mPackageName=com.syu.air`, uid 1000). Any SystemUI
nav edits are inert. App: `/oem/app/190000000_com.syu.air/…apk`, platform‑signed.

## The win: the flat layout already ships

`AirService.getHeaderLayoutParam()` builds the bar; the layout is picked in
`com/syu/air/canbus/Car_Null.smali` `headerLayoutId()`. For this unit (uiid=1, manufacturer=135,
platform=6315, `!IsNewPlatform`) it falls to the else branch → **`car_air_null.xml`** (solid beveled home,
tiny orange volume bar). The app **already contains the 7870 bar**: **`car_air_null_7870.xml`** (outline
`d_header_home_7870`/`d_header_back_7870`, flat, blue slider `d_car_vol_bar_7870`).

## Apply it (binary‑XML blob swap — `apktool b` segfaults here)

`com.syu.air` has 266 layouts; `apktool b` dies in aapt2 (exit 139). So don't recompile — swap the
**compiled** binary XML at the zip level (binary XML references resources by absolute id, so it renders
correctly under any filename):

```bash
unzip apk res/layout/car_air_null_7870.xml          # the flat 7870 bar
cp car_air_null_7870.xml res/layout/car_air_null.xml # over the beveled one
zip apk res/layout/car_air_null.xml                  # back into a copy of the apk
zipalign -p 4 … ; apksigner sign --key platform.…    # then /fem install + reboot
```

Result: outline HOME/BACK, flat blue volume slider. The slider's blue→cyan gradient
(`d_car_vol_bar_7870` ≈ `#7176FA → #6CDDFA`) is the source of the project's accent color.

> The orange volume **popup** (tap the status‑bar volume) is a third app, `com.syu.ms` — recolor its
> seekbar drawable separately if you want it to match. (Not done here.)
