import numpy as np
import pandas as pd

from continuous_fn import cts_mutate, cts_crossover
from algorithms.simulated_annealing import (simulated_annealing, 
                                    thermodynamic_simulated_annealing,
                                    thermodynamic_init_temp,
                                    print_simulated_annealing, 
                                    metropolis_hastings_algorithm_probability)
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

    def crossover(self, p1, p2, num_children=1):
        unclipped = cts_crossover(p1, p2, num_children=num_children)
        return [np.clip(unclip) for unclip in unclipped]

def prints(s):
    if print_alot:
        print(s)

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
    num_runs = 5
    print("-"*80)
    print("Thermodynamic Simulated Annealing")
    high_probability_ps = [0.8]#[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    k_A_ps = [0.1]#[0.01, 0.05, 0.1, 0.2, 0.5, 0.75, 0.9]
    results = {}
    for high_prob in high_probability_ps:
        results_prob = {}
        for k_A in k_A_ps:
            mfit = 0
            for _ in range(num_runs):
                prints("-"*60)
                prints(f"high_prob: {high_prob} k_A: {k_A}")
                init_temp = thermodynamic_init_temp(100, high_prob, rastrigin.fitness, rastrigin.random_feasible_point)
                
                prints(f"Thermodynamic SA init_temp = {init_temp} k_A = {k_A}")
                sols, fits, temps = thermodynamic_simulated_annealing(init, init_temp, k_A, rastrigin.mutate, metropolis_hastings_algorithm_probability, 
                    rastrigin.fitness, max_iterations=1000*n)
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

