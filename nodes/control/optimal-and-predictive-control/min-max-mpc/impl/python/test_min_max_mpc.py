# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-max-mpc/. The authors are listed in prov/SE9461.jsonl.

import itertools
import random
from fractions import Fraction as Fr

import pytest

from min_max_mpc import closed_loop, lp_min, min_max_mpc, path_cost

# The example of the page: x+ = 1.2 x + u + w, |w| <= 0.2, |u| <= 1, |x_N| <= 0.5.
A = [[Fr(6, 5)]]
B = [[1]]
V = [[Fr(-1, 5)], [Fr(1, 5)]]
Q = [[1]]
R = [[Fr(1, 10)]]
P = [[3]]
REST = ([10], [1], [[1], [-1]], [Fr(1, 2), Fr(1, 2)])


def test_lp_small_cases():
    # min x + y with x + y >= 1, x - y = 1/3, both free: value 1 at x = 2/3.
    val, z = lp_min([1, 1], [[-1, -1]], [-1], [[1, -1]], [Fr(1, 3)], tol=0)
    assert val == 1 and z == [Fr(2, 3), Fr(1, 3)]
    assert lp_min([1], [[1], [-1]], [-1, -1], tol=0) is None
    with pytest.raises(ValueError):
        lp_min([1], [[1]], [1], tol=0)


def test_lp_against_vertex_enumeration():
    rng = random.Random(7)
    for _ in range(40):
        k = rng.randint(1, 5)
        G = [[rng.uniform(-1, 1), rng.uniform(-1, 1)] for _ in range(k)]
        g = [rng.uniform(-0.5, 1.0) for _ in range(k)]
        G += [[1, 0], [-1, 0], [0, 1], [0, -1]]
        g += [1, 1, 1, 1]
        c = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        best = None
        for i, j in itertools.combinations(range(len(G)), 2):
            det = G[i][0] * G[j][1] - G[i][1] * G[j][0]
            if abs(det) < 1e-9:
                continue
            z = [(g[i] * G[j][1] - G[i][1] * g[j]) / det, (G[i][0] * g[j] - g[i] * G[j][0]) / det]
            if all(r[0] * z[0] + r[1] * z[1] <= b + 1e-9 for r, b in zip(G, g)):
                v = c[0] * z[0] + c[1] * z[1]
                best = v if best is None else min(best, v)
        sol = lp_min(c, G, g)
        assert (sol is None) == (best is None)
        if sol is not None:
            assert abs(sol[0] - best) < 1e-8


def test_example_values_are_exact():
    got = {}
    for N, x0 in [(1, 0), (1, Fr(1, 2)), (2, 0), (2, Fr(1, 2))]:
        fb = min_max_mpc(A, B, [x0], N, V, Q, R, P, *REST, feedback=True, tol=0)
        ol = min_max_mpc(A, B, [x0], N, V, Q, R, P, *REST, feedback=False, tol=0)
        got[N, x0] = (fb[0], ol[0], fb[1][0])
    assert got[1, 0] == (Fr(3, 5), Fr(3, 5), 0)
    assert got[1, Fr(1, 2)] == (Fr(29, 25), Fr(29, 25), Fr(-3, 5))
    assert got[2, 0] == (Fr(103, 125), Fr(38, 25), 0)
    assert got[2, Fr(1, 2)] == (Fr(173, 125), Fr(52, 25), Fr(-3, 5))
    # With N = 3 the open-loop spread 0.2 (1.44 + 1.2 + 1) = 0.728 does not fit in |x_3| <= 0.5.
    Af, Vf, Rf = [[1.2]], [[-0.2], [0.2]], [[0.1]]
    rest = ([10.0], [1.0], [[1.0], [-1.0]], [0.5, 0.5])
    assert min_max_mpc(Af, B, [0.0], 3, Vf, Q, Rf, P, *rest, feedback=False) is None
    assert abs(min_max_mpc(Af, B, [0.0], 3, Vf, Q, Rf, P, *rest)[0] - 131 / 125) < 1e-9


def scalar_value(a, b, x, k, N, ws, q, r, p, xmax, umax, f, step):
    """Worst-case cost to go from x at depth k, by dynamic programming over u."""
    if abs(x) > xmax + 1e-12:
        return float("inf")
    if k == N:
        return p * abs(x) if abs(x) <= f + 1e-12 else float("inf")
    if k == N - 1:
        # The cost is convex and piecewise linear in u, so the minimum is at a breakpoint.
        bound = min(xmax, f)
        lo = max(-umax, max((-bound - a * x - w) / b if b > 0 else (bound - a * x - w) / b for w in ws))
        hi = min(umax, min((bound - a * x - w) / b if b > 0 else (-bound - a * x - w) / b for w in ws))
        if lo > hi + 1e-12:
            return float("inf")
        # Kinks of |u|, of each |a x + b u + w|, and where two branches of the max cross.
        cands = [lo, hi, 0.0] + [(-a * x - w) / b for w in ws]
        cands += [(-a * x - (w1 + w2) / 2) / b for w1 in ws for w2 in ws]
        cands = [min(hi, max(lo, u)) for u in cands]
        return q * abs(x) + min(r * abs(u) + max(p * abs(a * x + b * u + w) for w in ws) for u in cands)
    best = float("inf")
    for i in range(int(round(2 * umax / step)) + 1):
        u = -umax + i * step
        v = r * abs(u) + max(scalar_value(a, b, a * x + b * u + w, k + 1, N, ws, q, r, p, xmax, umax, f, step)
                             for w in ws)
        best = min(best, v)
    return q * abs(x) + best


