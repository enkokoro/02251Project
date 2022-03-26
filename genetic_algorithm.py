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

def geneticAlgorithm (input, crossover, crossoverRate, mutate, mutationRate, fittnessFun, numGenerations):
    population = [input]
    fitnessScores = [fittnessFun(solution) for solution in population]
    for _ in range(numGenerations):
        # Select parents
        parents = selection(population, fitnessScores, )
        # Recombine
        nextGen = []
        for i in range(0, len(parents), 2):
            if random() < crossoverRate:
                p1 = parents[i]
                p2 = parents[i+1]
                nextGen.append([crossover(p1, p2)])
        nextGen.append(parents)

        # Mutate
        for p in nextGen:
            if random() < mutationRate:
                mutate(p)
        
        # Add selected children to population and recalc fitnesses to fitness list
        population = nextGen
        fitnessScores = [fittnessFun(solution) for solution in population]

    # Return fittest member of the population
    best = max(fitnessScores)
    bestIndex = fitnessScores.index(best)
    return population[bestIndex]