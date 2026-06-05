#!/usr/bin/env python3
# Convert an (upright) image to the FYT logo-partition BMP format:
# 768x1024, 32-bit BGRX, bottom-up (positive height), 54-byte header == stock.
# Content is rotated 180 deg (panel is mounted upside-down; stock logo is stored rotated too).
import struct, sys

src, dst = sys.argv[1], sys.argv[2]
d = open(src, 'rb').read()
off = struct.unpack('<I', d[10:14])[0]
W   = struct.unpack('<i', d[18:22])[0]
Hs  = struct.unpack('<i', d[22:26])[0]
H   = abs(Hs); topdown = Hs < 0
Bpp = struct.unpack('<H', d[28:30])[0] // 8
rowsz = ((W * Bpp + 3) // 4) * 4
assert W == 768 and H == 1024, (W, H)

def px(x, y):                       # image coords, y=0 = top; returns (B,G,R)
    fr = y if topdown else (H - 1 - y)
    p = off + fr * rowsz + x * Bpp
    return d[p], d[p+1], d[p+2]

imgsize = W * H * 4
hdr = (b'BM' + struct.pack('<I', 54 + imgsize) + struct.pack('<I', 0) +
       struct.pack('<I', 54) + struct.pack('<I', 40) +
       struct.pack('<i', W) + struct.pack('<i', H) +       # +H => bottom-up (matches stock)
       struct.pack('<H', 1) + struct.pack('<H', 32) +
       struct.pack('<I', 0) + struct.pack('<I', imgsize) +
       struct.pack('<I', 3779) + struct.pack('<I', 3779) +
       struct.pack('<I', 0) + struct.pack('<I', 0))

# 180 rotation + bottom-up storage reduce to: file row k (in file order) = input row k, columns reversed.
out = bytearray(imgsize); i = 0
for k in range(H):
    for x in range(W):
        b, g, r = px(W - 1 - x, k)
        out[i] = b; out[i+1] = g; out[i+2] = r; out[i+3] = 0; i += 4

open(dst, 'wb').write(hdr + out)
print("wrote %s : %d bytes (hdr54 + %d)" % (dst, 54 + imgsize, imgsize))
