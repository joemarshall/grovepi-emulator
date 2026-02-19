"""This module allows you to get data from sensors, and also to replay sensor data from pre-recorded csv files."""

from math import sqrt
import io, csv
import grove6axis, grove9axis, grovepi, grovegyro
from contextlib import contextmanager
import re

### TODO - 1 include grove lcd output (normally)
### TODO - 2 make graph equivalent on LCDs, using custom characters http://www.matidavid.com/pic/LCD%20interfacing/lcd-custom-character.htm


def set_pins(sensor_pin_mapping: dict):
    _PIN_MAP = sensor_pin_mapping
    accel_count = 0
    gyro_count = 0
    magnetometer_count = 0
    for sensorName, pin in sensor_pin_mapping.items():
        sensorName = sensorName.lower()
        sensorName, sensorNum = re.match(r"(\D+)(\d*)", sensorName).groups()
        new_sensor = None
        if (
            sensorName == "light"
            or sensorName == "temperature_analog"
            or sensorName == "sound"
            or sensorName == "rotary_angle"
            or sensorName == "analog"
        ):
            new_sensor = AnalogPinSensor(pin)
        elif sensorName == "gyro":
            # ignore the pin, must be an i2c port
            new_sensor = GyroSensor(gyro_count)
            gyro_count += 1
        elif sensorName == "accel":
            # ignore the pin, i2c sensor
            new_sensor = AccelSensor(accel_count)
            accel_count += 1
        elif sensorName == "magnetometer":
            # ignore the pin, i2c sensor
            new_sensor = MagnetometerSensor(magnetometer_count)
            magnetometer_count += 1
        elif sensorName == "dht":
            new_sensor = DHTSensor(pin)
        elif (
            sensorName == "pir"
            or sensorName == "button"
            or sensorName == "touch"
            or sensorName == "digital"
            or sensorName == "tilt"
        ):
            new_sensor = DigitalPinSensor(pin)
        elif sensorName == "ultrasonic":
            new_sensor = UltrasonicSensor(pin)
        if new_sensor != None:
            globals()[sensorName + sensorNum] = new_sensor


def _list_imu_sensors():
    attached_sensors = {"gyro": [], "accel": [], "magnetometer": []}
    for sensor_class in grovepi.attached_sensors.values():
        if sensor_class == "GroveSixAxisAccelerometer":
            attached_sensors["accel"].append(grove6axis.getAccel)
            attached_sensors["magnetometer"].append(grove6axis.getMag)
        elif sensor_class == "GroveGyro":
            attached_sensors["gyro"].append(grovegyro.getGyro)
            attached_sensors["accel"].append(grovegyro.getAccel)
        elif sensor_class == "Grove9AxisIMU":
            attached_sensors["gyro"].append(grove9axis.getGyro)
            attached_sensors["accel"].append(grove9axis.getAccel)
            attached_sensors["magnetometer"].append(grove9axis.getMag)
    return attached_sensors


def _does_i2c_device_exist(addr):
    if addr == 0x18:
        # check if grove6axis exists
        for sensor_class in grovepi.attached_sensors.values():
            if sensor_class == "GroveSixAxisAccelerometer":
                return True
    elif addr == 0x19:
        for sensor_class in grovepi.attached_sensors.values():
            if sensor_class == "GroveGyro":
                return True
    return False


# mapping from sensor to pin
_SENSOR_PIN_MAP = {}


class AnalogPinSensor:
    def __init__(self, pin):
        self.pin = pin

    def get_level(self):
        return grovepi.analogRead(self.pin)


class DigitalPinSensor:
    def __init__(self, pin):
        self.pin = pin

    def get_level(self):
        return grovepi.digitalRead(self.pin)


class DHTSensor:
    def __init__(self, pin):
        self.pin = pin

    def get_level(self):
        return grovepi.dht(self.pin, 0)


class UltrasonicSensor:
    def __init__(self, pin):
        self.pin = pin

    def get_level(self):
        return grovepi.ultrasonicRead(self.pin)


