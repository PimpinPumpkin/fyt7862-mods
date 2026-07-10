# Lawnchair config (what unit #1 runs)

Decoded from Lawnchair 15's Compose datastore
(`/data/data/app.lawnchair/files/datastore/preferences.preferences_pb`). These are the settings the
`lc_backup.tar` restore brings in. The layout db is separate (`launcher_5_4_4.db`), and widget bindings +
the exact icon arrangement do not survive a reinstall (re-add by hand).

## Grid & sizing
| Key | Value | Meaning |
|---|---|---|
| `drawer_columns` | `4` | app drawer is 4 columns |
| `home_icon_size_factor` | `1.5` | home icons 150% |
| `drawer_icon_size_factor` | `1.5` | drawer icons 150% |
| `home_icon_label_size_factor` | `1.2` | home labels 120% |
| `drawer_cell_height_factor` | `1.3` | drawer row height |

## Look & layout
| Key | Value |
|---|---|
| `icon_shape` | `cupertino` (iOS rounded square) |
| `hotseat_mode` | `disabled` (no dock) |
| `dock_search_bar` | `false` |
| `show_status_bar` | `false` (Lawnchair hides the status bar on its home) |
| `show_icon_labels_on_home_screen` | `true` |
| `launcher_popup_order` | `+carousel\|-lock\|-edit_mode\|+wallpaper\|+widgets\|+home_settings\|+sys_settings` |

## Features
| Key | Value |
|---|---|
| `enable_feed` | `false` |
| `enable_smartspace` | `false` |
| `enable_smartspace_now_playing` | `false` |
| `enable_fuzzy_search` | `true` |
| `hidden_apps_in_search` | `on` |
| `legacy_popup_options_migrated` | `true` |

## Hidden from the drawer (`hidden_apps`)
Clutter + helper apps unit #1 hides: calculator, `com.syu.filemanager`, `com.syu.gallery`,
Google search box, `com.fvsm.camera`, iGO (`com.nng.igo...`), `app.lawnchair.lawnicons` (the pack's own
launcher entry), `com.syu.music`, `com.syu.onekeynavi`, CarNet (`com.tima.carnet.vt`),
`com.txznet.smartadapter`, `com.txznet.aipal`, `com.fyt.screenbutton`, `com.syt.tmps`, `com.syu.tv`,
`com.syu.canbus`, `com.syu.video`, `com.syu.av`, `com.syu.market`, `com.fyt7862.clock` (widget host),
Yandex Navi, `com.mariodantas.fytmanagementcenter` (FMC), YouTube, Chrome, Play Store,
`com.hiqrecorder.full`, FUTO voice input, FUTO keyboard.

> Note: some of these apps are unit #1-specific and may not be installed on another unit; a hidden entry
> for a missing app is harmless.

## Not in the datastore
The home **workspace** grid (columns x rows) is the device default (single full-width page after the
two-panel smali fix, see [../docs/05-launcher.md](../docs/05-launcher.md)). Themed Icons / dark theme live
in `shared_prefs/com.android.launcher3.prefs.xml` (`themed_icons=true`, `pref_launcherTheme=dark`,
`pref_iconPackPackage=app.lawnchair.lawnicons`) - and remember the purple only shows in dark mode
([../docs/12-newer-builds-and-second-units.md](../docs/12-newer-builds-and-second-units.md)).
