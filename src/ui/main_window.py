import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QMainWindow, QSlider,
                             QPushButton, QApplication, QAction, QFileDialog)
from generation import Generation
from population_window import PopulationWindow
import simplejson as json
import marshal
import threading


class MainWindow(QMainWindow):
    training_generation = None
    current_generation = None
    generations = []

    population_window = None

    main_widget = None

    lbl_gen = None
    lbl_specimen = None
    lbl_max_fitness = None
    lbl_med_fitness = None
    lbl_status = None

    slider = None

    status = 'Idle'

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        exit_act = QAction('&Exit', self)
        exit_act.setShortcut('Ctrl+X')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(self.closeEvent)

        save_act = QAction('&Save', self)
        save_act.setShortcut('Ctrl+S')
        save_act.setStatusTip('Save')
        save_act.triggered.connect(self.saveEvent)

        load_act = QAction('&Load', self)
        load_act.setShortcut('Ctrl+O')
        load_act.setStatusTip('Load')
        load_act.triggered.connect(self.loadEvent)

        self.statusBar()

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(save_act)
        file_menu.addAction(load_act)
        file_menu.addAction(exit_act)

        grid = QGridLayout()
        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        self.main_widget = widget

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
        btn_train_10_gen.clicked.connect(self.test_10_generation)
        grid.addWidget(btn_train_10_gen, 4, 1)

        btn_train = QPushButton('Train')
        btn_train.clicked.connect(self.train)
        grid.addWidget(btn_train, 1, 3)

        btn_stop = QPushButton('Stop')
        btn_stop.clicked.connect(self.stop)
        grid.addWidget(btn_stop, 2, 3)

        btn_kill = QPushButton('Kill bad specimen')
        btn_kill.clicked.connect(self.kill)
        grid.addWidget(btn_kill, 5, 1)

        btn_reproduce = QPushButton('Reproduce new generation')
        btn_reproduce.clicked.connect(self.reproduce)
        grid.addWidget(btn_reproduce, 6, 1)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.setMaximum(0)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.changeGeneration)
        grid.addWidget(self.slider, 7, 1, 1, 3)

        self.lbl_gen = QLabel('Generation: ')
        grid.addWidget(self.lbl_gen, 1, 2)

        self.lbl_specimen = QLabel('Specimen: ')
        grid.addWidget(self.lbl_specimen, 2, 2)

        self.lbl_max_fitness = QLabel('Maximum Fitness: ')
        grid.addWidget(self.lbl_max_fitness, 3, 2)

        self.lbl_med_fitness = QLabel('Median Fitness: ')
        grid.addWidget(self.lbl_med_fitness, 4, 2)

        self.lbl_status = QLabel('Status: ' + self.status)
        grid.addWidget(self.lbl_status, 5, 2)

        self.show_info()

        self.move(100, 100)
        self.setWindowTitle('Training')
        self.show()

    def changeGeneration(self):
        slider = self.sender()
        self.current_generation = self.generations[slider.value()]
        self.show_info()

    def save(self, file_name):
        self.statusBar().showMessage("Saving generations at: " + file_name)
        generations = list(map(lambda gen: gen.to_hash(), self.generations))

        print('generate json: ')
        text = json.dumps(generations)
        print('text length: ' + str(len(text)))
        text_file = open(file_name, "w")
        text_file.write(text)
        text_file.close()
        self.statusBar().showMessage("File saved")

    def load(self, file_name):
        self.statusBar().showMessage("Loading generations at: " + file_name)
        text_file = open(file_name, "r")
        text = text_file.read()
        text_file.close()

        generations = json.loads(text)
        self.generations = list(map(lambda gen: Generation.from_hash(gen), generations))
        self.training_generation = self.generations[-1]
        self.show_info()

        self.statusBar().showMessage("File loaded")

    def saveEvent(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "","Neural Network Files (*.nn)", options=options)
        if file_name:
            t = threading.Thread(target=self.save, args=(file_name,))
            t.start()
        else:
            self.statusBar().showMessage("Save cancelled")

    def loadEvent(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Neural Network Files (*.nn)", options=options)
        if file_name:
            t = threading.Thread(target=self.load, args=(file_name,))
            t.start()
        else:
            print("Load cancelled")

    def closeEvent(self, event):
        sys.exit(0)

    def show_info(self):
        generation = self.current_generation
        gen_number = 0 if generation is None else generation.generation_number
        self.lbl_gen.setText('Generation: #' + str(gen_number))

        population = 0 if generation is None else generation.number()
        self.lbl_specimen.setText('Population: ' + str(population))

        best_fitness = 0 if generation is None else generation.max_fitness()
        best_specimen = 0 if generation is None else generation.max_specimen()
        self.lbl_max_fitness.setText('Maximum fitness: ' + str(best_fitness) + ' specimen: #' + str(best_specimen))

        avg_fitness = 0 if generation is None else generation.avg()
        self.lbl_med_fitness.setText('Median fitness: ' + str(avg_fitness))

        self.lbl_status.setText('Status: ' + self.status)

    def test_1_generation(self):
        self.status = 'Training'
        self.show_info()

        self.training_generation.train(self.on_train)

        self.status = 'Done'
        self.show_info()

    def test_10_generation(self):
        for i in range(10):
            new_gen = self.training_generation.next_generation(self.on_train)
            self.training_generation = new_gen
            self.generations.append(new_gen)
            self.slider.setMaximum(len(self.generations) - 1)
            self.slider.setValue(len(self.generations) - 1)
            self.show_info()

    def on_train(self, model):
        self.show_info()

    def kill(self):
        self.training_generation.kill()
        self.show_info()

    def reproduce(self):
        new_gen = self.training_generation.reproduce()
        self.training_generation = new_gen
        self.generations.append(new_gen)
        self.update_slider()
        self.show_info()

    def initPopulation(self):
        self.training_generation = Generation()
        self.current_generation = self.training_generation
        self.generations.append(self.training_generation)
        self.update_slider()
        self.show_info()

    def showPopulation(self):
        self.population_window = PopulationWindow()
        self.population_window.set_population(self.current_generation.population)
        self.population_window.show()

    training = False

    def train(self):
        self.training = True
        self.statusBar().showMessage("Training...")
        while self.training:
            new_gen = self.training_generation.next_generation(self.on_train)
            self.training_generation = new_gen
            self.generations.append(new_gen)
            self.update_slider()
            self.show_info()
        self.statusBar().showMessage("Training stopped")

    def update_slider(self):
        self.slider.setMaximum(len(self.generations) - 1)
        if self.slider.value() == len(self.generations) - 2:
            self.slider.setValue(len(self.generations) - 1)
            self.current_generation = self.generations[-1]

    def stop(self):
        self.training = False
        self.statusBar().showMessage("Will stop after this generation")

    def buttonClicked(self):
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
