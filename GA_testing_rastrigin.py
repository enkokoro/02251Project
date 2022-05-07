import numpy as np

from genetic_algorithm import *
from simulated_annealing import (simulated_annealing, 
                         thermodynamic_simulated_annealing,
                         thermodynamic_init_temp,
                         print_simulated_annealing, 
                         metropolis_hastings_algorithm_probability)

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

def cts_crossover(parent1, parent2, num_children):
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
    assert parent1.shape == parent2.shape, "parents need to have same shape"
    assert num_children > 0, "need strictly positive number of children"
    low = np.minimum(parent1, parent2)
    high = np.maximum(parent1, parent2)

    children = []
    for i in range(num_children):
        children.append(np.random.uniform(low, high))
    return children

class Rastrigin():
    def __init__(self, n, A=10):
        self.n = n 
        self.A = A

    def random_feasible_point(self):
        """
        Rastrigin continuous function
        Output
        result: a randomly generated point in the feasible solution space 
        x in range [-5.12, 5.12]^n
        """
        return np.random.uniform(-5.12, 5.12, self.n)

    def fitness(self, x):
        """
        Rastrigin continuous function: optimize for the minimum
        x in range [-5.12, 5.12]^n
        """
        return self.A*self.n + np.sum(np.square(x) - self.A*np.cos(2*np.pi*x))

    def mutate(self, x):
        return np.clip(cts_mutate(x, sigma=1), a_min=-5.12, a_max=5.12)

    def crossover(self, p1, p2, num_children=2):
        # print(p1, p2)
        unclipped = cts_crossover(p1, p2, num_children=num_children)
        # print(unclipped)
        return [np.clip(unclip, -5.12, 5.12) for unclip in unclipped]

Ns = [1, 5, 10]
for n in Ns:
    print("="*80)
    print(f"RASTRIGIN N={n}")
    rastrigin = Rastrigin(n)
    rastrigin_folder = "rastrigin_results/"
    """
    Coral Reef Optimization
    """

    """
    Genetic Algorithm
    """
    print("-"*80)
    print("Genetic Algorithm")
    popSize = 100
    crossoverRate = 0.7
    mutationRate = 0.05

    init = [rastrigin.random_feasible_point() for i in range(popSize)]
    res, best, avg, worst = geneticAlgorithm(init, rastrigin.crossover, crossoverRate, rastrigin.mutate, mutationRate, rastrigin.fitness, 10*n)
    printGA(best, avg, worst, f"{rastrigin_folder}GA_n={n}_elites.png")

    """
    Simulated Annealing
    """
    print("-"*80)
    print(f"Simulated Annealing")
    init = rastrigin.random_feasible_point()
    sols, fits, temps = simulated_annealing(init, lambda x: np.exp(x)-1, rastrigin.mutate, metropolis_hastings_algorithm_probability, 
        rastrigin.fitness, max_iterations=1000*n)
    print_simulated_annealing(sols, fits, temps, f"{rastrigin_folder}SA_n={n}_temp=e^x-1.png")

    """
    Thermodynamic Simulated Annealing
    """
    print("-"*80)
    high_prob = 0.8
    init_temp = thermodynamic_init_temp(100, high_prob, rastrigin.fitness, rastrigin.random_feasible_point)
    k_A = 0.1
    print(f"Thermodynamic SA init_temp = {init_temp} k_A = {k_A}")
    sols, fits, temps = thermodynamic_simulated_annealing(init, init_temp, k_A, rastrigin.mutate, metropolis_hastings_algorithm_probability, 
        rastrigin.fitness, max_iterations=1000*n)
    print_simulated_annealing(sols, fits, temps, f"{rastrigin_folder}TSA_n={n}_highprob={high_prob}_kA={k_A}.png")