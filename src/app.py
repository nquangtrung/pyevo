import sys, pygame
from track import Track
from car import Car
from nn_driver import NNDriver
from model import Model
import time
import numpy as np

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkBlue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
pink = (255, 200, 200)


pygame.init()

size = width, height = 480, 480

tracks = [
    {"filepath": "images/track-00.png", "start_point": (100, 440)},
    {"filepath": "images/track-01.png", "start_point": (110, 425)}
]

population = []
for i in range(0, 20):
    population.append(Model())
    model = Model()
    model.generation = 0

for gen in range(0, 100):
    for specimen in range(0, len(population)):
        sum_fitness = 0
        retry = 5
        for test in range(0, retry):
            screen = pygame.display.set_mode(size)

            track_id = 1
            track = Track(tracks[track_id]["filepath"], tracks[track_id]["start_point"])
            car = Car()
            track.add_car(car)
            driver = NNDriver(population[specimen])
            driver.drive(car)
            s = time.time()

            finish = False
            while 1:
                diff = time.time() - s
                s = time.time()

                if diff < 1. / 30.:
                    # print('sleep', str(1. / 30. - diff))
                    time.sleep(1. / 30. - diff)

                screen.fill(black)

                # Update and draw the new state of the car
                car.update(diff)
                car.draw(screen, red, green)

                # Check the game's logic
                car.check_hit(screen)
                driver.see(screen)
                finish = driver.control()

                myfont = pygame.font.SysFont("monospace", 15)
                label = myfont.render("Generation #" + str(gen) + " specimen #" + str(specimen) + " retry #" + str(test), 1, (0, 255, 0))
                screen.blit(label, (0, 100))
                label = myfont.render("Model survive from #" + str(population[specimen].generation), 1, (0, 255, 0))
                screen.blit(label, (0, 120))

                pygame.display.flip()

                if finish:
                    break
            sum_fitness += driver.fitness

        population[specimen].fitness = sum_fitness / retry
        population[specimen].save(gen, specimen)
        print("Final fitness: gen #" + str(gen) + " specie #" + str(specimen) + " : " + str(population[specimen].fitness))

    # Finish 1 generation
    print("Finished: gen #" + str(gen))

    # Order the population from best to worst
    population = sorted(population, key=lambda x: x.fitness, reverse=True)
    sum = 0
    for i in range(0, len(population)):
        # print("Generation #" + str(gen) + ": Specimen: #" + str(i) + ": " + str(population[i].fitness))
        sum += population[i].fitness
    print("Generation #" + str(gen) + ": " + str(sum))

    mid = len(population) / 4
    for i in range(0, len(population)):
        if i > mid:
            # print("Kill off specimen #" + str(i))
            # print("Produce new specimen randomly #" + str(i))
            population[i] = Model()
            population[i].generation = gen + 1
