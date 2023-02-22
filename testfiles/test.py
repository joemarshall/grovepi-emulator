import sensors,time

sensor_pins={ "ultrasonic":6 } 
# ultrasound on digital pin 6
sensors.set_pins(sensor_pins)
print("WOO")
while True:
    d=sensors.ultrasonic.get_level()
    print(d) 
    # Distance in cm
    time.sleep(0.1)