from continuous_fn import *
from algorithms.simulated_annealing import *
from algorithms.genetic_algorithm import *
from algorithms.coral_reef_optimization_rastrigin import CRO
from algorithms.coral_visualize import visualize_coral_reef_optimization
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

    def compare(self, x, y):
        if self.fitness(x) > self.fitness(y): return -1 # y has a better fitness than x
        elif self.fitness(x) < self.fitness(y): return 1 # x has a better fitness than y
        else: return 0

    # Sorted from best to worst fitness
    def sort(self, lst, rev=False):
        return sorted(lst, key=lambda x:self.fitness(x), reverse=rev)

Ns = [1, 5, 10]
for n in Ns:
    print("="*80)
    print(f"RASTRIGIN N={n}")
    rastrigin = Rastrigin(n)
    rastrigin_folder = "rastrigin_results/"

    N = 10
    M = 10
    num_generations = n * 100
    population_size = N * M
    num_runs = 10   # because algorithms are nondeterministic, we did some runs and took average

    final_results = {'CRO': [], 'GA':[], 'SA': [], 'TSA':[]}
    for run_idx in range(num_runs):
        init = [rastrigin.random_feasible_point() for i in range(population_size)]

        """
        Coral Reef Optimization
        """
        print("-"*80)
        print("CRO")
        p0 = 0.4 # paper: 0.4
        Fb = 0.9 # paper: 0.9
        k = 2
        Fa = 0.2 # paper: 0.1
        Fd = Fa # paper: Fa
        Pd = 0.05 # paper: [0, 0.1]
        solution, reef_evolutions = CRO(init, N, M, rastrigin, p0, Fb, k, Fa, Fd, Pd, num_generations)
        solution = np.array(solution)
        print(solution, rastrigin.fitness(solution))

        final_results['CRO'].append((solution, rastrigin.fitness(solution)))
        if rastrigin.fitness(solution) <= min([sol[1] for sol in final_results['CRO']]): # save best run
            visualize_coral_reef_optimization(reef_evolutions, filename=f"rastrigin_n={n}")

        """
        Genetic Algorithm
        """
        print("-"*80)
        print("Genetic Algorithm")
        crossoverRate = 0.7
        mutationRate = 0.05

        res, best, avg, worst = geneticAlgorithm(init, rastrigin.crossover, crossoverRate, rastrigin.mutate, mutationRate, rastrigin.fitness, num_generations)
        print(best[-1])
        res = np.array(res)
        final_results['GA'].append((res, rastrigin.fitness(res)))
        if rastrigin.fitness(res) <= min([sol[1] for sol in final_results['GA']]):
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
        best = min(sols, key=lambda x: rastrigin.fitness(x))
        print(best)
        final_results['SA'].append((best, rastrigin.fitness(best)))
        if rastrigin.fitness(best) <= min([sol[1] for sol in final_results['SA']]):
            print_simulated_annealing(sols, fits, temps, f"{rastrigin_folder}SA_n={n}_temp=e^x-1.png")

        """
        Thermodynamic Simulated Annealing
        """
        print("-"*80)
        print("Thermodynamic Simulated Annealing")
        high_prob = 0.8 #[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        k_A = 0.1 #[0.01, 0.05, 0.1, 0.2, 0.5, 0.75, 0.9]

        init_temp = thermodynamic_init_temp(100, high_prob, rastrigin.fitness, rastrigin.random_feasible_point)
        sols, fits, temps = thermodynamic_simulated_annealing(init, init_temp, k_A, rastrigin.mutate, metropolis_hastings_algorithm_probability, 
            rastrigin.fitness, max_iterations=population_size*num_generations*n)

        best = min(sols, key=lambda x: rastrigin.fitness(x))
        print(best)
        final_results['TSA'].append((best, rastrigin.fitness(best)))
        if rastrigin.fitness(best) <= min([sol[1] for sol in final_results['TSA']]):
            print_simulated_annealing(sols, fits, temps, f"{rastrigin_folder}TSA_n={n}_highprob={high_prob}_kA={k_A}.png")

print("="*80)
print("SUMMARY OF RUNS")
print("="*80)
for algo in final_results:
    print("Algorithm: ", algo)
    best_sol, best_fit = min(final_results[algo], key=lambda x: x[1])
    print("\tBest Solution: ", best_sol)
    print("\tBest Objective Value: ", best_fit)
    fitnesses = [sol[1] for sol in final_results[algo]]
    print("Statistics for fitness")
    print(pd.DataFrame(np.array(fitnesses)).describe())
    print("-"*80)
    

    
        

