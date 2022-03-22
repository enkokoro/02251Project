from random import random

def simulated_annealing(init, temperature, neighbor, probability, fitness, max_iterations):
    solutions = [init] 
    for k in range(max_iterations):
        T = temperature(1 - (k+1)/max_iterations)
        s_new = neighbor(s)
        if probability(fitness(s), fitness(s_new), T) >= random.uniform(0, 1):
            s = s_new
            solutions.append(s)
    return s

