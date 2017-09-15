from model import Model
from random import randint

METHOD_MUTATION = 0
METHOD_MATE = 1
METHOD_FREAK = 2


class Breeder:

    def __init__(self, population):
        self.population = population

    def breed_1st_gen(self):
        specimens = []
        for i in range(0, self.population.max_population):
            if i % 20 == 0:
                hidden_unit_num = Breeder.random_model_params()
                print("Breeding model of " + str(hidden_unit_num))

            model = Breeder.random_model(i, 0, hidden_unit_num=hidden_unit_num)
            specimens.append(model)

        return specimens

    def breed(self, gen):
        if gen == 0:
            return self.breed_1st_gen()

        specimens = []
        for i in range(0, self.population.max_population):
            model = self.population.specimen(i)
            if model.dead:
                print("Reproducing #" + str(gen) + "." + str(i))
                # model = self.init_model(i, next_gen)
            specimens.append(model)

        return specimens

    @staticmethod
    def random_model_params():
        layer_number = randint(3, 10)
        hidden_unit_num = []
        for i in range(layer_number - 1):
            hidden_unit_num.append(randint(5, 300))

        hidden_unit_num.append(4)
        return tuple(hidden_unit_num)

    @staticmethod
    def random_model(specimen, gen, hidden_unit_num=None):
        model = Model(hidden_unit_num=hidden_unit_num)
        model.generation = gen
        model.specimen = specimen
        return model

    @staticmethod
    def random_bread_method():
        what = randint(1, 100)

        if what <= 45:
            return METHOD_MUTATION

        if 45 < what <= 90:
            return METHOD_MATE

        if 90 < what <= 100:
            return METHOD_FREAK
