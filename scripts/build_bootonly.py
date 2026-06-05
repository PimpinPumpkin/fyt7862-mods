#!/usr/bin/env python3
# Build a minimal, testkey whole-file-signed boot-only lsec OTA for the FYT 7862.
# Signing recipe proven byte-identical to signapk -w (see calibration step).
import zipfile, struct, subprocess, os, hashlib

WORK  = "/Users/user/fyt-unbrick/bootonly"
PARTS = os.path.join(WORK, "parts")
BOOT  = "/tmp/magisk_patched.img"                 # bc05d244... Magisk v30.7 patched boot
KEY   = os.path.join(WORK, "testkey.key.pem")
CERT  = os.path.join(WORK, "testkey.x509.pem")
OUT   = os.path.join(WORK, "6315_1.zip")
MARKER = b"signed by SignApk\x00"                 # 18-byte SignApk comment marker

entries = [
    ("META-INF/com/android/metadata",             os.path.join(PARTS, "metadata"),       zipfile.ZIP_DEFLATED),
    ("META-INF/com/android/otacert",              os.path.join(PARTS, "otacert"),        zipfile.ZIP_DEFLATED),
    ("META-INF/com/google/android/update-binary", os.path.join(PARTS, "update-binary"),  zipfile.ZIP_DEFLATED),
    ("META-INF/com/google/android/updater-script",os.path.join(PARTS, "updater-script"), zipfile.ZIP_DEFLATED),
    ("boot.img",                                  BOOT,                                  zipfile.ZIP_STORED),
]

# 1. base zip (no archive comment)
base = OUT + ".base"
with zipfile.ZipFile(base, "w") as z:
    for arc, path, comp in entries:
        data = open(path, "rb").read()
        zi = zipfile.ZipInfo(arc, date_time=(2009, 1, 1, 0, 0, 0))
        zi.compress_type = comp
        zi.external_attr = 0o644 << 16
        z.writestr(zi, data)

raw = open(base, "rb").read(); n = len(raw)
assert raw[n-22:n-18] == b"PK\x05\x06", "EOCD not at tail: " + raw[n-22:n-18].hex()
eocd_off = n - 22
assert raw[eocd_off+20:eocd_off+22] == b"\x00\x00", "base unexpectedly has a comment"
signed_region = raw[:eocd_off+20]                 # verify_file signs up to (not incl) comment-len field
srp = OUT + ".signed_region"; open(srp, "wb").write(signed_region)

# 2. detached, sha1, no-attrs PKCS#7 over the region  (== signapk -w)
p7 = OUT + ".p7"
subprocess.run(["openssl", "smime", "-sign", "-binary", "-noattr", "-md", "sha1",
                "-in", srp, "-inkey", KEY, "-signer", CERT, "-outform", "DER", "-out", p7], check=True)
pkcs7 = open(p7, "rb").read()

# 3. assemble comment = marker + pkcs7 + 6-byte footer
sig_start    = len(pkcs7) + 6
comment_size = len(MARKER) + len(pkcs7) + 6
footer  = struct.pack("<H", sig_start) + b"\xff\xff" + struct.pack("<H", comment_size)
comment = MARKER + pkcs7 + footer
final   = signed_region + struct.pack("<H", comment_size) + comment
open(OUT, "wb").write(final)
print(f"pkcs7={len(pkcs7)} sig_start={sig_start} comment_size={comment_size} footer={footer.hex()}")
print(f"final size={len(final)} sha1={hashlib.sha1(final).hexdigest()}")

# 4. self-verify: re-parse like verify_file, then openssl cms -verify
fd = open(OUT, "rb").read(); N = len(fd); ft = fd[-6:]
ss = ft[0] | (ft[1] << 8); cs = ft[4] | (ft[5] << 8)
assert ft[2] == 0xff and ft[3] == 0xff
eo = N - cs - 22
assert fd[eo:eo+4] == b"PK\x05\x06" and (fd[eo+20] | (fd[eo+21] << 8)) == cs
open(OUT + ".v_region", "wb").write(fd[:N-cs-2])
open(OUT + ".v_sig", "wb").write(fd[N-ss:N-6])
r = subprocess.run(["openssl", "cms", "-verify", "-inform", "DER", "-in", OUT + ".v_sig",
                    "-content", OUT + ".v_region", "-certfile", CERT, "-noverify", "-binary",
                    "-out", "/dev/null"], capture_output=True, text=True)
print("CMS self-verify:", r.stderr.strip())
assert "Verification successful" in r.stderr, "SELF-VERIFY FAILED"

with zipfile.ZipFile(OUT) as z:
    bi = z.read("boot.img")
    us = z.read("META-INF/com/google/android/updater-script").decode()
    md = z.read("META-INF/com/android/metadata").decode()
print("embedded boot.img sha1:", hashlib.sha1(bi).hexdigest(), "len", len(bi))
print("expected patched sha1 :", hashlib.sha1(open(BOOT, "rb").read()).hexdigest())
print("metadata timestamp    :", [l for l in md.splitlines() if "timestamp" in l])
print("updater-script writes boot:", "/by-name/boot" in us)
print("OK -> wrote", OUT)
