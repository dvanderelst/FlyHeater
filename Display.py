import datetime as dt
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import time
import numpy

pyplot.ion()

pyplot.style.use('bmh')

class Display:
    def __init__(self, set_point):
        self.display_length = 250
        self.set_point = set_point

        target_line = numpy.array([set_point] * self.display_length)

        self.fig = pyplot.figure()
        self.x_values = range(self.display_length)
        self.temperature_series = [0] * self.display_length

        self.temperature_axis = self.fig.add_subplot(1, 1, 1)
        self.temperature_axis.set_ylim(self.set_point - 2, set_point + 2)
        self.line1, = self.temperature_axis.plot(self.x_values, self.temperature_series, 'r-')

        self.temperature_axis.plot(self.x_values, target_line, 'k-')
        self.temperature_axis.plot(self.x_values, target_line - 0.5, 'k--')
        self.temperature_axis.plot(self.x_values, target_line + 0.5, 'k--')
        self.temperature_axis.plot(self.x_values, target_line - 0.25, 'k--')
        self.temperature_axis.plot(self.x_values, target_line + 0.25, 'k--')


    def animate(self, temperature):
        # Update
        self.temperature_series.append(temperature)
        self.temperature_series = self.temperature_series[-self.display_length:]
        self.line1.set_ydata(self.temperature_series)
        # Update
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
