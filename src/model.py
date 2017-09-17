import tensorflow as td
import numpy as np
import json


class Model:
    input_shape = None
    hidden_unit_num = None
    params = None
    fitness = 0
    time = 0
    generation = 0
    specimen = 0
    layer_num = 0
    dead = False
    trained = False
    children = []
    parent = None

    def __init__(self, input_shape=(1056, 1), hidden_unit_num=(10, 5, 4), params=None, model=None):
        if model is None:
            self.input_shape = input_shape
            self.hidden_unit_num = hidden_unit_num
            self.layer_num = len(hidden_unit_num)
            if params is None:
                self.params = Model.initialize_nn(self.input_shape, self.hidden_unit_num)
            else:
                self.params = params
            return

        # Copy the model here
        self.input_shape = model.input_shape
        self.hidden_unit_num = model.hidden_unit_num
        self.layer_num = model.layer_num
        self.params = {}
        for key, value in model.params.items():
            self.params[key] = value.copy()

        # Initiate hierarchy
        self.parent = model
        model.children.append(self)

    def forward_prop(self, inp):
        a_prev = inp
        for l in range(1, self.layer_num):
            z = np.dot(self.params["W" + str(l - 1)], a_prev) + self.params["b" + str(l - 1)]
            a = Model.relu(z)
            a_prev = a

        z = np.dot(self.params["W" + str(l)], a_prev) + self.params["b" + str(l)]
        y = Model.sigmoid(z)

        return y

    def kill(self):
        self.dead = True
        del self.__dict__["params"]

    def save(self, gen, specimen):
        json_params = {}
        for l in range(self.layer_num):
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

    def to_hash(self):
        json_params = {}
        if not self.dead:
            for l in range(self.layer_num):
                json_params["W" + str(l)] = self.params["W" + str(l)].tolist()
                json_params["b" + str(l)] = self.params["b" + str(l)].tolist()

        return {
            # NN info
            "i": self.input_shape,
            "l": self.layer_num,
            "h": self.hidden_unit_num,
            "p": json_params,

            # Model's train status
            "f": self.fitness,
            "t": self.time,
            "d": self.dead,
            "tr": self.trained,

            # Generation info
            "g": self.generation,
            "s": self.specimen
        }

    @staticmethod
    def from_hash(h):
        layer_num = h['l']
        params = {}
        if not h["d"]:
            for l in range(layer_num):
                params["W" + str(l)] = np.array(h["p"]["W" + str(l)])
                params["b" + str(l)] = np.array(h["p"]["b" + str(l)])

        model = Model(input_shape=tuple(h["i"]), hidden_unit_num=h['h'], params=params)

        # Model's train status
        model.fitness = h["f"]
        model.time = h["t"]
        model.dead = h["d"]
        model.trained = h["tr"]

        # Generation info
        model.generation = h["g"]
        model.specimen = h["s"]

        return model

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
    def initialize_nn(input_shape, hidden_unit_num):
        layer_num = len(hidden_unit_num)
        n_l_prev = input_shape[0]

        params = {}
        for i in range(0, layer_num):
            n_l = hidden_unit_num[i]
            p = Model.initialize_layer(n_l_prev, n_l)
            params["W" + str(i)] = p["w"]
            params["b" + str(i)] = p["b"]
            n_l_prev = hidden_unit_num[i]

        return params