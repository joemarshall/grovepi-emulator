pyinstaller --add-data *.png;. --add-data main.ico;. grovepiemu.py --add-data testfiles/*;testfiles --add-data gpe_utils/pikeys;pikeys -p fakegrovepi --add-data Azure-ttk-theme;Azure-ttk-theme --hidden-import sensors --hidden-import graphs --hidden-import filters
cd dist
del grovepiemu-windows.zip
powershell.exe Compress-Archive grovepiemu grovepiemu-windows.zip
cd grovepiemu
grovepiemu.exe
cd ..\..
