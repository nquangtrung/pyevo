from population import Population
from tester import Tester


class Generation:
    population = None

    best_specimen = None
    best_fitness = -9999999999

    avg_fitness = 0

    generation_number = 0

    def __init__(self, population=None, generation_number=0):
        if population is None:
            population = Population(3)

        self.generation_number = generation_number
        self.population = population

    def best(self):
        return self.best_specimen

    def max_fitness(self):
        return 0 if self.best_specimen is None else self.best_specimen.fitness

    def max_specimen(self):
        return 0 if self.best_specimen is None else self.best_specimen.specimen

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

            print("Trained gen #" + str(self.generation_number)
                  + " specimen " + str(model.specimen)
                  + " fitness: " + str(model.fitness)
                  + " time: " + str(model.time))

        self.avg_fitness = total / self.population.population()

    def number(self):
        return self.population.population()

    def next_generation(self):
        self.train()
        self.kill()

        gen = self.reproduce()
        return gen

    def kill(self):
        self.population.kill(0.75)

    def reproduce(self):
        return Generation(population=self.population.reproduce(), generation_number=self.generation_number + 1)
