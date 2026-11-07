import subprocess, sys, os

clang = r"C:\Program Files\Windhawk\Compiler\bin\clang-20.exe"
lld = r"C:\Program Files\Windhawk\Compiler\bin\ld.lld.exe"
sdk = r"C:\theos\sdks\iPhoneOS12.4.sdk"
theos = r"C:\theos"

src = r"actionbutton12prefs\AB12RootListController.m"
obj = r"actionbutton12prefs\AB12RootListController.o"
out_dylib = r"actionbutton12prefs\ActionButton12"

compile_cmd = [
    clang,
    "-target", "arm64-apple-ios12.0",
    "-isysroot", sdk,
    "-F" + sdk + r"\System\Library\Frameworks",
    "-F" + sdk + r"\System\Library\PrivateFrameworks",
    "-I" + theos + r"\vendor\include",
    "-I.",
    "-fobjc-arc",
    "-O2",
    "-c", src,
    "-o", obj
]

print("Compiling Preferences controller...")
res = subprocess.run(compile_cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Compile error:", res.stderr)
    sys.exit(1)

link_cmd = [
    lld,
    "-flavor", "darwin",
    "-arch", "arm64",
    "-platform_version", "ios", "12.0.0", "12.4.0",
    "-syslibroot", sdk,
    "-F" + sdk + r"\System\Library\Frameworks",
    "-F" + sdk + r"\System\Library\PrivateFrameworks",
    "-framework", "UIKit",
    "-framework", "Foundation",
    "-framework", "Preferences",
    "-dylib",
    "-install_name", "/Library/PreferenceBundles/ActionButton12.bundle/ActionButton12",
    "-o", out_dylib,
    "-lSystem",
    obj
]

print("Linking Preferences bundle binary...")
res = subprocess.run(link_cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Link error:", res.stderr)
    sys.exit(1)

print("SUCCESS: Preferences bundle binary built!")
