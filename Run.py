import MyPhidgets
from matplotlib import pyplot

duration = 60 * 12
wait_scale = 1
set_points = [20, 30, 20, 30]
control_signs = [-1, 1, -1, 1]
t = MyPhidgets.ThermoTiles(set_points=set_points, control_signs=control_signs, do_plot=False)
t.run(duration=duration, wait_scale=wait_scale)

df = t.logger.export()
df['error0'] = df['t0'] - df['sp0']
pyplot.plot(df.error0)