from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton)
from tester import Tester
from pygame_window import PygameWindow


class PopulationWindow(QWidget):

    population = []
    pygame = None
    tester = None

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
            dead = " (Dead)" if model.dead else (" (" + str(model.fitness) + ")") if model.trained else ""
            btn_show = QPushButton("#" + str(model.generation) + "." + str(model.specimen) + dead)
            btn_show.specimen = model
            btn_show.clicked.connect(self.make_start_show(model))
            grid.addWidget(btn_show, int(i / col), int(i % col))

    # def start_test(self):
    #     if self.tester is not None:
    #         self.tester.stop()
    #
    #     self.tester = Tester(self.get_specimen())
    #     print(str(self.tester.test()))
    #     self.tester = None

    def make_start_show(self, model):
        def start_show():
            if self.tester is not None:
                self.tester.stop()
                self.pygame.close()

            self.pygame = PygameWindow()
            self.pygame.show()
            self.tester = Tester(model)
            self.tester.show(self.pygame)

        return start_show

    def init_ui(self):
        self.move(100, 100)
        self.setWindowTitle('Population')
