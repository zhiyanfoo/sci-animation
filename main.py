import matplotlib.pyplot as plt
from math import pi, sin, cos
from dataclasses import dataclass
from typing import Tuple, Any
import numpy as np
from intersection import circle_line_intersection, circle_circle_intersection
from linalg import project_u_on_v, reflection_sphere_line, normalize
from matplotlib import animation
from physics import bounce_circle

import random
import itertools

random.seed(0)

fig = plt.figure()
ax = plt.axes(xlim=(-10, 110), ylim=(-10, 110))

RADIUS = 30
r2 = (RADIUS - 3) ** 2

class Grid:
    def init_grid(self, circles, lines):
        self.circles = circles
        self.lines = lines

    def get_circles(self, origin):
        return self.circles

    def get_lines(self, origin):
        return self.lines

grid = Grid()

class Line:
    def __init__(self, p1, p2):
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)
        v = self.p1 - self.p2
        a = np.array([v[1], v[0]])
        self.n = normalize(a)

    def plot_2d(self, ax_2d, **kwargs):
        p1, p2 = self.p1, self.p2
        xs = [p1[0], p2[0]]
        ys = [p1[1], p2[1]]
        ax_2d.plot(xs, ys, **kwargs)


def new_velocity_sphere_sphere(v1, v2, x1, x2):
    d = x1-x2
    return v1 - d * (v1-v2).dot(d) / d.dot(d)


class Circle:
    def __init__(self, origin, radius):
        self.origin = np.array(origin)
        self.radius = radius
        self.matplotlib_circle = plt.Circle(self.origin, self.radius)
        va = 0.03
        self.velocity = np.array([random.uniform(-va, va), random.uniform(-va, va)])
        self.dirty = False
        self.heat = 0

    def plot_2d(self, ax_2d, **kwargs):
        ax_2d.add_patch(self.matplotlib_circle)

    def resolve_collisions(self):
        collision = False

        for line in grid.get_lines(self.origin):
            i = 0
            while circle_line_intersection(self, line):
                bounce_circle(self, line)
                # nv = reflection_sphere_line(self, line)
                # self.origin -= 1.1 *self.velocity
                # # print(self.velocity, nv)
                # self.velocity = nv
                # self.move(True)
                # i += 1
                # if i > 5:
                #     break

        for circle in grid.get_circles(self.origin):
            if circle.dirty:
                continue

            if circle == self:
                continue

            if circle_circle_intersection(circle, self):
                collision = True
                s2 = circle
                break

        if collision:
            v1 = self.velocity
            v2 = s2.velocity
            x1 = self.origin
            x2 = s2.origin
            nv1 = new_velocity_sphere_sphere(v1, v2, x1, x2)
            nv2 = new_velocity_sphere_sphere(v2, v1, x2, x1)

            # print (nv1)
            # print (nv2)

            self.velocity = nv1
            s2.velocity = nv2
            s2.dirty = True

            self.move(True)
            s2.move(True)



    def move(self, extra):
        if extra:
            self.origin += 1.1 * self.velocity
        else:
            self.origin += self.velocity

        self.matplotlib_circle.circle = self.origin


def get_balloon_polygon():
    points = []
    for i in range(-2, 9):
        x = 50 + RADIUS * cos(i * 2 * pi/12)
        y = 50 + RADIUS * sin(i * 2 * pi/12)
        points.append((x, y))

    lines = []
    for i in range(len(points) - 1):
        lines.append(Line(points[i], points[i+1]))

    return lines

def get_walls():
    wall_points = [(5, 5), (5, 95), (95, 95), (95, 5)]
    lines = []
    for i in range(len(wall_points)):
        lines.append(Line(wall_points[i], wall_points[(i + 1) % len(wall_points)]))

    return lines

balloon_polygon = get_balloon_polygon()
walls = get_walls()
lines = balloon_polygon + walls

def get_circles():
    circles = []
    for i in range(-30, 31, 6):
        for j in range(-30, 31, 6):
            if random.random() < 0.5:
                continue
            # if (i) ** 2 + (j) ** 2 > r2:
            #     continue


            d1 = random.uniform(-1, 1)
            d2 = random.uniform(-1, 1)
            circle = Circle((50 + i + d1, 50 + j +  d2) , 2)

            intersects = False
            for line in lines:
                if (circle_line_intersection(circle, line)):
                    intersects = True
                    break


            if intersects:
                continue

            circles.append(circle)

    return circles


def single_circle():
    c1 = Circle(np.array([24, 70], dtype=float), 2)
    c1.velocity = np.array([0.00, -0.10])
    return [c1]


def two_circles():
    c1 = Circle(np.array([0, 0], dtype=float), 2)
    c2 = Circle(np.array([5, 3], dtype=float), 2)

    c1.velocity = np.array([0.04, 0])
    c2.velocity = np.array([-0.04, 0])
    c1.name = "c1"
    c2.name = "c2"

    return [c1, c2]



circles = get_circles()
# circles = single_circle()

def init():
    for line in lines:
        line.plot_2d(ax)

    for circle in circles:
        circle.plot_2d(ax)

    return [circle.matplotlib_circle for circle in circles]


limits = ax.axis('equal')

def draw():
    init()
    plt.savefig('out.png')

balloon_circle = Circle((50, 50), RADIUS-3)

def next_frame(i):
    # for circle in circles:
    #     if circle_circle_intersection(circle, balloon_circle):
    #         if circle.heat < 40:
    #             circle.velocity *= 1.04
    #             circle.heat += 1

    for i in range(3):
        for circle in circles:
            circle.move(False)

        for circle in circles:
            circle.resolve_collisions()

        for circle in circles:
            circle.dirty = False


    # if (i > 4):
    #     exit()

    return [circle.matplotlib_circle for circle in circles]



def animate():
    anim = animation.FuncAnimation(fig, next_frame,
                                   init_func=init,
                                   frames=12 * 60,
                                   interval=40,
                                   blit=True)
    grid.init_grid(circles, lines)
    plt.show()

# draw()
animate()

# v1 = np.array([0, 0])
# v2 = np.array([-1, 0])
# x1 = np.array(0)
# x2 = np.array([-1,0.5])

# print(new_velocity_sphere_sphere(v1, v2, x1, x2))

