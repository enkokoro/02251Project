from ...algorithms.simulated_annealing import (simulated_annealing, thermodynamic_init_temp, 
                                 thermodynamic_simulated_annealing,
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
print("="*80)

def generate_random_number():
    return np.random.uniform(-100, 100)

high_prob = 0.8
init_temp = thermodynamic_init_temp(100, high_prob, square, generate_random_number)
k_A = 0.1
print(f"Thermodynamic SA init_temp = {init_temp} k_A = {k_A}")
sols, fits, temps = thermodynamic_simulated_annealing(generate_random_number(), init_temp, k_A, real_neighbor, metropolis_hastings_algorithm_probability, square, 100)
print_simulated_annealing(sols, fits, temps, "thermodynamic_SA_x^2_kA=1.png")