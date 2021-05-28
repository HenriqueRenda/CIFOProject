from random import uniform, sample
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    # Sum total fitnesses
    total_fitness = sum([i.score for i in population])
    # Get a 'position' on the wheel
    spin = uniform(0, total_fitness)
    position = 0
    # Find individual in the position of the spin
    for index, individual in enumerate(population):
        position += individual.score
        if position > spin:
            return index

def tournament(population, size=20):
    #Select individuals based on tournament size
    #print(population[0].score)
    tournament = sample(population, size)
    #Check if the problem is max or min
    maximo = max(tournament, key=attrgetter("score"))
    return population.index(maximo)


def rank(population):
    # Rank individuals based on optim approach
    population.sort(key=attrgetter('score'))
    # Sum all ranks
    total = sum(range(len(population)))
    # Get random position
    spin = uniform(0, total)
    position = 0
    # Iterate until spin is found
    for count, individual in enumerate(population):
        position += count + 1
        if position > spin:
            return count