import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import copy

import coral_reef_optimization as cro
# reef: 2D array of the coral names
# corals: dictionary of the corals
extra_space = 1000
def visualize_coral_reef_optimization(reef_evolutions, corals, empty_coral=0, filename="test"): 
    empty_coral = 0
    corals[empty_coral] = cro.Coral(empty_coral, lambda x: x)
    corals[empty_coral].health = np.nan

    filename = filename 
    T = len(reef_evolutions)

    # ax1: reef evolution, ax2: solution quality plot over time
    fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

    fig.suptitle("Coral Reef Optimization")

    ax1.set_title('Coral Reef')
    ax1.set_aspect('equal')

    health_evolution = [np.array([[corals[coral_name].health for coral_name in coral_rows] for coral_rows in reef]) for reef in reef_evolutions]
    print(health_evolution)
    masked_array = np.ma.array (health_evolution[0], mask=np.isnan(health_evolution[0]))
    cmap = copy.copy(matplotlib.cm.get_cmap("jet"))
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
        return (im, )

    def animate2d_from_logs_update(frame):
        reef = reef_evolutions[frame]
        masked_array = np.ma.array(health_evolution[frame], mask=np.isnan(reef))
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
    corals = {}
    N, M = 2, 3
    p0 = 0.5
    l = [0, 1]
    hf = lambda x: x
    empty_coral = 0
    corals[empty_coral] = cro.Coral(empty_coral, hf)
    corals[empty_coral].health = np.nan

    reef = [np.random.choice(l, M, p=[p0, 1-p0]) for y in range(N)]
    for i in range(N):
        for j in range(M):
            if (reef[i][j]==1):
                c = cro.make_coral(corals, hf)
                reef[i][j] = c.getName()
    reef_evolutions = []
    for i in range(10):
        for j in range(2):
            coral = cro.make_coral(corals, hf)
            cro.settle(corals, coral, reef)
        reef_evolutions.append(np.array(reef))

    visualize_coral_reef_optimization(reef_evolutions, corals, filename="test")

test()