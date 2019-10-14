from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.DigitalOutput import *
import time
import simple_pid
from matplotlib import pyplot
import Display
import threading


class MyTile:
    def __init__(self, hub_serial, hub_port, relay_channel):
        self.relay = DigitalOutput()
        self.relay.setChannel(relay_channel)
        self.relay.setHubPort(hub_port)
        self.relay.setDeviceSerialNumber(hub_serial)
        self.relay.openWaitForAttachment(5000)

    def set_state(self, state):
        self.relay.setState(state)

    def set_duty_cylce(self, duty_cycle):
        self.relay.setDutyCycle(duty_cycle)

    def __del__(self):
        self.relay.close()


class MyThermo:
    def __init__(self, hub_serial, hub_port, thermo_channel):
        self.sensor = TemperatureSensor()
        self.sensor.setHubPort(hub_port)
        self.sensor.setChannel(thermo_channel)
        self.sensor.setDeviceSerialNumber(hub_serial)
        self.sensor.openWaitForAttachment(5000)

    def get_temp(self):
        temp = self.sensor.getTemperature()
        return temp

    def __del__(self):
        self.sensor.close()


class ThermoTile_Single:
    def __init__(self, set_point, hub_serial, channels):
        # Assume that relay channel 0 (tile) is instrumented with thermocouple 0, etc
        hub_port_tile = 0
        hub_port_thermo = 1
        self.tile = MyTile(hub_serial, hub_port_tile, channels)
        self.thermo = MyThermo(hub_serial, hub_port_thermo, channels)
        self.pid = simple_pid.PID()
        self.set_point = set_point

        self.pid.setpoint = self.set_point
        self.pid.tunings = (0.35, 0.1, 0.75)
        self.pid.output_limits = (-1, 1)
        self.duty_cycle = 0.5

    def step(self):
        current = self.thermo.get_temp()
        output = self.pid(current)
        self.duty_cycle = self.duty_cycle + output
        if self.duty_cycle < 0: self.duty_cycle = 0
        if self.duty_cycle > 1: self.duty_cycle = 1
        self.tile.set_duty_cylce(self.duty_cycle)
        return current


class ThermoTiles:
    def __init__(self, set_points):
        self.thermo_tile_0 = ThermoTile_Single(set_point=set_points[0], hub_serial=560175, channels=0)
        self.thermo_tile_1 = ThermoTile_Single(set_point=set_points[1], hub_serial=560175, channels=1)
        self.display_0 = Display.Display(set_points[0])
        self.display_1 = Display.Display(set_points[1])

    def run(self):
        for x in range(1000):
            t0 = self.thermo_tile_0.step()
            t1 = self.thermo_tile_1.step()

            if x%100==0:
                self.display_0.animate(t0)
                self.display_1.animate(t1)


t = ThermoTiles([32, 40])
t.run()