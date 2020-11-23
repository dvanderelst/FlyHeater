import time
import SimpleLogger
import simple_pid
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.PhidgetException import *
import Display
import traceback
import math

hub_serial = 560175


class MyTile:
    def __init__(self, hub_serial, hub_port, relay_channel):
        self.relay = DigitalOutput()
        self.relay.setChannel(relay_channel)
        self.relay.setHubPort(hub_port)
        self.relay.setDeviceSerialNumber(hub_serial)
        self.relay.openWaitForAttachment(5000)
        self.relay_channel = relay_channel
        self.previous_duty_cycle = 100

    def set_state(self, state):
        self.relay.setState(state)

    def set_duty_cyclce(self, duty_cycle):
        try:
            diff = math.fabs(self.previous_duty_cycle - duty_cycle)
            if diff > 0.05:
                self.relay.setDutyCycle(duty_cycle)
                self.previous_duty_cycle = duty_cycle
        except PhidgetException as exception:
            print('Error on tile channel', self.relay_channel)

    def __del__(self):
        self.relay.close()


class MyThermo:
    def __init__(self, hub_serial, hub_port, thermo_channel):
        self.sensor = TemperatureSensor()
        self.sensor.setHubPort(hub_port)
        self.sensor.setChannel(thermo_channel)
        self.sensor.setDeviceSerialNumber(hub_serial)
        self.sensor.openWaitForAttachment(5000)
        self.previous_temp = 0
        self.thermo_channel = thermo_channel

    def get_temp(self):
        try:
            temp = self.sensor.getTemperature()
            self.previous_temp = temp
            return temp
        except PhidgetException as exception:
            print('Error on thermo channel', self.thermo_channel)
            return self.previous_temp

    def __del__(self):
        self.sensor.close()


class ThermoTile_Single:
    def __init__(self, set_point, hub_serial, channels, control_sign=1):
        # Assume that relay channel 0 (tile) is instrumented with thermocouple 0, etc

        # The phidget solid state relay should be connected to port 0 on the serial hub
        # The thermocouple  phidget should be connected to port 1 on the serial hub
        hub_port_tile = 0
        hub_port_thermo = 1
        self.control_sign = control_sign
        self.tile = MyTile(hub_serial, hub_port_tile, channels)
        self.thermo = MyThermo(hub_serial, hub_port_thermo, channels)
        self.pid = simple_pid.PID()

        self.pid.setpoint = set_point
        self.pid.tunings = (0.35, 0.1, 0.7)
        self.pid.output_limits = (-1, 1)
        self.duty_cycle = 0.5

    def step(self):
        current = self.thermo.get_temp()
        output = self.pid(current)
        self.duty_cycle = self.duty_cycle + output * self.control_sign
        if self.duty_cycle < 0: self.duty_cycle = 0
        if self.duty_cycle > 1: self.duty_cycle = 1
        self.tile.set_duty_cyclce(self.duty_cycle)
        return current


class ThermoTiles:
    def __init__(self, set_points, control_signs=(1, 1, 1, 1), log_name='log.xls', do_plot=True):
        self.log_name = log_name
        self.do_plot = do_plot
        self.set_points = set_points
        self.control_signs = control_signs
        self.logger = SimpleLogger.Logger()
        self.save_interval = 25
        self.display = False

        self.thermo_tile_0 = ThermoTile_Single(set_point=set_points[0], control_sign=control_signs[0],
                                               hub_serial=hub_serial, channels=0)
        self.thermo_tile_1 = ThermoTile_Single(set_point=set_points[1], control_sign=control_signs[1],
                                               hub_serial=hub_serial, channels=1)
        self.thermo_tile_2 = ThermoTile_Single(set_point=set_points[2], control_sign=control_signs[2],
                                               hub_serial=hub_serial, channels=2)
        self.thermo_tile_3 = ThermoTile_Single(set_point=set_points[3], control_sign=control_signs[3],
                                               hub_serial=hub_serial, channels=3)
        if self.do_plot: self.display = Display.Display(set_points)

    def print(self, iteration, time_running, t0, t1, t2, t3):
        error_0 = t0 - self.set_points[0]
        error_1 = t1 - self.set_points[1]
        error_2 = t2 - self.set_points[2]
        error_3 = t3 - self.set_points[3]

        i = '%6i' % iteration
        t = '%05i' % time_running
        temps = '%02.2f %02.2f %02.2f %02.2f' % (t0, t1, t2, t3)
        errors = '%+06.2f %+06.2f %+06.2f %+06.2f' % (error_0, error_1, error_2, error_3)

        print(i, t, '|', temps, '|', errors)

    def run(self, duration=None, wait_scale=1):
        between_polling_sleep = 0.01 * wait_scale
        iteration_sleep = 0.01 * wait_scale
        iteration = 0
        start_time = time.time()
        while True:
            stamp = time.asctime()
            # Update channel 0
            t0 = self.thermo_tile_0.step()
            time.sleep(between_polling_sleep)
            # Update channel 1
            t1 = self.thermo_tile_1.step()
            time.sleep(between_polling_sleep)
            # Update channel 2
            t2 = self.thermo_tile_2.step()
            time.sleep(between_polling_sleep)
            # Update channel 3
            t3 = self.thermo_tile_3.step()
            time.sleep(between_polling_sleep)

            time_running = time.time() - start_time
            # Print output
            self.print(iteration, time_running, t0, t1, t2, t3)
            if duration and time_running > duration: break
            if iteration % self.save_interval == 0:
                if self.display: self.display.animate([t0, t1, t2, t3])
                df = self.logger.export()
                df.to_excel(self.log_name)
            # Save data to logger
            self.logger['time'] = time_running
            self.logger['iteration'] = iteration
            self.logger['stamp'] = stamp
            self.logger['t0'] = t0
            self.logger['t1'] = t1
            self.logger['t2'] = t2
            self.logger['t3'] = t3
            self.logger['sp0'] = self.set_points[0]
            self.logger['sp1'] = self.set_points[1]
            self.logger['sp2'] = self.set_points[2]
            self.logger['sp3'] = self.set_points[3]

            time.sleep(iteration_sleep)
            iteration = iteration + 1

        self.thermo_tile_0.tile.set_duty_cyclce(0)
        self.thermo_tile_1.tile.set_duty_cyclce(0)
        self.thermo_tile_2.tile.set_duty_cyclce(0)
        self.thermo_tile_3.tile.set_duty_cyclce(0)
        print('Done')
