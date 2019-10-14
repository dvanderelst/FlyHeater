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


class ThermoTile:
    def __init__(self, set_point, hub_serial, channels):
        # Assume that relay channel 0 (tile) is instrumented with thermocouple 0, etc
        hub_port_tile = 0
        hub_port_thermo = 1
        self.tile = MyTile(hub_serial, hub_port_tile, channels)
        self.thermo = MyThermo(hub_serial, hub_port_thermo, channels)
        self.pid = simple_pid.PID()
        self.set_point = set_point
        self.display = Display.Display(set_point)

    def run(self, n=False):
        counter = 0
        self.pid.setpoint = self.set_point
        #self.pid.tunings = (0.75, 0.02, 0.75)
        self.pid.tunings = (0.35, 0.1, 0.75)
        self.pid.output_limits = (-1, 1)

        duty_cycle = 0.5
        while True:
            start = time.time()
            current = self.thermo.get_temp()
            output = self.pid(current)
            duty_cycle = duty_cycle + output

            if duty_cycle < 0: duty_cycle = 0
            if duty_cycle > 1: duty_cycle = 1

            self.tile.set_duty_cylce(duty_cycle)
            counter = counter + 1

            time.sleep(0.1)

            if counter % 50 == 0: self.display.animate(current)
            done = time.time()
            duration = 1000 * (done - start)
            txt = "%05.2fC  %05.2fDC %04iMS" % (current, duty_cycle, duration)
            print(txt)
            if n and counter > n: break
        self.tile.set_duty_cylce(0)


t0 = ThermoTile(set_point=30, hub_serial=560175, channels=0)
t1 = ThermoTile(set_point=40, hub_serial=560175, channels=1)

thread0 = threading.Thread(target=t0.run)
thread1 = threading.Thread(target=t1.run)


thread0.start()
thread1.start()