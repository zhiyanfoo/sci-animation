import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
from math import pi, sin, cos
from dataclasses import dataclass
from typing import Tuple, Any
import numpy as np
from intersection import circle_line_intersection, circle_circle_intersection
from linalg import project_u_on_v, reflection_sphere_line, normalize
from matplotlib import animation
import random

hot_air_balloon = mpimg.imread('HotAirBalloon/BalloonTest.PNG')
background = mpimg.imread('HotAirBalloon/Background.PNG')

CIRCLE_START_Y = 100

random.seed(0)

fig = plt.figure()
ax = plt.axes(xlim=[0, 200], ylim=[0, 100])

ax.imshow(background, zorder=0, extent=[0, 200, 0, 150])
ax.imshow(hot_air_balloon, zorder=1, extent=[50, 150, 0, 150])

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
        self.n = normalize(np.array(v[1], v[0]))

    def plot_2d(self, ax_2d, **kwargs):
        p1, p2 = self.p1, self.p2
        xs = [p1[0], p2[0]]
        ys = [p1[1], p2[1]]
        ax_2d.plot(xs, ys, **kwargs)


def new_velocity_sphere_sphere(v1, v2, x1, x2):
    d = x1-x2
    return v1 - d * (v1-v2).dot(d) / d.dot(d)


class Circle:
    def __init__(self, origin, radius, color):
        self.x = np.array(origin)[0]
        self.y = np.array(origin)[1]
        self.origin = np.array(origin)
        self.radius = radius
        self.color = color
        self.matplotlib_circle = plt.Circle(self.origin, self.radius, color=self.color)
        if (self.color == 'green'):
            va = 0.20
        else:
            va = 0.04
        self.velocity = np.array([random.uniform(-va, va), random.uniform(-va, va)])
        self.dirty = False
        self.heat = 0
        

    def plot_2d(self, ax_2d, **kwargs):
        ax_2d.add_patch(self.matplotlib_circle)

    def resolve_collisions(self):
        collision = False

        for line in grid.get_lines(self.origin):
            if circle_line_intersection(self, line):
                nv = reflection_sphere_line(self, line)
                self.velocity = nv
                self.origin += 1.1 * nv
                return

        for circle in grid.get_circles(self.origin):
            if circle.dirty:
                continue

            if circle == self:
                continue

            if circle_circle_intersection(circle, self):
                # print("collision")
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
            v = self.velocity
            if self.color == 'green':
                if (self.origin[0] < 50):
                    self.origin[0] = 50
                if (self.origin[0] > 150):
                    self.origin[0] = 150
                if (self.origin[1] < 50):
                    self.origin[1] = 50
                if (self.origin[1] > 140):
                    self.origin[1] = 140

                if (self.origin[0] + v[0] < 50 or self.origin[0] + v[0] > 150 or 
                    self.origin[1] + v[1] < 50 or self.origin[1] + v[1] > 140):
                    self.velocity = -self.velocity
                    self.origin += self.velocity
                else:
                    self.origin += self.velocity
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

balloon_polygon = get_balloon_polygon()

def get_circles():
    circles = []
    for i in range(-30, 31, 6):
        for j in range(-30, 31, 6):
            # if (i) ** 2 + (j) ** 2 > r2:
            #     continue


            d1 = random.uniform(-1, 1)
            d2 = random.uniform(-1, 1)
            circle = Circle((50 + i + d1, CIRCLE_START_Y + j +  d2), 2, 'g')

            intersects = False
            for line in balloon_polygon:
                if (circle_line_intersection(circle, line)):
                    intersects = True
                    break


            if intersects:
                continue

            circles.append(circle)

    return circles

def get_circles_outside():
    circles = []
    for j in range(0, 150, 10):
        for i in range(0, 200, 10):
            # if (i) ** 2 + (j) ** 2 > r2:
            #     continue

            d1 = random.uniform(-1, 1)
            d2 = random.uniform(-1, 1)
            circle = Circle((i + d1, j +  d2), 2, 'blue')

            intersects = False
            for line in balloon_polygon:
                if (circle_line_intersection(circle, line)):
                    intersects = True
                    break

            if intersects:
                continue

            circles.append(circle)
    return circles


def two_circles():
    c1 = Circle(np.array([0, 0], dtype=float), 2)
    c2 = Circle(np.array([5, 3], dtype=float), 2)

    c1.velocity = np.array([0.04, 0])
    c2.velocity = np.array([-0.04, 0])
    c1.name = "c1"
    c2.name = "c2"

    return [c1, c2]



circles = get_circles_outside()
#circles.append(get_circles_outside())

def init():
    # for line in balloon_polygon:
    #    line.plot_2d(ax)

    for circle in circles:
        circle.plot_2d(ax)

    return [circle.matplotlib_circle for circle in circles]


limits = ax.axis('equal')

def draw():
    init()
    plt.savefig('out.png')

balloon_circle = Circle((50, 50), RADIUS-3, 'g')

def next_frame(i):
    for i in range(3):
        for circle in circles:
            circle.move(False)

        # for circle in circles:
        #    circle.resolve_collisions()

        for circle in circles:
            circle.dirty = False
        
    found = False
    index = 0

    global BACKGROUND_LOWER
    global BACKGROUND_UPPER
    global img

    while not found:
        circle = circles[index]
        if (circle.origin[0] > 50 and circle.origin[0] < 150 and 
            circle.origin[1] > 50 and circle.origin[1] < 140 
        and circle.color != 'green'):
            found = True
            del circles[index]
            newCircle = Circle((circle.x, circle.y), 2, 'green')
            newCircle.plot_2d(ax)
            circles.append(newCircle)
            break
        else:
            index += 1
            if (found or index > len(circles) - 1): break

    return [circle.matplotlib_circle for circle in circles]

def animate():
    anim = animation.FuncAnimation(fig, next_frame,
                                   init_func=init,
                                   frames=10 * 60,
                                   interval=40,
                                   blit=True)
    grid.init_grid(circles, balloon_polygon)
    plt.show()

animate()
