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

res = {'1': [], '5':[], '10':[]}
testValues = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75, 0.8, 0.85, 0.9, 0.95]
# testValues = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5]
parameter = 'p0'

p0 = 0.2 # paper: 0.4
Fb = 0.75 # paper: 0.9
k = 2
Fa = 0.1 # paper: 0.1
Fd = Fa # paper: Fa
Pd = 0.05 # paper: [0, 0.1]


for p0 in testValues:
    Ns = [1, 5, 10]
    for n in Ns:
        # print("="*80)
        # print(f"RASTRIGIN N={n}")
        rastrigin = Rastrigin(n)
        rastrigin_folder = "rastrigin_results/"

        N = 5
        M = 6
        num_generations = n * 100
        population_size = N * M
        num_runs = 10  # because algorithms are nondeterministic, we did some runs and took average

        final_results = {'CRO': []}
        for run_idx in range(num_runs):
            init = [rastrigin.random_feasible_point() for i in range(population_size)]

            """
            Coral Reef Optimization
            """
            solution, reef_evolutions = CRO(init, N, M, rastrigin, p0, Fb, k, Fa, Fd, Pd, num_generations)
            solution = np.array(solution)

            final_results['CRO'].append((solution, rastrigin.fitness(solution)))

        print("="*80)
        print(f"SUMMARY OF RUNS, {parameter} = {p0}")
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
            res[str(n)].append(best_fit)

print(res)
fig, ax1 = plt.subplots()

ax1.set_xlabel(f'{parameter} Value')
ax1.set_ylabel('Fitness')
plt.title(f'{parameter} Parameter Search')
ax1.plot(range(len(testValues)), res['1'], color='blue', label='N=1')
ax1.plot(range(len(testValues)), res['5'], color='green', label='N=5')
ax1.plot(range(len(testValues)), res['10'], color='purple', label='N=10')
fig.legend()
plt.xticks(range(len(testValues)), testValues)
ax1.tick_params(axis='y')

fig.tight_layout()
fig.savefig(f'{parameter} Param Search')
    