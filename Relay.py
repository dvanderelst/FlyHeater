from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.DigitalOutput import *
import time

# digitalOutput0 = DigitalOutput()
# digitalOutput0.setChannel(0)
# digitalOutput0.setHubPort(0)
# digitalOutput0.setDeviceSerialNumber(560175)
# digitalOutput0.openWaitForAttachment(5000)
#
# print('Start?')
# digitalOutput0.setDutyCycle(0.1)
#
# time.sleep(5)
#
# digitalOutput0.close()

temperatureSensor0 = TemperatureSensor()
temperatureSensor0.setHubPort(1)
temperatureSensor0.setChannel(0)
temperatureSensor0.setDeviceSerialNumber(560175)
temperatureSensor0.openWaitForAttachment(5000)

temp = temperatureSensor0.getTemperature()

for x in range(100):
    print(temp)
    time.sleep(0.1)

temperatureSensor0.close()