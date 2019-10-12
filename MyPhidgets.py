from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.DigitalOutput import *
import time


class MyRelay:
    def __init__(self, hub_serial, hub_port):
        self.relay01 = DigitalOutput()
        self.relay01.setChannel(0)
        self.relay01.setHubPort(hub_port)
        self.relay01.setDeviceSerialNumber(hub_serial)
        self.relay01.openWaitForAttachment(5000)

    def set_states(self, states):
        self.relay01.setState(states[0])

    def set_duty_cylces(self, duty_cycles):
        self.relay01.setDutyCycle(duty_cycles[0])

    def __del__(self):
        self.relay01.close()


class MyThermo:
    def __init__(self, hub_serial, hub_port):
        self.sensor01 = TemperatureSensor()
        self.sensor01.setHubPort(hub_port)
        self.sensor01.setChannel(0)
        self.sensor01.setDeviceSerialNumber(hub_serial)
        self.sensor01.openWaitForAttachment(5000)

    def get_temps(self):
        temps = [0,0,0,0]
        temp01 = self.sensor01.getTemperature()
        temps[0] = temp01
        return temps

    def __del__(self):
        self.sensor01.close()
