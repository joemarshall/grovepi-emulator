GrovePi Emulation Environment 1.0
---------------------------------
This runs python scripts in an emulation environment that 
pretends to be a Raspberry PI with a Grove sensor board 
attached. I mainly created this for use during the G54UBI
Ubiquitous Computing course at University of Nottingham.

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

See here for details of the GrovePI board.
http://www.dexterindustries.com/grovepi/

See here for details of grove sensors
http://www.seeedstudio.com/wiki/Grove_System

This is public domain code, written by Joe Marshall 2015.
joe.marshall@nottingham.ac.uk

To run the emulator, just extract all these files, go to the folder
and run grovepiemu.py

You need python 2.7 and the wxpython module installed. Should work 
on 32 or 64 bit Windows, and I see no reason it shouldn't work on
Mac or Linux.

