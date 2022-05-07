import numpy as np
import matplotlib.pyplot as plt
import random
import copy

def initialize(reef, init, N, M, p0):
    # initialize N * M reef
    # p0 is a ratio of populated vs unpopulated colonies, not a probability!
    # Example in paper: N=5, M=6, p0=0.43, size=30, pop=9, unpop=21
    size = N * M
    numCorals = round((size * p0) / (1 + p0))

    # random.sample samples without replacement
    indices = random.sample(range(size), numCorals)
    samples = random.sample(init, len(indices))
    for idx, i in enumerate(indices):
        row = i // M
        col = i % M
        
        coral = samples[idx]
        reef[row][col] = coral

def separate(reef, Fb):
    bsp = [] #broadcast spawners
    br = [] #brooders
    corals = [c for row in reef for c in row if c is not None]
    numSpawners = round(len(corals) * Fb)

    bsp = random.sample(corals, numSpawners)
    br = copy.copy(corals)
    for elem in bsp:
        for i in range(len(br)):
            if np.array_equal(elem, br[i]):
                br.pop(i)
                break

    # Check that all corals are accounted for
    # assert len(bsp) + len(br) == len(corals) and sorted(bsp+br) == sorted(corals)

    return bsp, br

def broadcastSpawning(bsp, problem, newCorals):
    samples = random.sample(bsp, len(bsp)//2*2)
    for i in range(len(bsp)//2):
        c1 = samples[2*i]
        c2 = samples[2*i+1]
        larva = problem.crossover(c1, c2, num_children=1)[0] # crossover returns list of children

        newCorals.append(larva)

def brooding(br, problem, newCorals):
    for c in br:
        larva = problem.mutate(c)
        newCorals.append(larva)

def larvaeSetting(newCorals, k, reef, N, M, problem):
    for c in newCorals:
        for _ in range(k):
            settle(c, reef, N, M, problem)

def asexualReproduction(reef, Fa, k, N, M, problem):
    corals = [c for row in reef for c in row if c is not None]
    corals = problem.sort(corals) 
    numAR = round(len(corals) * Fa)
    ar = corals[:numAR]

    for c in ar:
        for _ in range(k):
            settle(c, reef, N, M, problem)

#new coral attempts to settle into reef
def settle(coral, reef, N, M, problem):
    i = random.randint(0, N - 1)
    j = random.randint(0, M - 1)

    if (reef[i][j] is None):
        reef[i][j] = coral
    else:
        c0 = coral
        c1 = reef[i][j]
        if (problem.compare(c0, c1) == 1):
            reef[i][j] = coral

def depredation(reef, Fd, pd, problem):
    corals = [(reef[row][col], row, col) for row in range(len(reef)) for col in range(row) if reef[row][col] is not None]
    corals.sort(key=lambda x:problem.fitness(x[0]), reverse=True) 

    numDep = round(len(corals) * Fd)
    dep = corals[-numDep:]

    for (_, i, j) in dep:
        r = random.random()
        if (r <= pd):
            reef[i][j] = None

#pk = fraction of broadcast spawners
#k = number of times corals attempt to settle before giving up
#fa = fraction of corals that asexually reproduce
#pd = probability for depredation
def CRO(init, N, M, problem, p0, Fb, k, Fa, Fd, pd, numIters):
    assert 0 < p0 and p0 < 1 and 0 <= pd and pd < 1
    assert 0 <= Fb and Fb <= 1 and 0 <= Fa and Fa <= 1 and 0 <= Fd and Fd <= 1
    assert 0 < N and 0 < M and 0 <= numIters and 0 < k
    assert type(init) == list
    assert len(init) == N * M
    assert Fa + Fd <= 1

    reef = [[None] * M for row in range(N)]
    initialize(reef, init, N, M, p0)
   
    reef_evolutions = []
    for _ in range(numIters):
        bsp, br = separate(reef, Fb)

        newCorals = []

        broadcastSpawning(bsp, problem, newCorals)

        brooding(br, problem, newCorals)

        larvaeSetting(newCorals, k, reef, N, M, problem)

        asexualReproduction(reef, Fa, k, N, M, problem)

        depredation (reef, Fd, pd, problem)

        reef_evolutions.append(np.array(reef))

    flatten = list(filter(lambda x: x is not None, [c for row in reef for c in row]))
    if len(flatten) == 0:
        assert False, "no solutions found"

    solution = problem.sort(flatten)[0]
    # fitness = problem.fitness(np.array(solution))
    
    return solution, reef_evolutions