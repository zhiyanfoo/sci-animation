import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

def main():
    fig = plt.figure()
    ax = plt.axes(xlim=(-10, 110), ylim=(-10, 110))
    origins = [np.array((0, 0))]
    circles = [plt.Circle(origins[0], 2)]

    def init_func():
        for circle in circles:
            ax.add_patch(circle)
        return circles

    def next_frame(i):
        for origin in origins:
            origin += np.array([1,1])
        return circles
    # fig

    anim = animation.FuncAnimation(fig, next_frame, init_func=init_func, frames=25*60,
            interval=40,
            blit=True)
    plt.show()

main()
