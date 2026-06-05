#!/usr/bin/env bash
# Fetch the PUBLIC AOSP signing keys this unit trusts. They are NOT committed to this repo
# (they only *look* like secrets — they're the well-known public test/platform keys).
#   - platform.*  signs SYU/system apps (keeps their system uid)            SHA-256 c8a2e9bc…
#   - testkey.*   whole-file-signs the boot-only root OTA (the unit trusts it) serial 936EACBE07F201DF
set -e
B="https://android.googlesource.com/platform/build/+/refs/heads/master/target/product/security"
mkdir -p keys && cd keys
for k in platform.pk8 platform.x509.pem testkey.pk8 testkey.x509.pem; do
  echo "fetching $k"
  curl -fsSL "$B/$k?format=TEXT" | base64 --decode > "$k"
done
# testkey PKCS#8 DER → PEM, for openssl smime signing of the boot OTA:
openssl pkcs8 -inform DER -nocrypt -in testkey.pk8 -out testkey.key.pem
echo "done → keys/ (platform.pk8/.x509.pem, testkey.pk8/.x509.pem/.key.pem)"
echo "if the branch 404s, swap 'master' for 'main' in this script."
