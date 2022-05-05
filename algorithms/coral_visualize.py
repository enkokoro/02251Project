import random
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import copy

import algorithms.coral_reef_optimization_rastrigin as cro
# reef: 2D array of the coral names
# corals: dictionary of the corals
extra_space = 5
def visualize_coral_reef_optimization(reef_evolutions, empty_coral=None, filename="test"): 
    filename = filename 
    T = len(reef_evolutions)

    # ax1: reef evolution, ax2: solution quality plot over time
    fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

    fig.suptitle("Coral Reef Optimization")

    ax1.set_title('Coral Reef')
    ax1.set_aspect('equal')

    health_evolution = [np.array([[np.nan if coral is None else coral[1] for coral in coral_rows] for coral_rows in reef]) for reef in reef_evolutions]
    print("Best Coral Health: ", np.nanmax(np.array(health_evolution)))
    masked_array = np.ma.array(health_evolution[0], mask=np.isnan(health_evolution[0]))
    cmap = copy.copy(matplotlib.cm.get_cmap("jet"))
    cmap.set_bad('white',1.)
    im = ax1.imshow(masked_array, interpolation='none', cmap="RdYlGn")

    ax2.set_title('Solution Quality')
    ax2.set(xlabel='Time')

    fig.tight_layout()

    time_data = range(0, T)
    best_solution_data = [np.nanmax(healths) for healths in health_evolution]
    avg_solution_data = [np.nanmean(healths) for healths in health_evolution]
    worst_solution_data = [np.nanmin(healths) for healths in health_evolution]
    best_solution_ln, = ax2.plot(time_data, best_solution_data, c='g')
    avg_solution_ln, = ax2.plot(time_data, avg_solution_data, c='y')
    ax2.legend(["best solution", "average solution"])

    im.set_clim(min(worst_solution_data), max(best_solution_data))
    fig.colorbar(im, ax=ax1)


    def animate2d_init():
        ax2.set_xlim(0, T-1)
        ax2.set_ylim(np.nanmin(np.array(health_evolution))-extra_space, np.nanmax(np.array(health_evolution))+extra_space)
        return (im, )

    def animate2d_from_logs_update(frame):
        reef = reef_evolutions[frame]
        masked_array = np.ma.array(health_evolution[frame], mask=np.isnan(health_evolution[frame]))
        im.set_array(masked_array)
        # im = ax1.imshow(masked_array, interpolation='none', cmap="RdYlGn")
        # fig.colorbar(im, ax=ax1)

        return (im, ) 

    update = animate2d_from_logs_update
    frames = T

    FFwriter = animation.writers['ffmpeg']
    writer = FFwriter(fps=1, metadata=dict(artist='Me'), bitrate=1800)
    anime = animation.FuncAnimation(fig, animate2d_from_logs_update, init_func=animate2d_init, 
                                frames=frames, interval=20, blit=True)  
    plt.show()
    if filename is not None:
        anime.save(filename+".mp4", writer=writer) 

def test():
    N, M = 2, 3
    p0 = 0.5
    l = [None, 1]
    hf = lambda x: x

    reef_vals = [np.random.choice(l, M, p=[p0, 1-p0]) for y in range(N)]
    reef = [[None if reef_vals[n][m] is None else (reef_vals[n][m], hf(reef_vals[n][m])) for m in range(M)] for n in range(N)]

    reef_evolutions = []
    for i in range(10):
        for j in range(2):
            c = random.randint(1,i+1)
            cro.settle((c, hf(c)), reef, N, M)
        reef_evolutions.append(np.array(reef, dtype=object))

    visualize_coral_reef_optimization(reef_evolutions, filename="test")

# test()