# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parks-mcclellan-algorithm/. The authors are listed in prov/6A2CCM.jsonl.

import math
import random

from parks_mcclellan_algorithm import amplitude, make_grid, max_error, parks_mcclellan_lowpass, weighted_error

SPECS = [
    (3, 0.3 * math.pi, 0.7 * math.pi, 1.0),
    (7, 0.3 * math.pi, 0.6 * math.pi, 1.0),
    (11, 0.3 * math.pi, 0.5 * math.pi, 1.0),
    (13, 0.4 * math.pi, 0.6 * math.pi, 1.0),
    (15, 0.4 * math.pi, 0.6 * math.pi, 10.0),
    (21, 0.4 * math.pi, 0.5 * math.pi, 1.0),
]


def grid_error(h, taps, wp, ws, k, density):
    grid, d, wt, _ = make_grid(taps, wp, ws, k, density)
    return [wt[j] * (d[j] - amplitude(h, grid[j])) for j in range(len(grid))]


def test_symmetric_coefficients() -> None:
    for taps, wp, ws, k in SPECS:
        h = parks_mcclellan_lowpass(taps, wp, ws, k).h
        assert len(h) == taps
        assert all(abs(h[n] - h[taps - 1 - n]) < 1e-15 for n in range(taps))


def test_alternation() -> None:
    """At the optimum the weighted error reaches |delta| at L + 2 points with alternating signs."""
    for taps, wp, ws, k in SPECS:
        density = 16
        des = parks_mcclellan_lowpass(taps, wp, ws, k, density=density)
        half = (taps - 1) // 2
        delta = abs(des.delta)
        assert len(des.extremals) == half + 2
        errs = [weighted_error(des.h, w, wp, ws, k) for w in des.extremals]
        assert all(abs(abs(e) - delta) < 1e-9 for e in errs)
        assert all(u * v < 0 for u, v in zip(errs, errs[1:]))
        # the levelled error is the largest error on the grid
        assert max(abs(e) for e in grid_error(des.h, taps, wp, ws, k, density)) <= delta * (1 + 1e-9)


def test_dense_grid_close_to_delta() -> None:
    """Off the design grid the error can exceed |delta| only by a little."""
    for taps, wp, ws, k in SPECS:
        des = parks_mcclellan_lowpass(taps, wp, ws, k, density=32)
        e = max_error(des.h, wp, ws, k)
        assert abs(des.delta) <= e <= abs(des.delta) * 1.01


def test_no_perturbation_does_better() -> None:
    """The weighted max error is convex in h; random perturbations of the optimum never lower it."""
    rng = random.Random(8101)
    for taps, wp, ws, k in SPECS:
        density = 16
        des = parks_mcclellan_lowpass(taps, wp, ws, k, density=density)
        best = max(abs(e) for e in grid_error(des.h, taps, wp, ws, k, density))
        half = (taps - 1) // 2
        for _ in range(60):
            scale = 10 ** rng.uniform(-6, -1)
            g = list(des.h)
            for j in range(half + 1):
                dv = rng.gauss(0, scale)
                g[half - j] += dv
                if j:
                    g[half + j] += dv
            other = max(abs(e) for e in grid_error(g, taps, wp, ws, k, density))
            assert other >= best * (1 - 1e-9)


def test_three_taps_against_brute_force() -> None:
    """For N = 3, A(w) = a0 + a1 cos w. A search over a1 with the best a0 finds the minimax pair on a dense grid."""
    wp, ws = 0.3 * math.pi, 0.7 * math.pi
    pts = [wp * i / 2000 for i in range(2001)] + [ws + (math.pi - ws) * i / 2000 for i in range(2001)]
    desired = [1.0] * 2001 + [0.0] * 2001
    cosines = [math.cos(w) for w in pts]

    def best_a0(a1):
        # for a fixed a1 the residuals r_j = d_j - a1 cos w_j are fixed; the best a0 is their midrange
        r = [d - a1 * c for d, c in zip(desired, cosines)]
        return (max(r) - min(r)) / 2

    lo, hi = -2.0, 3.0
    for _ in range(100):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if best_a0(m1) < best_a0(m2):
            hi = m2
        else:
            lo = m1
    brute = best_a0((lo + hi) / 2)
    des = parks_mcclellan_lowpass(3, wp, ws, density=200)
    pm = max_error(des.h, wp, ws)
    assert pm <= brute + 1e-9
    assert abs(pm - brute) < 1e-9
    # Alternation at wp, ws and pi with cos ws = -cos wp = -c gives delta = (1 - c) / (2 (1 + c)).
    c = math.cos(wp)
    assert abs(pm - (1 - c) / (2 * (1 + c))) < 1e-12


def test_more_taps_lower_error() -> None:
    wp, ws = 0.3 * math.pi, 0.5 * math.pi
    errs = [abs(parks_mcclellan_lowpass(n, wp, ws).delta) for n in (9, 13, 17, 21, 25)]
    assert all(u > v for u, v in zip(errs, errs[1:]))


def test_weight_trades_errors() -> None:
    """With stop band weight K the stop band ripple is the pass band ripple divided by K."""
    wp, ws = 0.4 * math.pi, 0.6 * math.pi
    des = parks_mcclellan_lowpass(15, wp, ws, 10.0)
    pts = [wp * i / 5000 for i in range(5001)]
    sts = [ws + (math.pi - ws) * i / 5000 for i in range(5001)]
    dp = max(abs(1 - amplitude(des.h, w)) for w in pts)
    ds = max(abs(amplitude(des.h, w)) for w in sts)
    assert abs(dp / ds - 10.0) < 0.2
