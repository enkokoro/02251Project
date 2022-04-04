"""
Continuous Function Optimization Common Functions

Assumes solutions are points in Euclidean (R^n) Space and are np.arrays
"""
import numpy as np


def cts_mutate(x, sigma=1):
    """
    cts_mutate: continuous space mutation operation, 
    selects a nearby point via a N(x, sigma)
    
    Inputs
    x: mean of Gaussian
    sigma: standard deviation

    Output
    result: a point selected from N(x, sigma)

    Notes
    for applications with bounded spaces - apply clipping afterwards
    
    if supplying as mutation operation where want to specify sigma,
    can pass in as lambda function
    lambda x: cts_mutate(x, custom_sigma)
    """
    return np.random.normal(x, sigma)

def cts_crossover(parent1, parent2, num_children=1):
    """
    cts_crossover: continuous space crossover operation,
    selects num_children many points randomly using uniform distribution
    in between parent 1 and parent 2

    Inputs
    parent1, parent2: parents to breed, numpy arrays
    num_children: how many children to generate

    Output
    result: list of children of length num_children

    Notes
    for applications with bounded spaces - assuming allowed space is convex
    
    if supplying as crossover operation where want to specify num_children,
    can pass in as lambda function
    lambda *parents: cts_crossover(parents[0], parents[1], custom_num_children)
    """
    assert parent1.shape == parent2.shape, "parents need to have same shape"
    assert num_children > 0, "need strictly positive number of children"
    low = np.minimum(parent1, parent2)
    high = np.maximum(parent1, parent2)

    children = []
    for i in range(num_children):
        children.append(np.random.uniform(low, high))
    return children

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