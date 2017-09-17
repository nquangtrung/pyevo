from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton)
from tester import Tester
from tester_window import TesterWindow


class PopulationWindow(QWidget):

    population = []
    # pygame = None
    # tester = None

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
            dead = " (Dead)" if model.dead else (" (" + str(round(model.fitness, 3)) + ")") if model.trained else ""
            btn_show = QPushButton("#" + str(model.generation) + "." + str(model.specimen) + dead)
            btn_show.specimen = model
            btn_show.clicked.connect(self.make_start_show(model))
            grid.addWidget(btn_show, int(i / col), int(i % col))

    def make_start_show(self, model):
        def start_show():
            tester = Tester(model)
            window = TesterWindow()
            window.show()
            tester.init(window)

        return start_show

    def init_ui(self):
        self.move(100, 100)
        self.setWindowTitle('Population')
