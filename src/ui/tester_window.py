from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QLabel)
from pygame_widget import PygameWidget
from PyQt5.QtCore import Qt


class TesterWindow(QWidget):
    surface = None
    image = None
    looper = None

    tester = None

    def __init__(self, parent=None):
        super().__init__()
        self.move(100, 100)
        self.setWindowTitle('Simulation')

    def closeEvent(self, event):
        self.looper.stop()

    def loop(self, looper):
        self.looper = looper

    def surface(self, surface):
        grid = QGridLayout()
        self.setLayout(grid)

        self.surface = surface
        self.image = PygameWidget(surface)
        grid.addWidget(self.image, 2, 1, 1, 4)

        btn_start = QPushButton('Start')
        btn_start.clicked.connect(self.start)
        grid.addWidget(btn_start, 1, 1)

        btn_stop = QPushButton('Stop')
        btn_stop.clicked.connect(self.stop)
        grid.addWidget(btn_stop, 1, 2)

        btn_reset = QPushButton('Reset')
        btn_reset.clicked.connect(self.reset)
        grid.addWidget(btn_reset, 1, 3)

        btn_run = QPushButton('Run')
        btn_stop.clicked.connect(self.run)
        grid.addWidget(btn_run, 1, 4)

        self.lbl_model = QLabel('Generation: \nSpecimen: \n')
        grid.addWidget(self.lbl_model, 1, 5, 2, 1, Qt.AlignTop)

    def run(self):
        pass

    def reset(self):
        pass

    def start(self):
        self.looper.show()

    def stop(self):
        self.looper.stop()

    def update(self):
        self.image.update()
