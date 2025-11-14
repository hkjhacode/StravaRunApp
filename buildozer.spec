[app]
title = StravaRunApp
package.name = stravarunnapp
package.domain = org.example
source.dir = app
version = 0.1
requirements = python3,kivy,android,plyer

[buildozer]
log_level = 2
warn_on_root = 1
android.permissions = ACCESS_FINE_LOCATION,INTERNET,WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25.1.8937393
android.accept_sdk_license = True