class AccelSensor:
    """Accelerometer sensor

    This allows you to get the acceleration of a device in metres per second squared, along three axes, X, Y and Z, which for a phone
    are typically X,Y axes side to side and top to bottom on the screen, Z coming out of the screen. Be aware that in addition
    to any motion of the phone, the accelerometer will pick up a constant $9.8 \\frac{m/s}^2$ acceleration due to gravity.
    """

    def __init__(self, index):
        attached_sensors = _list_imu_sensors()["accel"]
        if index < len(attached_sensors):
            self.accelFn = attached_sensors[index]
        else:
            raise IOError(f"Please connect an accelerometer board - trying to find {index+1} accelerometers")

    def get_xyz(self):
        """Get the acceleration of the device

        This is returned in terms of x,y and z axes

        Returns
        -------
        x: float
            x axis acceleration in m/s^2
        y: float
            y axis acceleration in m/s^2
        z: float
            z axis acceleration in m/s^2
        """
        return self.accelFn()

    def get_magnitude(self):
        """Get the magnitude of device acceleration.

        If the device is still, this will be 1G (about 9.8 m/s^2)

        Returns
        -------
        mag: float
            magnitude of device acceleration (i.e. sqrt(x^2+y^2+z^2))
        """
        x, y, z = self.get_xyz()
        return sqrt((x * x) + (y * y) + (z * z))


class MagnetometerSensor:
    """Magnetometer sensor

    This allows you to get the magnetic field affecting a device along three axes, X, Y and Z, which for a phone
    are typically X,Y axes side to side and top to bottom on the screen, Z coming out of the screen.
    """

    def __init__(self, index):
        attached_sensors = _list_imu_sensors()["magnetometer"]
        if index < len(attached_sensors):
            self.magFn = attached_sensors[index]
        else:
            raise IOError("Please connect a magnetometer board - trying to find %d magnetometers" % (index + 1))

    def get_xyz(self):
        """Get the acceleration of the device

        This is returned in terms of x,y and z axes

        Returns
        -------
        x: float
            x axis magnetic field strength
        y: float
            y axis magnetic field strength
        z: float
            z axis magnetic field strength
        """
        return self.magFn()

    def get_magnitude(self):
        """Get the magnitude of magnetic field strength

        Returns
        -------
        mag: float
            magnitude of device acceleration (i.e. sqrt(x^2+y^2+z^2))
        """
        x, y, z = self.get_xyz()
        return sqrt((x * x) + (y * y) + (z * z))


class GyroSensor:
    """Gyroscope sensor

    This allows you to get the rotation of a device in radians per second, around three axes, X, Y and Z, which for a phone
    are typically X,Y axes side to side and top to bottom on the screen, Z coming out of the screen.
    """

    def __init__(self, index):
        attached_sensors = _list_imu_sensors()["gyro"]
        if index < len(attached_sensors):
            self.gyroFn = attached_sensors[index]
        else:
            raise IOError(f"Please connect a gyro board (trying to find {index+1} gyro boards")

    def get_xyz(self):
        """Get the rotation of the device

        This is returned in terms of x,y and z axes

        Returns
        -------
        x: float
            x axis rotation in radians/s
        y: float
            y axis rotation in radians/s
        z: float
            z axis rotation in radians/s
        """
        return self.gyroFn()

    def get_magnitude(self):
        """Get the magnitude of device rotation

        If the device is still, this will be 0

        Returns
        -------
        mag: float
            magnitude of device rotation (i.e. sqrt(x^2+y^2+z^2))
        """
        x, y, z = self.get_xyz()
        return sqrt((x * x) + (y * y) + (z * z))


