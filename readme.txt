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

See here for details of the GrovePI board.
http://www.dexterindustries.com/grovepi/

See here for details of grove sensors
http://www.seeedstudio.com/wiki/Grove_System

This is public domain code, written by Joe Marshall 2015.
joe.marshall@nottingham.ac.uk