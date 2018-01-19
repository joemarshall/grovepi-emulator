from math import *
import time

magVals=[0,0,0]
accVals=[0,0,0]

def init6Axis():
    pass

def getAccel():
    """Get accelerometer values (in multiples of g)        
    """
    time.sleep(0.0054553399086) # simulate sensor delay
    return tuple(accVals)


def getMag():
    """Get magnetometer values. 
    """
    time.sleep(0.00540907430649) # simulate sensor delay
    return tuple(magVals)


def getRotationMatrix(mag=None,accel=None):
    """ Returns a 3x3 matrix of how the device is rotated, based on magnetometer and accelerometer values

    Args:
        mag: Magnetometer values from getMag()
        accel: Accelerometer values from getAccel()
        
        If either argument is None, it will call getMag / getAccel
      
    Returns:
        3x3 tuple rotation matrix, put this into getOrientation(matrix) to get yaw, pitch, roll values
        or None if there isn't enough information (device is in freefall)
    """
    if mag==None:
        mag=getMag()
    if accel==None:
        accel=getAccel()
    Ax = accel[0]
    Ay = accel[1]
    Az = accel[2]
    Ex = mag[0]
    Ey = mag[1]
    Ez = mag[2]
    Hx = Ey*Az - Ez*Ay
    Hy = Ez*Ax - Ex*Az
    Hz = Ex*Ay - Ey*Ax        
    normH = sqrt(Hx*Hx + Hy*Hy + Hz*Hz)
    if normH < 0.1:
        # in freefall or something
        return None
    invH = 1.0 / normH
    Hx *= invH
    Hy *= invH
    Hz *= invH
    invA = 1.0 / sqrt(Ax*Ax + Ay*Ay + Az*Az)
    Ax *= invA;
    Ay *= invA;
    Az *= invA;
    Mx = Ay*Hz - Az*Hy;
    My = Az*Hx - Ax*Hz;
    Mz = Ax*Hy - Ay*Hx;
    return ((Hx,Hy,Hz),(Mx,My,Mz),(Ax,Ay,Az))
    
def getOrientation(matrix=None,errorValue=(0,0,0)):
    """ Get orientation values (Yaw, pitch, roll) from rotation matrix
    
    Args: 
        matrix: Rotation matrix, from getRotationMatrix(mag,accel)
                if Matrix is None, then it will call the relevant getAccel functions itself
                
        errorValue: If the rotation matrix can't be found (if it is in freefall, this value is returned. 
                    By default this is set to be just a zero value, if you want to distinguish error events
                    then set this to some other value (e.g. None)
        
    Returns:
        (yaw, pitch, roll) tuple
    """
    if matrix==None:
        matrix=getRotationMatrix()
    if matrix==None:
        return errorValue
    yaw=atan2(matrix[0][1], matrix[1][1])
    pitch=asin(-matrix[2][1])
    roll=atan2(-matrix[2][0], matrix[2][2])
    return yaw,pitch,roll
