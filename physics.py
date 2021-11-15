import numpy as np
from linalg import normalize
from intersection import circle_line_intersection

def bounce_circle(circle, line):
    bln = bounce_line_normal(circle, line)
    d = circle.velocity.dot(bln)
    circle.origin -= 2 * d * bln
    while circle_line_intersection(circle, line):
        circle.move(False)

def bounce_line_normal(circle, line):
    v = circle.origin - point_on_line_closest_to_circle(circle, line)

    return normalize(v)

def point_on_line_closest_to_circle(circle, line):
    p1, p2 = line.p1, line.p2
    v = p2 - p1
    p1_to_circle = circle.origin - p1
    v_normalized =  normalize(v)
    projection = p1_to_circle.dot(v_normalized)
    if projection < 0:
        return p1
    elif projection > np.linalg.norm(v):
        return p2

    return p1 + v_normalized * projection
