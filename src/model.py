import tensorflow as td
import numpy as np
import json

class Model:
    input_shape = (1800, 1)
    layer_num = 3
    hidden_unit_num = (10, 5, 4)
    params = None
    fitness = 0
    generation = 0

    def __init__(self):
        self.params = Model.initialize_nn(self.input_shape, self.layer_num, self.hidden_unit_num)

    def forward_prop(self, inp):
        a_prev = inp
        for l in range(1, self.layer_num):
            z = np.dot(self.params["W" + str(l - 1)], a_prev) + self.params["b" + str(l - 1)]
            a = Model.relu(z)
            a_prev = a

        z = np.dot(self.params["W" + str(l)], a_prev) + self.params["b" + str(l)]
        y = Model.sigmoid(z)

        return y

    def save(self, gen, specimen):
        json_params = {};
        for l in range(0, self.layer_num):
            json_params["W" + str(l)] = self.params["W" + str(l)].tolist()
            json_params["b" + str(l)] = self.params["b" + str(l)].tolist()

        text = json.dumps({
            "input_shape": self.input_shape,
            "layer_num": self.layer_num,
            "hidden_unit_num": self.hidden_unit_num,
            "fitness": self.fitness,
            "params": json_params
        }, separators=(',', ':'))
        text_file = open("model_" + str(gen) + "_" + str(specimen) + ".txt", "w")
        text_file.write(text)
        text_file.close()

    @staticmethod
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    @staticmethod
    def relu(z):
        return np.maximum(z, 0)

    @staticmethod
    def initialize_layer(n_x, n_y):
        w = np.random.randn(n_y, n_x)
        b = np.random.randn(n_y, 1)

        return {"w": w, "b": b}

    @staticmethod
    def initialize_nn(input_shape, layer_num, hidden_unit_num):
        n_l_prev = input_shape[0]

        params = {}
        for i in range(0, layer_num):
            n_l = hidden_unit_num[i]
            p = Model.initialize_layer(n_l_prev, n_l)
            params["W" + str(i)] = p["w"]
            params["b" + str(i)] = p["b"]
            n_l_prev = hidden_unit_num[i]

        return params