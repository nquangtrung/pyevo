import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel,
                             QPushButton, QApplication)
from model import Model
from population_window import PopulationWindow


class MainWindow(QWidget):

    population = []
    population_window = None

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        btn_init = QPushButton('Initialize first generation')
        btn_init.clicked.connect(self.initPopulation)
        grid.addWidget(btn_init, 1, 1)

        btn_show_population = QPushButton('Show population')
        btn_show_population.clicked.connect(self.showPopulation)
        grid.addWidget(btn_show_population, 2, 1)

        btn_train_1_gen = QPushButton('Train 1 generation')
        btn_train_1_gen.clicked.connect(self.buttonClicked)
        grid.addWidget(btn_train_1_gen, 3, 1)

        btn_train_10_gen = QPushButton('Train 10 generation')
        btn_train_10_gen.clicked.connect(self.buttonClicked)
        grid.addWidget(btn_train_10_gen, 4, 1)

        # log = QLabel('Title')
        # grid.addWidget(log, 1, 2, 3, 1)

        self.population_window = PopulationWindow()

        self.move(300, 150)
        self.setWindowTitle('Training')
        self.show()

    def initPopulation(self):
        population = []
        for i in range(0, 20):
            population.append(Model())
            model = Model()
            model.generation = 0
            model.specimen = i

        self.population = population

    def showPopulation(self):
        self.population_window.set_population(self.population)
        self.population_window.show()

    def buttonClicked(self):
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
