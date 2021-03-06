import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QMainWindow, QSlider,
                             QPushButton, QApplication, QAction, QFileDialog, QCheckBox)
from generation import Generation
from population_window import PopulationWindow
import simplejson as json
import marshal
import threading
from plot_canvas import PlotCanvas


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
    canvas = None
    slider = None

    chk_plot_best = None
    chk_plot_avg = None

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

        save_current_act = QAction('Save current &generation', self)
        save_current_act.setShortcut('Ctrl+G')
        save_current_act.setStatusTip('Save current generation')
        save_current_act.triggered.connect(self.saveCurrentGenerationEvent)

        load_act = QAction('&Load', self)
        load_act.setShortcut('Ctrl+O')
        load_act.setStatusTip('Load')
        load_act.triggered.connect(self.loadEvent)

        self.statusBar()

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(save_act)
        file_menu.addAction(save_current_act)
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

        self.chk_plot_best = QCheckBox("Best fitness")
        self.chk_plot_best.setChecked(True)
        self.chk_plot_best.stateChanged.connect(self.update_plot)
        grid.addWidget(self.chk_plot_best, 8, 1)

        self.chk_plot_avg = QCheckBox("Average fitness")
        self.chk_plot_avg.setChecked(True)
        self.chk_plot_avg.stateChanged.connect(self.update_plot)
        grid.addWidget(self.chk_plot_avg, 8, 2)

        self.canvas = PlotCanvas()
        grid.addWidget(self.canvas, 9, 1, 1, 3)

        self.show_info()

        self.move(100, 100)
        self.setWindowTitle('Training')
        self.show()

    def update_plot(self):
        self.plot()

    def changeGeneration(self):
        slider = self.sender()
        self.current_generation = self.generations[slider.value()]
        self.show_info()

    def save(self, file_name, generations, ref=True):
        self.statusBar().showMessage("Saving generations at: " + file_name)
        generations = list(map(lambda gen: gen.to_hash(ref=ref), generations))

        text = json.dumps(generations)
        print('Size: ' + str(len(text)))
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
        for i in range(len(generations)):
            generation = self.generations[i]
            for j in range(generation.population.max_population):
                model = generation.population.specimen(j)
                if isinstance(model, dict):
                    index = 0 if model["g"] - self.generations[0].generation_number < 0 else model["g"] - self.generations[0].generation_number

                    obj = self.generations[index].population.specimen(model["s"])

                    generation.population.set_specimen(j, obj)

            generation.set_best_fitness()

        self.training_generation = self.generations[-1]
        self.current_generation = self.generations[-1]

        # Update UI
        self.update_slider()
        self.show_info(plot=True)
        self.slider.setValue(len(self.generations) - 1)

        # self.statusBar().showMessage("File loaded")

    def saveEvent(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "Neural Network Files (*.nn)", options=options)
        if file_name:
            t = threading.Thread(target=self.save, args=(file_name, self.generations))
            t.start()
        else:
            self.statusBar().showMessage("Save cancelled")

    def saveCurrentGenerationEvent(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "Neural Network Files (*.nn)", options=options)
        if file_name:
            t = threading.Thread(target=self.save, args=(file_name, [self.current_generation], False))
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

    def plot(self):
        if self.canvas is None:
            return

        plots = []
        if self.chk_plot_best.isChecked():
            plots.append({
                "data": list(map(lambda gen: gen.best_fitness if gen.trained else None, self.generations))
            })

        if self.chk_plot_avg.isChecked():
            plots.append({
                "data": list(map(lambda gen: gen.avg_fitness if gen.trained else None, self.generations))
            })

        self.canvas.plot(plots)

    def show_info(self, plot=False):
        generation = self.current_generation
        gen_number = 0 if generation is None else generation.generation_number
        self.lbl_gen.setText('Generation: #' + str(gen_number))

        population = 0 if generation is None else generation.number()
        self.lbl_specimen.setText('Population: ' + str(population))

        best_fitness = 0 if generation is None else round(generation.max_fitness(), 3)
        best_specimen = 0 if generation is None else generation.max_specimen()
        self.lbl_max_fitness.setText('Best fitness: ' + str(best_fitness) + ' specimen: #' + str(best_specimen))

        avg_fitness = 0 if generation is None else round(generation.avg(), 3)
        self.lbl_med_fitness.setText('Average fitness: ' + str(avg_fitness))

        self.lbl_status.setText('Status: ' + self.status)

        if plot:
            self.plot()

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
            self.show_info(plot=True)

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
        self.show_info(plot=True)

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
            self.show_info(plot=True)
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
