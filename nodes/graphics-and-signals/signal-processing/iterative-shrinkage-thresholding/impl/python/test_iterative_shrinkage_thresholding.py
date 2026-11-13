# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-shrinkage-thresholding/. The authors are listed in prov/XSY6C1.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from iterative_shrinkage_thresholding import ista, ista_step, objective, rmatvec, matvec, soft_threshold


def solve(M, b):
    n = len(M)
    T = [[F(v) for v in M[i]] + [F(b[i])] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if T[r][c] != 0), None)
        if p is None:
            return None
        T[c], T[p] = T[p], T[c]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c] / T[c][c]
                T[r] = [a - f * e for a, e in zip(T[r], T[c])]
    return [T[i][n] / T[i][i] for i in range(n)]


def lasso_brute_force(A, y, lam):
    """Exact lasso minimisers: try every support and sign pattern, keep the points that pass the KKT test."""
    m, n = len(A), len(A[0])
    found = []
    for k in range(n + 1):
        for S in itertools.combinations(range(n), k):
            for sg in itertools.product((1, -1), repeat=k):
                G = [[sum(F(A[i][a]) * A[i][b] for i in range(m)) for b in S] for a in S]
                rhs = [sum(F(A[i][a]) * y[i] for i in range(m)) - lam * s for a, s in zip(S, sg)]
                z = solve(G, rhs) if k else []
                if z is None or any(v * s <= 0 for v, s in zip(z, sg)):
                    continue
                x = [F(0)] * n
                for j, v in zip(S, z):
                    x[j] = v
                if kkt_holds(A, y, lam, x):
                    found.append(x)
    return found


def kkt_holds(A, y, lam, x):
    """0 is in the subdifferential: A^T (y - A x) = lam sign(x_j) on the support and |.| <= lam off it."""
    c = rmatvec(A, [b - a for a, b in zip(matvec(A, x), y)])
    for cj, xj in zip(c, x):
        if xj > 0 and cj != lam or xj < 0 and cj != -lam or xj == 0 and abs(cj) > lam:
            return False
    return True


A0 = [[1, 1, 0], [0, 1, 1]]  # A^T A has eigenvalues 3, 1, 0, so L = 3


def test_soft_threshold_is_the_prox() -> None:
    # S_t(v) minimises 1/2 (z - v)^2 + t |z|; compare with a fine exact grid.
    for v in [F(k, 4) for k in range(-12, 13)]:
        for t in (F(0), F(1, 2), F(1)):
            z = soft_threshold(v, t)
            phi = lambda u: (u - v) ** 2 / 2 + t * abs(u)
            assert all(phi(z) <= phi(F(k, 16)) for k in range(-64, 65))


def test_example_values() -> None:
    xs = ista(A0, [F(3), F(1)], F(1, 2), F(3), 2)
    assert xs[1] == [F(5, 6), F(7, 6), F(1, 6)]
    stars = lasso_brute_force(A0, [3, 1], F(1, 2))
    assert stars == [[F(3, 2), F(1), F(0)]]
    assert objective(A0, [3, 1], F(1, 2), stars[0]) == F(11, 8)
    assert objective(A0, [3, 1], F(1, 2), xs[0]) == 5
    assert objective(A0, [3, 1], F(1, 2), xs[1]) == F(59, 36)
    assert xs[2] == [F(1), F(11, 9), F(0)]


@pytest.mark.parametrize("seed", range(6))
def test_objective_gap_bound_exact(seed) -> None:
    rng = random.Random(seed)
    m, n = rng.choice([(2, 3), (3, 3), (2, 4)])
    A = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(m)]
    if all(v == 0 for row in A for v in row):
        A[0][0] = 1
    y = [F(rng.randint(-4, 4)) for _ in range(m)]
    lam = F(rng.randint(1, 4), 2)
    L = F(sum(v * v for row in A for v in row))  # Frobenius norm squared >= largest eigenvalue of A^T A
    stars = lasso_brute_force(A, y, lam)
    assert stars
    Fstar = objective(A, y, lam, stars[0])
    assert all(objective(A, y, lam, s) == Fstar for s in stars)
    x0 = [F(0)] * n
    R2 = min(sum((a - b) ** 2 for a, b in zip(x0, s)) for s in stars)
    xs = ista(A, y, lam, L, 40, x0)
    vals = [objective(A, y, lam, x) for x in xs]
    for k in range(1, len(xs)):
        assert vals[k] - Fstar >= 0
        assert vals[k] - Fstar <= L * R2 / (2 * k)  # Beck and Teboulle 2009, Theorem 3.1
        assert vals[k] <= vals[k - 1]  # the objective never goes up with step 1/L


def test_exact_bound_with_tight_L() -> None:
    y, lam, L = [F(3), F(1)], F(1, 2), F(3)
    (xstar,) = lasso_brute_force(A0, y, lam)
    Fstar = objective(A0, y, lam, xstar)
    xs = ista(A0, y, lam, L, 60)
    R2 = sum(v * v for v in xstar)
    for k in range(1, 61):
        gap = objective(A0, y, lam, xs[k]) - Fstar
        assert 0 <= gap <= L * R2 / (2 * k)
    assert objective(A0, y, lam, xs[60]) - Fstar < F(1, 10**6)


def test_minimiser_is_a_fixed_point() -> None:
    rng = random.Random(21)
    for _ in range(20):
        A = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(2)]
        y = [F(rng.randint(-5, 5)) for _ in range(2)]
        lam = F(rng.randint(1, 3))
        L = F(sum(v * v for row in A for v in row)) or F(1)
        for s in lasso_brute_force(A, y, lam):
            assert ista_step(A, y, lam, L, s) == s


def test_large_lambda_gives_zero() -> None:
    # If lam >= max |A^T y| then x = 0 is optimal and ISTA stays there.
    y = [F(3), F(1)]
    lam = max(abs(v) for v in rmatvec(A0, y))
    xs = ista(A0, y, lam, F(3), 5)
    assert all(x == [0, 0, 0] for x in xs)


def test_bad_L() -> None:
    with pytest.raises(ValueError):
        ista(A0, [1, 1], F(1), F(0), 3)
