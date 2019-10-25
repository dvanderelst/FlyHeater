import MyPhidgets
from matplotlib import pyplot

duration = 60 * 3
wait_scale = 0
set_points = [20, 40, 40, 20]
control_signs = [-1, 1, 1, -1]
t = MyPhidgets.ThermoTiles(set_points=set_points, control_signs=control_signs, do_plot=True)
t.run(duration=duration, wait_scale=wait_scale)

df = t.logger.export()
df['error0'] = df['t0'] - df['sp0']
pyplot.plot(df.error0)