from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

import matplotlib.patches as mpatches


class MplCanvas(FigureCanvas):
    """
        MplCanvas
    """
    def __init__(self, parent=None):
        self.fig = Figure()
        super().__init__(self.fig)

        self.axes = self.fig.add_subplot()
        self.fig.set_tight_layout(True)

        parent.layout().addWidget(self)

class ScopePlot(MplCanvas):
    """
        RulerPlot
    """
    def __init__(self, parent=None):
        if parent is not None:
            super().__init__(parent)

    def plot(self, y_in , t_in):    

        self.axes.clear()
        self.axes.plot(t_in,y_in,color='r')
        self.fig.canvas.draw()