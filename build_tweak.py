import subprocess, sys

clang = r"C:\Program Files\Windhawk\Compiler\bin\clang-20.exe"
lld = r"C:\Program Files\Windhawk\Compiler\bin\ld.lld.exe"
sdk = r"C:\theos\sdks\iPhoneOS12.4.sdk"
theos = r"C:\theos"

sources = ["Tweak.m", "AB12HUDView.m", "AB12Manager.m"]
objects = []

for src in sources:
    obj = src.replace('.m', '.o')
    cmd = [
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
    print("Compiling", src)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Compile error for", src)
        print(res.stderr)
        sys.exit(1)
    objects.append(obj)

link_cmd = [
    lld,
    "-flavor", "darwin",
    "-arch", "arm64",
    "-platform_version", "ios", "12.0.0", "12.4.0",
    "-syslibroot", sdk,
    "-F" + sdk + r"\System\Library\Frameworks",
    "-F" + sdk + r"\System\Library\PrivateFrameworks",
    "-F" + theos + r"\vendor\lib",
    "-framework", "UIKit",
    "-framework", "CoreGraphics",
    "-framework", "AudioToolbox",
    "-framework", "AVFoundation",
    "-framework", "Foundation",
    "-framework", "CydiaSubstrate",
    "-dylib",
    "-install_name", "/Library/MobileSubstrate/DynamicLibraries/ActionButton12.dylib",
    "-o", "ActionButton12.dylib",
    "-lSystem"
] + objects

print("Linking ActionButton12.dylib")
res = subprocess.run(link_cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Link error:")
    print(res.stderr)
    sys.exit(1)

print("SUCCESS: ActionButton12.dylib successfully built!")
