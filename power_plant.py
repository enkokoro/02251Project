"""
Optimal Power Plant Placement

Assumes solutions are lists of power plants
"""
import random
import numpy as np

class PowerPlant():
    """
    location: tuple denoting grid location
    energy_generated: positive real number specifying how 
        much energy power plant generates per unit in range
    does_serve: function which takes in a location and returns 
        if this power plant serves this location or not 
    """
    def __init__(self, location, energy_generated, does_serve):
        self.location = location 
        self.energy_generated = energy_generated
        self.does_serve = does_serve

class PowerPlantProblem():
    """
    energy_consumption_grid: grid of the positive energy consumption
        per grid unit (numpy array)
    power_plants: list of PowerPlant objects where locations are valid
        indices in the energy_consumption_grid
    """
    def __init__(self, energy_consumption_grid, power_plants):
        self.energy_consumption_grid = energy_consumption_grid
        self.power_plants = power_plants
    
    def fitness(self, selected_plants):
        energy_diff = self.energy_consumption_grid
        for idx, _ in np.ndenumerate(energy_diff):
            for p in selected_plants:
                if p.does_serve(idx):
                    energy_diff[idx] -= p.energy_generated
        return np.sum(np.square(energy_diff))

    def power_plant_mutate1(self, x, max_num_points_changed=1):
        """
        power_plant_mutate: power plant list mutation operation,
        selects a new power plant list which is similar to x
        by selecting max_num_points_changed random points from all points
        and removing if already exists in x, adding if not already exists in x

        Input
        x: original solution point that we want to generate a mutation of, 
            list that is subset of all power plants
        max_num_points_changed (hyperparameter): specifies how big of a mutation
            we want to allow, how many points may be changed

        Output
        result: a list that is a subset of all power plants, no duplicates, mutation of x
        
        if supplying as mutation operation, pass in as lambda function
        lambda x: power_plant.power_plant_mutate1(x, custom_num_points)
        """
        k = random.randrange(max_num_points_changed)+1
        random_points = random.sample(self.power_plants, k)

        mutation = x.copy()
        for p in random_points:
            if p in mutation:
                mutation.remove(p)
            else:
                mutation.append(p)

        return mutation

    def power_plant_mutate2(self, x, max_num_points_changed=1):
        """
        power_plant_mutate: power plant list mutation operation,
        selects a new power plant list which is similar to x
        by doing the following max_num_points_changed times:
        flip a coin to see if we are adding or removing, randomly select
        a point from the relevant set to add or remove

        Input
        x: original solution point that we want to generate a mutation of, 
            list that is subset of all power plants
        max_num_points_changed (hyperparameter): specifies how big of a mutation
            we want to allow, how many points may be changed

        Output
        result: a list that is a subset of all power plants, no duplicates, mutation of x
        
        if supplying as mutation operation, pass in as lambda function
        lambda x: power_plant.power_plant_mutate2(x, custom_num_points)
        """
        mutation = x.copy()
        for i in range(max_num_points_changed):
            # remove if mutation = all power plants or (coin says so and there are things to remove)
            if (random.uniform(0, 1) <= 0.5 and len(mutation) > 0) or len(mutation) == len(self.power_plants): 
                mutation.remove(random.choice(mutation))
            # otherwise add
            else: 
                new_plant = random.choice(self.power_plants)
                while new_plant in mutation:
                    new_plant = random.choice(self.power_plants)
                mutation.append(new_plant)
        return mutation

    def power_plant_crossover(self, parent1, parent2, num_children=1):
        """
        power_plant_crossover: continuous space crossover operation,
        selects num_children many points randomly using uniform distribution
        in between parent 1 and parent 2

        Inputs
        parent1, parent2: parents to breed, numpy arrays
        num_children: how many children to generate

        Output
        result: list of children of length num_children

        if supplying as crossover operation where want to specify num_children,
        can pass in as lambda function
        lambda *parents: power_plant.power_plant_crossover(parents[0], parents[1], custom_num_children)
        """
        assert num_children > 0, "need strictly positive number of children"
        
        total_points = parent1 + parent2 
        children = []
        for i in range(num_children):
            child = []
            for p in total_points:
                if random.uniform(0, 1) <= 0.5:
                    child.append(p)
            children.append(child)
        return children 

