import sys
import pygame
import numpy as np


class HumanDriver:
    fitness = 0
    max_fitness = 0
    car = None
    time_penalty = 10
    time = 0
    is_hit = False
    environment = None
    limit = 10

    def __init__(self):
        pass

    def drive(self, car):
        car.driven_by(self)
        self.car = car

    def moved(self, length, time):
        self.time += time
        self.fitness += length - self.time_penalty * time

    def set_limit(self, limit):
        self.limit = limit

    def see(self, screen):
        red = 255, 0, 0

        self.environment = np.zeros((1056, 1))
        count = 0
        for R in range(0, 200, 10):
            for alpha in range(0, 180, int(R / 20) + 1):
                dy = int(R * np.sin((alpha + self.car.steering) * np.pi / 180))
                dx = int(R * np.cos((alpha + self.car.steering) * np.pi / 180))

                terrain = self.car.track.height((int(self.car.position[0]) + dx, int(self.car.position[1]) - dy))
                self.environment[count] = terrain
                count += 1

                if screen is not None:
                    if terrain > 0:
                        color = red
                        x = int(screen.get_width() / 2)
                        y = int(screen.get_height() / 2)
                        pygame.draw.circle(screen, color, (x + dx, y - dy), 5, 3)

    def hit(self):
        self.is_hit = True

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == 276:
                    self.car.steer(15)
                elif event.key == 275:
                    self.car.steer(-15)
                elif event.key == 273:
                    self.car.accelerate()
                elif event.key == 274:
                    self.car.decelerate()
            elif event.type == pygame.KEYUP:
                pass

        return False
