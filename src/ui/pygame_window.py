from PyQt5.QtWidgets import (QWidget, QGridLayout)
from pygame_widget import PygameWidget


class PygameWindow(QWidget):
    surface = None
    image = None

    def __init__(self, parent=None):
        super().__init__()
        self.move(100, 100)
        self.setWindowTitle('Simulation')

    def surface(self, surface):
        self.surface = surface
        self.image = PygameWidget(surface)

        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.image, 1, 1)

    def update(self):
        self.image.update()
