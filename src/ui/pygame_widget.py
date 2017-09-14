from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow)
from PyQt5.QtGui import (QPainter, QImage)


class PygameWidget(QWidget):
    data = None
    image = None

    def __init__(self, surface, parent=None):
        super(PygameWidget, self).__init__(parent)
        self.surface = surface
        self.update()

    def update(self):
        surface = self.surface

        w = surface.get_width()
        h = surface.get_height()
        self.data = surface.get_buffer().raw
        self.image = QImage(self.data, w, h, QImage.Format_RGB32)

        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, self.image)
        qp.end()