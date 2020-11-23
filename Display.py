import matplotlib.pyplot as pyplot
import numpy

pyplot.ion()

pyplot.style.use('bmh')


class Display:
    def __init__(self, set_points):
        self.display_length = 250
        self.set_points = set_points

        self.fig = pyplot.figure(figsize=(20, 10))
        self.x_values = range(self.display_length)

        # 0 ##############################################################################
        self.temperature_series0 = [0] * self.display_length

        self.temperature_axis0 = self.fig.add_subplot(2, 2, 1)
        self.temperature_axis0.set_ylim(self.set_points[0] - 2, self.set_points[0] + 2)
        self.line0, = self.temperature_axis0.plot(self.x_values, self.temperature_series0, 'r-')

        target_line = numpy.array([self.set_points[0]] * self.display_length)

        self.temperature_axis0.plot(self.x_values, target_line, 'k-')
        self.temperature_axis0.plot(self.x_values, target_line - 0.5, 'k--')
        self.temperature_axis0.plot(self.x_values, target_line + 0.5, 'k--')
        self.temperature_axis0.plot(self.x_values, target_line - 0.25, 'k--')
        self.temperature_axis0.plot(self.x_values, target_line + 0.25, 'k--')
        self.temperature_axis0.set_title('Probe 0')

        # 1 ##############################################################################
        self.temperature_series1 = [0] * self.display_length

        self.temperature_axis1 = self.fig.add_subplot(2, 2, 2)
        self.temperature_axis1.set_ylim(self.set_points[1] - 2, self.set_points[1] + 2)
        self.line1, = self.temperature_axis1.plot(self.x_values, self.temperature_series0, 'r-')

        target_line = numpy.array([self.set_points[1]] * self.display_length)

        self.temperature_axis1.plot(self.x_values, target_line, 'k-')
        self.temperature_axis1.plot(self.x_values, target_line - 0.5, 'k--')
        self.temperature_axis1.plot(self.x_values, target_line + 0.5, 'k--')
        self.temperature_axis1.plot(self.x_values, target_line - 0.25, 'k--')
        self.temperature_axis1.plot(self.x_values, target_line + 0.25, 'k--')
        self.temperature_axis1.set_title('Probe 1')

        # 2 ##############################################################################
        self.temperature_series2 = [0] * self.display_length

        self.temperature_axis2 = self.fig.add_subplot(2, 2, 3)
        self.temperature_axis2.set_ylim(self.set_points[2] - 2, self.set_points[2] + 2)
        self.line2, = self.temperature_axis2.plot(self.x_values, self.temperature_series0, 'r-')

        target_line = numpy.array([self.set_points[2]] * self.display_length)

        self.temperature_axis2.plot(self.x_values, target_line, 'k-')
        self.temperature_axis2.plot(self.x_values, target_line - 0.5, 'k--')
        self.temperature_axis2.plot(self.x_values, target_line + 0.5, 'k--')
        self.temperature_axis2.plot(self.x_values, target_line - 0.25, 'k--')
        self.temperature_axis2.plot(self.x_values, target_line + 0.25, 'k--')
        self.temperature_axis2.set_title('Probe 2')

        # 3 ##############################################################################
        self.temperature_series3 = [0] * self.display_length

        self.temperature_axis3 = self.fig.add_subplot(2, 2, 4)
        self.temperature_axis3.set_ylim(self.set_points[3] - 2, self.set_points[3] + 2)
        self.line3, = self.temperature_axis3.plot(self.x_values, self.temperature_series0, 'r-')

        target_line = numpy.array([self.set_points[3]] * self.display_length)

        self.temperature_axis3.plot(self.x_values, target_line, 'k-')
        self.temperature_axis3.plot(self.x_values, target_line - 0.5, 'k--')
        self.temperature_axis3.plot(self.x_values, target_line + 0.5, 'k--')
        self.temperature_axis3.plot(self.x_values, target_line - 0.25, 'k--')
        self.temperature_axis3.plot(self.x_values, target_line + 0.25, 'k--')
        self.temperature_axis3.set_title('Probe 3')

    def animate(self, temperatures):
        # Update 0
        self.temperature_series0.append(temperatures[0])
        self.temperature_series0 = self.temperature_series0[-self.display_length:]
        self.line0.set_ydata(self.temperature_series0)

        # Update 1
        self.temperature_series1.append(temperatures[1])
        self.temperature_series1 = self.temperature_series1[-self.display_length:]
        self.line1.set_ydata(self.temperature_series1)

        # Update 2
        self.temperature_series2.append(temperatures[2])
        self.temperature_series2 = self.temperature_series2[-self.display_length:]
        self.line2.set_ydata(self.temperature_series2)

        # Update 3
        self.temperature_series3.append(temperatures[3])
        self.temperature_series3 = self.temperature_series3[-self.display_length:]
        self.line3.set_ydata(self.temperature_series3)

        # Update
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
