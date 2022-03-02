pyinstaller --add-data *.png;. --add-data main.ico;. grovepiemu.py --add-data testfiles/*;testfiles --add-data gpe_utils/pikeys;pikeys -p fakegrovepi --add-data Azure-ttk-theme;Azure-ttk-theme
cd dist\grovepiemu
grovepiemu.exe
cd ..\..
