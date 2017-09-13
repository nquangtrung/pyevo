import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel,
                             QPushButton, QApplication)
from generation import Generation
from population_window import PopulationWindow

class MainWindow(QWidget):
    current_generation = None
    generations = []

    population_window = None

    gen = 0
    specimen = 0
    max_fitness = 0
    avg_fitness = 0
    max_specimen = 0

    lbl_gen = None
    lbl_specimen = None
    lbl_max_fitness = None
    lbl_med_fitness = None

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
        btn_train_1_gen.clicked.connect(self.test_1_generation)
        grid.addWidget(btn_train_1_gen, 3, 1)

        btn_train_10_gen = QPushButton('Train 10 generation')
        btn_train_10_gen.clicked.connect(self.buttonClicked)
        grid.addWidget(btn_train_10_gen, 4, 1)

        btn_kill = QPushButton('Kill bad specimen')
        btn_kill.clicked.connect(self.buttonClicked)
        grid.addWidget(btn_train_10_gen, 4, 1)

        btn_reproduce = QPushButton('Reproduce new generation')
        btn_reproduce.clicked.connect(self.buttonClicked)
        grid.addWidget(btn_train_10_gen, 4, 1)

        self.lbl_gen = QLabel('Generation: ')
        grid.addWidget(self.lbl_gen, 1, 2)

        self.lbl_specimen = QLabel('Specimen: ')
        grid.addWidget(self.lbl_specimen, 2, 2)

        self.lbl_max_fitness = QLabel('Maximum Fitness: ')
        grid.addWidget(self.lbl_max_fitness, 3, 2)

        self.lbl_med_fitness = QLabel('Median Fitness: ')
        grid.addWidget(self.lbl_med_fitness, 4, 2)

        self.show_info()

        self.move(300, 150)
        self.setWindowTitle('Training')
        self.show()

    def show_info(self):
        self.lbl_gen.setText('Generation: #' + str(self.gen))
        self.lbl_specimen.setText('Population: ' + str(0 if self.current_generation is None else self.current_generation.number()))
        self.lbl_max_fitness.setText('Maximum fitness: ' + str(self.max_fitness) + ' specimen: #' + str(self.max_specimen))
        self.lbl_med_fitness.setText('Median fitness: ' + str(self.avg_fitness))

    def test_1_generation(self):
        self.current_generation.train()
        self.max_fitness = self.current_generation.best().fitness
        self.max_specimen = self.current_generation.best().specimen
        self.avg_fitness = self.current_generation.avg()
        self.show_info()

    def initPopulation(self):
        self.current_generation = Generation()
        self.generations.append(self.current_generation)
        self.show_info()

    def showPopulation(self):
        self.population_window = PopulationWindow()
        self.population_window.set_population(self.current_generation.population)
        self.population_window.show()

    def buttonClicked(self):
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
