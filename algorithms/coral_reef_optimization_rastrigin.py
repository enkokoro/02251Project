import numpy as np
import matplotlib.pyplot as plt
import random
from algorithms.coral_visualize import visualize_coral_reef_optimization

#notes/questions: don't know how to tune parameters, should larvae's health depend on parents, what's the purpose of sorting for asexual reproduction
#lots of repeats in results (also extremely optimized) - is this because of asexual reproduction???
#how to use/interpret results, how to deal with/represent colonies of corals

class Coral:
    def __init__(self, name, r, hf):
        self.name = name
        self.hf = hf
        self.health = hf(r)
    def getName(self):
        return self.name
    def getHealth(self):
        return self.health
    def setHealth(self, h):
        self.health = h

def make_coral(corals, hf):
    r = random.randint(1, 10000)
    r1 = random.uniform(-5, 5)
    c = Coral(r, r1, hf)
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
def step(corals, hf, reef, pk, k, fa, pd):
    N = len(reef)
    M = len(reef[0])
    #broadcast spawning
    bsp = [] #broadcast spawners
    br = [] #brooders
    newCorals = {}
    for coral in corals:
        r = random.random()
        if (r<=pk):
            bsp.append(coral)
        else: br.append(coral)
    while (len(bsp)>1):
        #select couple
        l = len(bsp)
        x = random.randint(0, l-1)
        y = x
        while (y == x): y = random.randint(0, l-1)
        c1 = bsp[x]
        c2 = bsp[y]
        cHealth = (corals[c1].getHealth()+corals[c2].getHealth())/2
        bsp.remove(bsp[max(x, y)])
        bsp.remove(bsp[min(x, y)])
        #make larvae - does health function of larvae depend on health of parents?
        #can't add larvae into corals yet - haven't successfully settled into reef
        #child's health = average of parents
        c = make_coral(newCorals, hf)
        newCorals[c.getName()] = c
        c.setHealth(cHealth)
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

def CRO(hf, N, M, p0, k):
    #hf is health function
    l = [0, 1]
    #initialize N * M reef
    reef = [np.random.choice(l, M, p=[p0, 1-p0]) for y in range(N)] 
    corals = {}
    empty_coral = 0
    corals[empty_coral] = Coral(empty_coral, 0, hf)
    corals[empty_coral].health = np.nan
    for i in range(N):
        for j in range(M):
            if (reef[i][j]==1):
                c = make_coral(corals, hf)
                reef[i][j] = c.getName()
    reef_evolutions = []
    for i in range(k):
        step(corals, hf, reef, 0.5, 10, 0.1, 0.05)
        reef_evolutions.append(np.array(reef))
    visualize_coral_reef_optimization(reef_evolutions, corals, filename="test")



