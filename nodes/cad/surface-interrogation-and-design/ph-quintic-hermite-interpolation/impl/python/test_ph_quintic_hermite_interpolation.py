# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ph-quintic-hermite-interpolation/. The authors are listed in prov/XD0FDH.jsonl.

import cmath
import math
import random

from ph_quintic_hermite_interpolation import (
    absolute_rotation_index,
    arc_length,
    evaluate,
    fairest,
    hodograph,
    ph_quintic_hermite,
    speed,
)


def legendre_nodes(n):
    """Gauss-Legendre nodes and weights on [-1, 1], by Newton's method on P_n."""
    nodes, weights = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        p0, p1 = 1.0, x
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1)
        nodes.append(x)
        weights.append(2 / ((1 - x * x) * dp * dp))
    return nodes, weights


NODES, WEIGHTS = legendre_nodes(12)


def gauss(f, a, b, panels=16):
    """Composite Gauss-Legendre quadrature of f on [a, b]."""
    h = (b - a) / panels
    total = 0.0
    for j in range(panels):
        lo = a + j * h
        for x, wt in zip(NODES, WEIGHTS):
            total += wt * f(lo + (x + 1) * h / 2) * h / 2
    return total


def bezier_derivative(points, t):
    """r'(t) from the control points alone: 5 times the Bezier curve of the differences."""
    diffs = [5 * (points[i + 1] - points[i]) for i in range(5)]
    return evaluate(diffs, t)


def random_data(rng):
    def z():
        return complex(rng.uniform(-2, 2), rng.uniform(-2, 2))

    d0, d1 = z(), z()
    while abs(d0) < 0.2:
        d0 = z()
    while abs(d1) < 0.2:
        d1 = z()
    return z(), z(), d0, d1


def close(a, b, tol=1e-10):
    return abs(a - b) <= tol * (1 + abs(a) + abs(b))


def test_gauss_legendre_rule():
    assert close(gauss(lambda t: t**7, 0, 1, panels=1), 1 / 8, 1e-14)
    assert close(gauss(math.exp, 0, 1), math.e - 1, 1e-14)


def test_end_data():
    rng = random.Random(20260101)
    for _ in range(300):
        p0, p5, d0, d1 = random_data(rng)
        sols = ph_quintic_hermite(p0, p5, d0, d1)
        assert len(sols) == 4
        for q in sols:
            pts = q.points
            assert close(pts[0], p0) and close(pts[5], p5)
            assert close(5 * (pts[1] - pts[0]), d0)
            assert close(5 * (pts[5] - pts[4]), d1)
            assert close(evaluate(pts, 0.0), p0) and close(evaluate(pts, 1.0), p5)


def test_hodograph_is_square_of_w():
    rng = random.Random(7)
    for _ in range(100):
        sols = ph_quintic_hermite(*random_data(rng))
        for q in sols:
            for k in range(11):
                t = k / 10
                assert close(bezier_derivative(q.points, t), hodograph(q.w, t))


def test_speed_is_polynomial_and_matches_numerical_arc_length():
    rng = random.Random(31337)
    for _ in range(60):
        sols = ph_quintic_hermite(*random_data(rng))
        for q in sols:
            for k in range(21):
                t = k / 20
                assert close(speed(q.w, t), abs(bezier_derivative(q.points, t)))
            # Arc length by Gauss-Legendre on |r'(t)| computed from the control points.
            numeric = gauss(lambda t: abs(bezier_derivative(q.points, t)), 0.0, 1.0)
            assert close(arc_length(q.w), numeric, 1e-9)
            numeric_half = gauss(lambda t: abs(bezier_derivative(q.points, t)), 0.0, 0.37)
            assert close(arc_length(q.w, 0.37), numeric_half, 1e-9)


