import numpy as np

import numpy
import matplotlib.pyplot as plt
import random

#notes/questions: don't know how to tune parameters, should larvae's health depend on parents, what's the purpose of sorting for asexual reproduction
#lots of repeats in results (also extremely optimized) - is this because of asexual reproduction???
#how to use/interpret results, how to deal with/represent colonies of corals

class Coral:
    def __init__(self, name, hf):
        self.name = name
        self.hf = hf
        self.health = hf(name)
    def getName(self):
        return self.name
    def getHealth(self):
        return self.health
    def setHealth(self, h):
        self.health = h

def make_coral(corals, hf):
    r = random.randint(1, 10000)
    c = Coral(r, hf)
    corals[r] = c
    return c

#new coral attempts to settle into reef
def settle(corals, coral, reef):
    N = len(reef)
    M = len(reef[0])
    i = random.randint(0, N-1)
    j = random.randint(0, M-1)
    n = coral.getName()
    if (reef[i][j]==0):
        reef[i][j] = n
        corals[n] = coral
    else:
        h0 = coral.getHealth()
        c1 = corals[reef[i][j]]
        h1 = c1.getHealth()
        if (h0>h1):
            reef[i][j] = coral.getName()
            corals[n] = coral

#pk = fraction of broadcast spawners
#k = number of times corals attempt to settle before giving up
#fa = fraction of corals that asexually reproduce
#pd = probability for depredation
def step(hf, reef, pk, k, fa, pd, N, M, crossover):
    #broadcast spawning
    bsp = [] #broadcast spawners
    br = [] #brooders
    newCorals = {}
    corals = [c for row in reef for c in row if c != None]

    for coral in corals:
        r = random.random()
        if (r<=pk):
            bsp.append(coral)
        else: br.append(coral)

    newCorals = []
    while (len(bsp)>1):
        #select couple
        couple = random.sample(bsp, 2)
        c1 = couple[0]
        c2 = couple[1]
        larvae = crossover(c1[0], c2[0], numChildren=1)

        bsp.remove(c1)
        bsp.remove(c2)

        #make larvae - does health function of larvae depend on health of parents?
        #can't add larvae into corals yet - haven't successfully settled into reef
        #child's health = average of parents
        newCorals.append(larvae)

    #brooding - same question as before
    for i in range(len(br)):
        c = make_coral(newCorals, hf)
        newCorals[c.getName()] = c
    #larvae setting
    for i in newCorals:
        for j in range(k):
            settle(corals, newCorals[i], reef)
    #asexual reproduction
    ar = []
    #make a sorting function??? 
    for c in corals:
        r = random.random()
        if (r<=fa):
            ar.append(corals[c])
        for c in ar:
            for i in range(k):
                settle(corals, c, reef)
    #depredation
    #find health "cutoff" for corals (used to find corals with worst health)
    count = 0
    healths = []
    for i in range(N):
        for j in range(M):
            if (not reef[i][j]==0):
                count = count+1
                c = corals[reef[i][j]]
                healths.append(c.getHealth())
    healths.sort()
    mh = healths[round(len(healths)*fa)]
    for i in range(N):
        for j in range(M):
            if (not reef[i][j]==0):
                r = random.random()
                if (r<=pd):
                    c = corals[reef[i][j]]
                    if (c.getHealth()<=mh):
                        reef[i][j] = 0
                        

def CRO(hf, N, M, p0, k, init, crossover):
    assert 0 < p0 and p0 < 1
    assert 0 < N and 0 < M
    assert type(init) == list
    # Each coral is labeled with an associated health function??

    #initialize N * M reef
    # p0 is a ratio of populated vs unpopulated colonies, not a probability!
    # Example in paper: N=5, M=6, p0=0.43, size=30, pop=9, unpop=21
    size = N * M
    numCorals = round((size * p0) / (1 + p0))
    indicies = np.random.randint(low=0, high=size, size=numCorals)
    reef = [[None for _ in range(M)] for _ in range(N)]

    for i in indicies:
        row = i // M
        col = i % M
        
        # Randomly select solution from initial list of solutions
        j = random.randint(0, len(init) - 1)
        coral = init[j]
        init.remove(coral)

        # Each coral is a tuple of solution and fitness
        reef[row][col] = (coral, hf(coral))

    reef_evolutions = []
    for i in range(k):
        step(hf, reef, 0.5, 10, 0.1, 0.05, N, M, crossover)
        reef_evolutions.append(np.array(reef))
    
    return solution??, reef_evolutions