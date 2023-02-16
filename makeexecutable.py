import subprocess
import sys
import os
import shutil
import version

cmd=["pyinstaller","-y","--add-data","*.png;.","--add-data","main.ico;.","grovepiemu.py","--add-data","testfiles/*;testfiles","--add-data","gpe_utils/pikeys;pikeys","-p","fakegrovepi","--add-data","Azure-ttk-theme;Azure-ttk-theme","--hidden-import","sensors","--hidden-import","graphs","--hidden-import","filters","--hidden-import","tkinter"]

platform=sys.platform
if platform=="darwin":
    print(f"pyinstaller command for {platform} (macos):")
    cmd.extend(["--onefile","--noconsole"])
    platform="mac"
elif platform=="win32":
    print(f"pyinstaller command for {platform} (windows):")
    platform="windows"
else:
    print(f"Generic pyinstaller command for {platform}:")
print(cmd)

proc=subprocess.run(cmd)
if proc.returncode==0:
    os.chdir("dist")
    shutil.make_archive(f"grovepiemu-{version.__version__}-{platform}",format="zip",base_dir="grovepiemu")
    os.chdir("grovepiemu")
    if platform=="windows":
        subprocess.run("grovepiemu.exe")
    else:
        subprocess.run("grovepiemu")
