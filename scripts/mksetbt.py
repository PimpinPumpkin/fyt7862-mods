import subprocess, os
SET = os.path.expanduser("~/fyt-unbrick/7862-mods/apps/stock_set/res/drawable-nodpi")
BT  = os.path.expanduser("~/fyt-unbrick/7862-mods/apps/stock_bt/res/drawable-nodpi-v4")
TMP="/tmp/setbt"; os.makedirs(TMP, exist_ok=True)
WHITE="#d7dbe2"; BLUE="#71b5ff"; DIM="#5a5e66"; CARD="#243049"

def render(name, svg, w, h, d):
    p=f"{TMP}/{name}.svg"; open(p,"w").write(svg)
    subprocess.run(["rsvg-convert","-w",str(w),"-h",str(h),p,"-o",f"{d}/{name}.png"], check=True)

def cell(glyph, color, g=50, W=128, H=80):
    s=g/24.0; tx=(W-g)/2.0; ty=(H-g)/2.0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<g transform="translate({tx},{ty}) scale({s})"><path fill="{color}" d="{glyph}"/></g></svg>')

def card_note(W=220,H=220):
    g=100; s=g/24.0; tx=(W-g)/2.0; ty=(H-g)/2.0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" rx="26" fill="{CARD}"/>'
            f'<g transform="translate({tx},{ty}) scale({s})"><path fill="{BLUE}" '
            f'd="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></g></svg>')

def blank(W,H):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"></svg>'

SETG = {
 "wifi": "M1 9l2 2c4.97-4.97 13.03-4.97 18 0l2-2C16.93 2.93 7.07 2.93 1 9zm8 8l3 3 3-3c-1.65-1.66-4.34-1.66-6 0zm-4-4l2 2c2.76-2.76 7.24-2.76 10 0l2-2C15.14 9.14 8.87 9.14 5 13z",
 "device": "M21 3H3c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h5v2h8v-2h5c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 14H3V5h18v12z",
 "system": "M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z",
 "factory": "M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z",
 "people": "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z",
 "common": "M3 17v2h6v-2H3zM3 5v2h10V5H3zm10 16v-2h8v-2h-8v-2h-2v6h2zM7 9v2H3v2h4v2h2V9H7zm14 4v-2H11v2h10zm-6-4h2V7h4V5h-4V3h-2v6z",
}
n_set=0
for n,g in SETG.items():
    for pref in ("rotate_set_menu_","set_menu_"):
        if os.path.exists(f"{SET}/{pref}{n}.png"):
            render(f"{pref}{n}", cell(g,WHITE), 128,80, SET); n_set+=1
        if os.path.exists(f"{SET}/{pref}{n}_p.png"):
            render(f"{pref}{n}_p", cell(g,BLUE), 128,80, SET)
        if os.path.exists(f"{SET}/{pref}{n}_u.png"):
            render(f"{pref}{n}_u", cell(g,DIM), 128,80, SET)
# BT: bt_navi_btav (the centered "Bluetooth 5.1" square) -> clean card+note; bt_av (vinyl) -> transparent
render("bt_navi_btav", card_note(), 220,220, BT)
render("bt_navi_btav_p", card_note(), 220,220, BT)
render("bt_av", blank(300,300), 300,300, BT)
print(f"settings glyphs rendered: {n_set}; BT card + transparent vinyl written")
