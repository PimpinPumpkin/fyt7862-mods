import subprocess, os
RES = os.path.expanduser("~/fyt-unbrick/7862-mods/apps/stock_bt/res/drawable-nodpi-v4")
TMP = "/tmp/bticons"; os.makedirs(TMP, exist_ok=True)
WHITE = "#d2d6dd"; BLUE = "#71b5ff"

def render(name, svg, w=80, h=80):
    p = f"{TMP}/{name}.svg"; open(p, "w").write(svg)
    subprocess.run(["rsvg-convert","-w",str(w),"-h",str(h),p,"-o",f"{RES}/{name}.png"], check=True)

def glyph(pathd, fill):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="80" height="80"><path fill="{fill}" d="{pathd}"/></svg>'

def dialpad(fill):
    dots = "".join(f'<circle cx="{cx}" cy="{cy}" r="2"/>' for cy in (6,12,18) for cx in (6,12,18))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="80" height="80"><g fill="{fill}">{dots}</g></svg>'

P = {
 "menucontact": "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z",
 "menuhistory": "M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z",
 "menuav": "M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z",
 "menupair": "M17.71 7.71L12 2h-1v7.59L6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 11 14.41V22h1l5.71-5.71-4.3-4.29 4.3-4.29zM13 5.83l1.88 1.88L13 9.59V5.83zm1.88 10.46L13 18.17v-3.76l1.88 1.88z",
 "menuset": "M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z",
 "diallinkcut": "M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z",
 "dialdel": "M22 3H7c-.69 0-1.23.35-1.59.88L0 12l5.41 8.11c.36.53.9.89 1.59.89h15c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-3 12.59L17.59 17 14 13.41 10.41 17 9 15.59 12.59 12 9 8.41 10.41 7 14 10.59 17.59 7 19 8.41 15.41 12 19 15.59z",
}
for name, pd in P.items():
    render(f"bt_{name}", glyph(pd, WHITE)); render(f"bt_{name}_p", glyph(pd, BLUE))
render("bt_menudial", dialpad(WHITE)); render("bt_menudial_p", dialpad(BLUE))

PHONE = "M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"
def circle(cfill, pathd, rot=0):
    s = 0.6; off = (24 - 24*s) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="92" height="92">'
            f'<circle cx="12" cy="12" r="11.5" fill="{cfill}"/>'
            f'<g transform="rotate({rot} 12 12) translate({off},{off}) scale({s})"><path fill="#ffffff" d="{pathd}"/></g></svg>')
render("bt_dialdial", circle("#43a047", PHONE), 92, 92)
render("bt_dialhang", circle("#e53935", PHONE, rot=135), 92, 92)
render("bt_dialdial_p", circle("#2e7d32", PHONE), 92, 92)
render("bt_dialhang_p", circle("#c62828", PHONE, rot=135), 92, 92)
print("rendered", len(os.listdir(TMP)), "svgs")
