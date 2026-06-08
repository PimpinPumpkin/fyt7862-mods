# 09 — Clock widget (custom, color‑selectable)

The 7870's home clock is **Google Deskclock's `DigitalStackedAppWidget`** (`com.google.android.deskclock`)
— a stacked digital time/date, but **white only, no color choice**. This is a tiny custom replacement that
looks like it and adds a **color picker**.

Source: `artifacts/clockwidget/` (package `com.fyt7862.clock`, label **FYT Clock**).

- **Widget** = three stacked elements (date `EEE, MMM d` 15sp over hour `hh` over minute `mm`, both **80sp
  `sans-serif-medium`**) on a tinted, shaped background `ImageView` (id `bg`). Defaults: lavender text
  `#C8BFFF` on a purple‑gray pill `#312E41` at ~80% opacity (`setColorFilter` + `setImageAlpha`) — a 7870
  match. `TextClock` is `@RemoteView`‑safe and self‑updates (no service/alarm). **Gotcha:** use
  `format12Hour="hh"` (not `h`) for the 7870's leading zero; resizing an instance needs re‑adding it.
- **Background shape** (`shape` pref → `ClockWidget.SHAPES[]`, applied with `RemoteViews.setImageViewResource`
  *before* the color filter): **Pill** (r54, default), **Rounded** (r26), **Ellipse** (oval), **Rectangle**
  (r6). Each is a plain white shape drawable tinted by the bg color, so one set covers every color.
- **Config / `PreviewActivity`** (launcher entry, live preview in a dark frame): text + background **swatches**,
  an **opacity** slider, the **shape** selector, free‑form **hex entry** (`#RRGGBB`/`#AARRGGBB`), and a
  **visual HSV color picker** (`ColorPickerView`) with a Text/Background target toggle. Saved per‑widget in
  `SharedPreferences`; `ClockWidget.updateAll` re‑renders live (force‑stop `app.lawnchair` if a placed
  instance doesn't refresh).

## Build (no Gradle)

```bash
cd artifacts/clockwidget && ./build.sh      # aapt2 → javac → d8 → zipalign → apksigner (debug key)
adb install -r out/clockwidget.apk
```

`build.sh` uses only the SDK command‑line tools (`build-tools 35`, `android-34` platform jar, JDK 17).

## Use

Long‑press the home screen → **Widgets** → **FYT Clock** → drop it → pick a color in the dialog.
To recolor later, remove + re‑add (or extend the provider with a tap‑to‑configure intent).

> Extending it: add swatches in `PreviewActivity.textColors`/`bgColors`, a new shape in `ClockWidget.SHAPES`
> (+ a matching `res/drawable/clock_shape_*.xml`), or swap the date format / font in
> `res/layout/clock_widget.xml`. Rebuild with `./build.sh`.