class replayer:
    """Replay pre-recorded sensor data from CSV files

    This class supports loading of CSV files into your code and replaying them. The actual CSV loading logic is done for you
    when your script is started, you just need to check if there is any replay data and use it if so. For example you might
    do this with a conditional if statement like this:

    \\`\\`\\`python
    if sensors.replayer.has_replay():
        this_time,x,y,z,sound = sensors.replayer.get_level("time","x","y","z","sound")
    else:
        this_time=time.time()-start_time
        x,y,z=sensors.accel.get_xyz()
        sound=sensors.sound.get_level()
    \\`\\`\\`

    """

    _pos = 0
    _start_time = None
    _replay_lines = None
    _replay_columns = None
    _filename = None

    # do nothing context manager, which forces interrupts to stop
    @staticmethod
    @contextmanager
    def run_fast():
        try:
            yield 0
        finally:
            return

    @staticmethod
    def reset():
        """Restart the replay of data"""
        replayer._startTime = None
        replayer._pos = 0

    @staticmethod
    def columns():
        """Return the mapping of columns in the current CSV file

        Returns
        -------
        columns: map
            list of column:index pairs
        """
        return replayer._replay_columns

    # parse text csv string
    @staticmethod
    def _on_lines(lines, filename):
        def make_numbers(x):
            retval = []
            for y in x:
                try:
                    retval.append(float(y))
                except ValueError:
                    retval.append(y)
            return retval

        if not lines or len(lines) == 0:
            replayer._replay_lines = None
            replayer._replay_columns = None
            replayer._filename = None
            return
        replayer._filename = filename
        print("ON LINES:", replayer._filename)
        f = io.StringIO(lines)
        r = csv.reader(f)
        replayer._replay_columns = r.__next__()
        # make lookup for columns
        replayer._replay_columns = {
            str(x): y for y, x in enumerate(replayer._replay_columns)
        }
        # only get rows with the correct amount of data
        replayer._replay_lines = [
            make_numbers(x) for x in r if len(x) == len(replayer._replay_columns)
        ]

        replayer.reset()

    @staticmethod
    def get_replay_name():
        """Return the name of the currently loaded replay file
        This is useful for example if you want to do different
        tests for different types of input data
        """
        print("GET FNAME:", replayer._filename)
        return replayer._filename

    @staticmethod
    def has_replay():
        """Find out if there is replay data

        Returns True if there is a replay CSV file set up, false otherwise.

        Returns
        -------
        has_csv: bool
            True iff there is a replay CSV file.

        """
        return replayer._replay_lines != None

    @staticmethod
    def finished():
        """Has replay finished yet?

        Returns True if there are no more lines left in the CSV file

        Returns
        -------
        finished_csv: bool
            True iff the CSV file is finished

        """
        if not replayer._replay_lines:
            return True
        return replayer._pos < len(replayer._replay_lines) - 1

    @staticmethod
    def get_level(*col_names):
        """Get a sample worth of sensor levels from the CSV file

        This returns selected columns from a line in the CSV file and then moves onto the next line. This means that
        if you want to read multiple columns, you have to do it in one call.

        Parameters
        ----------
        *col_names : tuple
            Pass the list of column names that you want to read, e.g.
            \`sensors.replayer.get_level("time","sound","light")\`

        Returns
        -------
        columns: tuple
            The value of each of the requested columns
        """
        if replayer._replay_lines and len(replayer._replay_lines) > replayer._pos:
            ret_val = replayer._replay_lines[replayer._pos]
            if replayer._pos < len(replayer._replay_lines) - 1:
                replayer._pos += 1
        else:
            ret_val = 0 * len(replayer._replay_columns)
        if col_names:
            # look up the columns and return in order
            return [ret_val[replayer._replay_columns[x]] for x in col_names]
        else:
            return ret_val


_LAST_SAMPLE_TIME = None
_SHOWN_DELAY_WARNING = False


def delay_sample_time(delay):
    """Sleep until *delay* seconds after the last time this was called.
    This allows you to steadily sample at a given rate even if sampling
    from your sensors takes some time.
    """
    global _LAST_SAMPLE_TIME, _SHOWN_DELAY_WARNING
    curtime = time.time()
    if _LAST_SAMPLE_TIME is not None:
        if _LAST_SAMPLE_TIME + delay > curtime:
            _LAST_SAMPLE_TIME += delay
            time.sleep(_LAST_SAMPLE_TIME - curtime)
            return
        else:
            if not _SHOWN_DELAY_WARNING:
                print(f"Warning, can't sample fast enough for delay {delay}")
                _SHOWN_DELAY_WARNING = True
    _LAST_SAMPLE_TIME = time.time()


if __name__ == "__main__":
    import time

    set_pins({"ultrasonic": 4})
    while True:
        print(ultrasonic.get_level())
        time.sleep(0.0)
