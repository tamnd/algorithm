# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-boor-algorithm/. The authors are listed in prov/TVCVSK.jsonl.

import random
from fractions import Fraction

import pytest

from de_boor_algorithm import de_boor, find_span, nurbs_point


def cox_de_boor(knots, i, p, u):
    """N_(i,p)(u) by the Cox-de Boor recursion, with 0/0 = 0 and half-open spans."""
    if p == 0:
        return Fraction(1) if knots[i] <= u < knots[i + 1] else Fraction(0)
    total = Fraction(0)
    if knots[i + p] != knots[i]:
        total += Fraction(u - knots[i]) / (knots[i + p] - knots[i]) * cox_de_boor(knots, i, p - 1, u)
    if knots[i + p + 1] != knots[i + 1]:
        total += (
            Fraction(knots[i + p + 1] - u)
            / (knots[i + p + 1] - knots[i + 1])
            * cox_de_boor(knots, i + 1, p - 1, u)
        )
    return total


def direct_sum(knots, p, ctrl, u):
    """The reference: sum_i N_(i,p)(u) P_i over all control points."""
    dim = len(ctrl[0])
    out = [Fraction(0)] * dim
    for i, pt in enumerate(ctrl):
        b = cox_de_boor(knots, i, p, u)
        for k in range(dim):
            out[k] += b * pt[k]
    return tuple(out)


def random_case(rng, dim=2):
    p = rng.randint(0, 4)
    n = rng.randint(p, p + 5)
    while True:
        knots = sorted(rng.randint(0, 6) for _ in range(n + p + 2))
        if max(knots.count(v) for v in knots) <= p + 1 and knots[p] < knots[n + 1]:
            break
    ctrl = [tuple(Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(dim)) for _ in range(n + 1)]
    return p, n, knots, ctrl


def test_example_of_the_page():
    knots = [0, 0, 0, 1, 2, 3, 3, 3]
    ctrl = [(0, 0), (1, 2), (3, 3), (5, 1), (6, 0)]
    assert de_boor(knots, 2, ctrl, Fraction(3, 2)) == (Fraction(3), Fraction(21, 8))
    assert de_boor(knots, 2, ctrl, 0) == (0, 0)
    assert de_boor(knots, 2, ctrl, 3) == (6, 0)


def test_against_the_direct_cox_de_boor_sum():
    rng = random.Random(11)
    for _ in range(700):
        p, n, knots, ctrl = random_case(rng, dim=rng.randint(1, 3))
        u = knots[p] + Fraction(rng.randint(0, 12 * (knots[n + 1] - knots[p]) - 1), 12)
        assert de_boor(knots, p, ctrl, u) == direct_sum(knots, p, ctrl, u)


def test_end_points_of_a_clamped_curve():
    rng = random.Random(12)
    for _ in range(200):
        p = rng.randint(1, 4)
        n = rng.randint(p, p + 4)
        inner = sorted(Fraction(rng.randint(1, 9), 10) for _ in range(n - p))
        knots = [0] * (p + 1) + inner + [1] * (p + 1)
        ctrl = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(n + 1)]
        assert de_boor(knots, p, ctrl, 0) == ctrl[0]
        assert de_boor(knots, p, ctrl, 1) == ctrl[-1]


def test_span_lies_in_the_hull_of_its_active_points():
    # In one dimension: C(u) lies between the min and max of P_(mu-p..mu).
    rng = random.Random(13)
    for _ in range(500):
        p, n, knots, ctrl = random_case(rng, dim=1)
        u = knots[p] + Fraction(rng.randint(0, 7 * (knots[n + 1] - knots[p]) - 1), 7)
        mu = find_span(knots, p, u)
        active = [c[0] for c in ctrl[mu - p : mu + 1]]
        assert min(active) <= de_boor(knots, p, ctrl, u)[0] <= max(active)


def quarter_arc_circle():
    """A full unit circle as a quadratic NURBS with four arcs and rational weights.

    Each arc is x = (1 - s^2)/(1 + s^2), y = 2s/(1 + s^2) turned by 90 degrees,
    with weights (1, 1, 2) times a power of 2 so that the arcs share weights.
    """
    pts = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]
    weights = [1, 1, 2, 2, 4, 4, 8, 8, 16]
    knots = [0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4]
    return knots, pts, weights


def test_nurbs_circle_satisfies_the_implicit_equation():
    knots, pts, weights = quarter_arc_circle()
    rng = random.Random(14)
    params = {Fraction(k, 8) for k in range(33)}
    params |= {Fraction(rng.randint(0, 4000), 1000) for _ in range(500)}
    for u in params:
        x, y = nurbs_point(knots, 2, pts, weights, u)
        assert x * x + y * y == 1
    assert nurbs_point(knots, 2, pts, weights, Fraction(1, 2)) == (Fraction(3, 5), Fraction(4, 5))


def barycentric(pt, a, b, c):
    """Exact barycentric coordinates of pt in the triangle a, b, c."""
    det = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
    l1 = ((pt[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (pt[1] - a[1])) / det
    l2 = ((b[0] - a[0]) * (pt[1] - a[1]) - (pt[0] - a[0]) * (b[1] - a[1])) / det
    return 1 - l1 - l2, l1, l2


def test_rational_quadratic_is_a_conic():
    # For weights w0, w1, w2 the curve satisfies w0 w2 tau1^2 = 4 w1^2 tau0 tau2
    # in barycentric coordinates of the control triangle: an ellipse when
    # w1^2 < w0 w2, a parabola when equal, a hyperbola when greater.
    rng = random.Random(15)
    knots = [0, 0, 0, 1, 1, 1]
    for _ in range(500):
        while True:
            tri = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(3)]
            a, b, c = tri
            if (b[0] - a[0]) * (c[1] - a[1]) != (c[0] - a[0]) * (b[1] - a[1]):
                break
        w = [Fraction(rng.randint(1, 9), rng.randint(1, 9)) for _ in range(3)]
        u = Fraction(rng.randint(0, 100), 100)
        pt = nurbs_point(knots, 2, tri, w, u)
        t0, t1, t2 = barycentric(pt, a, b, c)
        assert w[0] * w[2] * t1 * t1 == 4 * w[1] * w[1] * t0 * t2


def test_unit_weights_give_the_polynomial_curve():
    rng = random.Random(16)
    for _ in range(300):
        p, n, knots, ctrl = random_case(rng)
        u = knots[p] + Fraction(rng.randint(0, 5 * (knots[n + 1] - knots[p]) - 1), 5)
        assert nurbs_point(knots, p, ctrl, [1] * (n + 1), u) == de_boor(knots, p, ctrl, u)


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        de_boor([0, 0, 1, 1], 1, [(0,), (1,), (2,)], 0)
    with pytest.raises(ValueError):
        de_boor([0, 0, 1, 1], 1, [(0,), (1,)], 2)
    with pytest.raises(ValueError):
        nurbs_point([0, 0, 1, 1], 1, [(0,), (1,)], [1, 0], 0)
