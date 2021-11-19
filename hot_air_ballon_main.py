import matplotlib.pyplot as plt
import random
from numpy import pi
import numpy as np
import matplotlib.image as mpimg
import cv2

from animation import animate
from draw import draw
from circle import Circle, linear_interpolation

img_hot_air_obj = None
img_helium_obj = None

def setup(ax):
    inner_circles = []
    grow_frame_start = 0
    grow_frame_end = 200
    height_raise_info=(grow_frame_start + 150, grow_frame_end + 250, 0, 0)
    li_balloon_height = linear_interpolation(*height_raise_info)
    for i in range(-30, 30, 6):
        for j in range(-30, 30, 6):
            if i ** 2 + j ** 2 > 29**2:
                continue
            circle = Circle(
                    (50 + i, 50 + j),
                    (50 +  i, 50 + j),
                     inner_shell_radius=0.7,
                     outer_shell_radius=3.0,
                     start_volatility=0.5,
                     end_volatility=0.5,
                     grow_frame_start=0,
                     grow_frame_end=200,
                     height_raise_info=height_raise_info
                     )
            inner_circles.append(circle)

    return inner_circles, li_balloon_height

def setup_single(ax):
    inner_circles = [Circle((50, 50), 2)]
    for circle in inner_circles:
        circle.plot_2d(ax)

    return inner_circles

def main():
    fig = plt.figure(dpi=250, frameon=True)
    ax = plt.axes(xlim=(0, 100), ylim=(-100, 290 - 90))
    plt.gca().set_aspect('equal', adjustable='box')
    # img_hot_air = mpimg.imread('assets/hot_air_balloon.png')
    # img_helium = mpimg.imread('assets/helium_balloon.png')
    # img_background = mpimg.imread('assets/background.png')
    ax.set_axis_off()

    # plt.show()
    # plt.axis('equal')
    # plt.axis('square')
    circles, li_balloon_height = setup(ax)
    # circles = setup_single()
    # circles = [plt.Circle((0, 0), 2)]
    patches = ([circle.matplotlib_circle_inner for circle in circles]) + ([circle.matplotlib_circle_outer for circle in circles])

    def next_frame_gen(circle):
        frame_index = 0
        vibration_length = 4
        start = random.randint(0, vibration_length)
        circle.choose_new_axis(0)

        for _ in range(start):
            circle.vibrate(True, 0)

        while True:
            for _ in range(start, vibration_length):
                circle.vibrate(True, frame_index)
                frame_index = yield

            for _ in range(vibration_length):
                circle.vibrate(False, frame_index)
                frame_index = yield

            for _ in range(start):
                circle.vibrate(True, frame_index)
                frame_index = yield

            circle.choose_new_axis(frame_index)

    circle_generators = list(map(next_frame_gen, circles))
    for cg in circle_generators:
        next(cg)

    def init_func():
        for circle in circles:
            circle.plot_2d(ax)
        # global img_hot_air_obj
        # global img_helium_obj
        # img_hot_air_obj = ax.imshow(img_hot_air, zorder=2, extent=(-90, 205, -100, 100))
        # img_helium_obj = ax.imshow(img_helium, zorder=2, extent=(-23, 115, -60, 90))
        # imo_background_obj = ax.imshow(img_background, zorder=0, extent=(-90, 205, -100, 200))
        # patches.append(img_hot_air_obj)
        # patches.append(img_helium_obj)
        # patches.append(imo_background_obj)
        return patches

    def next_frame(i):
        for circle in circle_generators:
            circle.send(i)

        if i == 200:
            for circle in circles:
                circle.matplotlib_circle_inner.set_radius(0.5)
                circle.matplotlib_circle_inner.set_facecolor('purple')
                circle.matplotlib_circle_inner.set_edgecolor('purple')


        original_bottom, original_top = -100, 100
        # new_height_gain = li_balloon_height(i)
        # print("nh gain", new_height_gain)
        # global img_hot_air_obj
        # img_hot_air_obj.set_extent(
        #         (-90, 205, -100 + new_height_gain, 100 + new_height_gain))
        # global img_helium_obj
        # img_helium_obj.set_extent(
        #         (-90, 205, -100 + new_height_gain, 100 + new_height_gain))
        return patches

    animate(init_func, next_frame, fig)

main()

