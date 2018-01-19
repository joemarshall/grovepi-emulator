pyinstaller --add-data main.ico;. grovepiemu.py --add-data testfiles/*;testfiles -p fakegrovepi 
cd dist\grovepiemu
grovepiemu.exe
cd ..\..
