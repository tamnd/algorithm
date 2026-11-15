# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-mpc/. The authors are listed in prov/1PY7EN.jsonl.

import itertools
import math
import random

from ctlmat import solve
from hybrid_mpc import (
    closed_loop,
    condense,
    mld_rows_hold,
    mode_of,
    mpc_step,
    predict,
    pwa_step,
    pwa_to_mld,
    qp_cost,
    qp_solve,
    rotation_example,
)

I2 = [[1.0, 0.0], [0.0, 1.0]]
R = [[0.1]]
UMIN, UMAX = [-1.0], [1.0]
XMIN, XMAX = [-10.0, -10.0], [10.0, 10.0]
MODES = rotation_example(1.2)


def random_pd(rng, n):
    m = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    return [[sum(m[k][i] * m[k][j] for k in range(n)) + (0.5 if i == j else 0.0) for j in range(n)] for i in range(n)]


def random_qp(rng, n, k):
    h = random_pd(rng, n)
    f = [rng.uniform(-2, 2) for _ in range(n)]
    c = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(k)]
    x0 = [rng.uniform(-1, 1) for _ in range(n)]
    # Make x0 strictly feasible, so the QP is feasible.
    b = [sum(a * v for a, v in zip(row, x0)) + rng.uniform(0.05, 1.0) for row in c]
    return h, f, c, b


def check_kkt(h, f, c, b, x, lam, tol=1e-7):
    grad = [sum(h[i][j] * x[j] for j in range(len(x))) + f[i] + sum(c[k][i] * lam[k] for k in range(len(c))) for i in range(len(x))]
    assert max(abs(g) for g in grad) < tol
    for row, bi, li in zip(c, b, lam):
        s = bi - sum(a * v for a, v in zip(row, x))
        assert s > -tol and li > -tol and abs(s * li) < tol


def brute_force_qp(h, f, c, b):
    """Try every active set of size at most n; keep the best KKT point."""
    n = len(f)
    best = None
    for size in range(n + 1):
        for act in itertools.combinations(range(len(c)), size):
            kkt = [[0.0] * (n + size) for _ in range(n + size)]
            rhs = [-v for v in f] + [b[i] for i in act]
            for i in range(n):
                for j in range(n):
                    kkt[i][j] = h[i][j]
                for t, a in enumerate(act):
                    kkt[i][n + t] = c[a][i]
                    kkt[n + t][i] = c[a][i]
            try:
                sol = solve(kkt, rhs)
            except ValueError:
                continue
            x, mult = sol[:n], sol[n:]
            if min(mult, default=0.0) < -1e-9:
                continue
            if any(sum(a * v for a, v in zip(row, x)) > bi + 1e-9 for row, bi in zip(c, b)):
                continue
            val = qp_cost(h, f, x)
            if best is None or val < best:
                best = val
    return best


def test_qp_kkt_on_random_problems():
    rng = random.Random(1)
    for _ in range(200):
        n, k = rng.randint(1, 4), rng.randint(0, 8)
        h, f, c, b = random_qp(rng, n, k)
        x, lam = qp_solve(h, f, c, b)
        check_kkt(h, f, c, b, x, lam)


def test_qp_matches_active_set_enumeration():
    rng = random.Random(2)
    for _ in range(100):
        n, k = rng.randint(1, 3), rng.randint(1, 7)
        h, f, c, b = random_qp(rng, n, k)
        x, _ = qp_solve(h, f, c, b)
        assert abs(qp_cost(h, f, x) - brute_force_qp(h, f, c, b)) < 1e-8


def test_qp_detects_infeasibility():
    h, f = [[1.0]], [0.0]
    assert qp_solve(h, f, [[1.0], [-1.0]], [-1.0, -1.0]) is None  # x <= -1 and x >= 1
    h2 = [[2.0, 0.0], [0.0, 1.0]]
    c = [[1.0, 1.0], [-1.0, 0.0], [0.0, -1.0]]
    assert qp_solve(h2, [0.0, 0.0], c, [-1.0, 0.0, 0.0]) is None  # x + y <= -1 with x, y >= 0


def test_condensed_prediction_matches_simulation():
    rng = random.Random(3)
    for _ in range(20):
        seq = tuple(rng.randint(0, 1) for _ in range(4))
        x0 = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        us = [[rng.uniform(-1, 1)] for _ in range(4)]
        d, gam = condense(MODES, seq, x0)
        xs = predict(MODES, x0, us, seq)
        flat = [u[0] for u in us]
        for k in range(5):
            pred = [d[k][i] + sum(gam[k][i][j] * flat[j] for j in range(4)) for i in range(2)]
            assert max(abs(a - b) for a, b in zip(pred, xs[k])) < 1e-12