def test_dynamic_programming_brute_force():
    rng = random.Random(11)
    for _ in range(6):
        a, b = rng.uniform(0.6, 1.5), rng.choice([-1, 1]) * rng.uniform(0.6, 1.4)
        wb = rng.uniform(0.05, 0.25)
        q, r, p = rng.uniform(0.2, 1), rng.uniform(0.05, 0.5), rng.uniform(1, 3)
        x0 = rng.uniform(-1.5, 1.5)
        N = rng.choice([1, 2])
        sol = min_max_mpc([[a]], [[b]], [x0], N, [[-wb], [wb]], [[q]], [[r]], [[p]],
                          [3.0], [1.0], [[1.0], [-1.0]], [0.5, 0.5])
        dp = scalar_value(a, b, x0, 0, N, [-wb, wb], q, r, p, 3.0, 1.0, 0.5, 0.002)
        if sol is None:
            assert dp == float("inf")
        else:
            assert sol[0] <= dp + 1e-9
            assert dp <= sol[0] + (1e-9 if N == 1 else 0.02)


def test_feedback_never_worse_than_open_loop():
    rng = random.Random(2)
    Af, Vf, Rf = [[1.2]], [[-0.2], [0.2]], [[0.1]]
    rest = ([10.0], [1.0], [[1.0], [-1.0]], [0.5, 0.5])
    for _ in range(10):
        x0 = rng.uniform(-1.5, 1.5)
        fb = min_max_mpc(Af, B, [x0], 2, Vf, Q, Rf, P, *rest)
        ol = min_max_mpc(Af, B, [x0], 2, Vf, Q, Rf, P, *rest, feedback=False)
        assert fb is not None and ol is not None
        assert fb[0] <= ol[0] + 1e-9
        # The open-loop value is the worst case of the open-loop inputs over the vertex sequences.
        us = [ol[2][("u",) + (0,) * k] for k in range(2)]
        worst = max(path_cost(Af, B, [x0], us, ws, Q, Rf, P)[0] for ws in itertools.product(Vf, repeat=2))
        assert abs(worst - ol[0]) < 1e-9


def test_vertex_policy_covers_the_whole_disturbance_set():
    # Interpolating the vertex controls gives a causal policy for every w in the hull,
    # and its cost never exceeds the min-max value (two states, four vertices).
    rng = random.Random(5)
    A2 = [[1.0, 0.5], [0.0, 1.0]]
    B2 = [[0.125], [0.5]]
    V2 = [[0.05 * s, 0.05 * t] for s in (-1, 1) for t in (-1, 1)]
    Q2 = [[1.0, 0.0], [0.0, 1.0]]
    R2 = [[0.2]]
    P2 = [[2.0, 1.0], [0.0, 2.0]]
    F2 = [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]
    f2 = [0.6, 0.6, 0.6, 0.6]
    x0 = [0.4, -0.3]
    val, u0, tree = min_max_mpc(A2, B2, x0, 2, V2, Q2, R2, P2, [2.0, 2.0], [1.0], F2, f2)
    for _ in range(30):
        lam = [[rng.random() for _ in V2] for _ in range(2)]
        lam = [[v / sum(row) for v in row] for row in lam]
        ws = [[sum(l * vv[i] for l, vv in zip(row, V2)) for i in range(2)] for row in lam]
        u1 = [sum(lam[0][i] * tree[("u", i)][0] for i in range(4))]
        J, xN = path_cost(A2, B2, x0, [u0, u1], ws, Q2, R2, P2)
        assert J <= val + 1e-9
        assert all(sum(a * x for a, x in zip(row, xN)) <= b + 1e-9 for row, b in zip(F2, f2))
        assert abs(u1[0]) <= 1 + 1e-12


def test_closed_loop_stays_feasible():
    Af, Vf, Rf = [[1.2]], [[-0.2], [0.2]], [[0.1]]
    rest = ([10.0], [1.0], [[1.0], [-1.0]], [0.5, 0.5])
    rng = random.Random(3)
    ws = [[rng.uniform(-0.2, 0.2)] for _ in range(12)]
    xs, us, vals = closed_loop(Af, B, [1.5], 2, Vf, Q, Rf, P, *rest, ws)
    assert all(abs(u[0]) <= 1 + 1e-9 for u in us)
    assert all(abs(x[0]) <= 0.5 + 1e-9 for x in xs[2:])
    xs, us, vals = closed_loop(Af, B, [1.0], 2, Vf, Q, Rf, P, *rest, [[0.0]] * 4)
    assert abs(xs[1][0] - 0.2) < 1e-9 and all(abs(x[0]) < 1e-9 for x in xs[2:])
