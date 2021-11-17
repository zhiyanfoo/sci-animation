import matplotlib.pyplot as plt
import random
from numpy import pi
import numpy as np
import matplotlib.image as mpimg

from animation import animate
from draw import draw
from circle import Circle

def setup(ax):
    inner_circles = []
    for i in range(-30, 30, 5):
        for j in range(-30, 30, 5):
            if i ** 2 + j ** 2 > 30**2:
                continue
            circle = Circle(
                    (50 + i, 50 + j),
                    (50 + 1.3 *i, 50 + 1.3 * j),
                     0.6, 3, 0.5, 1.3, 0, 200)
            inner_circles.append(circle)

    return inner_circles

def setup_single(ax):
    inner_circles = [Circle((50, 50), 2)]
    for circle in inner_circles:
        circle.plot_2d(ax)

    return inner_circles

def main():
    fig = plt.figure(dpi=150)
    ax = plt.axes(xlim=(-10, 110), ylim=(-10, 110))
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()
    # plt.axis('equal')
    # plt.axis('square')
    circles = setup(ax)
    # circles = setup_single()
    # circles = [plt.Circle((0, 0), 2)]
    patches = ([circle.matplotlib_circle_inner for circle in circles]) + ([circle.matplotlib_circle_outer for circle in circles])

    def next_frame_gen(circle):
        frame_index = 0
        vibration_length = 4
        start = random.randint(0, vibration_length)
        while True:
            for i in range(start, vibration_length):
                circle.vibrate(True, frame_index)
                i = yield

            for i in range(vibration_length):
                circle.vibrate(False, frame_index)
                frame_index = yield

            for i in range(start):
                circle.vibrate(True, frame_index)
                frame_index = yield

            circle.choose_new_axis(frame_index)

    circle_generators = list(map(next_frame_gen, circles))
    for cg in circle_generators:
        next(cg)

    def init_func():
        for circle in circles:
            circle.plot_2d(ax)
        return patches

    def next_frame(i):
        for circle in circle_generators:
            circle.send(i)
        return patches

    animate(init_func, next_frame, fig)

main()

