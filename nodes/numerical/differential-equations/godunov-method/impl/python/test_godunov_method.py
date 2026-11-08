# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/godunov-method/. The authors are listed in prov/H99E04.jsonl.

import math
import random
from fractions import Fraction as Fr

import pytest

from godunov_method import godunov, riemann_face_state

f_b = lambda v: v * v / 2
df_b = lambda v: v


def osher_flux_sampled(f, ul, ur, n=2000):
    """Independent oracle: min of f over [ul, ur] if ul <= ur, else max over [ur, ul], by sampling."""
    lo, hi = min(ul, ur), max(ul, ur)
    vals = [f(lo + (hi - lo) * k / n) for k in range(n + 1)]
    return min(vals) if ul <= ur else max(vals)


def burgers_exact(ul, ur, xi):
    if ul > ur:
        return ul if xi < (ul + ur) / 2 else ur
    return ul if xi <= ul else ur if xi >= ur else xi


def cell_avg_exact(ul, ur, t, a, b, m, sub=200):
    dx = (b - a) / m
    out = []
    for i in range(m):
        xs = [a + (i + (j + 0.5) / sub) * dx for j in range(sub)]
        out.append(sum(burgers_exact(ul, ur, x / t) for x in xs) / sub)
    return out


def test_worked_example_transonic_rarefaction_exact():
    u = [Fr(-1), Fr(-1), Fr(1), Fr(1)]
    r = godunov(u, Fr(1), Fr(1, 2), Fr(1, 2), f_b, df_b, Fr(0))
    assert r.u == [-1, Fr(-3, 4), Fr(3, 4), 1] and r.riemann_solves == 5
    r = godunov(u, Fr(1), Fr(1, 2), Fr(1), f_b, df_b, Fr(0))
    assert r.u == [Fr(-57, 64), Fr(-39, 64), Fr(39, 64), Fr(57, 64)]
    r = godunov([Fr(1), Fr(1), Fr(0), Fr(0)], Fr(1), Fr(1, 2), Fr(1), f_b, df_b, Fr(0))
    assert r.u == [1, 1, Fr(31, 64), Fr(1, 64)]


def test_face_state_random_against_osher_formula():
    rng = random.Random(8)
    for case in range(600):
        kind = case % 3
        if kind == 0:
            p, q = rng.uniform(0.1, 2.0), rng.uniform(-2, 2)
            f = lambda v, p=p, q=q: p * v * v + q * v
            df = lambda v, p=p, q=q: 2 * p * v + q
            us = -q / (2 * p)
        elif kind == 1:
            f, df, us = math.exp, math.exp, None
        else:
            f, df, us = (lambda v: v ** 4 / 4), (lambda v: v ** 3), 0.0
        ul, ur = rng.uniform(-2, 2), rng.uniform(-2, 2)
        if rng.random() < 0.05:
            ur = ul
        got = f(riemann_face_state(ul, ur, f, df, us))
        want = osher_flux_sampled(f, ul, ur)
        assert got == pytest.approx(want, rel=1e-5, abs=1e-5)


def test_random_conservation_and_bounds():
    rng = random.Random(9)
    for case in range(500):
        m = rng.randint(1, 8)
        u = [Fr(rng.randint(-8, 8), rng.randint(1, 4)) for _ in range(m)]
        smax = max(abs(v) for v in u) or Fr(1)
        dt = Fr(rng.randint(1, 10), 10) / smax  # Courant number <= 1 with dx = 1
        r = godunov(u, Fr(1), dt, 2 * dt, f_b, df_b, Fr(0), bc="periodic")
        assert sum(r.u) == sum(u)
        assert min(u) <= min(r.u) and max(r.u) <= max(u)
        tv = lambda w: sum(abs(w[i] - w[i - 1]) for i in range(len(w)))
        assert tv(r.u) <= tv(u)


def test_linear_flux_is_upwind_and_exact_at_courant_one():
    u = [float(i % 3) for i in range(7)]
    r = godunov(u, 0.25, 0.25, 0.5, lambda v: v, lambda v: 1.0, None, bc="periodic")
    assert r.u == u[-2:] + u[:-2]
    r = godunov(u, 1.0, 0.5, 0.5, lambda v: -2 * v, lambda v: -2.0, None, bc="periodic")
    assert r.u == u[1:] + u[:1]


def test_entropy_fix_matters_transonic_rarefaction():
    def roe(ul, ur):
        a = (ul + ur) / 2
        return (f_b(ul) + f_b(ur)) / 2 - abs(a) * (ur - ul) / 2
    m = 200
    dx, dt = 2 / m, 0.8 * 2 / m
    u = [-1.0 if -1 + (i + 0.5) * dx < 0 else 1.0 for i in range(m)]
    w = list(u)
    for _ in range(round(0.5 / dt)):
        ext = [w[0]] + w + [w[-1]]
        F = [roe(ext[i], ext[i + 1]) for i in range(m + 1)]
        w = [w[i] - dt / dx * (F[i + 1] - F[i]) for i in range(m)]
    exact = cell_avg_exact(-1.0, 1.0, 0.5, -1, 1, m)
    roe_err = dx * sum(abs(a - b) for a, b in zip(w, exact))
    g = godunov(u, dx, dt, 0.5, f_b, df_b, 0.0)
    god_err = dx * sum(abs(a - b) for a, b in zip(g.u, exact))
    assert roe_err == pytest.approx(0.5, abs=1e-6)  # stationary expansion shock
    assert god_err < 0.03


def test_convergence_riemann_problems():
    rare, shock = [], []
    for m in (50, 100, 200, 400):
        dx = 2 / m
        for (ul, ur), store in (((-1.0, 1.0), rare), ((1.0, 0.0), shock)):
            u = [ul if -1 + (i + 0.5) * dx < 0 else ur for i in range(m)]
            r = godunov(u, dx, 0.8 * dx, 0.5, f_b, df_b, 0.0)
            assert r.max_cfl <= 0.8 + 1e-12
            exact = cell_avg_exact(ul, ur, 0.5, -1, 1, m)
            store.append(dx * sum(abs(a - b) for a, b in zip(r.u, exact)))
    assert rare[0] == pytest.approx(5.848e-2, rel=1e-3)
    assert all(1.4 < rare[k] / rare[k + 1] < 2.0 for k in range(3))
    assert all(e < 0.5 * 2 / m for e, m in zip(shock, (50, 100, 200, 400)))


def test_edge_cases():
    r = godunov([], 1.0, 0.1, 1.0, f_b, df_b, 0.0)
    assert r.u == [] and r.steps == 0
    r = godunov([1.0, 2.0], 1.0, 0.1, 0.0, f_b, df_b, 0.0)
    assert r.u == [1.0, 2.0] and r.steps == 0
    # dt larger than the interval: one shortened step; off-grid final time
    r = godunov([Fr(1), Fr(0)], Fr(1), Fr(10), Fr(1, 4), f_b, df_b, Fr(0))
    assert r.steps == 1 and r.u == [1, Fr(1, 8)]
    r = godunov([0.5, 0.0, 0.0], 1.0, 0.4, 1.0, f_b, df_b, 0.0)
    assert r.steps == 3
    # constant state is preserved, including a sonic state
    assert godunov([Fr(0)] * 4, Fr(1), Fr(1), Fr(3), f_b, df_b, Fr(0)).u == [0] * 4
    with pytest.raises(ValueError):
        godunov([1.0], 1.0, -0.1, 1.0, f_b, df_b, 0.0)
    with pytest.raises(ValueError):
        godunov([1.0], 1.0, 0.1, 1.0, f_b, df_b, 0.0, bc="wall")
