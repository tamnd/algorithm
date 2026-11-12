# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-kalman-filter/.

import bisect
import math
import random
from fractions import Fraction as Fr

from extended_kalman_filter import extended_kalman_filter, inverse, mat_add, mat_mul, mat_vec, transpose, vec_add


def kalman_filter(A, Q, H, R, m0, P0, ys):
    """The plain linear Kalman filter, written out for comparison."""
    m, P = list(m0), P0
    means, covs = [m], [P]
    for y in ys:
        m = mat_vec(A, m)
        P = mat_add(mat_mul(mat_mul(A, P), transpose(A)), Q)
        S = mat_add(mat_mul(mat_mul(H, P), transpose(H)), R)
        K = mat_mul(mat_mul(P, transpose(H)), inverse(S))
        m = vec_add(m, mat_vec(K, vec_add(y, mat_vec(H, m), -1)))
        P = mat_add(P, mat_mul(mat_mul(K, S), transpose(K)), -1)
        means.append(m)
        covs.append(P)
    return means, covs


def linear_ekf(A, Q, H, R, m0, P0, ys):
    return extended_kalman_filter(
        lambda x: mat_vec(A, x), lambda x: A, lambda x: mat_vec(H, x), lambda x: H, Q, R, m0, P0, ys
    )


def test_equals_kalman_filter_exactly_on_a_linear_model() -> None:
    A = [[Fr(1), Fr(1)], [Fr(0), Fr(9, 10)]]
    Q = [[Fr(1, 10), Fr(0)], [Fr(0), Fr(1, 5)]]
    H = [[Fr(1), Fr(0)]]
    R = [[Fr(1, 2)]]
    m0, P0 = [Fr(0), Fr(1)], [[Fr(1), Fr(0)], [Fr(0), Fr(1)]]
    ys = [[Fr(1)], [Fr(5, 2)], [Fr(3)], [Fr(9, 2)]]
    assert linear_ekf(A, Q, H, R, m0, P0, ys) == kalman_filter(A, Q, H, R, m0, P0, ys)


def test_equals_kalman_filter_on_random_linear_models() -> None:
    rng = random.Random(5)
    for _ in range(20):
        n, k, T = rng.randint(1, 3), rng.randint(1, 2), rng.randint(1, 6)
        A = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        Q = [[(0.3 if i == j else 0.0) for j in range(n)] for i in range(n)]
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(k)]
        R = [[(0.5 if i == j else 0.1) for j in range(k)] for i in range(k)]
        m0 = [rng.gauss(0, 1) for _ in range(n)]
        P0 = [[(1.0 if i == j else 0.0) for j in range(n)] for i in range(n)]
        ys = [[rng.gauss(0, 1) for _ in range(k)] for _ in range(T)]
        me, Pe = linear_ekf(A, Q, H, R, m0, P0, ys)
        mk, Pk = kalman_filter(A, Q, H, R, m0, P0, ys)
        for t in range(T + 1):
            assert all(abs(a - b) < 1e-12 for a, b in zip(me[t], mk[t]))
            assert all(abs(a - b) < 1e-12 for ra, rb in zip(Pe[t], Pk[t]) for a, b in zip(ra, rb))


# A mildly nonlinear scalar model.
def f(x):
    return 0.9 * x + 0.2 * math.sin(x)


def h(x):
    return x + 0.1 * x * x


Q, R, M0, P0 = 0.05, 0.1, 0.5, 0.1


def simulate(T, rng):
    x, ys = rng.gauss(M0, math.sqrt(P0)), []
    for _ in range(T):
        x = f(x) + rng.gauss(0, math.sqrt(Q))
        ys.append(h(x) + rng.gauss(0, math.sqrt(R)))
    return ys


def bootstrap_means(ys, n, rng):
    """A bootstrap particle filter as the reference for E[x_t | y_1..y_t]."""
    xs = [rng.gauss(M0, math.sqrt(P0)) for _ in range(n)]
    means = [sum(xs) / n]
    for y in ys:
        xs = [f(x) + rng.gauss(0, math.sqrt(Q)) for x in xs]
        lw = [-((y - h(x)) ** 2) / (2 * R) for x in xs]
        top = max(lw)
        w = [math.exp(v - top) for v in lw]
        s = sum(w)
        means.append(sum(wi * x for wi, x in zip(w, xs)) / s)
        c, acc = [], 0.0
        for wi in w:
            acc += wi / s
            c.append(acc)
        xs = [xs[min(bisect.bisect_right(c, rng.random()), n - 1)] for _ in range(n)]
    return means


def test_close_to_a_large_particle_filter_on_a_mild_nonlinearity() -> None:
    ys = simulate(10, random.Random(1))
    me, Pe = extended_kalman_filter(
        lambda v: [f(v[0])],
        lambda v: [[0.9 + 0.2 * math.cos(v[0])]],
        lambda v: [h(v[0])],
        lambda v: [[1 + 0.2 * v[0]]],
        [[Q]],
        [[R]],
        [M0],
        [[P0]],
        [[y] for y in ys],
    )
    ref = bootstrap_means(ys, 20000, random.Random(2))
    # Measured gap with these seeds: about 0.015. The tolerance covers the
    # linearization error and the Monte Carlo error of the reference.
    assert max(abs(a[0] - b) for a, b in zip(me, ref)) < 0.05
    assert all(P[0][0] > 0 for P in Pe)
