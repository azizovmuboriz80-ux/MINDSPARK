[app]
android.accept_sdk_license = True

title = MINDSPARK
package.name = mindspark
package.domain = org.mindspark

source.dir = .
source.include_exts = py,json,png,jpg,jpeg

version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 35
android.build_tools_version = 35.0.0
android.minapi = 24
android.ndk_api = 24

android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2
warn_on_root = 1