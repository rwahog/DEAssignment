import decimal
import math
import sys
from decimal import Decimal
import decimal
import numpy
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMdiSubWindow, QApplication, QVBoxLayout, QPushButton, QDockWidget, \
    QWidget, QTextEdit, QFormLayout, QLabel, QLineEdit, QSizePolicy, QTabWidget
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
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        x0 = 1
        y0 = 0.5
        X = 5
        N = 1000
        step_size = (X - x0) / N
        r = numpy.array(NumericalMethods.euler(self, Decimal(1), Decimal(0.5), Decimal(5), 1000))
        improved = numpy.array(NumericalMethods.improved_euler(self, Decimal(1), Decimal(0.5), Decimal(5), 1000))
        x = numpy.arange(x0, X, step_size)
        c = -(3 * numpy.e ** (2 * x0)+y0 * numpy.e ** (3*x0)) / y0
        exact = -(3*numpy.e**(2*x)) / (numpy.e**(3*x)+c)
        r[:-1][numpy.diff(r) < 0] = numpy.nan
        exact[:-1][numpy.diff(exact) < 0] = numpy.inf
        improved[:-1][numpy.diff(improved) < 0] = numpy.inf
        # print(NumericalMethods.evaluate_equation(self, Decimal(1.3894)))
        bx = self.figure.add_subplot(111)
        bx.axvline(x=numpy.log(6 * numpy.e ** 2 + numpy.e ** 3) / 3, linestyle='--', linewidth=0.5)
        bx.spines['left'].set_color('black')
        bx.spines['bottom'].set_color('black')
        bx.xaxis.set_ticks_position('bottom')
        bx.spines['top'].set_position(('data', 0))
        bx.yaxis.set_ticks_position('left')
        bx.spines['right'].set_position(('data', 0))
        bx.set_xlabel('x')
        bx.set_ylabel('y(x)')
        bx.set_ylim([-10, 10])
        bx.plot(x, r, color="black", label="euler")
        bx.plot(x, exact, color="red", label="exact")
        bx.plot(x, improved, color="blue", label="improved")
        bx.grid()
        bx.legend(loc='upper left')
        bx.set_title('Numerical Methods')
        self.draw()


class NumericalMethods:
    def __init__(self, x0, y0, X, N):
        NumericalMethods.__init__(self, x0, y0, X, N)

    def evaluate_equation(self, x: Decimal) -> Decimal:
        c = -6 * (Decimal(2)).exp()-(Decimal(3)).exp()
        r = -(3 * (2 * x).exp()) / ((3*x).exp() + c)
        return r

    def evaluate_DE(self, x, y):
        try:
            # print(x, y)
            r = numpy.power(y, 2) * x.exp() + (2 * y)
        except OverflowError as err:
            pass
        return r

    def euler(self, x0:Decimal, y0: Decimal, X:Decimal, n):
        k1 = []
        k2 = []
        h = Decimal((X - x0) / n)
        x = Decimal(x0)
        y = Decimal(y0)
        i = 0
        while x < X:
            if math.isclose(x, numpy.log(6 * numpy.e ** 2 + numpy.e ** 3) / 3, abs_tol=h / 2):
                x += h
                i += 1
                print(i, "1", x, y)
                y = NumericalMethods.evaluate_equation(self, X)
                k1.append(y)
                break
            y += h * NumericalMethods.evaluate_DE(self, x, y)
            i += 1
            print(i, "0", x, y)
            k1.append(y)
            x += h
        while X > x:
            i += 1
            print(i, "2", X, y)
            y += h * NumericalMethods.evaluate_DE(self, X, y)
            k2.append(y)
            X -= h
        k2.reverse()
        k1 = k1 + k2
        return k1

    def improved_euler(self, x0:Decimal, y0:Decimal, X: Decimal, n):
        l1 = []
        h = Decimal((X - x0) / n)
        x = x0
        y = y0
        while x < (Decimal(numpy.log(6 * numpy.e ** 2 + numpy.e ** 3) / 3) - (h/2)):
            k1 = NumericalMethods.evaluate_DE(self,  x, y)
            k2 = NumericalMethods.evaluate_DE(self, x + h, y + h * k1)
            y += (h/2)*(k1+k2)
            x += h
            l1.append(y)
        y = NumericalMethods.evaluate_equation(self, Decimal(numpy.log(6 * numpy.e ** 2 + numpy.e ** 3) / 3) + h)

        x = Decimal(numpy.log(6 * numpy.e ** 2 + numpy.e ** 3) / 3) + (h / 2)
        while x < X:
            k1 = NumericalMethods.evaluate_DE(self, x, y)
            k2 = NumericalMethods.evaluate_DE(self, x + h, y + h * k1)
            y += (h/2)*(k1+k2)
            x += h
            l1.append(y)
            # print("here", x, y)
        return l1


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        decimal.getcontext().traps[decimal.Overflow] = False
        decimal.getcontext().prec = 28
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
