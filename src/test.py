from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow)
from PyQt5.QtGui import (QPainter, QImage)
import pygame
import sys
import threading
import time


class ImageWidget(QWidget):
    data = None
    image = None

    def __init__(self, surface, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.surface = surface
        self.update()

    def update(self):
        print('update')
        surface = self.surface

        w = surface.get_width()
        h = surface.get_height()
        self.data = surface.get_buffer().raw
        self.image = QImage(self.data, w, h, QImage.Format_RGB32)

        self.repaint()

    def paintEvent(self, event):
        print('paintEvent')
        qp = QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, self.image)
        qp.end()


class MainWindow(QMainWindow):

    def __init__(self, surface, parent=None):
        super(MainWindow, self).__init__(parent)
        self.surface = surface
        self.image = ImageWidget(surface)
        self.setCentralWidget(self.image)

    def loop(self):
        for i in range(500):
            print("test " + str(i))
            s.fill((64, 128, 192, 224))
            pygame.draw.circle(s, (255, 255, 255, 255), (i, i), 50)

            self.update()
            time.sleep(0.01)

    def showEvent(self, event):
        t = threading.Thread(target=self.loop)
        t.start()

    def update(self):
        self.image.update()

pygame.init()
s = pygame.Surface((640, 480))

app = QApplication(sys.argv)
w = MainWindow(s)
w.show()
app.exec_()