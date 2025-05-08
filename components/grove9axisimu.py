import grove9axis

from gpe_utils.tkimports import *
from . import propgrid


class Grove9AxisIMU:

    def __init__(self, inputNum):
        self.pin = inputNum
        self.axisNames = [
            "acc_x",
            "acc_y",
            "acc_z",
            "mag_x",
            "mag_y",
            "mag_z",
            "gyro_x",
            "gyro_y",
            "gyro_z",
        ]
        self.formatString = "{sensor:4s}: {x: 7.2f} {y: 7.2f} {z: 7.2f}"

    def title(self):
        return "I2C-%d: Grove Nine/Ten Axis IMU" % self.pin

    @classmethod
    def classDescription(cls):
        return "Grove Nine/Ten Axis IMU"

    def initSmall(self, parent):
        self.titleLabel = ttk.Label(parent, text=self.title())

        self.labelA = ttk.Label(
            parent,
            text=self.formatString.format(sensor="Acc", x=0, y=0, z=0),
            font="courier",
        )
        self.labelM = ttk.Label(
            parent,
            text=self.formatString.format(sensor="Mag", x=0, y=0, z=0),
            font="courier",
        )
        self.labelG = ttk.Label(
            parent,
            text=self.formatString.format(sensor="Gyro", x=0, y=0, z=0),
            font="courier",
        )
        self.titleLabel.grid()
        self.labelA.grid()
        self.labelM.grid()
        self.labelG.grid()
        self.setValue(0, 0.0)
        self.setValue(1, 10.0)
        self.setValue(2, -5.0)

    def initPropertyPage(self, parent):
        self.propGrid = propgrid.PropertyGrid(parent, title=self.title())
        self.axProp = propgrid.FloatProperty("acc_x", value=0)
        self.ayProp = propgrid.FloatProperty("acc_y", value=0)
        self.azProp = propgrid.FloatProperty("acc_z", value=0)
        self.mxProp = propgrid.FloatProperty("mag_x", value=0)
        self.myProp = propgrid.FloatProperty("mag_y", value=0)
        self.mzProp = propgrid.FloatProperty("mag_z", value=0)
        self.gxProp = propgrid.FloatProperty("gyro_x", value=0)
        self.gyProp = propgrid.FloatProperty("gyro_y", value=0)
        self.gzProp = propgrid.FloatProperty("gyro_z", value=0)
        self.propGrid.Append(self.axProp)
        self.propGrid.Append(self.ayProp)
        self.propGrid.Append(self.azProp)
        self.propGrid.Append(self.mxProp)
        self.propGrid.Append(self.myProp)
        self.propGrid.Append(self.mzProp)
        self.propGrid.Append(self.gxProp)
        self.propGrid.Append(self.gyProp)
        self.propGrid.Append(self.gzProp)
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack(fill=tk.X)

    def OnPropGridChange(self, property, value):
        axisIndex = self.axisNames.index(property)
        self.setValue(axisIndex, float(value))

    def update(self):
        pass

    def getNumAxes(self):
        return 9

    def getAxisName(self, num):
        return self.axisNames[num]

    def setValue(self, axisIndex, value):
        properties = [
            self.axProp,
            self.ayProp,
            self.azProp,
            self.mxProp,
            self.myProp,
            self.mzProp,
            self.gxProp,
            self.gyProp,
            self.gzProp,
        ]
        if axisIndex < 3:
            grove9axis.accVals[axisIndex] = value
            x, y, z = grove9axis.accVals
            self.labelA.config(
                text=self.formatString.format(sensor="Acc", x=x, y=y, z=z)
            )
        elif axisIndex < 6:
            grove9axis.magVals[axisIndex - 3] = value
            x, y, z = grove9axis.magVals
            self.labelM.config(
                text=self.formatString.format(sensor="Mag", x=x, y=y, z=z)
            )
        else:
            grove9axis.gyroVals[axisIndex - 6] = value
            x, y, z = grove9axis.gyroVals
            self.labelG.config(
                text=self.formatString.format(sensor="Gyro", x=x, y=y, z=z)
            )
        properties[axisIndex].SetValue(value)

    def getCSVCode(self):
        return {
            "imports": ["sensors"],
            "pin_mappings": [
                '"accel%d":%d' % (self.pin, self.pin),
                '"magnetometer%d":%d' % (self.pin, self.pin),
                '"gyro%d":%d' % (self.pin, self.pin),
            ],
            "reader": [
                "sensors.accel%d.get_xyz()" % self.pin,
                "sensors.magnetometer%d.get_xyz()" % self.pin,
                "sensors.gyro%d.get_xyz()" % self.pin,
            ],
            "variable": [
                "magnetometer%d_x,magnetometer%d_y,magnetometer%d_z"
                % (self.pin, self.pin, self.pin),
                "accel%d_x,accel%d_y,accel%d_z" % (self.pin, self.pin, self.pin),
                "gyro%d_x,gyro%d_y,gyro%d_z" % (self.pin, self.pin, self.pin),
            ],
            "type": "%f,%f,%f",
        }
