import zlib, struct

W, H = 768, 880
top  = (0x13, 0x16, 0x20)   # dark near-neutral, hair of blue
dark = (0x0a, 0x0b, 0x10)   # near-black
GRAD_END = 300              # reach near-black by ~34% (above the presets), then hold

def lerp(a, b, t): return tuple(round(a[i] + (b[i]-a[i])*t) for i in range(3))
def smooth(t): return t*t*(3-2*t)

rows = bytearray()
for y in range(H):
    c = lerp(top, dark, smooth(y/GRAD_END)) if y <= GRAD_END else dark
    rows.append(0)               # PNG filter type 0 (none)
    rows.extend(bytes(c) * W)

def chunk(typ, data):
    return struct.pack('>I', len(data)) + typ + data + struct.pack('>I', zlib.crc32(typ+data) & 0xffffffff)

png  = b'\x89PNG\r\n\x1a\n'
png += chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))  # 8-bit RGB
png += chunk(b'IDAT', zlib.compress(bytes(rows), 9))
png += chunk(b'IEND', b'')
open('/tmp/radio_bk_new.png', 'wb').write(png)
print("wrote /tmp/radio_bk_new.png", len(png), "bytes")
