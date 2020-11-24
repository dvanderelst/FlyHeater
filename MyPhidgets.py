import time
import SimpleLogger
import simple_pid
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.PhidgetException import *
from Phidget22.LogLevel import *
from Phidget22.Devices.Log import *
import Display
import traceback
import math

Log.enable(LogLevel.PHIDGET_LOG_INFO, "phidget_log.log")

# Serial numbers of the hub(s) and port on those hubs
relay_hub = [561064, 0]
thermal_hub = [560175, 0]


class MyRelay:
    def __init__(self, hub_serial, hub_port, relay_channel):
        self.updated_n = 0
        self.relay = DigitalOutput()
        self.relay.setChannel(relay_channel)
        self.relay.setHubPort(hub_port)
        self.relay.setDeviceSerialNumber(hub_serial)
        self.relay_channel = relay_channel
        self.relay.openWaitForAttachment(5000)
        self.previous_duty_cycle = 100

    def set_state(self, state):
        self.relay.setState(state)

    def reconnect(self):
        self.relay.close()
        self.relay.openWaitForAttachment(5000)

    def set_duty_cycle(self, duty_cycle):
        if self.updated_n%50==0: self.reconnect()

        try:
            diff = math.fabs(self.previous_duty_cycle - duty_cycle)
            if diff > 0.05:
                self.relay.setDutyCycle(duty_cycle)
                self.previous_duty_cycle = duty_cycle
                self.updated_n = self.updated_n + 1
        except PhidgetException as exception:
            print('Error on relay channel', self.relay_channel, exception)
            self.reconnect()

    def __del__(self):
        self.relay.close()



class MyThermo:
    def __init__(self, hub_serial, hub_port, thermal_channel):
        self.sensor = TemperatureSensor()
        self.sensor.setHubPort(hub_port)
        self.sensor.setChannel(thermal_channel)
        self.sensor.setDeviceSerialNumber(hub_serial)
        self.sensor.openWaitForAttachment(5000)
        self.previous_temp = 0
        self.thermal_channel = thermal_channel

    def get_temp(self):
        try:
            temp = self.sensor.getTemperature()
            self.previous_temp = temp
            return temp
        except PhidgetException as exception:
            print('Error on thermal channel', self.thermal_channel, exception)
            return self.previous_temp

    def __del__(self):
        self.sensor.close()


class SingleThermalTile:
    def __init__(self, set_point, channel, control_sign=1):
        self.control_sign = control_sign
        self.relay = MyRelay(relay_hub[0], relay_hub[1], channel)
        self.thermal = MyThermo(thermal_hub[0], thermal_hub[1], channel)
        self.pid = simple_pid.PID()

        self.pid.setpoint = set_point
        self.pid.tunings = (0.35, 0.1, 0.7)
        self.pid.output_limits = (-1, 1)
        self.duty_cycle = 0.5

    def step(self):
        current = self.thermal.get_temp()
        output = self.pid(current)
        self.duty_cycle = self.duty_cycle + (output * self.control_sign)
        if self.duty_cycle < 0: self.duty_cycle = 0
        if self.duty_cycle > 1: self.duty_cycle = 1
        #self.relay.set_duty_cycle(self.duty_cycle)
        self.relay.set_state(self.duty_cycle)
        return current


class ThermalTiles:
    def __init__(self, set_points, control_signs=(1, 1, 1, 1), log_name='log.xls', do_plot=True):
        self.log_name = log_name
        self.do_plot = do_plot
        self.set_points = set_points
        self.control_signs = control_signs
        self.logger = SimpleLogger.Logger()
        self.save_interval = 25
        self.display = False

        self.thermal_tile_0 = SingleThermalTile(set_point=set_points[0], channel=0, control_sign=control_signs[0])
        self.thermal_tile_1 = SingleThermalTile(set_point=set_points[1], channel=1, control_sign=control_signs[1])
        self.thermal_tile_2 = SingleThermalTile(set_point=set_points[2], channel=2, control_sign=control_signs[2])
        self.thermal_tile_3 = SingleThermalTile(set_point=set_points[3], channel=3, control_sign=control_signs[3])
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

    def run(self, duration=None, update_sleep=1, iteration_sleep=1):
        iteration = 0
        start_time = time.time()
        while True:
            stamp = time.asctime()
            # Update channel 0
            t0 = self.thermal_tile_0.step()
            time.sleep(update_sleep)
            # Update channel 1
            t1 = self.thermal_tile_1.step()
            time.sleep(update_sleep)
            # Update channel 2
            t2 = self.thermal_tile_2.step()
            time.sleep(update_sleep)
            # Update channel 3
            t3 = self.thermal_tile_3.step()
            time.sleep(update_sleep)

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

        self.thermal_tile_0.relay.set_duty_cycle(0)
        self.thermal_tile_1.relay.set_duty_cycle(0)
        self.thermal_tile_2.relay.set_duty_cycle(0)
        self.thermal_tile_3.relay.set_duty_cycle(0)
        print('Done')
