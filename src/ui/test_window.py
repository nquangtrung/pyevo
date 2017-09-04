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
    {"filepath": "../images/track-01.png", "start_point": (110, 425)}
]


class TestWindow:
    model = None

    def __init__(self, model):
        self.model = model
        pygame.init()

    def test(self):
        model = self.model

        track_id = 1
        track = Track(tracks[track_id]["filepath"], tracks[track_id]["start_point"])
        car = Car()
        track.add_car(car)
        driver = NNDriver(model)
        driver.drive(car)
        s = time.time()
        finish = False
        while 1:
            diff = time.time() - s
            s = time.time()

            # Update and draw the new state of the car
            car.update(diff)

            # Check the game's logic
            car.check_hit(None)
            driver.see(None)
            finish = driver.control()

            if finish:
                model.fitness = driver.fitness
                break

        print("Final fitness: " + str(model.fitness))

    def show(self):
        model = self.model
        screen = pygame.display.set_mode((480, 480))

        track_id = 1
        track = Track(tracks[track_id]["filepath"], tracks[track_id]["start_point"])
        car = Car()
        track.add_car(car)
        driver = NNDriver(model)
        driver.drive(car)
        s = time.time()

        finish = False
        while 1:
            diff = time.time() - s
            s = time.time()

            screen.fill(black)

            # Update and draw the new state of the car
            car.update(diff)
            car.draw(screen, red, green)

            # Check the game's logic
            car.check_hit(screen)
            driver.see(screen)
            finish = driver.control()

            myfont = pygame.font.SysFont("monospace", 15)
            label = myfont.render("Generation #" + str(model.generation) + " Specimen #" + str(model.specimen), 1, (0, 255, 0))
            screen.blit(label, (0, 100))

            pygame.display.flip()

            if finish:
                break