def test_four_distinct_solutions():
    rng = random.Random(99)
    for _ in range(200):
        sols = ph_quintic_hermite(*random_data(rng))
        for i in range(4):
            for j in range(i + 1, 4):
                assert sols[i].w != sols[j].w
                # Different w with the same w0 give different curves somewhere.
                diff = max(abs(evaluate(sols[i].points, k / 8) - evaluate(sols[j].points, k / 8)) for k in range(9))
                assert diff > 1e-9


def newton_reference(p0, p5, d0, d1, start):
    """Solve w2^2 = d1 and integral of w^2 = p5 - p0 for (w1, w2) by complex Newton."""
    w0 = cmath.sqrt(d0)
    w1, w2 = start
    delta = p5 - p0
    for _ in range(100):
        f1 = w2 * w2 - d1
        f2 = (w0 * w0 + w0 * w1 + (2 * w1 * w1 + w0 * w2) / 3 + w1 * w2 + w2 * w2) / 5 - delta
        a, b = 0, 2 * w2
        c, d = (w0 + 4 * w1 / 3 + w2) / 5, (w0 / 3 + w1 + 2 * w2) / 5
        det = a * d - b * c
        if det == 0:
            return None
        s1 = (d * f1 - b * f2) / det
        s2 = (a * f2 - c * f1) / det
        w1, w2 = w1 - s1, w2 - s2
        if abs(s1) + abs(s2) < 1e-14:
            return w1, w2
    return None


def test_against_newton_on_the_raw_equations():
    rng = random.Random(4242)
    for _ in range(25):
        data = random_data(rng)
        sols = ph_quintic_hermite(*data)
        found = set()
        for _ in range(60):
            start = (complex(rng.uniform(-4, 4), rng.uniform(-4, 4)), complex(rng.uniform(-4, 4), rng.uniform(-4, 4)))
            r = newton_reference(*data, start)
            if r is None:
                continue
            # Every root of the raw system is one of the four solutions.
            matches = [i for i, q in enumerate(sols) if abs(q.w[1] - r[0]) < 1e-8 and abs(q.w[2] - r[1]) < 1e-8]
            assert len(matches) == 1
            found.add(matches[0])
        assert found == {0, 1, 2, 3}


def test_worked_example():
    sols = ph_quintic_hermite(0, 1, 3j, -3j)
    good = sols[0]
    expected = (0, 0.6j, 0.3 + 0.9j, 0.7 + 0.9j, 1 + 0.6j, 1)
    assert all(close(a, b, 1e-14) for a, b in zip(good.points, expected))
    assert close(arc_length(good.w), 2.0, 1e-14)
    loop = sols[1]
    assert close(loop.w[1], -2 * math.sqrt(6), 1e-14)
    assert all(close(a, b, 1e-14) for a, b in zip(loop.points, (0, 0.6j, -1.2 - 0.6j, 2.2 - 0.6j, 1 + 0.6j, 1)))
    assert close(arc_length(loop.w), 2.0, 1e-14)
    assert close(arc_length(sols[2].w), 1.5, 1e-14) and close(arc_length(sols[3].w), 1.5, 1e-14)
    assert abs(absolute_rotation_index(good.w) - 0.5) < 1e-9
    assert abs(absolute_rotation_index(loop.w) - 1.5) < 1e-9
    assert fairest(sols) is good


def test_straight_line_data():
    sols = ph_quintic_hermite(0, 1, 1, 1)
    line = fairest(sols)
    assert all(close(line.w[i], 1, 1e-14) for i in range(3))
    for k in range(11):
        assert close(evaluate(line.points, k / 10), k / 10, 1e-14)


def test_invariance_under_similarity():
    rng = random.Random(5)
    for _ in range(50):
        p0, p5, d0, d1 = random_data(rng)
        a = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        b = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        base = {round(arc_length(q.w), 9) for q in ph_quintic_hermite(p0, p5, d0, d1)}
        moved = {round(arc_length(q.w) / abs(a), 9) for q in ph_quintic_hermite(a * p0 + b, a * p5 + b, a * d0, a * d1)}
        assert base == moved


def test_zero_derivative_rejected():
    try:
        ph_quintic_hermite(0, 1, 0, 1)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