def test_example_of_the_page():
    x0 = [1.0, 0.0]
    best = mpc_step(MODES, x0, 3, I2, R, I2, UMIN, UMAX, XMIN, XMAX)
    u, seq, cost = best
    assert seq == (0, 0, 0)
    assert abs(cost - 1.5474) < 1e-4
    assert all(abs(a - b) < 1e-4 for a, b in zip(u, [-0.8270, -0.6812, -0.1698]))
    other = mpc_step(MODES, x0, 3, I2, R, I2, UMIN, UMAX, XMIN, XMAX, sequences=[(0, 0, 1)])
    assert abs(other[2] - 1.5940) < 1e-4
    for seq in itertools.product((0, 1), repeat=3):
        if seq not in ((0, 0, 0), (0, 0, 1)):
            assert mpc_step(MODES, x0, 3, I2, R, I2, UMIN, UMAX, XMIN, XMAX, sequences=[seq]) is None


def true_cost(x0, us, horizon):
    xs = [x0]
    for u in us:
        xs.append(pwa_step(MODES, xs[-1], [u]))
    if any(abs(v) > 10 for x in xs for v in x):
        return math.inf
    return sum(x[0] ** 2 + x[1] ** 2 for x in xs) + 0.1 * sum(u * u for u in us)


def test_optimum_against_input_grid():
    """No input sequence on a grid beats the solver, and the best grid point is close to it."""
    for x0 in ([1.0, 0.0], [0.5, -1.0], [-1.0, 1.0], [0.2, 0.3]):
        _, _, cost = mpc_step(MODES, x0, 2, I2, R, I2, UMIN, UMAX, XMIN, XMAX)
        grid = [-1.0 + 0.02 * i for i in range(101)]
        best = min(true_cost(x0, [a, b], 2) for a in grid for b in grid)
        assert cost <= best + 1e-9
        assert best - cost < 2e-3


def test_closed_loop_reaches_origin():
    """The open loop diverges (rho = 1.2); the MPC loop meets |u| <= 1 and goes to 0."""
    x = [1.0, 1.0]
    for _ in range(15):
        x = pwa_step(MODES, x, [0.0])
    assert math.hypot(*x) > 10
    for x0 in ([1.0, 1.0], [1.0, 0.0], [-1.0, -0.5]):
        xs, us = closed_loop(MODES, x0, 15, 3, I2, R, I2, UMIN, UMAX, XMIN, XMAX)
        assert len(us) == 15
        assert all(-1 - 1e-9 <= u[0] <= 1 + 1e-9 for u in us)
        assert all(abs(v) <= 10 for x in xs for v in x)
        assert math.hypot(*xs[-1]) < 1e-4


def test_mld_big_m_agrees_with_pwa():
    rng = random.Random(4)
    xlo, xhi, ulo, uhi = [-5.0, -5.0], [5.0, 5.0], [-1.0], [1.0]
    rows, eq = pwa_to_mld(MODES, xlo, xhi, ulo, uhi)
    for _ in range(300):
        x = [rng.uniform(-5, 5), rng.uniform(-5, 5)]
        if rng.random() < 0.1:
            x[0] = 0.0
        u = [rng.uniform(-1, 1)]
        feasible = []
        for i in range(2):
            delta = [1.0 if j == i else 0.0 for j in range(2)]
            assert sum(a * v for a, v in zip(eq[3:5], delta)) == 1.0
            g = pwa_step(MODES, x, u, mode=i)
            z = [v * delta[j] for j in range(2) for v in g]
            w = x + u + delta + z
            if mld_rows_hold(rows, w):
                feasible.append(i)
                xnext = [z[k] + z[2 + k] for k in range(2)]
                assert xnext == g
                # z is fixed by the rows: moving one entry breaks a row.
                for k in range(4):
                    for step in (1e-6, -1e-6):
                        w2 = list(w)
                        w2[5 + k] += step
                        assert not mld_rows_hold(rows, w2, tol=1e-12)
        if x[0] > 0:
            assert feasible == [0]
        elif x[0] < 0:
            assert feasible == [1]
        else:
            assert feasible == [0, 1]
        assert mode_of(MODES, x) == feasible[0]
