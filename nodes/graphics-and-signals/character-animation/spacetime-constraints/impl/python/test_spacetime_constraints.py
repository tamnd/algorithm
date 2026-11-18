# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spacetime-constraints/. The authors are listed in prov/5ZYH4C.jsonl.
"""Tests of spacetime constraints on a one degree of freedom body.

The toy of the page: a unit mass from x(0) = 0 to x(1) = 1, at rest at both
ends, minimizing the integral of x''^2. The exact discrete minimum is
12 n^2 / ((n - 1)(n - 2)), which tends to 12, and the path tends to
3 t^2 - 2 t^3. Gravity adds g^2 h (n - 1) and leaves the path the same. For
the nonlinear pendulum, the constraints hold and the solution is a
stationary point and a local minimum of the effort after the forces are
eliminated, a reference that does not use the KKT system.
"""

import math
import random

from spacetime_constraints import residuals, spacetime


def eliminated_effort(x, n, h, k, g):
    """Effort of a path x that meets the boundary rows, with f from the dynamics."""
    e = 0.0
    for i in range(1, n):
        f = (x[i + 1] - 2.0 * x[i] + x[i - 1]) / (h * h) + k * math.sin(x[i]) + g
        e += h * f * f
    return e


def test_toy_exact_discrete_minimum():
    for n in (10, 20, 40):
        _, _, e, it = spacetime(n)
        assert abs(e - 12.0 * n * n / ((n - 1) * (n - 2))) < 1e-8
        assert it == 2


def test_toy_tends_to_the_cubic():
    errs = []
    for n in (10, 20, 40):
        x, _, e, _ = spacetime(n)
        errs.append(max(abs(x[i] - (3 * (i / n) ** 2 - 2 * (i / n) ** 3)) for i in range(n + 1)))
    assert errs[0] > errs[1] > errs[2]
    assert errs[2] < 0.01
    assert abs(e - 12.0) < 1.0


def test_toy_force_is_linear_in_time():
    n = 20
    _, f, _, _ = spacetime(n)
    d = [f[i + 1] - f[i] for i in range(len(f) - 1)]
    assert all(abs(v - d[0]) < 1e-8 for v in d)
    assert d[0] < 0.0 and f[0] > 0.0 > f[-1]


def test_gravity_adds_a_constant():
    n = 20
    g = 9.81
    x0, _, e0, _ = spacetime(n)
    x1, f1, e1, _ = spacetime(n, g=g)
    assert abs(e1 - e0 - g * g * (n - 1) / n) < 1e-8
    assert max(abs(p - q) for p, q in zip(x0, x1)) < 1e-10


def test_linear_case_matches_unconstrained_least_squares():
    # Eliminate the forces and the boundary rows, and solve the normal
    # equations of the remaining least squares problem in x_2 .. x_(n-2).
    n, g = 12, 2.0
    h = 1.0 / n
    x, _, e, _ = spacetime(n, g=g)
    free = list(range(2, n - 1))
    base = [0.0, 0.0] + [0.0] * (n - 3) + [1.0, 1.0]
    rows, rhs = [], []
    for i in range(1, n):
        r = [0.0] * len(free)
        known = g
        for j, w in ((i - 1, 1.0), (i, -2.0), (i + 1, 1.0)):
            if j in free:
                r[free.index(j)] += w / (h * h)
            else:
                known += w * base[j] / (h * h)
        rows.append(r)
        rhs.append(-known)
    m = len(free)
    ata = [[sum(r[a] * r[b] for r in rows) for b in range(m)] for a in range(m)]
    atb = [sum(r[a] * v for r, v in zip(rows, rhs)) for a in range(m)]
    for p in range(m):
        for q in range(p + 1, m):
            t = ata[q][p] / ata[p][p]
            for c in range(p, m):
                ata[q][c] -= t * ata[p][c]
            atb[q] -= t * atb[p]
    sol = [0.0] * m
    for p in range(m - 1, -1, -1):
        sol[p] = (atb[p] - sum(ata[p][c] * sol[c] for c in range(p + 1, m))) / ata[p][p]
    for j, v in zip(free, sol):
        assert abs(x[j] - v) < 1e-9
    assert abs(e - eliminated_effort(x, n, h, 0.0, g)) < 1e-9


def test_pendulum_meets_the_constraints_and_is_a_local_minimum():
    n, k = 20, 9.81
    h = 1.0 / n
    x, f, e, it = spacetime(n, k=k, b=1.0)
    assert it < 15
    c = residuals(list(x) + list(f), n, h, k, 0.0, 0.0, 1.0)
    assert max(abs(v) for v in c) < 1e-9
    free = list(range(2, n - 1))

    def j(vals):
        y = list(x)
        for idx, v in zip(free, vals):
            y[idx] = v
        return eliminated_effort(y, n, h, k, 0.0)

    start = [x[i] for i in free]
    eps = 1e-6
    for a in range(len(free)):
        up = list(start)
        dn = list(start)
        up[a] += eps
        dn[a] -= eps
        assert abs(j(up) - j(dn)) / (2 * eps) < 1e-4
    rng = random.Random(4)
    for _ in range(30):
        assert j([v + rng.gauss(0, 1e-3) for v in start]) >= e - 1e-12


def test_swing_up_converges():
    n, k = 20, 9.81
    x, f, _, it = spacetime(n, k=k, b=math.pi, duration=2.0)
    h = 2.0 / n
    c = residuals(list(x) + list(f), n, h, k, 0.0, 0.0, math.pi)
    assert it < 30
    assert max(abs(v) for v in c) < 1e-9
