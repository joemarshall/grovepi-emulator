#!/bin/bash

#pyinstaller --add-data main.ico:. grovepiemu.py --add-data testfiles/*:testfiles --add-data gpe_utils/pikeys:pikeys -p fakegrovepi

pyinstaller --onefile --windowed --add-data *.png:. --add-data main.ico:. grovepiemu.py --add-data testfiles/*:testfiles --add-data gpe_utils/pikeys:pikeys -p fakegrovepi


