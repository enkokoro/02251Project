import numpy as np
import matplotlib.pyplot as plt
import random

#notes/questions: don't know how to tune parameters, should larvae's health depend on parents, what's the purpose of sorting for asexual reproduction
#lots of repeats in results (also extremely optimized) - is this because of asexual reproduction???
#how to use/interpret results, how to deal with/represent colonies of corals

def initialize(reef, init, N, M, p0, hf):
    # initialize N * M reef
    # p0 is a ratio of populated vs unpopulated colonies, not a probability!
    # Example in paper: N=5, M=6, p0=0.43, size=30, pop=9, unpop=21
    size = N * M
    numCorals = round((size * p0) / (1 - p0))
    indices = np.random.randint(low=0, high=size, size=numCorals)

    # random.sample samples without replacement
    samples = random.sample(init, len(indices))
    for idx, i in enumerate(indices):
        row = i // M
        col = i % M
        
        coral = samples[idx]

        # Each coral is a tuple of solution and fitness
        reef[row][col] = (coral, hf(coral)) # TODO need fitness??

def separate(reef, pk):
    bsp = [] #broadcast spawners
    br = [] #brooders
    corals = [c for row in reef for c in row if c != None]

    for coral in corals:
        r = random.random()
        if (r <= pk):
            bsp.append(coral)
        else: 
            br.append(coral)
    return bsp, br

def broadcastSpawning(bsp, crossover, newCorals, hf):
    samples = random.sample(bsp, len(bsp)//2*2)
    for i in range(len(bsp)//2):
        c1 = samples[2*i]
        c2 = samples[2*i+1]
        larva = crossover(c1[0], c2[0], num_children=1)[0] # crossover returns array of children

        newCorals.append((larva, hf(larva)))

def brooding(br, mutate, newCorals, hf):
    for c in br:
        larva = mutate(c[0])
        newCorals.append((larva, hf(larva)))

def larvaeSetting(newCorals, k, reef, N, M):
    for c in newCorals:
        for _ in range(k):
            settle(c, reef, N, M)

def asexualReproduction(reef, Fa, k, N, M):
    ar = []
    # TODO make a sorting function???
    corals = [c for row in reef for c in row if c != None]
    
    for c in corals:
        r = random.random()
        if (r <= Fa):
            ar.append(c)

    for c in ar:
        for _ in range(k):
            settle(c, reef, N, M)

#new coral attempts to settle into reef
def settle(coral, reef, N, M):
    i = random.randint(0, N - 1)
    j = random.randint(0, M - 1)

    if (reef[i][j] == None):
        reef[i][j] = coral
    else:
        h0 = coral[1]
        h1 = reef[i][j][1]
        if (h0 > h1):
            reef[i][j] = coral

def depredation(reef, Fd, pd, N, M):
    #find health "cutoff" for corals (used to find corals with worst health)
    healths = []
    for i in range(N):
        for j in range(M):
            if (not reef[i][j] == None):
                h = reef[i][j][1]
                healths.append(h)

    healths.sort()
    if len(healths) > 0: # do nothing if there are no corals
        mh = healths[round(len(healths)*Fd)]

        for i in range(N):
            for j in range(M):
                if (not reef[i][j] == None):
                    r = random.random()
                    if (r <= pd):
                        c = reef[i][j]
                        if (c[1] <= mh):
                            reef[i][j] = None

#pk = fraction of broadcast spawners
#k = number of times corals attempt to settle before giving up
#fa = fraction of corals that asexually reproduce
#pd = probability for depredation
def CRO(init, N, M, fitness_fn, crossover, mutate, p0, pk, k, Fa, Fd, pd, numIters):
    infty = 1e12
    hf = lambda x: fitness_fn(x[0])
    assert 0 < p0 and p0 < 1 and 0 < pk and pk < 1 and 0 < pd and pd < 1
    assert 0 < Fa and Fa < 1 and 0 < Fd and Fd < 1
    assert 0 < N and 0 < M and 0 <= numIters and 0 < k
    assert type(init) == list
    assert len(init) == N * M
    assert Fa + Fd <= 1

    reef = [([None] * M) for row in range(N)]
    initialize(reef, init, N, M, p0, hf)
   
    reef_evolutions = []
    for _ in range(numIters):
        bsp, br = separate(reef, pk)

        newCorals = []

        broadcastSpawning(bsp, crossover, newCorals, hf)

        brooding(br, mutate, newCorals, hf)

        larvaeSetting(newCorals, k, reef, N, M)

        # TODO come back!! check paper
        asexualReproduction(reef, Fa, k, N, M)

        depredation (reef, Fd, pd, N, M)

        reef_evolutions.append(np.array(reef, dtype=object))

    flatten = list(filter(lambda x: x is not None, [c for row in reef for c in row]))
    if len(flatten) == 0:
        assert False, "no solutions found"
    solution = max(flatten, key=lambda x: x[1])
    
    return solution, reef_evolutions