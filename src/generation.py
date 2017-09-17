from population import Population
from tester import Tester


class Generation:
    population = None

    best_specimen = None
    best_fitness = -9999999999

    avg_fitness = 0

    generation_number = 0

    trained = False

    def __init__(self, population=None, generation_number=0):
        if population is None:
            population = Population(300)

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

    def train(self, cb=None):
        total = 0
        for i in range(self.population.max_population):
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

            if cb is not None:
                cb(model)

        self.avg_fitness = total / self.population.max_population
        self.trained = True

    def number(self):
        return self.population.population()

    def next_generation(self, cb=None):
        self.train(cb)
        self.kill()

        gen = self.reproduce()
        return gen

    def kill(self):
        self.population.kill(0.75)

    def reproduce(self):
        return Generation(population=self.population.reproduce(self.generation_number + 1),
                          generation_number=self.generation_number + 1)

    def to_hash(self):
        print("Dumping generation #" + str(self.generation_number) + " to hash")
        return {
            "p": self.population.to_hash(),
            "b": self.best_fitness,
            "a": self.avg_fitness,
            "g": self.generation_number,
            "t": self.trained
        }

    @staticmethod
    def from_hash(h):
        population = Population.from_hash(h["p"])
        generation_number = h["g"]
        gen = Generation(population=population, generation_number=generation_number)

        gen.best_fitness = h["b"]
        gen.avg_fitness = h["a"]
        gen.trained = h["t"]

        for i in range(gen.population.max_population):
            model = gen.population.specimen(i)
            fitness = model.fitness
            if fitness > gen.best_fitness:
                gen.best_fitness = fitness
                gen.best_specimen = model

        return gen

