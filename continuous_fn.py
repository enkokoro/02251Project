import numpy as np

def cts_mutate(x, sigma=1):
    """
    cts_mutate: continuous space mutation operation

    selects a nearby point via a N(x, sigma)
    x: mean of Gaussian
    sigma: standard deviation

    for applications with bounded spaces - apply clipping afterwards
    
    if supplying as mutation operation where want to specify sigma,
    can pass in as lambda function
    lambda x: cts_mutate(x, custom_sigma)
    """
    return np.random.normal(x, sigma)

def cts_crossover(parent1, parent2, num_children=1):
    """
    cts_crossover: continuous space crossover operation

    selects num_children many points randomly using uniform distribution
    in between parent 1 and parent 2

    for applications with bounded spaces - assuming allowed space is convex
    
    assumes parents are numpy arrays

    if supplying as crossover operation where want to specify num_children,
    can pass in as lambda function
    lambda *parents: cts_crossover(parents[0], parents[1], custom_num_children)
    """
    assert parent1.shape == parent2.shape, "parents need to have same shape"
    assert num_children > 0, "need strictly positive number of children"
    low = np.minimum(parent1, parent2)
    high = np.maximum(parent1, parent2)
    return np.random.uniform(low, high)

def rastrigin(x, A=10):
    """
    Rastrigin continuous function

    x in range [-5.12, 5.12]^n
    """
    return A*len(x) + np.sum(np.square(x) - A*np.cos(2*np.pi*x))