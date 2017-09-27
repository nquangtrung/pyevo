from PyQt5.QtWidgets import (QSizePolicy, QWidget, QGridLayout, QPushButton, QLabel, QComboBox)
from pygame_widget import PygameWidget
from PyQt5.QtCore import Qt


class TesterWindow(QWidget):
    surface = None
    image = None
    looper = None
    combo_box = None
    grid = None

    tester = None

    lbl_model = None

    def __init__(self, parent=None):
        super().__init__()
        self.move(100, 100)
        self.resize(800, 500)
        self.setWindowTitle('Simulation')

        self.init_ui()

    def closeEvent(self, event):
        self.looper.stop()

    def loop(self, looper):
        self.looper = looper
        self.image.set_surface(looper.screen)

        tracks = self.looper.get_tracks()

        # Show combo box for selecting tracks
        self.combo_box = QComboBox(self)
        for i in range(len(tracks)):
            self.combo_box.addItem(tracks[i]["name"])
        self.combo_box.setCurrentIndex(self.looper.get_track_id())
        self.combo_box.activated[str].connect(self.on_track_chosen)
        self.grid.addWidget(self.combo_box, 1, 7)

    def on_track_chosen(self):
        self.looper.set_track_id(self.combo_box.currentIndex())
        self.looper.reset()

    def get_available_size(self):
        return self.image.width(), self.image.height()

    def init_ui(self):
        grid = QGridLayout()
        self.grid = grid
        self.setLayout(grid)

        self.image = PygameWidget()
        grid.addWidget(self.image, 2, 1, 1, 6)

        btn_start = QPushButton('Start')
        btn_start.clicked.connect(self.start)
        grid.addWidget(btn_start, 1, 1)

        btn_stop = QPushButton('Stop')
        btn_stop.clicked.connect(self.stop)
        grid.addWidget(btn_stop, 1, 2)

        btn_reset = QPushButton('Reset')
        btn_reset.clicked.connect(self.reset)
        grid.addWidget(btn_reset, 1, 3)

        btn_run = QPushButton('Run')
        btn_run.clicked.connect(self.run)
        grid.addWidget(btn_run, 1, 4)

        btn_kill = QPushButton('Kill')
        btn_kill.clicked.connect(self.kill)
        grid.addWidget(btn_kill, 1, 5)

        btn_resurrect = QPushButton('Resurrect')
        btn_resurrect.clicked.connect(self.resurrect)
        grid.addWidget(btn_resurrect, 1, 6)

        btn_show_train = QPushButton('Show Train')
        btn_show_train.clicked.connect(self.show_train)
        grid.addWidget(btn_show_train, 1, 6)

        self.lbl_model = QLabel('')
        grid.addWidget(self.lbl_model, 2, 7, 1, 1, Qt.AlignTop)

        self.show_info()

    def show_info(self):
        if self.looper is None:
            return

        text = ''
        text += 'Model: \n'
        text += '+ Generation: ' + str(self.looper.model.generation) + '\n'
        text += '+ Specimen: ' + str(self.looper.model.specimen) + '\n'
        text += '+ Dead: ' + str(self.looper.model.dead) + '\n'
        text += '+ Fitness: ' + str(round(self.looper.model.fitness, 3)) + '\n'
        text += '+ Time: ' + str(round(self.looper.model.time, 3)) + '\n'
        text += '+ Gene: ' + str(self.looper.model.layer_num) + '\n'
        text += str(self.looper.model.hidden_unit_num) + '\n'

        text += 'Driver: \n'
        text += '+ Fitness: ' + str(round(self.looper.driver.fitness, 3)) + '\n'
        text += '+ Time: ' + str(round(self.looper.driver.time, 3)) + '\n'
        text += '+ Hit: ' + str(self.looper.driver.is_hit) + '\n'

        text += 'Car: \n'
        text += '+ Speed: ' + str(self.looper.car.velocity) + '\n'
        text += '+ Steering: ' + str(self.looper.car.steering) + '\n'

        self.lbl_model.setText(text)
        self.lbl_model.setFixedSize(150, 210)

    def on_update(self):
        self.show_info()

    def kill(self):
        self.looper.model.dead = True
        self.show_info()

    def resurrect(self):
        self.looper.model.dead = False
        self.show_info()

    def run(self):
        self.looper.reset()
        self.looper.run(on_update=self.on_update)

    def reset(self):
        self.looper.reset()
        self.show_info()

    def show_train(self):
        self.looper.reset()
        self.looper.show_train(on_update=self.on_update)

    def start(self):
        self.looper.reset()
        self.looper.show(on_update=self.on_update)

    def stop(self):
        self.looper.stop()
        self.show_info()

    def update(self):
        self.image.update()
