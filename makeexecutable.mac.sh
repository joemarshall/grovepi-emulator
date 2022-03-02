#!/bin/bash

#pyinstaller --add-data main.ico:. grovepiemu.py --add-data testfiles/*:testfiles --add-data gpe_utils/pikeys:pikeys -p fakegrovepi

pyinstaller --onefile --console --add-data *.png:. --add-data main.ico:. grovepiemu.py --add-data testfiles/*:testfiles --add-data gpe_utils/pikeys:pikeys --add-data Azure-ttk-theme:Azure-ttk-theme -p fakegrovepi


