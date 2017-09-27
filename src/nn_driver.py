import tensorflow as td
import numpy as np
from human_driver import HumanDriver


class NNDriver(HumanDriver):
    model = None

    current_limit = 0
    current_limit_threshold = 0
    limit = 0

    def __init__(self, model):
        self.model = model

    def set_limit(self, limit):
        self.limit = limit
        self.current_limit = limit

    def control(self, forever=False):
        output = self.model.forward_prop(self.environment) > 0.5
        if output[0]:
            self.car.steer(15)
        if output[1]:
            self.car.steer(-15)
        if output[2]:
            self.car.accelerate()
        if output[3]:
            self.car.decelerate()

        if self.time > 30 and not forever:
            # It's enough for training
            return True

        if self.time > self.current_limit > 0 or self.is_hit:
            if self.fitness < self.current_limit_threshold:
                return True
            else:
                self.current_limit = self.current_limit + self.limit
                self.current_limit_threshold = self.fitness
                return False
        else:
            return super(NNDriver, self).control()
