from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.patches as mpatches
from scipy.fft import fft



class MplCanvas(FigureCanvas):
    """
        MplCanvas
    """
    def __init__(self, parent=None):
        self.fig = Figure()

        super().__init__(self.fig)
        self.axes = self.fig.add_subplot(121)
        self.axes2 = self.fig.add_subplot(122)
        self.navToolBar = NavigationToolbar(self, parent)

        parent.layout().addWidget(self.navToolBar)
        parent.layout().addWidget(self)

        self.fig.set_tight_layout(True)

class ScopePlot(MplCanvas):
    """
        ScopePlot
    """
    def __init__(self, parent=None):
        if parent is not None:
            super().__init__(parent)


    def plot(self, y_in, t_in, amp_in, freq_in):    

        # Gráficos en el tiempo
        self.axes.clear()
        self.axes.grid(which='major', axis='both')
        self.axes.plot(t_in, y_in, color='r')

        # Gráficos en frecuencia
        self.axes2.clear()

        self.axes2.plot(freq_in, amp_in)
        self.axes2.grid(which='major', axis='both')
        self.axes2.set_title("FFT in Frequency Domain")
        self.axes2.set_xlim(0, 150e3)


        self.fig.canvas.draw()


class MplCanvas_single(FigureCanvas):
    """
        MplCanvas
    """
    def __init__(self, parent=None):
        self.fig = Figure()

        super().__init__(self.fig)
        self.axes = self.fig.add_subplot()
        self.fig.set_tight_layout(True)

        parent.layout().addWidget(self)


class TauPlot(MplCanvas_single):
    """
        TauPlot
    """
    def __init__(self, parent=None):
        if parent is not None:
            super().__init__(parent)

    def plot(self, DC):


        self.axes.clear()

        # Define the pulse parameters
        amplitude = 1.0
        duration = 0.1
        start_time = 0.0
        end_time = 0.2

        # Define the x-axis values
        time = np.linspace(start_time, end_time, 1000)

        # Define the pulse function
        pulse = np.zeros_like(time)
        pulse[(time >= start_time) & (time <= start_time + duration)] = amplitude
        pulse2 = np.zeros_like(time)
        pulse2[(time >= start_time) & (time <= start_time + DC/10)] = amplitude
        # Create the plot
        self.axes.plot(time, pulse,color = 'k')
        self.axes.plot(time,pulse2, color='m')
        self.axes.set_xticklabels([])

        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Amplitude')
        self.axes.set_title('Pulse')
        self.fig.canvas.draw()


class MultipleViews(MplCanvas_single):

    def __init__(self, parent=None):
        if parent is not None:
            super().__init__(parent)
        
    def plot(self, y_1, y_2 , t_in):
        self.axes.clear()
        self.axes.plot(t_in,y_1,color='g', label = "Signal 1")
        self.axes.plot(t_in,y_2,'-b' , label = 'Signal 2')
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Amplitude')
        self.axes.set_title('Compare')
        self.axes.set_xticklabels([])
        self.fig.canvas.draw()