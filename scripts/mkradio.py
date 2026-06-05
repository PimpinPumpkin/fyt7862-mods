import subprocess, os
RES = os.path.expanduser("~/fyt-unbrick/7862-mods/apps/stock_radio_full/res/drawable-nodpi-v4")
TMP = "/tmp/rdicons"; os.makedirs(TMP, exist_ok=True)
WHITE="#d7dbe2"; BLUE="#71b5ff"

def render(name, svg, w, h):
    p=f"{TMP}/{name}.svg"; open(p,"w").write(svg)
    subprocess.run(["rsvg-convert","-w",str(w),"-h",str(h),p,"-o",f"{RES}/{name}.png"], check=True)

def labeled(glyph, label, color, gsize=40):
    s=gsize/24.0; tx=(154-gsize)/2; ty=14
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 154 100" width="154" height="100">'
            f'<g transform="translate({tx},{ty}) scale({s})"><path fill="{color}" d="{glyph}"/></g>'
            f'<text x="77" y="86" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="15" font-weight="600" letter-spacing="0.5" fill="{color}">{label}</text></svg>')

def card(fill, rx=18, W=196, H=96):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" rx="{rx}" fill="{fill}"/></svg>')

G = {
 "band": ("M6.99 11L3 15l3.99 4v-3H14v-2H6.99v-3zM21 9l-3.99-4v3H10v2h7.01v3L21 9z", "BAND"),
 "scan": ("M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z", "SCAN"),
 "st": ("M12 1c-4.97 0-9 4.03-9 9v7c0 1.66 1.34 3 3 3h3v-8H5v-2c0-3.87 3.13-7 7-7s7 3.13 7 7v2h-4v8h3c1.66 0 3-1.34 3-3v-7c0-4.97-4.03-9-9-9z", "ST"),
 "ta": ("M20 10h-3V8.86c1.72-.45 3-2 3-3.86h-3V3c0-.55-.45-1-1-1H8c-.55 0-1 .45-1 1v2H4c0 1.86 1.28 3.41 3 3.86V10H4c0 1.86 1.28 3.41 3 3.86V15H4c0 1.86 1.28 3.41 3 3.86V21c0 .55.45 1 1 1h8c.55 0 1-.45 1-1v-2.14c1.72-.45 3-2 3-3.86h-3v-1.14c1.72-.45 3-2 3-3.86zM12 19c-.83 0-1.5-.67-1.5-1.5S11.17 16 12 16s1.5.67 1.5 1.5S12.83 19 12 19zm0-5c-.83 0-1.5-.67-1.5-1.5S11.17 11 12 11s1.5.67 1.5 1.5S12.83 14 12 14zm0-5c-.83 0-1.5-.67-1.5-1.5S11.17 6 12 6s1.5.67 1.5 1.5S12.83 9 12 9z", "TA"),
 "af": ("M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z", "AF"),
 "pty": ("M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z", "PTY"),
 "loc": ("M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z", "LOC"),
 "local": ("M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z", "LOCAL"),
 "edit": ("M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z", "NOTES"),
 "save": ("M17 3H7c-1.1 0-1.99.9-1.99 2L5 21l7-3 7 3V5c0-1.1-.9-2-2-2z", "SAVE"),
 "set": ("M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z", "SET"),
}
for n,(g,label) in G.items():
    if os.path.exists(f"{RES}/radio_menu_{n}.png"):
        render(f"radio_menu_{n}", labeled(g,label,WHITE), 154,100)
    if os.path.exists(f"{RES}/radio_menu_{n}_p.png"):
        render(f"radio_menu_{n}_p", labeled(g,label,BLUE), 154,100)
    if os.path.exists(f"{RES}/radio_menu_{n}_u.png"):
        render(f"radio_menu_{n}_u", labeled(g,label,"#5a5e66"), 154,100)
# presets: flat neutral cards (FytRadio style), slider-blue when selected
render("radio_ch", card("#1b1c22"), 196, 96)
render("radio_ch_p", card("#4a72b8"), 196, 96)
print("rendered", len(os.listdir(TMP)), "svgs")
