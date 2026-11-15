# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luenberger-observer/. The authors are listed in prov/7T6PY4.jsonl.

import math
import random
from fractions import Fraction

import pytest

import ctlmat as cm
from ctlsim import simulate, simulate_discrete
from luenberger_observer import observer_gain, observer_rhs, observer_step, place


def poly_from_roots(roots):
    p = [1]
    for r in roots:
        p = cm.polymul(p, [1, -r])
    return p


def obs_matrix_rank(A, C):
    rows = []
    M = [list(r) for r in C]
    for _ in range(len(A)):
        rows += M
        M = cm.mul(M, A)
    # rank of the stacked rows by exact elimination
    R = [[Fraction(v) for v in r] for r in rows]
    rank = 0
    for c in range(len(A)):
        piv = next((i for i in range(rank, len(R)) if R[i][c] != 0), None)
        if piv is None:
            continue
        R[rank], R[piv] = R[piv], R[rank]
        for i in range(len(R)):
            if i != rank and R[i][c] != 0:
                f = R[i][c] / R[rank][c]
                R[i] = [a - f * b for a, b in zip(R[i], R[rank])]
        rank += 1
    return rank


def rand_observable(rng, n, p):
    while True:
        A = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        C = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(p)]
        if obs_matrix_rank(A, C) == n:
            return A, C


def a_minus_lc(A, L, C):
    return cm.sub(A, cm.mul(L, C))


def test_double_integrator():
    A = [[0, 1], [0, 0]]
    C = [[1, 0]]
    L = observer_gain(A, C, [1, 5, 6])
    assert L == [[5], [6]]
    assert cm.charpoly(a_minus_lc(A, L, C)) == [1, 5, 6]


def test_random_exact_multi_output():
    rng = random.Random(1)
    for n, p in [(2, 1), (3, 1), (3, 2), (4, 2), (5, 3), (5, 1)]:
        for _ in range(4):
            A, C = rand_observable(rng, n, p)
            roots = [rng.randint(-6, -1) for _ in range(n)]
            poly = poly_from_roots(roots)
            L = observer_gain(A, C, poly)
            assert len(L) == n and len(L[0]) == p
            assert cm.charpoly(a_minus_lc(A, L, C)) == poly


def test_place_multi_input_exact():
    rng = random.Random(2)
    for n, m in [(3, 2), (4, 3), (4, 2)]:
        for _ in range(4):
            At, Bt = rand_observable(rng, n, m)
            A, B = cm.transpose(At), cm.transpose(Bt)
            poly = poly_from_roots([rng.randint(-5, 0) for _ in range(n)])
            K = place(A, B, poly)
            assert cm.charpoly(cm.sub(A, cm.mul(B, K))) == poly


def test_error_follows_matrix_exponential():
    A = [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [-1.0, -2.0, 0.5]]
    B = [[0.0], [0.0], [1.0]]
    C = [[1.0, 0.0, 0.0]]
    L = observer_gain(A, C, poly_from_roots([-2.0, -3.0, -4.0]))
    obs = observer_rhs(A, B, C, L)
    n = 3

    def f(t, z, u):
        x, xh = z[:n], z[n:]
        dx = [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, u))]
        return dx + obs(t, xh, (u, cm.matvec(C, x)))

    x0 = [1.0, -0.5, 0.25]
    ts, zs, _ = simulate(f, x0 + [0.0, 0.0, 0.0], 0.0, 6.0, 0.001, control=lambda t, z: [math.sin(3 * t)])
    Acl = a_minus_lc(A, L, C)
    for k in (500, 1500, 3000, 6000):
        e = [a - b for a, b in zip(zs[k][:n], zs[k][n:])]
        want = cm.matvec(cm.expm(cm.scale(ts[k], Acl)), x0)
        assert max(abs(a - b) for a, b in zip(e, want)) < 1e-9
    # the plant is unstable, but the estimation error goes to 0
    e = [a - b for a, b in zip(zs[-1][:n], zs[-1][n:])]
    assert cm.norm2(e) < 1e-3 * cm.norm2(x0)
    assert cm.norm2(zs[-1][:n]) > 4 * cm.norm2(x0)


def test_discrete_deadbeat_observer_exact():
    rng = random.Random(3)
    for n, p in [(3, 1), (4, 2), (5, 2)]:
        A, C = rand_observable(rng, n, p)
        B = [[rng.randint(-2, 2)] for _ in range(n)]
        L = observer_gain(A, C, [1] + [0] * n)
        us = [[Fraction(rng.randint(-5, 5), rng.randint(1, 4))] for _ in range(n + 3)]

        def F(k, z, u):
            x, xh = z[:n], z[n:]
            xn = [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, u))]
            return xn + observer_step(A, B, C, L, xh, u, cm.matvec(C, x))

        x0 = [Fraction(rng.randint(-4, 4)) for _ in range(n)]
        zs, _ = simulate_discrete(F, x0 + [0] * n, n + 3, control=lambda k, z: us[k])
        for k in range(n, n + 4):
            assert zs[k][:n] == zs[k][n:]


def test_error_does_not_depend_on_input():
    A = [[1, 1], [0, 1]]
    B = [[0], [1]]
    C = [[1, 0]]
    L = observer_gain(A, C, poly_from_roots([Fraction(1, 2), Fraction(-1, 3)]))
    errs = []
    for scale_u in (0, 1, -7):
        x, xh = [3, -1], [0, 0]
        run = []
        for k in range(6):
            u = [scale_u * (k * k - 2)]
            y = cm.matvec(C, x)
            xh = observer_step(A, B, C, L, xh, u, y)
            x = [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, u))]
            run.append([a - b for a, b in zip(x, xh)])
        errs.append(run)
    assert errs[0] == errs[1] == errs[2]


def test_complex_poles_float():
    A = [[0.0, 1.0, 0.0, 0.0], [-2.0, -0.1, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0], [1.0, 0.0, -3.0, -0.2]]
    C = [[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
    want = [complex(-1, 2), complex(-1, -2), -3.0, -4.0]
    L = observer_gain(A, C, [c.real for c in poly_from_roots(want)])
    got = cm.polyroots(cm.charpoly(a_minus_lc(A, L, C)))
    for w in want:
        assert min(abs(g - w) for g in got) < 1e-8


def test_rejects_unobservable_and_bad_polynomial():
    A = [[1, 0], [0, 2]]
    C = [[1, 0]]
    with pytest.raises(ValueError):
        observer_gain(A, C, [1, 3, 2])
    with pytest.raises(ValueError):
        observer_gain([[0, 1], [0, 0]], [[1, 0]], [1, 3])
    with pytest.raises(ValueError):
        place([[0, 1], [0, 0]], [[0], [0]], [1, 3, 2])
