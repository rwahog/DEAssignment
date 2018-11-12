import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMdiSubWindow, QApplication, QVBoxLayout, QPushButton, QDockWidget, \
    QWidget, QTextEdit, QFormLayout, QLabel, QLineEdit, QSizePolicy, QTabWidget
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
        self.button = QPushButton("Button")
        self.tab1.layout.addWidget(self.graph)
        self.tab1.setLayout(self.tab1.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=7, height=7, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.set_title('Numerical Methods')
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
