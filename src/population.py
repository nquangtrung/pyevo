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

    def specimen(self, index):
        return self.specimens[index]

    def kill(self, ratio):
        s = sorted(self.specimens, key=lambda x: x.fitness)
        print("We will kill " + str(int(self.max_population * ratio)) + " specimens")
        for i in range(int(self.max_population * ratio)):
            model = s[i]
            print('Kill ' + str(model.specimen) + ' fitness: ' + str(model.fitness))
            s[i].dead = True

    def reproduce(self, next_gen):
        specimens = self.breeder.breed(next_gen)
        return Population(specimens=specimens)

    def population(self):
        return sum(map(lambda model: 0 if model.dead else 1, self.specimens))

    def is_fill(self):
        return self.population() == self.max_population
