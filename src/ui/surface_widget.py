from PyQt5.QtWidgets import (QWidget, QImage, QPainter)


class SurfaceWidget(QWidget):
    def __init__(self, surface, parent=None):
        super(SurfaceWidget,self).__init__(parent)

        w = surface.get_width()
        h = surface.get_height()
        self.data = surface.get_buffer().raw
        self.image = QImage(self.data, w, h, QImage.Format_RGB32)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, self.image)
        qp.end()
