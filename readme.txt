GrovePi Emulation Environment
---------------------------------
This runs python scripts in an emulation environment that 
pretends to be a Raspberry PI with a Grove sensor board 
attached. I mainly created this for use during the Comp4104 
Designing Sensor Based System module at University of Nottingham.

As such I've only implemented components that were in our
box of tricks. If you want new components integrating, it 
is pretty straightforward, just add them to the components
module (and to the __init__.py in that module). For many 
things you can just use a generic digital or analog sensor,
so you don't need to add a new component.

It allows you to replay data from a CSV file (which you could output 
from your code on a real GrovePI board, or make up in Excel.)
For CSV files, make sure you have one column that has timestamps 
Python format (Unix time but floating point), ie. you save the 
value output by time.time()

Also supports reading data from a webserver via JSON at 1hz update
rate. Data should be in the format:
{"sound":56,"temperature":491,"light":728,"button":32767,"motion":0,
"ultrasonic":1059,"touch":32767}
ie. sensorname:value pairs. For digital sensors you can treat them in two
ways - one is to just send the raw data, which risks missing short 
presses. The other is to send them as 'seconds since last press' 
and round them down. When choosing your column mapping in the program
you can select -TIME_SINCE_PRESSED versions of each column for this.


See here for details of the GrovePI board.
http://www.dexterindustries.com/grovepi/

See here for details of grove sensors
http://www.seeedstudio.com/wiki/Grove_System

This is public domain code, written by Joe Marshall 2015-2025.
joe.marshall@nottingham.ac.uk

To run the emulator, download the latest release from the releases tab.

If you want to run it in your own python installation, just clone the
github and run grovepiemu.py. You need python 3.11 or later.



