import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin, pi
import random

def quadratic_interpolation(a):
    return (-(a - 1.5) ** 2 + 3)/ 6


class Circle:
    def __init__(self, origin, radius, inner_shell_radius):
        self.origin = np.array(origin, dtype=float)
        self.radius = radius
        self.inner_shell_radius = inner_shell_radius
        self.choose_new_axis()
        self.matplotlib_circle_outer =  plt.Circle(self.origin, self.inner_shell_radius,
                color="red", zorder=10)
        self.matplotlib_circle_inner =  plt.Circle(self.origin, self.radius, color="aqua",
                zorder=1)
        for i in range(2):
            self.vibrate(True, i)

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

        self.origin += np.array([0.0, 0.1])

        # print(self.matplotlib_circle.circle)

    def choose_new_axis(self):
        self.displacement_radius = random.uniform(0.6, 0.9)
        self.displacement_angle = random.uniform(0, 1) * 2 * pi
        self.displacment_vector = self.get_displacment_vector()
