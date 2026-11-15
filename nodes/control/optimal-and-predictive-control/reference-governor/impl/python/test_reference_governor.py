# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reference-governor/. The authors are listed in prov/JN3QT7.jsonl.

import itertools
import random
from fractions import Fraction as F

from reference_governor import _solve, admissible, build_admissible_set, governor_step, lp_max, run

# The example of the page: y = x1 / 2 follows v with the step response 0, 0, 0.5, 1, 1.25, 1.25, 1.125, ...
A = [[0, 1], [F(-1, 2), 1]]
B = [[0], [1]]
C = [[F(1, 2), 0]]
H = [[1], [-1]]
h = [F(11, 10), F(11, 10)]
EPS = F(1, 20)


def outputs(Am, Bm, Cm, x, v, steps):
    ys = []
    for _ in range(steps):
        ys.append(sum(c * xi for c, xi in zip(Cm[0], x)))
        x = [sum(a * xi for a, xi in zip(row, x)) + Bm[i][0] * v for i, row in enumerate(Am)]
    return ys


def random_schur(rng, n):
    while True:
        M = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        # Gershgorin: spectral radius below max row sum of |entries|; scale it to 0.8.
        s = max(sum(abs(v) for v in row) for row in M)
        M = [[0.8 * v / s for v in row] for row in M]
        b = [[rng.uniform(-1, 1)] for _ in range(n)]
        c = [[rng.uniform(-1, 1) for _ in range(n)]]
        # Steady state gain away from 0 so that references matter.
        I_A = [[(1 if i == j else 0) - M[i][j] for j in range(n)] for i in range(n)]
        g0 = sum(c[0][i] * _solve(I_A, b)[i][0] for i in range(n))
        if abs(g0) > 0.3:
            return M, b, c, g0


def test_lp_against_vertex_enumeration():
    rng = random.Random(4)
    for _ in range(40):
        k = rng.randint(3, 7)
        G = [[rng.uniform(-1, 1), rng.uniform(-1, 1)] for _ in range(k)]
        g = [rng.uniform(0.1, 1.0) for _ in range(k)]
        c = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        best = None
        for i, j in itertools.combinations(range(k), 2):
            det = G[i][0] * G[j][1] - G[i][1] * G[j][0]
            if abs(det) < 1e-9:
                continue
            z = [(g[i] * G[j][1] - G[i][1] * g[j]) / det, (G[i][0] * g[j] - g[i] * G[j][0]) / det]
            if all(G[r][0] * z[0] + G[r][1] * z[1] <= g[r] + 1e-9 for r in range(k)):
                val = c[0] * z[0] + c[1] * z[1]
                best = val if best is None else max(best, val)
        val = lp_max(c, G, g)
        # In the plane, the cone {d : G d <= 0} is spanned by directions along the lines G_i d = 0.
        dirs = [[s * G[i][1], -s * G[i][0]] for i in range(k) for s in (1, -1)] + [c]
        ray = any(all(G[r][0] * d[0] + G[r][1] * d[1] <= 1e-12 for r in range(k)) and c[0] * d[0] + c[1] * d[1] > 1e-12
                  for d in dirs)
        if val is None:
            assert ray
        else:
            assert not ray and best is not None and abs(val - best) < 1e-8


def test_lp_unbounded_and_exact():
    assert lp_max([1, 0], [[0, 1], [0, -1]], [1, 1]) is None
    assert lp_max([F(1), F(1)], [[1, 0], [0, 1], [-1, 0], [0, -1]], [F(1, 3), F(2, 7), 1, 1], tol=0) == F(13, 21)


def test_example_set_is_exact_and_small():
    rows, ts = build_admissible_set(A, B, C, None, H, h, EPS, tol=0)
    assert ts == 7 and len(rows) == 16
    # The row of t = 4 is the peak 1.25 v of the step response.
    assert ([F(-1, 8), 0, F(5, 4)], F(11, 10)) in rows


def test_membership_matches_simulation():
    rows, ts = build_admissible_set(A, B, C, None, H, h, EPS, tol=0)
    rng = random.Random(9)
    inside = outside = 0
    for _ in range(300):
        x = [F(rng.randint(-24, 24), 10), F(rng.randint(-24, 24), 10)]
        v = F(rng.randint(-12, 12), 10)
        ss_ok = abs(v) <= (1 - EPS) * h[0]
        ys = outputs(A, B, C, x, v, 60)
        ok = ss_ok and all(abs(y) <= h[0] for y in ys)
        assert admissible(rows, x, [v]) == ok
        # A violation, if any, happens before t_star.
        if ss_ok and not ok:
            assert any(abs(y) > h[0] for y in ys[:ts])
        inside += ok
        outside += not ok
    assert inside > 20 and outside > 20


def test_example_closed_loop():
    rows, _ = build_admissible_set(A, B, C, None, H, h, EPS, tol=0)
    xs, vs, ys, ks = run(A, B, C, None, rows, [0, 0], [0], [[1]] * 30)
    assert vs[0] == [F(22, 25)] and vs[3] == [F(22, 25)] and vs[4] == [1]
    assert max(y[0] for y in ys) == F(11, 10)
    assert all(vs[k][0] <= vs[k + 1][0] for k in range(29))
    assert abs(ys[-1][0] - 1) < 1e-3
    # Without the governor the output peaks at 1.25.
    assert max(outputs(A, B, C, [0, 0], 1, 12)) == F(5, 4)


def test_inadmissible_reference_stops_at_the_margin():
    Af = [[0.0, 1.0], [-0.5, 1.0]]
    rows, _ = build_admissible_set(Af, [[0.0], [1.0]], [[0.5, 0.0]], None, H, [1.1, 1.1], 0.05)
    xs, vs, ys, ks = run(Af, [[0.0], [1.0]], [[0.5, 0.0]], None, rows, [0.0, 0.0], [0.0], [[1.2]] * 40)
    assert max(abs(y[0]) for y in ys) <= 1.1 + 1e-12
    assert abs(vs[-1][0] - 1.045) < 1e-9


def test_random_loops_and_references():
    rng = random.Random(21)
    for _ in range(6):
        n = rng.choice([2, 3])
        M, b, c, g0 = random_schur(rng, n)
        hh = [1.0, 1.0]
        rows, ts = build_admissible_set(M, b, c, None, H, hh, 0.1)
        x = [0.0] * n
        v = [0.0]
        for k in range(60):
            if k % 15 == 0:
                r = [rng.uniform(-2.0, 2.0) / g0]
            assert admissible(rows, x, v, 1e-9)
            v, kappa = governor_step(rows, x, v, r)
            assert 0 <= kappa <= 1
            assert admissible(rows, x, v, 1e-9)
            y = sum(ci * xi for ci, xi in zip(c[0], x))
            assert abs(y) <= 1.0 + 1e-9
            x = [sum(a * xi for a, xi in zip(row, x)) + b[i][0] * v[0] for i, row in enumerate(M)]


def test_set_is_invariant_with_constant_v():
    rows, _ = build_admissible_set(A, B, C, None, H, h, EPS, tol=0)
    rng = random.Random(5)
    for _ in range(200):
        x = [F(rng.randint(-20, 20), 10), F(rng.randint(-20, 20), 10)]
        v = F(rng.randint(-10, 10), 10)
        if admissible(rows, x, [v]):
            x1 = [x[1], -x[0] / 2 + x[1] + v]
            assert admissible(rows, x1, [v])
            # kappa = 0 is always allowed, so the governor never gets stuck.
            assert governor_step(rows, x1, [v], [F(-3)])[1] >= 0
