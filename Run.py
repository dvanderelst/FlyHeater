import MyPhidgets
from matplotlib import pyplot

duration = 60 * 5
wait_scale = 1
set_points = [40, 40, 40, 40]
t = MyPhidgets.ThermoTiles(set_points=set_points, do_plot=True)
t.run(duration=duration, wait_scale=wait_scale)

pyplot.figure()
pyplot.subplot(2,2,1)
pyplot.hist(t.log.t0)
pyplot.subplot(2,2,2)
pyplot.hist(t.log.t1)
pyplot.subplot(2,2,3)
pyplot.hist(t.log.t2)
pyplot.subplot(2,2,4)
pyplot.hist(t.log.t3)

pyplot.show()