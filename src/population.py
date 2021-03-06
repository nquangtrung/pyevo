from model import Model
from breeder import Breeder


class Population:
    specimens = []
    max_population = 0

    breeder = None

    def __init__(self, max_population=300, specimens=None):
        self.breeder = Breeder(self)
        if specimens is None:
            self.max_population = max_population
            self.specimens = self.breeder.breed_1st_gen()
            return

        self.specimens = specimens
        self.max_population = len(specimens)

    def set_specimen(self, index, specimen):
        self.specimens[index] = specimen

    def specimen(self, index):
        return self.specimens[index]

    def kill(self, ratio):
        s = sorted(self.specimens, key=lambda x: x.fitness)
        print("We will kill " + str(int(self.max_population * ratio)) + " specimens")
        for i in range(int(self.max_population * ratio)):
            model = s[i]
            print('Kill ' + str(model.specimen) + ' fitness: ' + str(round(model.fitness, 3)))
            s[i].dead = True

    def reproduce(self, next_gen):
        specimens = self.breeder.breed(next_gen)
        return Population(specimens=specimens)

    def population(self):
        return sum(map(lambda model: 0 if model.dead else 1, self.specimens))

    def is_fill(self):
        return self.population() == self.max_population

    def to_hash(self, ref=True, generation=0):
        models = list(map(lambda model: model.to_hash(ref=ref, generation=generation), self.specimens))

        return {
            "p": self.max_population,
            "m": models
        }

    @staticmethod
    def from_hash(h):
        specimens = []
        for i in range(len(h["m"])):
            specimens.append(Model.from_hash(h["m"][i]))

        return Population(specimens=specimens)

