# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unknown-input-observer/. The authors are listed in prov/A7P4SP.jsonl.

import math
import random
from fractions import Fraction

import pytest

import ctlmat as cm
from ctlsim import simulate
from unknown_input_observer import (
    estimate,
    observer_rhs,
    observer_step,
    place,
    uio_matrices,
    unknown_input_observer,
)

A_EX = [[0, 1, 0], [0, 0, 1], [-1, -3, -3]]
B_EX = [[0], [0], [1]]
E_EX = [[1], [0], [0]]
C_EX = [[1, 0, 0], [0, 1, 0]]
ALPHA = [1, 9, 26, 24]  # (s + 2)(s + 3)(s + 4)


def as_float(M):
    return [[float(v) for v in r] for r in M]


def test_example_matrices():
    H, T, A1, G = uio_matrices(A_EX, B_EX, C_EX, E_EX)
    assert H == [[1, 0], [0, 0], [0, 0]]
    assert T == [[0, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert A1 == [[0, 0, 0], [0, 0, 1], [-1, -3, -3]]
    F, G, K, H = unknown_input_observer(A_EX, B_EX, C_EX, E_EX, ALPHA)
    assert cm.charpoly(F) == ALPHA
    assert cm.mul(T, E_EX) == [[0], [0], [0]]


def rand_case(rng, n, p, q):
    while True:
        A = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        B = [[rng.randint(-2, 2)] for _ in range(n)]
        C = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(p)]
        E = [[rng.randint(-2, 2) for _ in range(q)] for _ in range(n)]
        try:
            return A, B, C, E, unknown_input_observer(A, B, C, E, [1] + [0] * n)
        except ValueError:
            continue


def test_identities_random_exact():
    rng = random.Random(7)
    for n, p, q in [(3, 2, 1), (4, 2, 1), (4, 3, 2), (5, 3, 1), (5, 4, 2)]:
        for _ in range(3):
            A, B, C, E, _ = rand_case(rng, n, p, q)
            alpha = [1]
            for r in [rng.randint(-5, -1) for _ in range(n)]:
                alpha = cm.polymul(alpha, [1, -r])
            F, G, K, H = unknown_input_observer(A, B, C, E, alpha)
            T = cm.sub(cm.eye(n), cm.mul(H, C))
            assert cm.mul(cm.mul(H, C), E) == [[Fraction(v) for v in r] for r in E]
            assert cm.mul(T, E) == cm.zeros(n, q)
            assert cm.add(cm.mul(F, T), cm.mul(K, C)) == cm.mul(T, A)  # F T + K C = T A
            assert G == cm.mul(T, B)
            assert cm.charpoly(F) == alpha


def test_discrete_error_ignores_unknown_input_exact():
    rng = random.Random(8)
    for n, p, q in [(3, 2, 1), (4, 3, 2)]:
        A, B, C, E, (F, G, K, H) = rand_case(rng, n, p, q)
        x = [Fraction(rng.randint(-4, 4)) for _ in range(n)]
        z = [0] * n
        T = cm.sub(cm.eye(n), cm.mul(H, C))
        e0 = [a - b for a, b in zip(cm.matvec(T, x), z)]
        for k in range(n + 3):
            u = [Fraction(rng.randint(-9, 9), 2)]
            d = [Fraction(rng.randint(-50, 50), rng.randint(1, 7)) for _ in range(q)]
            y = cm.matvec(C, x)
            err = [a - b for a, b in zip(x, estimate(H, z, y))]
            assert err == cm.matvec(cm.mat_power(F, k), e0)
            z = observer_step(F, G, K, z, u, y)
            x = [a + b + c for a, b, c in zip(cm.matvec(A, x), cm.matvec(B, u), cm.matvec(E, d))]
        # deadbeat: alpha = z^n, so the estimate is exact from step n on
        assert cm.mat_power(F, n) == cm.zeros(n)


def test_continuous_against_luenberger():
    F, G, K, H = unknown_input_observer(A_EX, B_EX, C_EX, E_EX, ALPHA)
    L = cm.transpose(place(cm.transpose(A_EX), cm.transpose(C_EX), ALPHA))
    A, B, C, Lf = as_float(A_EX), as_float(B_EX), as_float(C_EX), as_float(L)
    obs = observer_rhs(as_float(F), as_float(G), as_float(K))
    n = 3

    def d(t):
        return (1.0 if t >= 1.0 else 0.0) + 0.5 * math.sin(5 * t)

    def f(t, s, u):
        x, z, xl = s[:n], s[n:2 * n], s[2 * n:]
        y = cm.matvec(C, x)
        dx = [a + b + e * d(t) for a, b, e in zip(cm.matvec(A, x), cm.matvec(B, u), [1.0, 0.0, 0.0])]
        r = [a - b for a, b in zip(y, cm.matvec(C, xl))]
        dxl = [a + b + c for a, b, c in zip(cm.matvec(A, xl), cm.matvec(B, u), cm.matvec(Lf, r))]
        return dx + obs(t, z, (u, y)) + dxl

    x0 = [0.5, 0.3, -0.2]
    ts, ss, _ = simulate(f, x0 + [0.0] * 6, 0.0, 6.0, 0.001, control=lambda t, s: [math.sin(t)])
    T = cm.sub(cm.eye(n), cm.mul(as_float(H), C))
    e0 = cm.matvec(T, x0)
    for k in (1000, 3000, 6000):
        x, z, xl = ss[k][:n], ss[k][n:2 * n], ss[k][2 * n:]
        err = [a - b for a, b in zip(x, estimate(as_float(H), z, cm.matvec(C, x)))]
        want = cm.matvec(cm.expm(cm.scale(ts[k], as_float(F))), e0)
        assert max(abs(a - b) for a, b in zip(err, want)) < 1e-8
        if ts[k] >= 3:
            assert max(abs(a - b) for a, b in zip(x, xl)) > 0.1  # the Luenberger observer is biased
    assert cm.norm2(err) < 1e-5


def test_invariant_zero_is_a_fixed_eigenvalue():
    # (A, E, C) has the invariant zero s = 1: (I - A) e3 = E (-1) and C e3 = 0.
    A = [[0, 1, 1], [0, 0, 0], [1, -1, 1]]
    B = [[0], [0], [1]]
    H, T, A1, G = uio_matrices(A, B, C_EX, E_EX)
    rng = random.Random(9)
    for _ in range(20):
        K1 = [[rng.randint(-9, 9) for _ in range(2)] for _ in range(3)]
        F = cm.sub(A1, cm.mul(K1, C_EX))
        assert cm.det(cm.sub(cm.eye(3), F)) == 0
    with pytest.raises(ValueError):
        unknown_input_observer(A, B, C_EX, E_EX, ALPHA)


def test_rank_condition():
    with pytest.raises(ValueError):  # C E = 0
        uio_matrices(A_EX, B_EX, [[0, 1, 0], [0, 0, 1]], E_EX)
    with pytest.raises(ValueError):  # E rank deficient
        uio_matrices(A_EX, B_EX, C_EX, [[1, 2], [0, 0], [0, 0]])
