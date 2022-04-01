from simulated_annealing import (simulated_annealing, 
                                 metropolis_hastings_algorithm_probability, 
                                 print_simulated_annealing)
import numpy as np

def square(x):
    return x**2

def real_neighbor(x):
    return np.random.normal(x, 5)

print("Temp(x) = 100*x")
sols, fits, temps = simulated_annealing(100, lambda x: x*100, real_neighbor, metropolis_hastings_algorithm_probability, square, 100)
print_simulated_annealing(sols, fits, temps, "SA_x^2_temp=100x.png")
print("="*80)

print("Temp(x) = x")
sols, fits, temps = simulated_annealing(100, lambda x: x, real_neighbor, metropolis_hastings_algorithm_probability, square, 100)
print_simulated_annealing(sols, fits, temps, "SA_x^2_temp=x.png")
print("="*80)

print("Temp(x) = e^x-1")
sols, fits, temps = simulated_annealing(100, lambda x: np.exp(x)-1, real_neighbor, metropolis_hastings_algorithm_probability, square, 100)
print_simulated_annealing(sols, fits, temps, "SA_x^2_temp=e^x-1.png")

# TODO the thermodynamic temperature function