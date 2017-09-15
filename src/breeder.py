from model import Model
from random import randint
import numpy as np

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

    def pick_next_survival(self, itor):
        for i in range(0, self.population.max_population):
            real_itor = (i + itor) % self.population.max_population
            model = self.population.specimen(real_itor)
            if not model.dead:
                return (real_itor + 1) % self.population.max_population, model

    @staticmethod
    def mutate(model):
        # This will decide how easy it is to mutate the genome
        severity = Breeder.random_mutation_severity()
        print("Mutating with: #" + str(model.generation) + "." + str(model.specimen))
        print("With severity: " + str(severity))

        child = Model(model=model)
        for layer in range(child.layer_num):
            w = child.params["W" + str(layer)]
            b = child.params["b" + str(layer)]
            child.params["W" + str(layer)] = Breeder.mutate_matrix(w, severity)
            child.params["b" + str(layer)] = Breeder.mutate_matrix(b, severity)

        return child

    @staticmethod
    def mutate_matrix(m, severity):
        mutated = np.random.randn(m.shape[0], m.shape[1])
        affected = np.random.randint(1, high=100, size=m.shape, dtype=np.int32)

        return mutated * (affected < severity) + m * (affected > severity)

    def breed(self, gen):
        if gen == 0:
            return self.breed_1st_gen()

        specimens = []
        itor = 0
        for i in range(0, self.population.max_population):
            model = self.population.specimen(i)
            if model.dead:
                breed_method = Breeder.random_breed_method()
                method_name = "METHOD_MUTATION" if breed_method == METHOD_MUTATION else "METHOD_MATE" if breed_method == METHOD_MATE else "METHOD_FREAK"
                print("Breeding #" + str(gen) + "." + str(i) + " with method " + method_name)

                itor, survived = self.pick_next_survival(itor)
                if breed_method == METHOD_MUTATION:
                    model = Breeder.mutate(survived)
                    model.generation = gen
                    model.specimen = i
                elif breed_method == METHOD_MATE:
                    pass
                elif breed_method == METHOD_FREAK:
                    # We look for a specie and breed another model so we can have better chance of mating in the future
                    hidden_unit_num = survived.hidden_unit_num
                    print("Breeding with gene: " + str(hidden_unit_num))
                    model = Breeder.random_model(i, gen=gen, hidden_unit_num=hidden_unit_num)
                    pass

            specimens.append(model)

        return specimens

    @staticmethod
    def random_mutation_severity():
        return randint(10, 90)

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
    def random_breed_method():
        what = randint(1, 100)
        if what <= 80:
            return METHOD_MUTATION

        if 80 < what <= 100:
            return METHOD_FREAK
