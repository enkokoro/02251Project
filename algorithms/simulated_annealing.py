from random import random
import numpy as np
import matplotlib.pyplot as plt

# todo make this into object?
epsilon = 1e-5

def simulated_annealing(init, temp_fn, neighbor_fn, prob_fn, fitness_fn, max_iterations):
    """
    Inputs
    init: initial solution
    temp_fn: temperature cooling schedule
    neighbor_fn: generates neighbor solutions
    prob_fn: acceptance probability function
    fitness_fn: solution fitness evaluation function
    max_iterations: number of iterations to run simulated annealing

    Outputs
    solutions: list of solutions for each iteration
    fitnesses: corresponding fitnesses of the solutions
    temperatures: temperatures over the iterations
    """
    assert max_iterations > 0
    s = init
    solutions = [s] 
    f = fitness_fn(s)
    fitnesses = [f]
    temperatures = [temp_fn(1)]
    for k in range(max_iterations):
        T = temp_fn(1 - (k+1)/max_iterations)
        temperatures.append(T)

        # generate nearby solution
        s_new = neighbor_fn(s)

        # based off of temperature and new solution quality, choose whether to accept new solution
        if prob_fn(fitness_fn(s), fitness_fn(s_new), T) >= np.random.random():
            s = s_new
            f = fitness_fn(s)

        solutions.append(s)
        fitnesses.append(f)

    assert len(solutions) == len(temperatures)
    assert len(solutions) == len(fitnesses)
    return solutions, fitnesses, temperatures

def thermodynamic_init_temp(num_samples, high_prob, fitness_fn, random_generator_fn):
    temps = []
    for i in range(num_samples):
        f1 = fitness_fn(random_generator_fn())
        f2 = fitness_fn(random_generator_fn())
        temps.append(-abs(f1-f2)*np.log(high_prob))
    return np.average(np.array(temps))

def thermodynamic_simulated_annealing(init, init_temp, k_A, neighbor_fn, prob_fn, fitness_fn, max_iterations):
    """
    Inputs
    init: initial solution
    init_temp: initial temperature
    k_A (hyperparameter): tunes how fast we want the temperature to change
    neighbor_fn: generates neighbor solutions
    prob_fn: acceptance probability function
    fitness_fn: solution fitness evaluation function
    max_iterations: number of iterations to run simulated annealing

    Outputs
    solutions: list of solutions for each iteration
    fitnesses: corresponding fitnesses of the solutions
    temperatures: temperatures over the iterations
    """
    assert max_iterations > 0
    s = init
    solutions = [s] 
    f = fitness_fn(s)
    fitnesses = [f]
    T = init_temp
    temperatures = [T]
    total_cost_variation = 0 # delta_C_T
    total_entropy_variation = 0 # delta S_T
    for k in range(max_iterations):
        # generate nearby solution
        s_new = neighbor_fn(s)

        delta_cost = fitness_fn(s_new) - fitness_fn(s) # delta C_k

        # based off of temperature and new solution quality, choose whether to accept new solution
        if prob_fn(fitness_fn(s), fitness_fn(s_new), T) >= np.random.random():
            s = s_new
            f = fitness_fn(s)
            total_cost_variation += delta_cost
        
        if delta_cost > 0: # update total entropy variation
            total_entropy_variation = total_entropy_variation - delta_cost/(T+epsilon) 
        
        if total_cost_variation >= 0 or total_entropy_variation == 0: # use default temp
            T = init_temp 
        else:
            T = k_A*total_cost_variation/total_entropy_variation

        solutions.append(s)
        fitnesses.append(f)
        temperatures.append(T)
    assert len(solutions) == len(temperatures)
    return solutions, fitnesses, temperatures

def metropolis_hastings_algorithm_probability(e, e_new, T):
    if e_new < e:
        return 1 
    else:
        return np.exp(-(e_new-e)/(T+epsilon))

"""Temperature(x): x in [0,1] starts at 1 and decreases linearly to 0"""
def exponential_temperature(x, alpha):
    return np.exp(alpha*x)-1

def print_simulated_annealing(solutions, fitnesses, temperatures, filename):
    fig, ax1 = plt.subplots()
    fitness_color = 'blue'
    best_fitness_color = 'green'
    temperatures_color = 'red'

    best_fitness = []
    bf = None
    for f in fitnesses:
        if bf is None or f < bf:
            bf = f 
        best_fitness.append(bf)

    ax1.set_xlabel('iterations')
    ax1.set_ylabel('fitness')
    plt.yscale("log")
    ax1.plot(fitnesses, color=fitness_color, label='fitness')
    ax1.plot(best_fitness, color=best_fitness_color, label='best fitness')
    fig.legend()
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    plt.yscale("log")
    ax2.set_ylabel('temperature', color=temperatures_color)
    ax2.plot(temperatures, color=temperatures_color)
    ax2.tick_params(axis='y', labelcolor=temperatures_color)
    fig.tight_layout()
    fig.savefig(filename)


    print("Final Solution: ", solutions[-1], " Fitness: ", fitnesses[-1])
    print("Best Solution: ", solutions[np.argmin(fitnesses)], " Fitness: ", min(fitnesses))
    

