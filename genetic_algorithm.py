from random import random

# Roulette wheel based selection
def selection(population, fitnessScores):
    totalFitness = sum(fitnessScores)
    relFitness = [f/totalFitness for f in fitnessScores]
    prob = [sum(relFitness[:i+1]) for i in range(len(relFitness))]
    randNums = [random() for _ in range(len(population))]
    selected = []

    for selectionNum in randNums:
        for i, cutoff in enumerate(prob):
            if selectionNum <= cutoff:
                selected.append(population[i])
                break

    return selected

def recombination(parents, crossover, crossoverRate):
    nextGen = []
    lenParents = len(parents)
    for i in range(0, lenParents, 2):
        p1 = parents[i]

        if (lenParents <= i + 1): # Odd number of parents
            nextGen.append(p1)
        else:
            p2 = parents[i + 1]
            if random() <= crossoverRate:
                nextGen.extend([crossover(p1, p2)])
            else:
                nextGen.extend([p1, p2])

def mutation(nextGen, mutate, mutationRate):
    population = []
    for p in nextGen:
        if random() <= mutationRate:
            population.append(mutate(p))
        else:
            population.append(p)



def geneticAlgorithm(input, crossover, crossoverRate, mutate, mutationRate, fitness, numGenerations):
    # TODO Assertion about input?
    assert 0 <= crossoverRate and crossoverRate <= 1.0
    assert 0 <= crossoverRate and crossoverRate <= 1.0
    assert 0 < numGenerations

    population = input
    fitnessScores = [fitness(p) for p in population]
    for _ in range(numGenerations):
        # Select parents
        parents = selection(population, fitnessScores)

        # Recombine
        nextGen = recombination(parents, crossover, crossoverRate)

        # Mutate
        population = mutation(nextGen, mutate, mutationRate)
        
        # Recalculate fitness
        fitnessScores = [fitness(p) for p in population]

    # Return fittest member of the population
    best = max(fitnessScores)
    bestIndex = fitnessScores.index(best)
    return population[bestIndex]