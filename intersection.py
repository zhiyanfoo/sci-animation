from math import sqrt

eps = 10 ** -10

def sq(x):
    return x * x

def circle_circle_intersection(c1, c2):
    v = c1.origin - c2.origin
    v_sq = v.dot(v)
    return sq(c1.radius+ c2.radius) > v_sq

def circle_line_intersection(circle, line):
    x0, y0 = circle.origin
    x1, y1 = line.p1
    x2, y2 = line.p2
    r = circle.radius
    res = []

    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    a = sq(A) + sq(B)

    bnz = True
    if abs(B) >= eps:
        b = 2 * (A*C + A*B*y0 - sq(B)*x0)
        c = sq(C) + 2*B*C*y0 - sq(B)*(sq(r)-sq(x0)-sq(y0))
    else:
        b = 2 * (B*C + A*B*x0 - sq(A)*y0)
        c = sq(C) + 2*A*C*x0 - sq(A)*(sq(r)-sq(x0)-sq(y0))
        bnz = False

    d = sq(b) - 4 * a * c
    if d < 0:
        return res

    def within(x, y):
        d1 = sqrt(sq(x2-x1) + sq(y2-y1)) # distance between end-points
        d2 = sqrt(sq(x-x1) + sq(y-y1))   # distance from point to one end
        d3 = sqrt(sq(x2-x) + sq(y2-y))   # distance from point to other end
        delta = d1 - d2 - d3
        return abs(delta) < eps

    def fx(x):
        return -(A*x + C) / B

    def fy(x):
        return -(B*y + C) / A


    def rxy(x, y):
        if within(x, y):
            res.append([x, y])

    if d == 0.0:
        if bnz:
            x = -b / (2 * a);
            y = fx(x);
            rxy(x, y);
        else:
            y = -b / (2 * a);
            x = fy(y);
            rxy(x, y);

    else:
        d = sqrt(d)
        if bnz:
            x = (-b + d) / (2 * a);
            y = fx(x);
            rxy(x, y);
            x = (-b - d) / (2 * a);
            y = fx(x);
            rxy(x, y);
        else:
            y = (-b + d) / (2 * a);
            x = fy(y);
            rxy(x, y);
            y = (-b - d) / (2 * a);
            x = fy(y);
            rxy(x, y);

    return res
