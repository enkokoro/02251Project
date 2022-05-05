from continuous_fn import *
from algorithms.simulated_annealing import *
from algorithms.genetic_algorithm import *
from algorithms.coral_reef_optimization_rastrigin import CRO
import numpy as np
import pandas as pd

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
        unclipped = cts_crossover(p1, p2, num_children=num_children)
        return [np.clip(unclip, -5.12, 5.12) for unclip in unclipped]

def prints(s):
    if print_alot:
        print(s)

Ns = [1] #, 5, 10]
for n in Ns:
    N = 5
    M = 6
    num_generations = 50
    population_size = N * M
    num_runs = 10   # because algorithms are nondeterministic, we did some runs and took average
    init = [rastrigin.random_feasible_point() for i in range(population_size)]

    print("="*80)
    print(f"RASTRIGIN N={n}")
    rastrigin = Rastrigin(n)
    rastrigin_folder = "rastrigin_results/"
    """
    Coral Reef Optimization
    """
    print("-"*80)
    print("CRO")
    p0 = 0.01
    pk = 0.5
    k = 10
    Fa = 0.1
    Fd = Fa
    Pd = 0.05
    solution, history = CRO(init, N, M, lambda x: -rastrigin.fitness(x-2), rastrigin.crossover, rastrigin.mutate, p0, pk, k, Fa, Fd, Pd, num_generations)
    print(solution, history)

    """
    Genetic Algorithm
    """
    print("-"*80)
    print("Genetic Algorithm")
    crossoverRate = 0.7
    mutationRate = 0.032

    res, best, avg, worst = geneticAlgorithm(init, rastrigin.crossover, crossoverRate, rastrigin.mutate, mutationRate, rastrigin.fitness, num_generations)
    printGA(best, avg, worst, f"{rastrigin_folder}GA_n={n}_Pop={population_size}_Gens={num_generations}_crossRate={crossoverRate}_mutRat={mutationRate}.png", 
        f"Rastrigin - Genetic Algorithm (n = {n})")

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
    print_alot = True
    print("-"*80)
    print("Thermodynamic Simulated Annealing")
    high_probability_ps = [0.8]#[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    k_A_ps = [0.1]#[0.01, 0.05, 0.1, 0.2, 0.5, 0.75, 0.9]
    results = {}
    for high_prob in high_probability_ps:
        results_prob = {}
        for k_A in k_A_ps:
            mfit = 0
            prints("-"*60)
            prints(f"high_prob: {high_prob} k_A: {k_A}")
            for _ in range(num_runs):
                init_temp = thermodynamic_init_temp(100, high_prob, rastrigin.fitness, rastrigin.random_feasible_point)
                sols, fits, temps = thermodynamic_simulated_annealing(init, init_temp, k_A, rastrigin.mutate, metropolis_hastings_algorithm_probability, 
                    rastrigin.fitness, max_iterations=population_size*num_generations*n)
                mfit += min(fits)
            if print_alot:
                print_simulated_annealing(sols, fits, temps, f"{rastrigin_folder}TSA_n={n}_highprob={high_prob}_kA={k_A}.png")

            results_prob[k_A] = mfit/num_runs
        results[high_prob] = results_prob
    
    prints("-"*80)
    print("Parameter Search Results")
    results = pd.DataFrame(results)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(results)

