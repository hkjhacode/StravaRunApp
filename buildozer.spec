# ===== FILE: buildozer.spec =====
[app]
title = StravaRunApp
package.name = stravarunnapp
package.domain = org.example
source.dir = .
version = 0.1
requirements = python3,kivy,pillow,android
orientation = portrait
fullscreen = 0

[app:permissions]
permissions = ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True