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
    for i in range(-30, 31, 5):
        for j in range(-30, 31, 5):
            if i ** 2 + j ** 2 > 30**2:
                continue
            circle = Circle((50 + i, 50 + j), 3, 0.6)
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
    img = mpimg.imread("assets/balloon.png")
    imgplot = plt.imshow(img)
    # plt.show()
    # plt.axis('equal')
    # plt.axis('square')
    circles = setup(ax)
    # circles = setup_single()
    # circles = [plt.Circle((0, 0), 2)]
    patches = ([circle.matplotlib_circle_inner for circle in circles]) + ([circle.matplotlib_circle_outer for circle in circles])
    def init_func():
        for circle in circles:
            circle.plot_2d(ax)

        return patches

    def next_frame_gen(circle):
        vibration_length = 4
        while True:
            for i in range(2, 4):
                circle.vibrate(True, i)
                yield

            for i in range(vibration_length):
                circle.vibrate(False, i)
                yield

            for i in range(vibration_length - 2):
                circle.vibrate(True, i)
                yield
            yield

            circle.choose_new_axis()

    circle_generators = list(map(next_frame_gen, circles))

    def next_frame(i):
        for circle in circle_generators:
            next(circle)
        return patches

    animate(init_func, next_frame, fig)

main()

