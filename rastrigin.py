import numpy as np

from continuous_fn import cts_mutate, cts_crossover
from simulated_annealing import simulated_annealing, print_simulated_annealing, metropolis_hastings_algorithm_probability

def rastrigin_random_feasible_point(n):
    """
    Rastrigin continuous function

    Input
    n: dimension of the input space

    Output
    result: a randomly generated point in the feasible solution space 

    x in range [-5.12, 5.12]^n
    """
    return np.random.uniform(-5.12, 5.12, n)

def rastrigin(x, A=10):
    """
    Rastrigin continuous function: optimize for the minimum

    x in range [-5.12, 5.12]^n
    """
    return A*len(x) + np.sum(np.square(x) - A*np.cos(2*np.pi*x))

def rastrigin_mutate(x):
    return np.clip(cts_mutate(x, sigma=1), a_min=-5.12, a_max=5.12)

Ns = [1, 5, 10]
"""
Simulated Annealing Test
"""
for n in Ns:
    init = rastrigin_random_feasible_point(n)
    sols, fits, temps = simulated_annealing(init, lambda x: np.exp(x)-1, rastrigin_mutate, metropolis_hastings_algorithm_probability, 
        rastrigin, max_iterations=1000*n)
    print_simulated_annealing(sols, fits, temps, f"Rastrigin_SA_n={n}_temp=e^x-1.png")