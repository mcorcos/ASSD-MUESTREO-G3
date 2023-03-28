from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
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
        self.fig.set_tight_layout(True)

        parent.layout().addWidget(self)

class ScopePlot(MplCanvas):
    """
        ScopePlot
    """
    def __init__(self, parent=None):
        if parent is not None:
            super().__init__(parent)

    def plot(self, y_in , t_in):    

#graficos en el tiempo

        self.axes.clear()
        self.axes.plot(t_in,y_in,color='r')


        self.axes2.clear()
        # Compute the one-dimensional discrete Fourier Transform.

        fft_wave = np.fft.fft(y_in)

        # Compute the Discrete Fourier Transform sample frequencies.

        fft_fre = np.fft.fftfreq(n=y_in.size, d=1/100)

        self.axes2.plot(fft_fre, fft_wave.real, label="Real part")
        self.axes2.set_xlim(0,50)
        self.axes2.set_ylim(-20,20)
        self.axes2.legend(loc=1)
        self.axes2.set_title("FFT in Frequency Domain")

        # # graficos en frecuencia
        # self.axes2.clear()

        # Y = fft(y_in)
        # n = len(y_in)
        # # convierto a HZ
        # f = np.linspace(0, 1, n) * (1/t_in[1])
        # self.axes2.plot(f, np.abs(Y) , color='m')
        # self.axes2.set_xlabel('Frequency (Hz)')
        # self.axes2.set_ylabel('Magnitude')

        self.fig.canvas.draw()






class MplCanvas_tau(FigureCanvas):
    """
        MplCanvas
    """
    def __init__(self, parent=None):
        self.fig = Figure()

        super().__init__(self.fig)
        self.axes_tau = self.fig.add_subplot()
        self.fig.set_tight_layout(True)

        parent.layout().addWidget(self)



class TauPlot(MplCanvas_tau):
    """
        TauPlot
    """
    def __init__(self, parent=None):
        if parent is not None:
            super().__init__(parent)

    def plot(self,DC):


        self.axes_tau.clear()




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
        self.axes_tau.plot(time, pulse,color = 'k')
        self.axes_tau.plot(time,pulse2, color='m')
        self.axes_tau.set_xticklabels([])

        self.axes_tau.set_xlabel('Time')
        self.axes_tau.set_ylabel('Amplitude')
        self.axes_tau.set_title('Pulse')
        self.fig.canvas.draw()
