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
    {"filepath": "../images/track-00.png", "start_point": (100, 440)},
    {"filepath": "../images/track-01.png", "start_point": (110, 425)},
    {"filepath": "../images/track-02.png", "start_point": (90, 455)}
]


class Tester:
    model = None
    testing = False

    def __init__(self, model):
        self.model = model
        pygame.init()

    def stop(self):
        self.testing = False

    def test(self):
        if self.model.trained:
            # Now the result is consistent, we don't need to re-train everything
            return self.model.fitness, self.model.time

        return self.execute(show=False, interval=0.1)

    def show(self, window=None):
        self.execute(show=True, window=window, interval=0.1)

    def execute(self, show=True, interval=0, window=None):
        self.testing = True

        model = self.model
        if show:
            screen = pygame.Surface((640, 480))
            window.surface(screen)
            window.loop(self)
        else:
            screen = None

        track_id = 2
        track = Track(tracks[track_id]["filepath"], tracks[track_id]["start_point"])
        car = Car()
        track.add_car(car)
        driver = NNDriver(model)
        driver.drive(car)
        s = time.time()

        finish = False
        while self.testing:
            diff = time.time() - s
            s = time.time()
            if show:
                screen.fill(black)

            diff = interval if interval > 0 else diff
            # Update and draw the new state of the car
            car.update(diff)
            if show:
                car.draw(screen, red, green)

            # Check the game's logic
            car.check_hit(screen)
            driver.see(screen)
            finish = driver.control()

            if show:
                myfont = pygame.font.SysFont("monospace", 15)
                label = myfont.render("Generation #" + str(model.generation) + " Specimen #" + str(model.specimen), 1, (0, 255, 0))
                screen.blit(label, (0, 100))
                window.update()
                # pygame.display.flip()

            if finish:
                model.fitness = driver.fitness
                model.time = driver.time
                if not show:
                    model.trained = True

                break

        return driver.fitness, model.time
