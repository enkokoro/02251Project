from algorithms.genetic_algorithm import *
import random
import numpy as np

maxValue = 2047
inputs = random.sample(range(0, maxValue), maxValue//10)
crossoverRate = 0.7
mutationRate = 0.032
numGenerations = maxValue//10
# numGenerations = 1000

def fitness(p):
    return p**2 + 0.001

def mutate(p):
    # b = bin(p)[2:]
    b = format(p, '011b')
    numMutations = random.randint(0,2)
    for i in range(numMutations):
        index = random.randint(0,len(b) - 1)
        new = '0' if b[index] == '1' else '1'
        b = b[:index] + new + b[index+1:]

    return int(b, 2)

def real_neighbor(x):
    return int(np.random.normal(x, 5))

def crossover(p1, p2):
    # b1 = bin(p1)[2:]
    # b2 = bin(p2)[2:]
    b1 = format(p1, '011b')
    b2 = format(p2, '011b')
    index = random.randint(0,len(b1) - 1)
    c1 = b1[:index] + b2[index:]
    c2 = b2[:index] + b1[index:]

    return [int(c1, 2), int(c2, 2)]

def crossover2(p1, p2):
    c1 = random.randint(min(p1,p2),max(p1,p2))
    c2 = random.randint(min(p1,p2),max(p1,p2))
    return [c1, c2]

aList = []
bList = []
bave = []
cList = []
dList = []
# for j in [1]: #range(25,36):
# #     mutationRate = j/1000
#     a = 0
#     b = 0
#     c = 0
#     d = 0
#     ave = 0
#     # print('')
#     # print(j, end=' ', flush=True)

#     for _ in range(100):
#         inputs = random.sample(range(0, maxValue), 10)
#         # print('.', end='', flush=True)
#         res, best, avg, worst = geneticAlgorithm(inputs, crossover, crossoverRate, mutate, mutationRate, fitness, numGenerations)
#         if res == 0: a += 1
#         aList.append(res)
#         res, best, avg, worst = geneticAlgorithm(inputs, crossover, crossoverRate, real_neighbor, mutationRate, fitness, numGenerations)
#         if res == 0: b += 1
#         # ave += abs(res)
#         bList.append(res)
#         res, best, avg, worst = geneticAlgorithm(inputs, crossover2, crossoverRate, mutate, mutationRate, fitness, numGenerations)
#         if res == 0: c += 1
#         cList.append(res)
#         res, best, avg, worst = geneticAlgorithm(inputs, crossover2, crossoverRate, real_neighbor, mutationRate, fitness, numGenerations)
#         if res == 0: d += 1
#         dList.append(res)
#         # print(res, best, avg, worst, inputs)
#     # aList.append(a)
#     # ave = ave / 100
#     # bList.append(b)
#     # bave.append(ave)
# # print(res, pop)
# print(a, b, c, d)
# # print('')
# print(aList, '\n', bList, '\n', cList, '\n', dList, '\n')  #, bave)


def cts_mutate(x, sigma=1):
    """
    cts_mutate: continuous space mutation operation, 
    selects a nearby point via a N(x, sigma)
    
    Inputs
    x: mean of Gaussian
    sigma: standard deviation
    Output
    result: a point selected from N(x, sigma)
    Notes
    for applications with bounded spaces - apply clipping afterwards
    
    if supplying as mutation operation where want to specify sigma,
    can pass in as lambda function
    lambda x: cts_mutate(x, custom_sigma)
    """
    return np.random.normal(x, sigma)

def cts_crossover(parent1, parent2, num_children=2):
    """
    cts_crossover: continuous space crossover operation,
    selects num_children many points randomly using uniform distribution
    in between parent 1 and parent 2
    Inputs
    parent1, parent2: parents to breed, numpy arrays
    num_children: how many children to generate
    Output
    result: list of children of length num_children
    Notes
    for applications with bounded spaces - assuming allowed space is convex
    
    if supplying as crossover operation where want to specify num_children,
    can pass in as lambda function
    lambda *parents: cts_crossover(parents[0], parents[1], custom_num_children)
    """
    # assert parent1.shape == parent2.shape, "parents need to have same shape"
    assert num_children > 0, "need strictly positive number of children"
    low = np.minimum(parent1, parent2)
    high = np.maximum(parent1, parent2)

    children = []
    for i in range(num_children):
        children.append(np.random.uniform(low, high))
    return children

# a = 0
# ave = 0
# runs = 100
# for _ in range(runs):
#     inputs = random.sample(range(0, maxValue), maxValue//10)
#     res, best, avg, worst = geneticAlgorithm(inputs, cts_crossover, crossoverRate, cts_mutate, mutationRate, fitness, numGenerations)
#     if -0.0001 <= res and res <= 0.01: a += 1
#     ave += abs(res)
#     print(res)
# print(a, ave / runs)

maxValue = 2047
inputs = random.sample(range(0, maxValue), maxValue//10)
numGenerations = max(100, maxValue//10)
res, best, avg, worst = geneticAlgorithm(inputs, cts_crossover, crossoverRate, cts_mutate, mutationRate, fitness, numGenerations)
res2, best2, avg2, worst2 = geneticAlgorithm(inputs, crossover2, crossoverRate, cts_mutate, mutationRate, fitness, numGenerations)
printGA(best, avg, worst, "testingcts.png")
printGA(best2, avg2, worst2, "testingcross2.png")