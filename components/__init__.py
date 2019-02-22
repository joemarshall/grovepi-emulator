
from .genericdigital import *
from .grovebutton import *
from .groveled import *
from .genericanalog import *
from .grovetemperature import *
from .grovelight import *
from .grovesound import *
from .groveloudness import *
from .grovepir import *
from .groveultrasonic import *
from .grovetilt import *
from .grovelcddisplay import *
from .grove6axisaccel import *
from .grovenfctagmodule import *
from .grovedht import *

digitalSensors=[GenericDigital,GroveButton,GrovePIR,GroveUltrasonic,GroveTilt,GroveDHT]
analogSensors=[GenericAnalog,GroveTemperature,GroveLight,GroveSound,GroveLoudness]
digitalOutputs=[GroveLED]
i2cConnections=[GroveLCDDisplay,GroveSixAxisAccelerometer,GroveNFCTagModule]
allSensors=digitalSensors+analogSensors+digitalOutputs+i2cConnections
