from random import random
from copy import copy
import matplotlib.pyplot as plt

# Roulette wheel based selection
def selection(population, fitnessScores):
    assert len(fitnessScores) == len(population)

    # maxFitness = max(fitnessScores)
    fit = fitnessScores
    fitnessScores = [1/f for f in fitnessScores]  # do this to minimize fitness
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
    # if (len(population) != len(selected)):
    #     print(population, "\n", fitnessScores, "\n", fit, "\n", selected)
    #     print(len(population), len(selected))
    assert len(population) == len(selected)
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
                nextGen.extend(crossover(p1, p2))
            else:
                nextGen.extend([p1, p2])

    assert len(parents) == len(nextGen)
    return nextGen

def mutation(nextGen, mutate, mutationRate):
    population = []
    for p in nextGen:
        if random() <= mutationRate:
            population.append(mutate(p))
        else:
            population.append(p)
            
    assert len(nextGen) == len(population)
    return population

def findBest(fitnessScores, population):
    assert len(fitnessScores) == len(population)

    best = min(fitnessScores)
    bestIndex = fitnessScores.index(best)
    return (population[bestIndex], best)


def geneticAlgorithm(population, crossover, crossoverRate, mutate, mutationRate, fitness, numGenerations):
    assert type(population) == list
    assert 0 <= crossoverRate and crossoverRate <= 1.0
    assert 0 <= mutationRate and mutationRate <= 1.0
    assert 0 <= numGenerations

    historyBest = []
    historyWorst = []
    historyAve = []
    fitnessScores = [fitness(p) for p in population]
    eliteCount = max(len(population) // 20, 1)

    for i in range(numGenerations):
        # Save history of solutions at the start of each generation
        historyBest.append(findBest(fitnessScores, population))
        historyAve.append(sum(fitnessScores)/len(fitnessScores))
        historyWorst.append(max(fitnessScores))

        # Save "elites"
        tmp = sorted(enumerate(fitnessScores), key=lambda x: x[1])[:eliteCount]
        elites = [population[i] for (i,f) in tmp]
        lenBefore = len(population)
        # tmpPop = copy(population)
        # for e in elites: 
        #     i = population.index(e)
        #     population.pop(i)
        #     fitnessScores.pop(i)
        # assert len(elites) + len(population) == lenBefore
        assert len(elites) == eliteCount
        # assert set(elites + population) == set(tmpPop)
        # print (elites, population)

        # Select parents
        parents = selection(population, fitnessScores)

        # Recombine
        nextGen = recombination(parents, crossover, crossoverRate)

        # Mutate
        population = mutation(nextGen, mutate, mutationRate)

        # remove worst and add in elites if elites were removed
        for e in elites:
            i = fitnessScores.index(max(fitnessScores))
            fitnessScores.pop(i)
            population.pop(i)
            population.append(e)
            fitnessScores.append(fitness(e))
                
        
        # Recalculate fitness
        fitnessScores = [fitness(p) for p in population]

    # Save history of solutions at the last generation
    historyBest.append(findBest(fitnessScores, population))
    historyAve.append(sum(fitnessScores)/len(fitnessScores))
    historyWorst.append(max(fitnessScores))

    # Return fittest member of the population along with additional data
    solution = historyBest[-1][0]
    return solution, historyBest, historyAve, historyWorst


def printGA(bestTuples, avg, worst, filename):
    fig, ax1 = plt.subplots()
    bestColor = 'green'
    avgColor = 'blue'
    # worstColor = 'red'

    best = [f for (s,f) in bestTuples]
    solutions = [s for (s,f) in bestTuples]

    ax1.set_xlabel('Generations')
    ax1.set_ylabel('Fitness')
    plt.yscale("log")
    ax1.plot(best, color=bestColor, label='Best fitness')
    ax1.plot(avg, color=avgColor, label='Average fitness')
    # ax1.plot(worst, color=worstColor, label='Worst fitness')
    fig.legend()
    ax1.tick_params(axis='y')

    fig.tight_layout()
    fig.savefig(filename)


    print("Final Solution: ", solutions[-1], " Fitness: ", best[-1])
    print("Best Solution: ", solutions[best.index(min(best))], " Fitness: ", min(best))