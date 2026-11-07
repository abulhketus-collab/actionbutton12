import os, sys, shutil, subprocess, tarfile, io, time

def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    print("=== Building ActionButton12 for iOS 12.0 - 12.5.8 ===")

    # 1. Preprocess Logos
    print("[1/5] Preprocessing Tweak.xm...")
    res = subprocess.run([sys.executable, "preprocess_logos.py"], capture_output=True, text=True)
    if res.returncode != 0:
        print("Preprocess failed:", res.stderr)
        sys.exit(1)

    # 2. Compile and Link Tweak
    print("[2/5] Compiling and linking ActionButton12.dylib...")
    res = subprocess.run([sys.executable, "build_tweak.py"], capture_output=True, text=True)
    if res.returncode != 0:
        print("Tweak build failed:", res.stderr)
        sys.exit(1)

    # 3. Compile and Link Preferences
    print("[3/5] Compiling and linking PreferenceBundle...")
    res = subprocess.run([sys.executable, "build_prefs.py"], capture_output=True, text=True)
    if res.returncode != 0:
        print("Prefs build failed:", res.stderr)
        sys.exit(1)

    # 4. Prepare Staging Directory
    print("[4/5] Preparing package layout...")
    stage_dir = os.path.join(base_dir, ".theos", "_stage")
    if os.path.exists(stage_dir):
        shutil.rmtree(stage_dir)

    dylib_dir = os.path.join(stage_dir, "Library", "MobileSubstrate", "DynamicLibraries")
    bundle_dir = os.path.join(stage_dir, "Library", "PreferenceBundles", "ActionButton12.bundle")
    support_dir = os.path.join(stage_dir, "Library", "Application Support", "ActionButton12")
    debian_dir = os.path.join(stage_dir, "DEBIAN")

    os.makedirs(dylib_dir, exist_ok=True)
    os.makedirs(bundle_dir, exist_ok=True)
    os.makedirs(support_dir, exist_ok=True)
    os.makedirs(debian_dir, exist_ok=True)

    # Copy tweak dylib and plist
    shutil.copy2("ActionButton12.dylib", os.path.join(dylib_dir, "ActionButton12.dylib"))
    shutil.copy2("ActionButton12.plist", os.path.join(dylib_dir, "ActionButton12.plist"))

    # Copy Preference bundle files
    shutil.copy2(os.path.join("actionbutton12prefs", "ActionButton12"), os.path.join(bundle_dir, "ActionButton12"))
    shutil.copy2(os.path.join("actionbutton12prefs", "Resources", "Info.plist"), os.path.join(bundle_dir, "Info.plist"))
    shutil.copy2(os.path.join("actionbutton12prefs", "Resources", "Root.plist"), os.path.join(bundle_dir, "Root.plist"))
    for f in os.listdir(os.path.join("actionbutton12prefs", "Resources")):
        if f.endswith(".png"):
            shutil.copy2(os.path.join("actionbutton12prefs", "Resources", f), os.path.join(bundle_dir, f))

    # Copy Application Support resources (icons)
    if os.path.exists("Resources"):
        for f in os.listdir("Resources"):
            if f.endswith(".png"):
                shutil.copy2(os.path.join("Resources", f), os.path.join(support_dir, f))

    # Copy control file
    shutil.copy2("control", os.path.join(debian_dir, "control"))

    # 5. Build .deb package
    print("[5/5] Packaging .deb...")
    packages_dir = os.path.join(base_dir, "packages")
    os.makedirs(packages_dir, exist_ok=True)

    deb_filename = "com.cocxace.actionbutton12_1.0.0_iphoneos-arm.deb"
    deb_pkg_path = os.path.join(packages_dir, deb_filename)
    deb_root_path = os.path.join(base_dir, deb_filename)

    # Create control.tar.gz
    ctrl_buf = io.BytesIO()
    with tarfile.open(fileobj=ctrl_buf, mode="w:gz") as tar:
        ctrl_path = os.path.join(debian_dir, "control")
        ti = tar.gettarinfo(ctrl_path, arcname="./control")
        ti.uid = 0
        ti.gid = 0
        ti.uname = "root"
        ti.gname = "wheel"
        ti.mode = 0o644
        with open(ctrl_path, "rb") as f:
            tar.addfile(ti, f)
    ctrl_data = ctrl_buf.getvalue()

    # Create data.tar.gz
    data_buf = io.BytesIO()
    with tarfile.open(fileobj=data_buf, mode="w:gz") as tar:
        # Walk stage_dir
        for root, dirs, files in os.walk(stage_dir):
            rel = os.path.relpath(root, stage_dir).replace("\\", "/")
            if rel == "DEBIAN" or rel.startswith("DEBIAN/"):
                continue
            
            if rel != ".":
                ti = tarfile.TarInfo("./" + rel)
                ti.type = tarfile.DIRTYPE
                ti.mode = 0o755
                ti.uid = 0
                ti.gid = 0
                ti.uname = "root"
                ti.gname = "wheel"
                ti.mtime = int(time.time())
                tar.addfile(ti)

            for file in files:
                full_path = os.path.join(root, file)
                file_rel = ("./" + rel + "/" + file).replace("/./", "/")
                ti = tar.gettarinfo(full_path, arcname=file_rel)
                ti.uid = 0
                ti.gid = 0
                ti.uname = "root"
                ti.gname = "wheel"
                if file.endswith(".dylib") or file == "ActionButton12":
                    ti.mode = 0o755
                else:
                    ti.mode = 0o644
                with open(full_path, "rb") as f:
                    tar.addfile(ti, f)
    data_tar = data_buf.getvalue()

    # Create ar archive (.deb)
    # ar archive header: !<arch>\n
    def make_ar_header(name, size):
        # 16 char name, 12 date, 6 uid, 6 gid, 8 mode, 10 size, 2 trailer
        date_str = str(int(time.time())).ljust(12)
        uid_str = "0".ljust(6)
        gid_str = "0".ljust(6)
        mode_str = "100644".ljust(8)
        size_str = str(size).ljust(10)
        hdr = (name.ljust(16) + date_str + uid_str + gid_str + mode_str + size_str + "`\n").encode("ascii")
        return hdr

    ar_buf = io.BytesIO()
    ar_buf.write(b"!<arch>\n")

    # debian-binary
    deb_binary_content = b"2.0\n"
    ar_buf.write(make_ar_header("debian-binary", len(deb_binary_content)))
    ar_buf.write(deb_binary_content)
    if len(deb_binary_content) % 2 == 1:
        ar_buf.write(b"\n")

    # control.tar.gz
    ar_buf.write(make_ar_header("control.tar.gz", len(ctrl_data)))
    ar_buf.write(ctrl_data)
    if len(ctrl_data) % 2 == 1:
        ar_buf.write(b"\n")

    # data.tar.gz
    ar_buf.write(make_ar_header("data.tar.gz", len(data_tar)))
    ar_buf.write(data_tar)
    if len(data_tar) % 2 == 1:
        ar_buf.write(b"\n")

    deb_bytes = ar_buf.getvalue()

    # Write to packages/ and root
    with open(deb_pkg_path, "wb") as f:
        f.write(deb_bytes)
    with open(deb_root_path, "wb") as f:
        f.write(deb_bytes)

    print(f"DEB created in packages/: {deb_pkg_path} ({len(deb_bytes)} bytes)")
    print(f"DEB copied to root: {deb_root_path}")
    print("Build and packaging complete!")

if __name__ == '__main__':
    build()
