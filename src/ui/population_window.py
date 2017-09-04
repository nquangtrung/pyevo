from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel,
                             QPushButton, QApplication)
from test_window import TestWindow


class PopulationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def set_population(self, population):
        self.population = population
        grid = QGridLayout()
        self.setLayout(grid)

        col = 10
        for i in range(len(population)):
            btn_test = QPushButton(str(i))
            btn_test.clicked.connect(self.startTest)
            grid.addWidget(btn_test, int((i * 2) / col), (i * 2) % col)

            btn_show = QPushButton(str(i))
            btn_show.clicked.connect(self.startShow)
            grid.addWidget(btn_show, int((i * 2 + 1) / col), (i * 2 + 1) % col)

    def startTest(self):
        sender = self.sender()
        specimen = int(sender.text())
        model = self.population[specimen]
        test = TestWindow(model)
        test.test()

    def startShow(self):
        sender = self.sender()
        specimen = int(sender.text())
        model = self.population[specimen]
        test = TestWindow(model)
        test.show()

    def initUI(self):

        self.move(300, 150)
        self.setWindowTitle('Population')
