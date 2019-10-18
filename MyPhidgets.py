import time
import SimpleLogger
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
    def __init__(self, set_points, log_name='log.xls', do_plot=False):
        self.logger = SimpleLogger.Logger()
        self.log_name = log_name
        self.do_plot = do_plot
        self.set_points = set_points

        self.thermo_tile_0 = ThermoTile_Single(set_point=set_points[0], hub_serial=560175, channels=0)
        self.thermo_tile_1 = ThermoTile_Single(set_point=set_points[1], hub_serial=560175, channels=1)
        self.thermo_tile_2 = ThermoTile_Single(set_point=set_points[2], hub_serial=560175, channels=2)
        self.thermo_tile_3 = ThermoTile_Single(set_point=set_points[3], hub_serial=560175, channels=3)
        if self.do_plot: self.display = Display.Display(set_points)

    def plot_and_save(self, t0, t1, t2, t3):
        if self.do_plot: self.display.animate([t0, t1, t2, t3])
        data = self.logger.export()
        data.to_excel('log.xls')

    def print(self, time_running, t0, t1, t2, t3):
        error_0 = t0 - self.set_points[0]
        error_1 = t1 - self.set_points[1]
        error_2 = t2 - self.set_points[2]
        error_3 = t3 - self.set_points[3]

        t = '%+05i' % time_running

        temps = '%02.2f %02.2f %02.2f %02.2f' % (t0, t1, t2, t3)
        errors = '%+06.2f %+06.2f %+06.2f %+06.2f' % (error_0, error_1, error_2, error_3)

        print(t, temps, errors)

    def run(self, duration=None):
        small_sleep_time = 0.01
        big_sleep_time = 0.01
        iteration = 0
        start_time = time.time()
        while True:
            stamp0 = time.asctime()
            t0 = self.thermo_tile_0.step()
            time.sleep(small_sleep_time)

            stamp1 = time.asctime()
            t1 = self.thermo_tile_1.step()
            time.sleep(small_sleep_time)

            stamp2 = time.asctime()
            t2 = self.thermo_tile_2.step()
            time.sleep(small_sleep_time)

            stamp3 = time.asctime()
            t3 = self.thermo_tile_3.step()
            time.sleep(small_sleep_time)

            time_running = time.time() - start_time
            self.logger['time'] = time_running
            self.logger['iteration'] = iteration
            self.logger['stamp0'] = stamp0
            self.logger['stamp1'] = stamp1
            self.logger['stamp2'] = stamp2
            self.logger['stamp3'] = stamp3
            self.logger['t0'] = t0
            self.logger['t1'] = t1
            self.logger['t2'] = t2
            self.logger['t3'] = t3
            self.logger['sp0'] = self.set_points[0]
            self.logger['sp1'] = self.set_points[1]
            self.logger['sp2'] = self.set_points[2]
            self.logger['sp3'] = self.set_points[3]

            self.print(time_running, t0, t1, t2, t3)

            if iteration % 100 == 0: self.plot_and_save(t0, t1, t2, t3)
            if duration and time_running > duration: break
            iteration = iteration + 1
            time.sleep(big_sleep_time)

        self.plot_and_save(t0, t1, t2, t3)
        print('Done')
