from population import Population
from tester import Tester


class Generation:
    population = None

    best_specimen = -1
    best_fitness = -9999999999

    avg_fitness = 0

    generation_number = 0

    def __init__(self, population=None, generation_number=0):
        if population is None:
            population = Population(300)

        self.generation_number = generation_number
        self.population = population

    def best(self):
        return self.best_specimen

    def avg(self):
        return self.avg_fitness

    def train(self):
        total = 0
        for i in range(self.population.population()):
            model = self.population.specimen(i)
            test = Tester(model)
            fitness, time = test.test()

            total += fitness
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_specimen = model

        self.avg_fitness = total / self.population.population()

    def number(self):
        return self.population.population()

    def next_generation(self):
        self.train()
        self.kill()

        gen = Generation(population=self.reproduce(), generation_number=self.generation_number + 1)
        return gen

    def kill(self):
        self.population.kill(0.75)

    def reproduce(self):
        return self.population.reproduce()
