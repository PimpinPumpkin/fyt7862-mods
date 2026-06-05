# 09 — Clock widget (custom, color‑selectable)

The 7870's home clock is **Google Deskclock's `DigitalStackedAppWidget`** (`com.google.android.deskclock`)
— a stacked digital time/date, but **white only, no color choice**. This is a tiny custom replacement that
looks like it and adds a **color picker**.

Source: `artifacts/clockwidget/` (package `com.fyt7862.clock`, label **FYT Clock**).

- **Widget** = three **vertically stacked** elements — hour (`h`, 66sp) over minute (`mm`, 66sp) over date
  (`EEE, MMM d`, 14sp), all `sans-serif-light`, white default — the 7870's stacked look (not `h:mm` on one
  line). `TextClock` is `@RemoteView`‑safe and self‑updates, so no service/alarm is needed. A
  `PreviewActivity` (launcher entry) inflates the widget into a dark frame for on‑device preview.
- **Config activity** launches when you drop the widget; it shows swatches — **white (default, = the 7870),**
  slider‑blue `#71B5FF`, red, green, amber, purple — and applies the pick with
  `RemoteViews.setTextColor` (saved per‑widget in `SharedPreferences`).

## Build (no Gradle)

```bash
cd artifacts/clockwidget && ./build.sh      # aapt2 → javac → d8 → zipalign → apksigner (debug key)
adb install -r out/clockwidget.apk
```

`build.sh` uses only the SDK command‑line tools (`build-tools 35`, `android-34` platform jar, JDK 17).

## Use

Long‑press the home screen → **Widgets** → **FYT Clock** → drop it → pick a color in the dialog.
To recolor later, remove + re‑add (or extend the provider with a tap‑to‑configure intent).

> Extending it: add more swatches in `ConfigActivity.colors`, or swap the date format / font in
> `res/layout/clock_widget.xml`. Rebuild with `./build.sh`.
