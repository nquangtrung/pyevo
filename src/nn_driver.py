import tensorflow as td
import numpy as np
from human_driver import HumanDriver


class NNDriver(HumanDriver):
    model = None

    def __init__(self, model):
        self.model = model

    def control(self):
        output = self.model.forward_prop(self.environment) > 0.5
        if output[0]:
            self.car.steer(15)
        if output[1]:
            self.car.steer(-15)
        if output[2]:
            self.car.accelerate()
        if output[3]:
            self.car.decelerate()

        if self.time > self.limit > 0 or self.is_hit:
            return True
        else:
            return super(NNDriver, self).control()
