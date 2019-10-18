import time

import simple_pid
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.TemperatureSensor import *

import Display


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

        self.pid.setpoint = set_point
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
        self.thermo_tile_2 = ThermoTile_Single(set_point=set_points[2], hub_serial=560175, channels=2)
        self.thermo_tile_3 = ThermoTile_Single(set_point=set_points[3], hub_serial=560175, channels=3)
        self.display = Display.Display(set_points)

    def run(self):
        sleep_time = 0.05
        iteration = 0
        while True:
            t0 = self.thermo_tile_0.step()
            time.sleep(sleep_time)

            t1 = self.thermo_tile_1.step()
            time.sleep(sleep_time)

            t2 = self.thermo_tile_2.step()
            time.sleep(sleep_time)

            t3 = self.thermo_tile_3.step()
            time.sleep(sleep_time)

            print(t0, t1, t2, t3)
            if iteration % 10 == 0: self.display.animate([t0, t1, t2, t3])
            iteration = iteration + 1



t = ThermoTiles([32, 40, 40, 37])
t.run()
