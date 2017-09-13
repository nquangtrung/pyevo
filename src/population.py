from model import Model


class Population:
    specimens = []
    max_population = 0

    def __init__(self, max_population=300, specimens=None):
        if specimens is None:
            self.max_population = max_population
            for i in range(0, max_population):
                model = self.init_model(i)
                self.specimens.append(model)
            return

        self.specimens = specimens
        self.max_population = len(specimens)

    def init_model(self, specimen, gen=0):
        model = Model()
        model.generation = gen
        model.specimen = specimen
        return model

    def specimen(self, index):
        return self.specimens[index]

    def kill(self, ratio):
        s = sorted(self.specimens, key=lambda x: x.fitness)
        print("We will kill " + str(int(self.max_population * ratio)) + " specimens")
        for i in range(self.max_population):
            model = s[i]
            print("Specimen " + str(model.specimen) + " fitness: " + str(model.fitness))

        for i in range(int(self.max_population * ratio)):
            model = s[i]
            print('Kill ' + str(model.specimen) + ' fitness: ' + str(model.fitness))
            s[i].dead = True

    def reproduce(self, next_gen):
        specimens = []
        for i in range(0, self.population()):
            model = self.specimen(i)
            if model.dead:
                model = self.init_model(i, next_gen)
            specimens.append(model)

        return Population(specimens)

    def population(self):
        return sum(map(lambda model: 0 if model.dead else 1, self.specimens))

    def is_fill(self):
        return self.population() == self.max_population
