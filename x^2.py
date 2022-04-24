from continuous_fn import cts_mutate
from algorithms.simulated_annealing import (simulated_annealing, thermodynamic_init_temp, 
                                 thermodynamic_simulated_annealing,
                                 metropolis_hastings_algorithm_probability, 
                                 print_simulated_annealing)
import numpy as np

def square(x):
    return x**2

def mutate(x):
    return cts_mutate(x, sigma=5)

folder = "x^2_results/"

"""
Simulated Annealing
"""
print("="*80)
print("Simulated Annealing")
print("Temp(x) = 100*x")
sols, fits, temps = simulated_annealing(100, lambda x: x*100, mutate, metropolis_hastings_algorithm_probability, square, 100)
print_simulated_annealing(sols, fits, temps, f"{folder}SA_x^2_temp=100x.png")
print("-"*80)

print("Temp(x) = x")
sols, fits, temps = simulated_annealing(100, lambda x: x, mutate, metropolis_hastings_algorithm_probability, square, 100)
print_simulated_annealing(sols, fits, temps, f"{folder}SA_x^2_temp=x.png")
print("-"*80)

print("Temp(x) = e^x-1")
sols, fits, temps = simulated_annealing(100, lambda x: np.exp(x)-1, mutate, metropolis_hastings_algorithm_probability, square, 100)
print_simulated_annealing(sols, fits, temps, f"{folder}SA_x^2_temp=e^x-1.png")

"""
Thermodynamic Simulated Annealing
"""
print("="*80)
print("Thermodynamic Simulated Annealing")
def generate_random_number():
    return np.random.uniform(-100, 100)

high_prob = 0.8
init_temp = thermodynamic_init_temp(100, high_prob, square, generate_random_number)
k_A = 0.1
print(f"Thermodynamic SA init_temp = {init_temp} k_A = {k_A}")
sols, fits, temps = thermodynamic_simulated_annealing(generate_random_number(), init_temp, k_A, mutate, metropolis_hastings_algorithm_probability, square, 100)
print_simulated_annealing(sols, fits, temps, f"{folder}TSA_x^2_kA=1.png")