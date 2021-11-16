import numpy as np

from linalg import project_u_on_v, reflection_sphere_line, normalize

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


