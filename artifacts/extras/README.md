# Extras

- **DocumentsUI.apk** — the AOSP file picker (`com.android.documentsui`, A10/v29). FYT ships without it,
  which breaks the system file/document picker (`ACTION_GET_CONTENT` / `ACTION_OPEN_DOCUMENT`) that apps
  like FUTO, Magisk, and browsers use to pick files. Install it to make the picker work:
  `adb install -r -g DocumentsUI.apk`.
