import subprocess
import sys
import os
import shutil
import typer

def main(release:str=typer.Option("",help="Update version number and push a release to github",metavar="VERSION"),run_test:bool = typer.Option(True,help="Run grovepiemulator before uploading release")):
    release=release.strip("v")
    if len(release)>0:
        # update version
        print(f"Updating version to v{release}")
        with open("version.py","w") as version_file:
            version_file.write(f"__version__='{release}'")
        subprocess.run(["git","add","version.py"])
        subprocess.run(["git","commit","-m","Update version"])

    import version

    cmd=["pyinstaller","-y","--add-data","*.png;.","--add-data","main.ico;.","grovepiemu.py","--add-data","testfiles/*;testfiles","--add-data","gpe_utils/pikeys;pikeys","-p","fakegrovepi","--add-data","Azure-ttk-theme;Azure-ttk-theme","--hidden-import","sensors","--hidden-import","graphs","--hidden-import","filters","--hidden-import","tkinter"]
    cmd= [s.replace(';',os.pathsep) for s in cmd]
    platform=sys.platform
    if platform=="darwin":
        print(f"pyinstaller command for {platform} (macos):")
        cmd.extend(["--onefile","--noconsole",'--distpath','dist/grovepiemu','--target-arch','universal2'])
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

        zip_name=shutil.make_archive(f"grovepiemu-{version.__version__}-{platform}",format="zip",base_dir="grovepiemu")
        os.chdir("grovepiemu")
        if run_test:
            if platform=="windows":
                subprocess.run("grovepiemu.exe")
            else:
                subprocess.run("./grovepiemu")
        os.chdir("..")
        if len(release)>0:
            tag=f"v{release}"
            try:
                subprocess.check_call(["gh","release","view",tag])
            except subprocess.CalledProcessError:
                print(f"Creating release {tag}")
                subprocess.check_call(["gh","release","create",tag])
            print("Uploading asset to github")
            subprocess.check_call(["gh","release","upload",tag,zip_name,"--clobber"])
            print("Successfully made release")
    else:
        print("Failed to build, error:",proc.returncode)



if __name__=="__main__":
    typer.run(main)