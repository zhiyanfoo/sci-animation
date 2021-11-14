import numpy as np

def project_u_on_v(u, v):
    r = (u.dot(v) / v.dot(v)) * v
    return r

def normalize(v):
    return v/ np.linalg.norm(v)


def reflection_sphere_line(sphere, line):
    d = sphere.velocity
    n = line.n
    return d - 2 * d.dot(n) * n
