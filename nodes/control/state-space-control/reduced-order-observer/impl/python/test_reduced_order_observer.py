# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduced-order-observer/. The authors are listed in prov/3BXD4W.jsonl.

import math
import random
from fractions import Fraction

import pytest

import ctlmat as cm
from ctlsim import simulate, simulate_discrete
from reduced_order_observer import estimate, observer_rhs, observer_step, place, reduced_order_observer


def poly_from_roots(roots):
    p = [1]
    for r in roots:
        p = cm.polymul(p, [1, -r])
    return p


def rank(rows):
    R = [[Fraction(v) for v in r] for r in rows]
    rk = 0
    for c in range(len(R[0]) if R else 0):
        piv = next((i for i in range(rk, len(R)) if R[i][c] != 0), None)
        if piv is None:
            continue
        R[rk], R[piv] = R[piv], R[rk]
        for i in range(len(R)):
            if i != rk and R[i][c] != 0:
                f = R[i][c] / R[rk][c]
                R[i] = [a - f * b for a, b in zip(R[i], R[rk])]
        rk += 1
    return rk


def observable(A, C):
    rows, M = [], [list(r) for r in C]
    for _ in range(len(A)):
        rows += M
        M = cm.mul(M, A)
    return rank(rows) == len(A)


def rand_system(rng, n, p, m=1):
    while True:
        A = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        C = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(p)]
        B = [[rng.randint(-2, 2) for _ in range(m)] for _ in range(n)]
        if rank(C) == p and observable(A, C):
            return A, B, C


def test_double_integrator():
    A = [[0, 1], [0, 0]]
    B = [[0], [1]]
    C = [[1, 0]]
    F, G, H, L, Tinv = reduced_order_observer(A, B, C, [1, 3])
    assert (F, G, H, L) == ([[-3]], [[-9]], [[1]], [[3]])
    assert Tinv == cm.eye(2)


def test_eigenvalues_of_F_exact():
    rng = random.Random(4)
    for n, p in [(3, 1), (3, 2), (4, 1), (4, 2), (5, 2), (5, 3)]:
        for _ in range(3):
            A, B, C = rand_system(rng, n, p)
            alpha = poly_from_roots([rng.randint(-5, -1) for _ in range(n - p)])
            F, G, H, L, Tinv = reduced_order_observer(A, B, C, alpha)
            assert len(F) == n - p
            assert cm.charpoly(F) == alpha


def test_discrete_error_is_F_power_exact():
    rng = random.Random(5)
    for n, p in [(3, 1), (4, 2), (5, 2)]:
        A, B, C = rand_system(rng, n, p)
        alpha = poly_from_roots([Fraction(rng.randint(-3, 3), 4) for _ in range(n - p)])
        F, G, H, L, Tinv = reduced_order_observer(A, B, C, alpha)
        T = cm.inv(Tinv)
        us = [[Fraction(rng.randint(-5, 5), 3)] for _ in range(8)]
        x = [Fraction(rng.randint(-4, 4)) for _ in range(n)]
        z = [0] * (n - p)
        w0 = cm.matvec(T, x)[p:]
        e0 = [a - b for a, b in zip(w0, cm.matvec(L, cm.matvec(C, x)))]  # z_true(0) - z(0)
        for k in range(8):
            y = cm.matvec(C, x)
            xh = estimate(L, Tinv, z, y)
            err = [a - b for a, b in zip(x, xh)]
            want = cm.matvec(Tinv, [0] * p + cm.matvec(cm.mat_power(F, k), e0))
            assert err == want
            assert cm.matvec(C, xh) == y  # the measured part is exact
            z = observer_step(F, G, H, z, us[k], y)
            x = [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, us[k]))]


def test_deadbeat_reduced_observer():
    rng = random.Random(6)
    for n, p in [(3, 1), (4, 2), (5, 3)]:
        A, B, C = rand_system(rng, n, p)
        F, G, H, L, Tinv = reduced_order_observer(A, B, C, [1] + [0] * (n - p))
        us = [[rng.randint(-5, 5)] for _ in range(n)]

        def step(k, s, u):
            x, z = s[:n], s[n:]
            xn = [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, u))]
            return xn + observer_step(F, G, H, z, u, cm.matvec(C, x))

        x0 = [rng.randint(-4, 4) for _ in range(n)]
        ss, _ = simulate_discrete(step, x0 + [0] * (n - p), n, control=lambda k, s: us[k])
        for k in range(n - p, n + 1):
            x, z = ss[k][:n], ss[k][n:]
            assert estimate(L, Tinv, z, cm.matvec(C, x)) == x


def test_continuous_error_follows_matrix_exponential():
    A = [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [-1.0, -2.0, 0.5]]
    B = [[0.0], [0.0], [1.0]]
    C = [[1.0, 1.0, 0.0]]
    F, G, H, L, Tinv = reduced_order_observer(A, B, C, poly_from_roots([-2.0, -3.0]))
    T = cm.inv(Tinv)
    n, p = 3, 1
    obs = observer_rhs(F, G, H)

    def f(t, s, u):
        x, z = s[:n], s[n:]
        dx = [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, u))]
        return dx + obs(t, z, (u, cm.matvec(C, x)))

    x0 = [1.0, -0.5, 0.25]
    ts, ss, _ = simulate(f, x0 + [0.0, 0.0], 0.0, 4.0, 0.001, control=lambda t, s: [math.cos(2 * t)])
    e0 = [a - b for a, b in zip(cm.matvec(T, x0)[p:], cm.matvec(L, cm.matvec(C, x0)))]
    for k in (1000, 2000, 4000):
        x, z = ss[k][:n], ss[k][n:]
        xh = estimate(L, Tinv, z, cm.matvec(C, x))
        err = [a - b for a, b in zip(x, xh)]
        want = cm.matvec(Tinv, [0.0] + cm.matvec(cm.expm(cm.scale(ts[k], F)), e0))
        assert max(abs(a - b) for a, b in zip(err, want)) < 1e-9


def test_place_multi_input():
    A = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    B = [[1, 0], [0, 0], [0, 1]]
    K = place(A, B, [1, 6, 11, 6])
    assert cm.charpoly(cm.sub(A, cm.mul(B, K))) == [1, 6, 11, 6]


def test_rejections():
    with pytest.raises(ValueError):  # C rank deficient
        reduced_order_observer([[0, 1], [0, 0]], [[0], [1]], [[1, 0], [2, 0]], [1])
    with pytest.raises(ValueError):  # p = n
        reduced_order_observer([[0, 1], [0, 0]], [[0], [1]], [[1, 0], [0, 1]], [1])
    with pytest.raises(ValueError):  # unobservable
        reduced_order_observer([[1, 0], [0, 2]], [[1], [1]], [[1, 0]], [1, 3])
