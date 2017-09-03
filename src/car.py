import sys, pygame
import numpy as np


class Car:

    width = 10
    length = 20
    velocity = 50
    steering = 0
    running = False
    hit = False
    position = (0, 0)
    driver = None
    track = None

    def __init__(self):
        pass

    def accelerate(self):
        self.velocity += 5

    def decelerate(self):
        self.velocity -= 5

    def driven_by(self, driver):
        self.driver = driver
        self.running = True

    def steer(self, deg):
        self.steering += deg

    def update(self, time):
        len = self.velocity * time
        if not self.running:
            len = 0

        theta = self.steering * np.pi / 180

        len_y = np.cos(theta) * len
        len_x = np.sin(theta) * len
        self.position = (self.position[0] - len_x, self.position[1] - len_y)

        self.driver.moved(len, time)

    def check_hit(self, screen):
        x = screen.get_width() / 2
        y = screen.get_height() / 2

        hit = False
        # Check if hit
        for dx in range(int(-self.width / 2), int(self.width / 2) + 1, 2):
            for dy in range(int(-self.length / 2), int(self.length / 2) + 1, 2):
                pos_x = int(self.position[0]) + dx
                pos_y = int(self.position[1]) + dy
                terrain = self.track.height(self.rotate_corner(self.position[0], self.position[1], pos_x, pos_y))

                if terrain > 0:
                    hit = True
                    color = 255, 0, 0
                else:
                    color = 0, 255, 0

                pos = self.rotate_corner(x, y, x + dx, y + dy)
                pygame.draw.circle(screen, color, pos, 1, 1)
        if hit:
            self.hit = True
            self.running = False
            self.driver.hit()

    def set_position(self, track, position):
        self.position = position
        self.track = track

    def rotate(self):
        pass

    def rotate_corner(self, cx, cy, x, y):
        temp_x = x - cx
        temp_y = y - cy

        theta = -self.steering * np.pi / 180
        rotated_x = temp_x * np.cos(theta) - temp_y * np.sin(theta)
        rotated_y = temp_x * np.sin(theta) + temp_y * np.cos(theta)

        # translate back
        x = rotated_x + cx
        y = rotated_y + cy

        return int(x), int(y)

    def draw(self, screen, color, head_color):
        x = screen.get_width() / 2
        y = screen.get_height() / 2

        trackrect = self.track.find_rect(x, y, self.position)
        screen.blit(self.track.track, trackrect)

        top_left = self.rotate_corner(x, y, x - self.width / 2, y - self.length / 2)
        top_right = self.rotate_corner(x, y, x + self.width / 2, y - self.length / 2)
        bot_left = self.rotate_corner(x, y, x - self.width / 2, y + self.length / 2)
        bot_right = self.rotate_corner(x, y, x + self.width / 2, y + self.length / 2)

        # pygame.draw.lines(screen, color, True, [top_left, top_right, bot_right, bot_left], 1)
        pygame.draw.line(screen, head_color, top_left, top_right, 1)
        pygame.draw.line(screen, color, top_right, bot_right, 1)
        pygame.draw.line(screen, color, bot_right, bot_left, 1)
        pygame.draw.line(screen, color, top_left, bot_left, 1)

        # render text
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("Speed: " + str(self.velocity), 1, (255, 255, 0))
        screen.blit(label, (0, 0))
        label = myfont.render("Steering: " + str(self.steering), 1, (255, 255, 0))
        screen.blit(label, (0, 20))
