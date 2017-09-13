from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel,
                             QPushButton, QApplication)
from tester import Tester
import functools


class PopulationWindow(QWidget):

    population = []

    test = None

    def __init__(self):
        super().__init__()

        self.init_ui()

    def set_population(self, population):
        self.population = population
        grid = QGridLayout()
        self.setLayout(grid)

        col = 15
        for i in range(population.max_population):
            model = population.specimen(i)
            dead = " (Dead)" if model.dead else ""
            btn_show = QPushButton("#" + str(model.generation) + "." + str(model.specimen) + dead)
            btn_show.specimen = model
            btn_show.clicked.connect(self.make_start_show(model))
            grid.addWidget(btn_show, int(i / col), int(i % col))

    def start_test(self):
        if self.test is not None:
            self.test.stop()

        self.test = Tester(self.get_specimen())
        print(str(self.test.test()))
        self.test = None

    def make_start_show(self, model):
        def start_show():
            if self.test is not None:
                self.test.stop()

            self.test = Tester(model)
            self.test.show()
            self.test = None

        return start_show

    def init_ui(self):
        self.move(300, 150)
        self.setWindowTitle('Population')
