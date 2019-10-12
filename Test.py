import MyPhidgets
import time
from matplotlib import pyplot

relay = MyPhidgets.MyRelay(hub_serial=560175, hub_port=0)
thermo = MyPhidgets.MyThermo(hub_serial=560175, hub_port=1)

set_temperature = 32
dead_zone = 0.1
measurements = 2000
sleep_time = 0.001

record = []

duty_cyle = 0.5

for iteration in range(measurements):
    temps = thermo.get_temps()
    temp0 = temps[0]
    record.append(temp0)
    time.sleep(sleep_time)
    if temp0 < set_temperature: duty_cyle = (set_temperature - temp0)
    if temp0 > set_temperature: duty_cyle = 0
    if duty_cyle < 0: duty_cyle = 0
    if duty_cyle > 1: duty_cyle = 1

    relay.set_duty_cylces([duty_cyle, 0, 0, 0])

    progress = 100 * iteration / measurements
    txt = '%i PCT %.2fC %.2f Duty' % (progress, temp0, duty_cyle)
    if iteration % 10 == 0: print(txt)

record = record[1000:]
relay.set_states([0, 0, 0, 0])

#%%

pyplot.figure()
pyplot.subplot(1, 2, 1)
pyplot.plot(record)
pyplot.subplot(1, 2, 2)
pyplot.hist(record, bins=25)
pyplot.show()
