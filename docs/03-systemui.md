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

## Transparent bar · hidden volume · thick wifi · bigger data arrows

All resource‑only (no smali), in the `-s` decode of `status_bar_h.xml` + drawables:

- **Transparent bar** (kill the black strip over apps). The bar bg is **not** AOSP's
  `BarTransitions$BarBackgroundDrawable` color (`system_bar_background_opaque`) — FYT overrides it.
  `PhoneStatusBarView.<init>` runs `setBackground(getDrawable(StatusBarConfig.statusBarBK()))`, and
  `statusBarBK()` returns **`R.drawable.system_bar_background_yf`**, a values alias
  (`res/values/drawables.xml`) → `@color/system_bar_background_opaque_yf` (`#ff010101`). **Repoint the
  alias to `@android:color/transparent`** → the bar view is truly transparent. App windows are full‑height
  `[0,0][768,880]` (they sit *under* the 60px bar), so apps that paint to y=0 show through (verified over
  `com.android.settings`); apps that inset their content below the bar (radio/BT) still read dark there —
  that's the app's own top region, not the bar.
- **Hide the volume indicator**: `com.syu.view.VolLayout @id/vol_layout` → `visibility="gone"` +
  `layout_width="0.0px"` (don't delete it — it's a code‑referenced SYU ViewGroup; just collapse it).
- **Thicker wifi** (match 7870): overwrite `ic_wifi_signal_0..4` with a **stroke‑based** arc vector
  (`android:strokeColor=@android:color/white`, `strokeWidth=2.3`, `strokeLineCap=round`, 3 quadratic
  arcs + a filled dot) rather than the thin fill arcs — `strokeWidth` is the thickness lever.
- **Bigger tx/rx data arrows**: `wifi_in`/`wifi_out` (in `status_bar_wifi_group.xml`) are `wrap_content`
  over `ic_activity_up`/`ic_activity_down`; the stock PNGs live in a huge `drawable-2000x1100` dir so they
  render tiny. Render 22px white arrow PNGs into `drawable-nodpi` and delete the old ones.

> **Edge‑to‑edge over apps:** with the bar transparent, what shows under it is the *app's own* top region.
> Apps whose window background is the app surface look seamless (BT: `windowBackground=@drawable/bt_bk`). Apps
> that paint their own top strip still show a band — FM radio draws a near‑black top in its root view above
> `radio_bk`; setting `ActRadio`'s `windowBackground=#131620` fixes the window layer but the root view sits on
> top, so true seamlessness there needs a code change to the radio's root. Low priority — `radio_bk` is already
> near‑black (`#131620`), so the band is barely visible.

## Smali edits without losing the `-s` resource tree

Keep your accumulated resource edits in the `-s` decode. Do the smali edit in a **full** decode of the
same APK, `apktool b` it (SystemUI's aapt2 does *not* segfault), `unzip` the rebuilt `classes.dex` and
`zip` it **over** classes.dex in the `-s`‑built APK (resource IDs match → compatible) → zipalign →
platform‑sign. First boot is slower (dex2oat). **Gotcha:** never reparent a code‑referenced child of a
SYU custom `ViewGroup` (e.g. `com.syu.view.VolLayout`) — it casts the child's LayoutParams to the parent
type in a lifecycle callback → `ClassCastException` crash‑loop. Add new elements as direct siblings.

## Quick Settings accent (the two blues)

Stock SYU QS uses one hardcoded active blue `#41A4F7` in two places:

- **Brightness slider fill** — a baked PNG (`brightness_progress_drawable_p_default.png`, solid `#41A4F7`)
  referenced by `brightness_progress_drawable.xml`. **Fixed** by swapping the `<clip android:drawable=…png>`
  for an inline `<clip><shape><gradient>` = the volume‑slider purple→cyan (`#7176FA → #6CDDFA`, thin r5). Pure
  resource edit — `artifacts/systemui-qs/brightness_progress_drawable.xml`.
- **Active tile circle** — **fixed by recoloring baked PNGs** (no smali, no framework, no bootloop). The active
  tiles are *not* tinted at runtime: `QSIconViewImpl.setIcon` swaps to `icon_p_save` with the color filter
  **cleared** for the active state, because SYU bakes the `#41A4F7` blue straight into per‑tile "pressed" PNGs —
  the `_p` / `_lsec` variants (`ic_qs_wifi_connected_lsec`, `ic_signal_airplane_lsec_p`, `icon_sys_reboot_p`,
  `qs_screenshot_p`, `bluethooth_lsec_p`, … 27 in all). `QSTileBaseView.mColorActive`/`getCircleColor` are dead
  code (the `getCircleColor` call has no `move-result`) — the red herring; the color lives in the assets, not
  `colorAccent`. Recolor those PNGs `#41A4F7` → theme accent (`#7176FA`) and rebuild. See
  `scripts/recolor_qs_active.py`.

Plus two declutter/finish tweaks:

- **Panel background gradient** — the pull‑down bg is `quick_settings_background.png` (a flat `#1C1C1C`
  rounded‑rect, 1241×536; `qs_panel.xml` → `quick_settings_background` view). Recolored its RGB to a vertical
  gradient `#1C1D26` (top) → `#060608` (bottom) — the same fade as the nav/volume bar — while keeping its alpha
  (rounded shape), so the QS reads like the nav bar instead of a flat slab.
  `artifacts/systemui-qs/quick_settings_background.png`.
- **Tile declutter + even spread** — the QS tile list is a plain string: `quick_settings_tiles_default` in
  `strings.xml` (`quick_settings_tiles = "default"` selects it). Removed `shurtcut:standby` (kept reboot) →
  `wifi,night,cell,airplane,shurtcut:blackscreen,shurtcut:clean,shurtcut:reboot` (7 tiles). Then dropped
  `quick_settings_num_columns` 8→7 and `quick_qs_panel_max_columns` 9→7 (`integers.xml`) so the 7 tiles spread
  evenly across the full width instead of left‑clustering with a right‑side gap — also gives the labels a touch
  more room.
