#!/usr/bin/env bash
# Build the FYT Clock widget APK with the SDK command-line tools (no Gradle).
set -e
SDK=~/Library/Android/sdk
AJAR=$SDK/platforms/android-34/android.jar
BT=$SDK/build-tools/35.0.0
cd "$(dirname "$0")"
rm -rf out && mkdir -p out/gen out/classes

$BT/aapt2 compile --dir res -o out/res.zip
$BT/aapt2 link -o out/base.apk -I "$AJAR" --manifest AndroidManifest.xml --java out/gen \
  --min-sdk-version 21 --target-sdk-version 29 out/res.zip
javac -nowarn -source 8 -target 8 -cp "$AJAR" -d out/classes $(find java out/gen -name '*.java')
$BT/d8 --lib "$AJAR" --min-api 21 --output out $(find out/classes -name '*.class')
cp out/base.apk out/app.apk && zip -qj out/app.apk out/classes.dex
$BT/zipalign -p -f 4 out/app.apk out/app-aligned.apk
[ -f ~/.android/debug.keystore ] || keytool -genkeypair -keystore ~/.android/debug.keystore \
  -storepass android -keypass android -alias androiddebugkey -dname "CN=Android Debug,O=Android,C=US" \
  -keyalg RSA -validity 10000
$BT/apksigner sign --ks ~/.android/debug.keystore --ks-pass pass:android --ks-key-alias androiddebugkey \
  --out out/clockwidget.apk out/app-aligned.apk
echo "built: out/clockwidget.apk"
