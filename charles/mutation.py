from random import randint, uniform, sample


def random_mutation(individual, mutation_rate):
    """[summary]

    Args:
        individual ([type]): [description]

    Returns:
        [type]: [description]
    """
    for i in range(len(individual)):
        if(uniform(0, 1)<mutation_rate):
            individual[i] = uniform(-1, 1)
    return individual


def binary_mutation(individual):
    """Binary muation for a GA individual

    Args:
        individual (Individual): A GA individual from charles libray.py

    Raises:
        Exception: When individual is not binary encoded.py

    Returns:
        Individual: Mutated Individual
    """
    mut_point = randint(0, len(individual) - 1)

    if individual[mut_point] == 0:
        individual[mut_point] = 1
    elif individual[mut_point] == 1:
        individual[mut_point] = 0
    else:
        raise Exception(
            f"Trying to do binary mutation on {individual}. But it's not binary."
        )

    return individual

def swap_mutation(individual):
    #Get two mutation points
    mut_points = sample(range(len(individual)),2)
    #Rename to shorthen variable name
    i = individual
    i[mut_points[0]], i[mut_points[1]] = i[mut_points[1]], i[mut_points[0]]
    

def inversion_mutation(individual):
    i = individual
    #position of the start and end of substring
    mut_points = sample(range(len(i)), 2)
    #This method assumes that the second point is after the first one
    #sort the list
    mut_points.sort()
    #Invert for the mutation
    i[mut_points[0]:mut_points[1]] = i[mut_points[0]:mut_points[1]][::-1]
    return i