# 03 — Status bar (SystemUI, 7870 clone)

The top **status bar is `com.android.systemui`** (`/system/priv-app/SystemUI/SystemUI.apk`, A10, ~47MB,
signed with the **AOSP platform key** → rebuild+platform‑sign keeps its system uid). Install to
`/fem/priv-app/SystemUI/SystemUI.apk` + reboot.

## The active layout

Portrait (768×1024) uses **`status_bar_h.xml`**, chosen at runtime in
`StatusBarConfig.statusBarLayout()` (`heightPixels > widthPixels → status_bar_h`). Editing base
`status_bar.xml` does nothing (that's the landscape one). `apktool d -s` (resources‑only) keeps the dex;
decode **with the device `framework-res.apk` installed** (`apktool if framework-res_7862.apk`).

## Edits (to match the 7870)

- **Clock centered**: set both side weights equal (75/75) and add `Clock` as a centered direct child
  after `centered_icon_area`; remove the right‑side clock. **Keep 12h AM/PM** (don't set time_12_24).
- **Wifi on the left**: move `<include layout="@layout/system_icons"/>` into `status_bar_left_side`.
- **Hide home/back**: `visibility="gone"`. The code‑reshown app‑icon (`@id/app_state_icon`) ignores
  `gone` → zero its `layout_width/height` instead.
- **Wifi glyph** (solid fan → outline arcs): the live set is AOSP **`WIFI_FULL_ICONS = ic_wifi_signal_0..4`**
  (used when wifi has validated internet). Overwrite those vectors with the 7870's arc vectors recolored
  `#5a5a5a → @android:color/white`. Size lever = `status_bar_system_icon_size` (dimens.xml).
- **Recents / volume icons**: ported 7870 vectors; recents sized via `icon_recent.xml` width/height
  (scaleType=center → intrinsic == rendered).

## Smali edits without losing the `-s` resource tree

Keep your accumulated resource edits in the `-s` decode. Do the smali edit in a **full** decode of the
same APK, `apktool b` it (SystemUI's aapt2 does *not* segfault), `unzip` the rebuilt `classes.dex` and
`zip` it **over** classes.dex in the `-s`‑built APK (resource IDs match → compatible) → zipalign →
platform‑sign. First boot is slower (dex2oat). **Gotcha:** never reparent a code‑referenced child of a
SYU custom `ViewGroup` (e.g. `com.syu.view.VolLayout`) — it casts the child's LayoutParams to the parent
type in a lifecycle callback → `ClassCastException` crash‑loop. Add new elements as direct siblings.
