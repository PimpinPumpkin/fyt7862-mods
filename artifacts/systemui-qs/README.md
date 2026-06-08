# SystemUI — Quick Settings

`brightness_progress_drawable.xml` — the QS brightness‑slider fill, recolored from the stock solid
`#41A4F7` blue (a baked PNG, `brightness_progress_drawable_p_default.png`) to an inline purple→cyan
gradient (`#7176FA → #6CDDFA`, the volume‑slider accent). Drop into `res/drawable/` of the SystemUI
`-s` decode and rebuild (see `docs/03-systemui.md` → "Quick Settings accent").

The QS *active‑tile circle* is the same `#41A4F7`, but it's framework‑accent‑bound (`colorAccent` via
the framework `Theme.DeviceDefault.QuickSettings`) and was deliberately left as‑is — patching it cleanly
isn't possible without a `framework-res` edit. See the doc for the full trace.
