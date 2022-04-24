import numpy as np
from algorithms.coral_reef_optimization_rastrigin import CRO
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

Ns = [1, 5, 10]
for n in Ns:
    print("="*80)
    print(f"RASTRIGIN N={n}")
    rastrigin = Rastrigin(n)
    rastrigin_folder = "rastrigin_results/"
    """
    Coral Reef Optimization
    """
    CRO(lambda x: -rastrigin.fitness(x-2), 5, 6, 0.01, 50)
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
    print("-"*80)
    high_prob = 0.8
    init_temp = thermodynamic_init_temp(100, high_prob, rastrigin.fitness, rastrigin.random_feasible_point)
    k_A = 0.1
    print(f"Thermodynamic SA init_temp = {init_temp} k_A = {k_A}")
    sols, fits, temps = thermodynamic_simulated_annealing(init, init_temp, k_A, rastrigin.mutate, metropolis_hastings_algorithm_probability, 
        rastrigin.fitness, max_iterations=1000*n)
    print_simulated_annealing(sols, fits, temps, f"{rastrigin_folder}TSA_n={n}_highprob={high_prob}_kA={k_A}.png")

