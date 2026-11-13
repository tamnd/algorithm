# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-matching-pursuit/. The authors are listed in prov/DHYVW6.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from orthogonal_matching_pursuit import coherence_squared, least_squares, omp


def matvec(A, x):
    return [sum((F(a) * b for a, b in zip(row, x)), F(0)) for row in A]


def hadamard(n):
    H = [[1]]
    while len(H) < n:
        H = [r + r for r in H] + [r + [-v for v in r] for r in H]
    return H


def identity_plus_hadamard():
    H = hadamard(16)
    return [[F(int(i == j)) for j in range(16)] + [F(H[i][j], 4) for j in range(16)] for i in range(16)]


def brute_force_sparse(A, y, s):
    """Reference: every support of size s whose least squares fit is exact."""
    out = []
    for S in itertools.combinations(range(len(A[0])), s):
        try:
            z = least_squares(A, list(S), y)
        except ZeroDivisionError:
            continue
        x = [F(0)] * len(A[0])
        for j, v in zip(S, z):
            x[j] = v
        if matvec(A, x) == [F(v) for v in y] and all(v != 0 for v in z):
            out.append(x)
    return out


def test_coherence_exact() -> None:
    A = identity_plus_hadamard()
    assert coherence_squared(A) == F(1, 16)  # mu = 1/4
    tetra = [[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]]
    assert coherence_squared(tetra) == F(1, 9)  # mu = 1/3


def mu_condition(A, s):
    """mu < 1/(2s - 1), tested exactly as mu^2 (2s - 1)^2 < 1."""
    return coherence_squared(A) * (2 * s - 1) ** 2 < 1


def test_recovery_under_coherence() -> None:
    A = identity_plus_hadamard()
    assert mu_condition(A, 2) and not mu_condition(A, 3)
    rng = random.Random(8)
    for t in range(30):
        S = rng.sample(range(32), 2)
        x0 = [F(0)] * 32
        for j in S:
            x0[j] = F(rng.choice([-5, -2, -1, 1, 3, 7]), rng.choice([1, 2, 3]))
        x, support = omp(A, matvec(A, x0), 2)
        assert x == x0 and sorted(support) == sorted(S)
        if t < 3:
            assert brute_force_sparse(A, matvec(A, x0), 2) == [x0]


def test_recovery_on_random_matrices_when_condition_holds() -> None:
    rng = random.Random(12)
    checked = 0
    for _ in range(400):
        m, n = 6, 8
        A = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(m)]
        for s in (1, 2):
            if not mu_condition(A, s):
                continue
            S = rng.sample(range(n), s)
            x0 = [F(0)] * n
            for j in S:
                x0[j] = F(rng.choice([-3, -1, 2, 4]))
            x, support = omp(A, matvec(A, x0), s)
            assert x == x0
            checked += 1
    assert checked > 50


def test_residual_is_orthogonal_to_chosen_columns() -> None:
    rng = random.Random(4)
    for _ in range(50):
        A = [[rng.randint(-3, 3) for _ in range(7)] for _ in range(5)]
        y = [rng.randint(-5, 5) for _ in range(5)]
        x, support = omp(A, y, 3)
        r = [F(a) - b for a, b in zip(y, matvec(A, x))]
        assert len(set(support)) == len(support)
        for j in support:
            assert sum(A[i][j] * r[i] for i in range(5)) == 0


def test_omp_fails_where_bp_succeeds() -> None:
    w = (F(6, 11), F(6, 11), F(7, 11))
    A = [[1, 0, 0, w[0]], [0, 1, 0, w[1]], [0, 0, 1, w[2]]]
    x0 = [F(1), F(1), F(0), F(0)]
    x, support = omp(A, matvec(A, x0), 2)
    assert support == [3, 2]
    assert x == [F(0), F(0), F(-7, 6), F(11, 6)]
    assert matvec(A, x) == matvec(A, x0)  # exact fit, wrong support
    assert not mu_condition(A, 2)  # mu = 7/11


def test_omp_succeeds_where_bp_fails() -> None:
    A = [[F(7, 9), F(-3, 7), F(1, 9), F(8, 9)], [F(4, 9), F(2, 7), F(8, 9), F(1, 9)], [F(4, 9), F(6, 7), F(4, 9), F(-4, 9)]]
    x0 = [F(2), F(-1), F(0), F(0)]
    x, support = omp(A, matvec(A, x0), 2)
    assert x == x0 and support == [0, 1]


def test_stops_at_zero_residual() -> None:
    A = [[1, 0, 1], [0, 1, 1]]
    x, support = omp(A, [2, 2], 3)
    assert support == [2] and x == [0, 0, 2]
