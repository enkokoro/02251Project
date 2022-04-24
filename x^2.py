from continuous_fn import *
from algorithms.simulated_annealing import *
from algorithms.genetic_algorithm import *
import random
import numpy as np

def square(x):
    return x**2 + 0.001

def mutate(x):
    return cts_mutate(x, sigma=5)

def crossover(parent1, parent2, num_children=2):
    low = np.minimum(parent1, parent2)
    high = np.maximum(parent1, parent2)

    children = []
    for i in range(num_children):
        children.append(np.random.uniform(low, high))
    return children

folder = "x^2_results/"


"""
Genetic Algorithm
"""
print("-"*80)
print("Genetic Algorithm")

maxValue = 100
populationSize = maxValue//10
inputs = random.sample(range(0, maxValue), populationSize)
crossoverRate = 0.7
mutationRate = 0.032
numGenerations = max(100, maxValue//10)

res, best, avg, worst = geneticAlgorithm(inputs, crossover, crossoverRate, mutate, mutationRate, square, numGenerations)
printGA(best, avg, worst, f"{folder}GA_Pop={populationSize}_Gens={numGenerations}_crossRate={crossoverRate}_mutRat={mutationRate}.png", f"X^2 - Genetic Algorithm")

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