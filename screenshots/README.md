# Screenshots

Visual record of the de‑skeuomorphizing / 7870‑clone work on the UIS7862.

- **`after/`** — current state, how the unit looks now (the README gallery pulls from here).
- **`before/`** — stock SYU (glossy, skeuomorphic), where captures were preserved.
- **`comparison/`** — stock ⟶ modded, and 7862‑vs‑7870 target comparisons.
- The full raw build‑process archive (~158 device captures) is kept in a separate **private** research repo — it
  contains incidental on‑screen PII (WiFi SSID, a dialed phone number), so it's not published here.

## `after/` — modded, current (flat, dark, 7870‑style)
| File | What |
|---|---|
| `home.png` | Lawnchair home: custom clock widget + purple themed (Lawnicons) icons |
| `quicksettings_quick.png` | Quick settings — quick pull (tile row: WiFi/Night/Data/Flight/Sleep/Reboot) |
| `quicksettings.png` | Quick settings — expanded: header w/ Material glyphs, 6 tiles, purple→cyan brightness |
| `radio.png` | Reskinned FM radio (flat presets, dark) |
| `bt_dialer.png` | Flat square Bluetooth dialer keypad |
| `eq.png` | Dark‑gradient graphic equalizer |
| `settings.png` | Flattened SYU Settings |
| `clock_config.png` | Clock widget config — swatches, hex entry, **visual color picker** |
| `incall_osd.png` | **In‑call OSD** — Bluetooth call overlay (talk timer + hangup); phone number redacted |
| `steering.png` | Flat steering‑wheel control page |

## `before/` — stock SYU (glossy, skeuomorphic)
| File | What |
|---|---|
| `home.png` | **Stock home**: default colorful icons, white stock clock, cluttered status bar, stock nav bar with the glossy volume slider |
| `status_bar.png` | **Stock status bar**: SYU gear icon, visible volume, opaque gray, thin wifi |
| `navbar.png` | **Stock nav bar**: skeuomorphic HOME/BACK plus the glossy blue volume slider |
| `quicksettings.png` | **Stock quick settings**: 8 tiles (incl. Standby / Clean Memory), long labels, scissors glyph |
| `bt_dialer.png` | Stock BT dialer: glossy round keys, blue "earth" wallpaper (unit MAC blurred) |
| `bt_app_stock.png` | **Whole stock Bluetooth app** (`com.syu.bt`): all 6 tabs (dialer, contacts, call log, BT music, pairing, BT settings) in one grid |
| `settings_app_stock.png` | **Whole stock FYT Settings app** (`com.syu.settings`): all six tabs (Network, Device, Car/driving, System, Personal, Factory PIN) |
| `settings_about.png` | Stock **About device** page: UIS7862(S), 8 GB / 128 GB, MCU / Bluetooth / baseband versions, build `QP1A.190711.020` |
| `settings.png` | Stock FYT settings: carbon-fiber skeuomorphic list |
| `steering.png` | Stock steering-wheel control page: galaxy wallpaper, glossy translucent keys |
| `eq.png` | Stock 16-band graphic EQ, blue gradient |
| `radio.png` | Stock FM radio: glossy "earth" wallpaper, gradient presets |
| `boot_logo.png` | Stock boot logo |

## `comparison/`
| File | What |
|---|---|
| `home_before_after.png` | **Stock ⟶ modded home** — the headline transformation |
| `statusbar_before_after.png` | Stock ⟶ modded status bar |
| `navbar_before_after.png` | Stock ⟶ modded nav bar |
| `quicksettings_before_after.png` | Stock ⟶ modded quick settings |
| `bt_before_after.png` | Stock ⟶ modded BT dialer |
| `eq_before_after.png` | Stock ⟶ modded EQ |
| `radio_before_after.png` | Stock ⟶ modded radio |
| `settings_before_after.png` | Stock ⟶ modded settings |
| `steering_before_after.png` | Stock ⟶ modded steering-wheel page |
| `icons_vs_7870.png` | Lawnicons matched to the 7870 (top = 7870, bottom = 7862) |
| `wifi_vs_7870.png` | WiFi icon matched to the 7870 (top = 7862, bottom = 7870) |

> Note: every `before/` shot is now a native 768x1024 framebuffer capture (`adb exec-out screencap`)
> pulled from a second, still-stock, identical UIS7862 unit, so the stock state is pixel-clean rather
> than a low-res phone photo. The only edits are privacy blurs: the WiFi SSID on the quick-settings tile
> and the head unit's own BT MAC on the dialer. The `before_after` composites were regenerated from these.
