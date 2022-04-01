from random import random
import numpy as np
import matplotlib.pyplot as plt

# todo make this into object?

def simulated_annealing(init, temp_fn, neighbor_fn, prob_fn, fitness_fn, max_iterations):
    assert max_iterations > 0
    s = init
    solutions = [s] 
    f = fitness_fn(s)
    fitnesses = [f]
    temperatures = [temp_fn(1)]
    for k in range(max_iterations):
        T = temp_fn(1 - (k+1)/max_iterations)
        temperatures.append(T)
        s_new = neighbor_fn(s)
        if prob_fn(fitness_fn(s), fitness_fn(s_new), T) >= np.random.random():
            s = s_new
            f = fitness_fn(s)
        solutions.append(s)
        fitnesses.append(f)
    assert len(solutions) == len(temperatures)
    return solutions, fitnesses, temperatures

def metropolis_hastings_algorithm_probability(e, e_new, T):
    if e_new < e:
        return 1 
    else:
        return np.exp(-(e_new-e)/(T+1e-5))

def print_simulated_annealing(solutions, fitnesses, temperatures, filename):
    fig, ax1 = plt.subplots()
    solutions_color = 'blue'
    temperatures_color = 'red'

    ax1.set_xlabel('iterations')
    ax1.set_ylabel('solutions', color=solutions_color)
    ax1.plot(solutions, color='blue')
    ax1.tick_params(axis='y', labelcolor=solutions_color)

    ax2 = ax1.twinx()
    ax2.set_ylabel('temperature', color=temperatures_color)
    ax2.plot(temperatures, color=temperatures_color)
    ax2.tick_params(axis='y', labelcolor=temperatures_color)
    fig.tight_layout()
    fig.savefig(filename)

    # todo
    # graph of best, worst from history

    print("Final Solution: ", solutions[-1], " Fitness: ", fitnesses[-1])
    print("Best Solution: ", solutions[np.argmin(fitnesses)], " Fitness: ", min(fitnesses))

