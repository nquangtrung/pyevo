import sys, pygame
import cv2
import numpy as np

class Track:
    car = None
    start_point = (0, 0)

    def __init__(self, filepath, start_point):
        self.start_point = start_point
        self.track = pygame.image.load(filepath)
        self.img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

    def height(self, position):
        shape = self.img.shape
        if position[0] < 0 or position[1] < 0 or position[0] >= shape[1] or position[1] >= shape[0]:
            return 0
        return self.img[(position[1], position[0])]

    def get_starting_point(self):
        return self.start_point

    def add_car(self, car):
        self.car = car
        car.set_position(self, self.get_starting_point())

    def find_rect(self, x, y, point):
        rect = self.track.get_rect()
        rect.left = x - point[0]
        rect.top = y - point[1]
        return rect
