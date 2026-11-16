# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-snap-trajectory/. The authors are listed in prov/GASDKD.jsonl.
"""Tests: constraints, the one-segment closed form, the two methods agree, natural continuity, and perturbations."""

import random
from fractions import Fraction as F

from minimum_snap_trajectory import _hermite_inverse, min_snap, min_snap_free_derivatives, poly_eval, snap_cost


def test_one_segment_closed_form():
    # Rest to rest from 0 to 1 in time 1: s = 35 t^4 - 84 t^5 + 70 t^6 - 20 t^7.
    c = min_snap([F(0), F(1)], [F(1)])[0]
    assert c == [0, 0, 0, 0, 35, -84, 70, -20]
    assert snap_cost([c], [F(1)]) == 100800
    assert poly_eval(c, F(1, 2), 1) == F(35, 16)


def test_constraints_exact():
    w = [F(0), F(2), F(-1), F(3)]
    T = [F(1), F(2), F(1)]
    cs = min_snap(w, T)
    for i, c in enumerate(cs):
        assert poly_eval(c, F(0)) == w[i] and poly_eval(c, T[i]) == w[i + 1]
    for d in (1, 2, 3):
        assert poly_eval(cs[0], F(0), d) == 0 and poly_eval(cs[-1], T[-1], d) == 0


def test_natural_continuity_up_to_six():
    # Only derivatives 1 to 3 are forced to be continuous; the optimum makes 4, 5 and 6 continuous too.
    w = [F(0), F(1), F(3), F(2)]
    T = [F(1), F(1), F(2)]
    cs = min_snap(w, T)
    for i in range(len(T) - 1):
        for d in range(1, 7):
            assert poly_eval(cs[i], T[i], d) == poly_eval(cs[i + 1], F(0), d)
    # The seventh derivative jumps in general.
    assert any(poly_eval(cs[i], T[i], 7) != poly_eval(cs[i + 1], F(0), 7) for i in range(2))


def test_two_methods_agree():
    rng = random.Random(41)
    for m in (1, 2, 3):
        w = [F(rng.randint(-5, 5)) for _ in range(m + 1)]
        T = [F(rng.randint(1, 3), rng.randint(1, 2)) for _ in range(m)]
        assert min_snap(w, T) == min_snap_free_derivatives(w, T)


def test_perturbations_cost_more():
    # Change the free derivatives at the inner waypoints: the cost grows.
    w = [F(0), F(1), F(-1)]
    T = [F(1), F(1)]
    best = min_snap(w, T)
    base = snap_cost(best, T)
    rng = random.Random(42)
    for _ in range(5):
        dv, da, dj = (F(rng.randint(-3, 3), 4) for _ in range(3))
        if not (dv or da or dj):
            continue
        # A feasible trajectory: Hermite segments with shifted inner derivatives.
        knot = [poly_eval(best[0], T[0], d) for d in range(4)]
        knot = [knot[0], knot[1] + dv, knot[2] + da, knot[3] + dj]
        segs = []
        ends = [[w[0], F(0), F(0), F(0)], knot, [w[2], F(0), F(0), F(0)]]
        for i in range(2):
            minv = _hermite_inverse(T[i])
            d = ends[i] + ends[i + 1]
            segs.append([sum(minv[r][c] * d[c] for c in range(8)) for r in range(8)])
        assert snap_cost(segs, T) > base


def test_float_inputs():
    cs = min_snap([0.0, 1.0, 0.5], [1.0, 1.5])
    assert abs(poly_eval(cs[1], 1.5) - 0.5) < 1e-9
    assert abs(poly_eval(cs[0], 1.0, 2) - poly_eval(cs[1], 0.0, 2)) < 1e-9


def test_bad_input():
    try:
        min_snap([F(0)], [F(1)])
    except ValueError:
        pass
    else:
        raise AssertionError("wrong number of waypoints must fail")
