# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pencil-cut-machining/. The authors are listed in prov/K6TS7H.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from pencil_cut_machining import contacts, cross, dot, pencil_trace, plane

# Rational unit vectors from Pythagorean quadruples a^2 + b^2 + c^2 = d^2.
QUADS = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (0, 3, 4, 5), (0, 0, 1, 1)]


def random_unit(rng):
    a, b, c, d = rng.choice(QUADS)
    v = [F(a, d), F(b, d), F(c, d)]
    rng.shuffle(v)
    return tuple(x if rng.random() < 0.5 else -x for x in v)


def det3(a, b, c):
    return dot(a, cross(b, c))


def closed_form(n1, d1, n2, d2, r):
    """The reference: a point of the edge line, by Cramer's rule, plus
    r (n1 + n2) / (1 + n1 . n2)."""
    e = cross(n1, n2)
    D = det3(n1, n2, e)
    rhs = (d1, d2, 0)
    cols = []
    for k in range(3):
        m = [list(n1), list(n2), list(e)]
        for i in range(3):
            m[i][k] = rhs[i]
        cols.append(det3(*m) / D)
    p = tuple(cols)
    s = r / (1 + dot(n1, n2))
    c = tuple(p[i] + s * (n1[i] + n2[i]) for i in range(3))
    return p, e, c


def dist2_to_line(x, p, e):
    w = tuple(x[i] - p[i] for i in range(3))
    return dot(w, w) - dot(w, e) ** 2 / dot(e, e)


def test_two_planes_exact_against_closed_form():
    rng = random.Random(3)
    done = 0
    while done < 60:
        n1, n2 = random_unit(rng), random_unit(rng)
        e = cross(n1, n2)
        if e == (0, 0, 0):
            continue
        d1, d2 = F(rng.randint(-20, 20), rng.randint(1, 5)), F(rng.randint(-20, 20), rng.randint(1, 5))
        r = F(rng.randint(1, 12), rng.randint(1, 4))
        g1, dg1 = plane(n1, d1, r)
        g2, dg2 = plane(n2, d2, r)
        p, e, c = closed_form(n1, d1, n2, d2, r)
        x0 = tuple(c[i] + F(rng.randint(-9, 9), 7) for i in range(3))
        path = pencil_trace(g1, dg1, g2, dg2, x0, F(1, 3), 5, tol=0, normalize=False)
        for k, x in enumerate(path):
            # the center is on the closed-form line
            assert cross(tuple(x[i] - c[i] for i in range(3)), e) == (0, 0, 0)
            # at the distance r / sin(alpha / 2) from the edge: squared, 2 r^2 / (1 + n1 . n2)
            assert dist2_to_line(x, p, e) == 2 * r * r / (1 + dot(n1, n2))
            # the ball touches both planes, at x - r n_i
            q1, q2 = contacts(x, r, dg1, dg2)
            assert dot(n1, q1) == d1 and dot(n2, q2) == d2
            if k:
                step = tuple(x[i] - path[k - 1][i] for i in range(3))
                assert step != (0, 0, 0) and cross(step, e) == (0, 0, 0)
        done += 1


def test_floor_and_leaning_wall_example():
    # floor z = 0, and a wall through the line x = 10, z = 0 with normal (-4, 0, 3)/5
    r = F(5)
    n1, d1 = (F(0), F(0), F(1)), F(0)
    n2 = (F(-4, 5), F(0), F(3, 5))
    d2 = dot(n2, (F(10), F(0), F(0)))
    g1, dg1 = plane(n1, d1, r)
    g2, dg2 = plane(n2, d2, r)
    path = pencil_trace(g1, dg1, g2, dg2, (F(0), F(0), F(0)), F(1), 3, tol=0, normalize=False)
    for x in path:
        assert (x[0], x[2]) == (F(15, 2), F(5))
        q1, q2 = contacts(x, r, dg1, dg2)
        assert (q1[0], q1[2]) == (F(15, 2), F(0)) and (q2[0], q2[2]) == (F(23, 2), F(2))
    ys = [x[1] for x in path]
    assert len(set(ys)) == len(ys)


def test_pencil_center_is_the_deepest_admissible_center():
    # brute force: every center at distance >= r from both planes (the ball fits
    # in the wedge) is at least r / sin(alpha / 2) from the edge
    rng = random.Random(8)
    for _ in range(20):
        n1, n2 = random_unit(rng), random_unit(rng)
        if cross(n1, n2) == (0, 0, 0):
            continue
        n1f, n2f = tuple(map(float, n1)), tuple(map(float, n2))
        r = rng.uniform(0.5, 4.0)
        g1, dg1 = plane(n1f, 0.0, r)
        g2, dg2 = plane(n2f, 0.0, r)
        path = pencil_trace(g1, dg1, g2, dg2, (1.0, 2.0, 3.0), 0.5, 2)
        e = cross(n1f, n2f)
        best = dist2_to_line(path[0], (0.0, 0.0, 0.0), e)
        half = math.acos(-dot(n1f, n2f)) / 2  # alpha / 2, alpha the opening angle
        assert math.isclose(math.sqrt(best), r / math.sin(half), rel_tol=1e-9)
        for _ in range(2000):
            x = tuple(rng.uniform(-20, 20) for _ in range(3))
            if dot(n1f, x) >= r and dot(n2f, x) >= r:
                assert dist2_to_line(x, (0.0, 0.0, 0.0), e) >= best * (1 - 1e-9)


def test_floor_and_cylinder_wall_gives_a_circle():
    rho, r = 20.0, 3.0

    def g1(x):
        return x[2] - r

    def dg1(x):
        return (0.0, 0.0, 1.0)

    def g2(x):
        return rho - math.hypot(x[0], x[1]) - r

    def dg2(x):
        q = math.hypot(x[0], x[1])
        return (-x[0] / q, -x[1] / q, 0.0)

    h = 0.05
    m = int(2 * math.pi * (rho - r) / h)
    path = pencil_trace(g1, dg1, g2, dg2, (rho - r + 0.3, 0.1, r + 0.2), h, m)
    for x in path:
        assert abs(x[2] - r) <= 1e-9
        assert abs(math.hypot(x[0], x[1]) - (rho - r)) <= 1e-9
        q1, q2 = contacts(x, r, dg1, dg2)
        assert abs(q1[2]) <= 1e-9 and abs(math.hypot(q2[0], q2[1]) - rho) <= 1e-9
    # the steps follow the circle, so the path goes once round
    turn = 0.0
    for a, b in zip(path, path[1:]):
        turn += math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])
    assert abs(abs(turn) - m * h / (rho - r)) <= 1e-3
    assert abs(abs(turn) - 2 * math.pi) <= h / (rho - r)


def test_parallel_planes_have_no_pencil_curve():
    g1, dg1 = plane((0.0, 0.0, 1.0), 0.0, 1.0)
    g2, dg2 = plane((0.0, 0.0, -1.0), -10.0, 1.0)
    with pytest.raises(ValueError):
        pencil_trace(g1, dg1, g2, dg2, (0.0, 0.0, 5.0), 0.1, 3)
