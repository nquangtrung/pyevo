import sys, pygame
from track import Track
from car import Car
from nn_driver import NNDriver
from model import Model
import time

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkBlue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
pink = (255, 200, 200)

tracks = [
    {"name": "Track 1", "filepath": "../images/track-00.png", "start_point": (100, 440)},
    {"name": "Track 2", "filepath": "../images/track-01.png", "start_point": (110, 425)},
    {"name": "Track 3", "filepath": "../images/track-02.png", "start_point": (90, 455)}
]

INTERVAL = 0.03


class Tester:
    model = None
    testing = False
    screen = None
    window = None

    track = None
    car = None
    driver = None

    track_id = 2

    def __init__(self, model):
        self.model = model
        pygame.init()

    def stop(self):
        self.testing = False

    def test(self):
        if self.model.trained:
            # Now the result is consistent, we don't need to re-train everything
            return self.model.fitness, self.model.time

        return self.execute(show=False, interval=INTERVAL)

    def show_train(self, on_update=None):
        self.execute(show=True, on_update=on_update, train=False, interval=INTERVAL)

    def show(self, on_update=None):
        self.execute(show=True, on_update=on_update, train=False)

    def init(self, window):
        self.screen = pygame.Surface(window.get_available_size())
        self.screen.fill(black)

        self.window = window
        self.window.loop(self)
        self.window.update()

        self.init_car(self.model)
        self.frame(0, True, on_update=window.on_update)

    def run(self, show=True, interval=INTERVAL, on_update=None):
        self.execute(show=show, train=False, interval=interval, limit=0, on_update=on_update)

    def get_tracks(self):
        return tracks

    def get_track_id(self):
        return self.track_id

    def set_track_id(self, track_id):
        self.track_id = track_id

    def reset(self):
        self.stop()
        self.init_car(self.model)
        self.frame(0, True)

    def init_car(self, model):
        track_id = self.track_id
        self.track = Track(tracks[track_id]["filepath"], tracks[track_id]["start_point"])
        self.car = Car()
        self.track.add_car(self.car)
        self.driver = NNDriver(model)
        self.driver.drive(self.car)

    def frame(self, diff, show, on_update=None, train=True):
        screen = self.screen

        if show:
            screen.fill(black)

        # Update and draw the new state of the car
        self.car.update(diff)
        if show:
            self.car.draw(screen, red, green)

        # Check the game's logic
        self.car.check_hit(screen)
        self.driver.see(screen)
        finish = self.driver.control(forever=(not train))

        if show:
            self.window.update()

        if on_update is not None:
            on_update()

        return finish

    def execute(self, show=True, train=True, interval=0, limit=1, on_update=None):
        self.testing = True
        model = self.model

        if model.dead:
            return model.fitness, model.time

        if self.driver is None:
            self.init_car(self.model)

        self.driver.set_limit(limit)

        s = time.time()
        while self.testing:
            diff = time.time() - s
            s = time.time()
            diff = interval if interval > 0 else diff

            finish = self.frame(diff, show, on_update=on_update, train=train)

            if finish:
                if train:
                    model.fitness = self.driver.fitness
                    model.time = self.driver.time
                    model.trained = True

                break

        return self.driver.fitness, self.driver.time
