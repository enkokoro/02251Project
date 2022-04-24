from curses.panel import new_panel
import numpy as np
import random
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from continuous_fn import cts_mutate, cts_crossover

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

    def crossover(self, p1, p2, num_children=1):
        unclipped = cts_crossover(p1, p2, num_children=num_children)
        return [np.clip(unclip) for unclip in unclipped]

Ns = [1, 5, 10]
for n in Ns:
    print("="*80)
    print(f"RASTRIGIN N={n}")
    rastrigin = Rastrigin(n)
    rastrigin_folder = "rastrigin_results/"
    """
    Coral Reef Optimization
    """
    class Coral:
        def __init__(self, name, hf):
            self.name = name
            self.hf = hf
            self.health = hf(name)
        def getName(self):
            return self.name
        def getHealth(self):
            return self.health
        def setHealth(self, h):
            self.health = h

    def make_coral(corals, hf):
        r = random.randint(1, 100)
        c = Coral(r, hf)
        corals[r] = c
        return c

    #new coral attempts to settle into reef
    def settle(corals, coral, reef):
        N = len(reef)
        M = len(reef[0])
        i = random.randint(0, N-1)
        j = random.randint(0, M-1)
        n = coral.getName()
        if (reef[i][j]==0):
            reef[i][j] = n
            corals[n] = coral
        else:
            h0 = coral.getHealth()
            c1 = corals[reef[i][j]]
            h1 = c1.getHealth()
            if (h0>h1):
                reef[i][j] = coral.getName()
                corals[n] = coral

    #pk = fraction of broadcast spawners
    #k = number of times corals attempt to settle before giving up
    #fa = fraction of corals that asexually reproduce
    #pd = probability for depredation
    def step(corals, hf, reef, pk, k, fa, pd):
        N = len(reef)
        M = len(reef[0])
        #broadcast spawning
        bsp = [] #broadcast spawners
        br = [] #brooders
        newCorals = {}
        for coral in corals:
            r = random.random()
            if (r<=pk):
                bsp.append(coral)
            else: br.append(coral)
        while (len(bsp)>1):
            #select couple
            l = len(bsp)
            x = random.randint(0, l-1)
            y = x
            while (y == x): y = random.randint(0, l-1)
            c1 = bsp[x]
            c2 = bsp[y]
            cHealth = (corals[c1].getHealth()+corals[c2].getHealth())/2
            bsp.remove(bsp[max(x, y)])
            bsp.remove(bsp[min(x, y)])
            #make larvae - does health function of larvae depend on health of parents?
            #can't add larvae into corals yet - haven't successfully settled into reef
            #child's health = average of parents
            c = make_coral(newCorals, hf)
            newCorals[c.getName()] = c
            c.setHealth(cHealth)
        #brooding - same question as before
        for i in range(len(br)):
            c = make_coral(newCorals, hf)
            newCorals[c.getName()] = c
        #larvae setting
        for i in newCorals:
            for j in range(k):
                settle(corals, newCorals[i], reef)
        #asexual reproduction
        ar = []
        #make a sorting function??? 
        for c in corals:
            r = random.random()
            if (r<=fa):
                ar.append(corals[c])
            for c in ar:
                for i in range(k):
                    settle(corals, c, reef)
        #depredation
        #find health "cutoff" for corals (used to find corals with worst health)
        count = 0
        healths = []
        for i in range(N):
            for j in range(M):
                if (not reef[i][j]==0):
                    count = count+1
                    c = corals[reef[i][j]]
                    healths.append(c.getHealth())
        healths.sort()
        mh = healths[round(len(healths)*fa)]
        for i in range(N):
            for j in range(M):
                if (not reef[i][j]==0):
                    r = random.random()
                    if (r<=pd):
                        c = corals[reef[i][j]]
                        if (c.getHealth()<=mh):
                            reef[i][j] = 0

    def hf(x):
        return rastrigin.fitness(x)

    # reef: 2D array of the coral names
    # corals: dictionary of the corals
    extra_space = 1000
    def visualize_coral_reef_optimization(reef_evolutions, corals, empty_coral=0, filename="test"): 
        filename = filename 
        T = len(reef_evolutions)
        # best_health = ?
        # worst_health = ?
        reef_height = len(reef_evolutions[0])
        reef_width = len(reef_evolutions[0][0])

        # ax1: reef evolution, ax2: solution quality plot over time
        fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        fig.suptitle("Coral Reef Optimization")

        ax1.set_title('Coral Reef')
        ax1.set_aspect('equal')

        health_evolution = [np.array([[corals[coral_name].health for coral_name in coral_rows] for coral_rows in reef]) for reef in reef_evolutions]
        print(health_evolution)
        masked_array = np.ma.array (health_evolution[0], mask=np.isnan(health_evolution[0]))
        cmap = matplotlib.cm.jet
        cmap.set_bad('white',1.)
        im = ax1.imshow(masked_array, interpolation='none', cmap="RdYlGn")
        fig.colorbar(im, ax=ax1)

        ax2.set_title('Solution Quality')
        ax2.set(xlabel='Time')

        fig.tight_layout()

        time_data = range(0, T)
        best_solution_data = [np.nanmax(healths) for healths in health_evolution]
        avg_solution_data = [np.nanmean(healths) for healths in health_evolution]
        best_solution_ln, = ax2.plot(time_data, best_solution_data, c='g')
        avg_solution_ln, = ax2.plot(time_data, avg_solution_data, c='y')
        ax2.legend(["best solution", "average solution"])

        def animate2d_init():
            ax2.set_xlim(0, T-1)
            ax2.set_ylim(np.nanmin(np.array(health_evolution))-extra_space, np.nanmax(np.array(health_evolution))+extra_space)
            return (im, )# best_solution_ln, avg_solution_ln)

        def animate2d_from_logs_update(frame):
            reef = reef_evolutions[frame]
            masked_array = np.ma.array(health_evolution[frame], mask=np.isnan(reef))
            im.set_array(masked_array)
            # im = ax1.imshow(masked_array, interpolation='none', cmap="RdYlGn")
            # fig.colorbar(im, ax=ax1)

            return (im, ) #best_solution_ln, avg_solution_ln)

        update = animate2d_from_logs_update
        frames = T

        FFwriter = animation.writers['ffmpeg']
        writer = FFwriter(fps=1, metadata=dict(artist='Me'), bitrate=1800)
        anime = animation.FuncAnimation(fig, animate2d_from_logs_update, init_func=animate2d_init, 
                                    frames=frames, interval=20, blit=True)  
        plt.show()
        if filename is not None:
            anime.save(filename+".mp4", writer=writer) 

    def CRO(hf, N, M, p0, k):
        #hf is health function
        l = [0, 1]
        #initialize N * M reef
        reef = [np.random.choice(l, M, p=[p0, 1-p0]) for y in range(N)] 
        corals = {}
        empty_coral = 0
        corals[empty_coral] = Coral(empty_coral, hf)
        corals[empty_coral].health = np.nan
        for i in range(N):
            for j in range(M):
                if (reef[i][j]==1):
                    c = make_coral(corals, hf)
                    reef[i][j] = c.getName()
        reef_evolutions = []
        for i in range(k):
            step(corals, hf, reef, 0.5, 5, 0.1, 0.05)
            reef_evolutions.append(np.array(reef))
        visualize_coral_reef_optimization(reef_evolutions, corals, filename="test")
CRO(hf, 5, 6, 0.01, 5)
