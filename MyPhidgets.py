from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.DigitalOutput import *
import time
import simple_pid
from matplotlib import pyplot
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


class ThermoTile:
    def __init__(self, set_point, hub_serial, channels):
        # Assume that relay channel 0 (tile) is instrumented with thermocouple 0, etc
        hub_port_tile = 0
        hub_port_thermo = 1
        self.tile = MyTile(hub_serial, hub_port_tile, channels)
        self.thermo = MyThermo(hub_serial, hub_port_thermo, channels)
        self.pid = simple_pid.PID()
        self.history = []
        self.ticks = []
        self.set_point = set_point
        self.display = Display.Display(set_point)

    def run(self, n=False):
        counter = 0
        self.pid.sample_time = 0.1
        self.pid.setpoint = self.set_point
        self.pid.tunings = (0.5, 0.001, 0.01)
        self.pid.output_limits = (-1, 1)

        duty_cycle = 0.5
        while True:
            start = time.time()
            current = self.thermo.get_temp()
            #if current > self.set_point: current = 10000

            output = self.pid(current)
            duty_cycle = duty_cycle + output

            if duty_cycle < 0: duty_cycle = 0
            if duty_cycle > 1: duty_cycle = 1

            self.tile.set_duty_cylce(duty_cycle)
            counter = counter + 1
            self.history.append(current)
            self.ticks.append(counter)

            self.display.animate(current)

            if n and counter > n: break
            done = time.time()
            duration = 1000 * (done - start)
            txt = "%05.2fC  %05.2fC %04iMS" % (current, duty_cycle, duration)
            print(txt)

        self.tile.set_duty_cylce(0)


tt = ThermoTile(set_point=40, hub_serial=560175, channels=0)
tt.run(3000)
