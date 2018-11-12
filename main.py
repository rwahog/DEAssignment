import sys
from math import sin

import numpy
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMdiSubWindow, QApplication, QVBoxLayout, QPushButton, QDockWidget, \
    QWidget, QTextEdit, QFormLayout, QLabel, QLineEdit, QSizePolicy, QTabWidget
from matplotlib import pyplot
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        # self.tabs.resize(300, 200)

        self.tabs.addTab(self.tab1, "Numerical Methods")
        self.tabs.addTab(self.tab2, "Local Error")
        self.tabs.addTab(self.tab3, "Global Error")

        self.tab1.layout = QVBoxLayout()
        self.graph = PlotCanvas(self)
        self.toolbar = NavigationToolbar2QT(self.graph, self)
        self.tab1.layout.addWidget(self.toolbar)
        self.tab1.layout.addWidget(self.graph)
        self.tab1.setLayout(self.tab1.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=7, height=7, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.canvas = FigureCanvas.__init__(self, fig)
        # self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()


    def plot(self):
        x0 = 1
        y0 = 0.5
        X = 7
        N = 1000
        step_size = (X - x0)/N
        x = numpy.arange(x0, X, step_size, 'float')
        c = -(3*numpy.e**(2*x0)+y0*numpy.e**(3*x0))/y0
        r = -(3*numpy.e**(2*x))/ (numpy.e**(3*x)+c)
        r[:-1][numpy.diff(r) < 0] = numpy.nan
        bx = self.figure.add_subplot(111)
        bx.spines['left'].set_color('black')
        bx.spines['bottom'].set_color('black')
        bx.xaxis.set_ticks_position('bottom')
        bx.spines['top'].set_position(('data', 0))
        bx.yaxis.set_ticks_position('left')
        bx.spines['right'].set_position(('data', 0))
        bx.set_xlabel('x')
        bx.set_ylabel('y(x)')
        bx.set_ylim([-10,10])
        bx.plot(x, r, color="black", label="y(x)")
        bx.grid()
        bx.legend(loc='upper left')
        bx.set_title('Numerical Methods')
        self.draw()


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.sidePanel = QDockWidget(self)
        self.sidePanel.setFeatures(QDockWidget.NoDockWidgetFeatures)
        w = QWidget(self.sidePanel)
        v = QWidget(self)
        lay = QFormLayout(w)
        lay2 = QVBoxLayout(v)
        lay.setContentsMargins(1, 1, 1, 1)
        w.setLayout(lay)
        v.setLayout(lay2)
        equation = QLabel("y' = y^2*e^x+2y")
        text = QLabel("Initial Values")
        x0 = QLineEdit()
        y0 = QLineEdit()
        n = QLineEdit()
        lay.addRow(equation)
        lay.addRow(text)
        lay.addRow(QLabel("x0"), x0)
        lay.addRow(QLabel("y0"), y0)
        lay.addRow(QLabel("Number of steps"), n)
        self.tab_widget.setLayout(lay2)
        self.sidePanel.setWidget(w)
        # self.tree.activated.connect(self.handle_dblclick)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidePanel)

        self.setWindowTitle("Computational Practicum")

    def add_plots(self):
        sub = QMdiSubWindow()
        sub.setWidget(QTextEdit())
        sub.setWindowTitle("Plot")
        self.mdi.addSubWindow(sub)
        sub.show()


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
