import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin, pi
import random

def quadratic_interpolation(a):
    return (-(a - 1.5) ** 2 + 3)/ 6

def linear_interpolation_diff(start_iteration, end_iteration, start_position, end_position):
    iter_diff = 1/(end_iteration - start_iteration)
    m = (end_position - start_position) * iter_diff
    def li(current_iteration):
        if current_iteration < start_iteration:
            return 0

        if current_iteration > end_iteration:
            return 0

        return m

    return li

def linear_interpolation(start_iteration, end_iteration, start_position, end_position):
    iter_diff = 1/(end_iteration - start_iteration)
    m = (end_position - start_position) * iter_diff
    def li(current_iteration):
        if current_iteration < start_iteration:
            return start_position

        if current_iteration > end_iteration:
            return end_position

        return (current_iteration - start_iteration) * m + start_position

    return li



class Circle:
    def __init__(self, start_position, end_position, inner_shell_radius, outer_shell_radius,
            start_volatility, end_volatility, grow_frame_start, grow_frame_end,
            height_raise_info):
        self.origin = np.array(start_position, dtype=float)
        self.start_position = np.array(start_position, dtype=float)
        self.end_position = np.array(end_position, dtype=float)
        self.inner_shell_radius = inner_shell_radius
        self.outer_shell_radius = outer_shell_radius
        self.matplotlib_circle_outer =  plt.Circle(self.origin, self.inner_shell_radius,
                color="green", zorder=10)
        self.matplotlib_circle_inner =  plt.Circle(self.origin, self.outer_shell_radius, color="aqua",
                zorder=4)
        self.grow_frame_start = grow_frame_start
        self.grow_frame_end = grow_frame_end
        self.li_vibration_radius = linear_interpolation(
                grow_frame_start + 50, grow_frame_end + 50, start_volatility, end_volatility)
        self.li_d = linear_interpolation_diff(grow_frame_start + 50 + 50, grow_frame_end + 50 + 50, self.start_position, self.end_position)
        self.li_height_gain = linear_interpolation_diff(*height_raise_info)
        self.choose_new_axis(0)


    def get_displacment_vector(self):
        return self.displacement_radius * np.array([cos(self.displacement_angle), sin(self.displacement_angle)])

    def plot_2d(self, ax_2d, **kwargs):
        ax_2d.add_patch(self.matplotlib_circle_outer)
        ax_2d.add_patch(self.matplotlib_circle_inner)

    def vibrate(self, direction, i):
        v = quadratic_interpolation(self.displacment_vector)
        # v = self.displacment_vector
        if direction:
            self.origin -= v
        else:
            self.origin += v

        self.origin += self.li_d(i)
        hgd = self.li_height_gain(i)
        # print("hgd", hgd)
        self.origin += np.array([0, hgd])

        # print(self.matplotlib_circle.circle)

    def choose_new_axis(self, i):
        vibration_radius = self.li_vibration_radius(i)
        self.displacement_radius = random.uniform(vibration_radius/2, vibration_radius)
        self.displacement_angle = random.uniform(0, 1) * 2 * pi
        self.displacment_vector = self.get_displacment_vector()
