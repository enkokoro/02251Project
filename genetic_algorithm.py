from random import random

# Roulette wheel based selection
def selection(population, fitnessScores, size):
    totalFitness = sum(fitnessScores)
    relFitness = [f/totalFitness for f in fitnessScores]
    prob = [sum(relFitness[:i+1]) for i in range(len(relFitness))] 
    nextGen = []
    for i in range(size):
        cutoff = random
        for j in range(len(population)):
            if cutoff <= prob[j]:
                nextGen.append([population[j]])
                break
    return nextGen

def geneticAlgorithm (input, crossover, crossoverRate, mutate, mutationRate, fitness, numGenerations):
    population = [input]
    fitnessScores = [fitness(p) for p in population]
    for _ in range(numGenerations):
        # Select parents
        parents = selection(population, fitnessScores, )

        # Recombine
        nextGen = []
        lenParents = len(parents)
        for i in range(0, lenParents, 2):
            p1 = parents[i]
            # Handle last step when parents len is odd
            if (lenParents <= i + 1):
                p2 = parents[i]
            else:
                p2 = parents[i + 1]
            if random() < crossoverRate:
                nextGen.append([crossover(p1, p2)])
            else:
                nextGen.append([p1, p2])

        # Mutate
        for p in nextGen:
            if random() < mutationRate:
                mutate(p)
        
        # Update population and recalculate fitness
        population = nextGen
        fitnessScores = [fitness(solution) for solution in population]

    # Return fittest member of the population
    best = max(fitnessScores)
    bestIndex = fitnessScores.index(best)
    return population[bestIndex]