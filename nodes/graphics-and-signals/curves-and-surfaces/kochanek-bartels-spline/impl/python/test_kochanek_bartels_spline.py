# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kochanek-bartels-spline/. The authors are listed in prov/9M4696.jsonl.

import random
from fractions import Fraction as F

from kochanek_bartels_spline import kb_curve, kb_tangents, one_sided_velocity


def rp(rng, d=2):
    return tuple(F(rng.randint(-30, 30), rng.randint(1, 5)) for _ in range(d))


def rpar(rng):
    return tuple(F(rng.randint(-4, 4), 4) for _ in range(3))


def catmull_rom(p0, p1, p2, p3, u):
    """Reference: the uniform Catmull-Rom segment in matrix form."""
    w = (-u * (1 - u) ** 2 / 2, (3 * u ** 3 - 5 * u ** 2 + 2) / 2, (-3 * u ** 3 + 4 * u ** 2 + u) / 2, -u ** 2 * (1 - u) / 2)
    return tuple(sum(wk * p[k] for wk, p in zip(w, (p0, p1, p2, p3))) for k in range(len(p0)))


def keys(rng, n, d=2):
    return [rp(rng, d) for _ in range(n + 1)]


def test_zero_parameters_give_catmull_rom():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(3, 5)
        pts = keys(rng, n, rng.choice([2, 3]))
        params = [(0, 0, 0)] * (n + 1)
        s = F(rng.randint(10, 10 * (n - 1)), 10)
        i = min(int(s), n - 2)
        assert kb_curve(pts, params, s) == catmull_rom(*pts[i - 1 : i + 3], s - i)


def test_interpolates_keys_and_c1_when_continuity_zero():
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randint(3, 5)
        pts = keys(rng, n)
        params = [(rpar(rng)[0], F(0), rpar(rng)[2]) for _ in range(n + 1)]
        for k in range(1, n):
            assert kb_curve(pts, params, F(k)) == pts[k]
        for k in range(2, n - 1):
            assert one_sided_velocity(pts, params, k, "left") == one_sided_velocity(pts, params, k, "right")


def test_continuity_parameter_breaks_c1_by_the_tangent_difference():
    rng = random.Random(3)
    jumps = 0
    for _ in range(500):
        n = 4
        pts = keys(rng, n)
        params = [rpar(rng) for _ in range(n + 1)]
        left = one_sided_velocity(pts, params, 2, "left")
        right = one_sided_velocity(pts, params, 2, "right")
        tin, tout = kb_tangents(pts[1], pts[2], pts[3], *params[2])
        assert left == tin and right == tout
        # Reference: T_out - T_in = (1 - t) c ((1 + b) Din - (1 - b) Dout).
        t, c, b = params[2]
        din = tuple(y - x for x, y in zip(pts[1], pts[2]))
        dout = tuple(y - x for x, y in zip(pts[2], pts[3]))
        want = tuple((1 - t) * c * ((1 + b) * x - (1 - b) * y) for x, y in zip(din, dout))
        assert tuple(o - i for o, i in zip(tout, tin)) == want
        jumps += left != right
    assert jumps > 0


def test_special_values():
    rng = random.Random(4)
    for _ in range(500):
        pts = keys(rng, 3)
        u = F(rng.randint(0, 20), 20)
        a, b = pts[1], pts[2]
        # Tension 1: zero tangents, the point moves on the chord and stops at the keys.
        on = kb_curve(pts, [(1, 0, 0)] * 4, 1 + u)
        h3 = -2 * u ** 3 + 3 * u ** 2
        assert on == tuple(x + h3 * (y - x) for x, y in zip(a, b))
        # Continuity -1 with t = b = 0: the chord at constant speed.
        lin = kb_curve(pts, [(0, -1, 0)] * 4, 1 + u)
        assert lin == tuple(x + u * (y - x) for x, y in zip(a, b))


def test_timed_keys_are_c1_in_time_when_continuity_zero():
    rng = random.Random(5)
    for _ in range(500):
        n = rng.randint(3, 5)
        pts = keys(rng, n)
        times = [F(0)]
        for _ in range(n):
            times.append(times[-1] + F(rng.randint(1, 20), rng.randint(1, 4)))
        params = [(rpar(rng)[0], F(0), rpar(rng)[2]) for _ in range(n + 1)]
        for k in range(1, n):
            assert kb_curve(pts, params, times[k], times) == pts[k]
        for k in range(2, n - 1):
            assert one_sided_velocity(pts, params, k, "left", times) == one_sided_velocity(pts, params, k, "right", times)


def test_worked_example():
    pts = [(F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(2), F(1))]
    assert kb_tangents(*pts[0:3]) == ((F(1, 2), F(1, 2)), (F(1, 2), F(1, 2)))
    assert kb_tangents(*pts[0:3], 0, F(-1, 2), 0) == ((F(3, 4), F(1, 4)), (F(1, 4), F(3, 4)))
    assert kb_tangents(*pts[0:3], 0, 0, F(1, 2)) == ((F(3, 4), F(1, 4)), (F(3, 4), F(1, 4)))
    assert kb_tangents(*pts[0:3], F(1, 2), 0, 0) == ((F(1, 4), F(1, 4)), (F(1, 4), F(1, 4)))
