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


    def plot(self, y_in, t_in, amp_in, freq_in, dB = False):    

        # Gráficos en el tiempo
        self.axes.clear()
        self.axes.grid(which='major', axis='both')
        self.axes.plot(t_in, y_in, color='r')

        # Gráficos en frecuencia
        self.axes2.clear()

        if not dB:
            self.axes2.plot(freq_in, amp_in)
        else:
            new_amp = np.zeros(len(amp_in))
            for i in range(len(amp_in)):
                x = 20*np.log10(amp_in[i])
                if x < -100:
                    x = -100
                new_amp[i] = x

            self.axes2.plot(freq_in, new_amp)

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

    def plot(self, DC, freq):


        self.axes.clear()

        # Define the pulse parameters
        amplitude = 5.0
        duration = 1 / (2*freq)
        start_time = 0.0
        end_time = 1 / freq

        # Define the x-axis values
        time = np.linspace(0, end_time, 1000)

        start1 = end_time * 0.75
        end1 = end_time * 0.25

        start2 = (end_time - end_time * DC)/2
        end2 = end_time - start2

        # Define the pulse function
        pulse = np.zeros_like(time)
        pulse[(time >= start1) | (time <= end1)] = amplitude
        pulse2 = np.zeros_like(time)
        pulse2[(time >= start2) & (time <= end2)] = amplitude
        # Create the plot
        self.axes.plot(time, pulse,color = 'k')
        self.axes.plot(time,pulse2, color='m')

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