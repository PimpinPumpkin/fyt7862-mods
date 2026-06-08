#!/usr/bin/env python3
# Recolor the SYU Quick-Settings ACTIVE-tile icons from the stock #41A4F7 blue
# to the theme accent. The active QS tiles are NOT tinted at runtime — SYU bakes
# the blue into per-tile "_p" / "_lsec" PNGs (icon_p_save, shown with no color
# filter for the active state). So this is a pure resource edit: no smali, no
# framework, no bootloop.
#
# Usage: run from a SystemUI "-s" (resources-only) apktool decode dir, then
#        rebuild + platform-sign + /fem install (see docs/03-systemui.md).
#
#   cd 7862_dec && python3 recolor_qs_active.py
#
import glob, os
from PIL import Image

TARGET = (0x71, 0x76, 0xFA)   # #7176FA — volume-slider purple. Change to taste.

def is_active(n):
    n = n.lower()
    # skip other skins (yf/tzy), status-bar signal bars, brightness (handled via
    # its own drawable), theme-picker previews, dividers, misc switches.
    if any(x in n for x in ['_yf', '_tzy', 'brightness', 'switch_theme',
                            'ic_qs_theme', 'divider', 'seekbar', 'sound_mc',
                            's_switch', 'close', 'docked',
                            'signal_1', 'signal_2', 'signal_3', 'signal_4', 'signal_5',
                            'bt_online']):
        return False
    return ('_lsec' in n or '_lesc' in n or n.endswith('_p.png')
            or n.endswith('_p_white.png') or 'connected' in n)

changed = 0
for fp in glob.glob('res/drawable*/*.png'):
    if not is_active(os.path.basename(fp)):
        continue
    im = Image.open(fp).convert('RGBA'); px = im.load(); w, h = im.size; hit = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            # match the stock active blue (#41A4F7) incl. anti-aliased edges;
            # b>g>=r keeps white glyphs (and the alpha) untouched.
            if a > 0 and b > g and g >= r and abs(r-65) < 55 and abs(g-164) < 55 and abs(b-247) < 62:
                px[x, y] = (TARGET[0], TARGET[1], TARGET[2], a); hit += 1
    if hit:
        im.save(fp); changed += 1

print(f'recolored {changed} QS active-tile PNGs -> #{TARGET[0]:02X}{TARGET[1]:02X}{TARGET[2]:02X}')
