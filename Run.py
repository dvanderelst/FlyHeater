import MyPhidgets

duration = 60 * 5
set_points = [32, 40, 40, 37]
t = MyPhidgets.ThermoTiles(set_points=set_points)
t.run(duration=duration)