# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mercer-theorem/. The authors are listed in prov/Z2X9JZ.jsonl.

import math
import random

from mercer_theorem import (
    brownian,
    brownian_eigenvalue,
    brownian_partial_sum,
    gaussian,
    gram,
    jacobi_eigen,
    nystrom_eigenvalues,
)


def reconstruct(vals, v):
    n = len(vals)
    return [[sum(v[i][k] * vals[k] * v[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


def test_jacobi_solves_small_symmetric_matrices() -> None:
    vals, _ = jacobi_eigen([[2.0, 1.0], [1.0, 2.0]])
    assert sorted(round(x, 12) for x in vals) == [1.0, 3.0]
    rng = random.Random(9)
    for n in (1, 3, 6, 10):
        a = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                a[i][j] = a[j][i] = rng.uniform(-1, 1)
        vals, v = jacobi_eigen(a)
        b = reconstruct(vals, v)
        assert all(abs(a[i][j] - b[i][j]) < 1e-10 for i in range(n) for j in range(n))
        vtv = [[sum(v[k][i] * v[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        assert all(abs(vtv[i][j] - (i == j)) < 1e-10 for i in range(n) for j in range(n))


def test_gaussian_gram_eigenvalues_are_nonnegative() -> None:
    rng = random.Random(1909)
    for sigma in (0.3, 1.0, 3.0):
        for n in (5, 12, 20):
            xs = [rng.uniform(-2, 2) for _ in range(n)]
            vals, _ = jacobi_eigen(gram(xs, gaussian(sigma)))
            assert min(vals) >= -1e-12 * n
            assert math.isclose(sum(vals), n, rel_tol=1e-10)  # the trace is n


def test_a_symmetric_function_that_is_not_a_kernel() -> None:
    vals, _ = jacobi_eigen(gram([0.0, 1.0], lambda x, z: abs(x - z)))
    assert math.isclose(min(vals), -1.0, abs_tol=1e-12)
    rng = random.Random(2)
    xs = [rng.uniform(0, 1) for _ in range(10)]
    vals, _ = jacobi_eigen(gram(xs, lambda x, z: abs(x - z)))
    assert min(vals) < -1e-3


def test_brownian_expansion_converges_uniformly() -> None:
    grid = [i / 40 for i in range(41)]
    errs = []
    for terms in (5, 20, 80, 320):
        errs.append(max(abs(brownian_partial_sum(terms, x, z) - min(x, z)) for x in grid for z in grid))
    assert all(e2 < e1 for e1, e2 in zip(errs, errs[1:]))
    # The tail of sum lam_j e_j(x)^2 is at most 2 sum_{j > N} lam_j < 2 / (pi^2 (N - 1/2)).
    for terms, e in zip((5, 20, 80, 320), errs):
        assert e <= 2 / (math.pi**2 * (terms - 0.5))


def test_brownian_diagonal_partial_sums_increase_to_the_kernel() -> None:
    for x in (0.1, 0.5, 0.9, 1.0):
        sums = [brownian_partial_sum(t, x, x) for t in (1, 2, 4, 8, 16, 64)]
        assert all(s1 <= s2 + 1e-15 for s1, s2 in zip(sums, sums[1:]))
        assert all(s <= x + 1e-12 for s in sums)
        assert abs(sums[-1] - x) < 0.01


def test_trace_formula() -> None:
    # sum_j lam_j = int_0^1 min(x, x) dx = 1/2
    assert abs(sum(brownian_eigenvalue(j) for j in range(1, 200001)) - 0.5) < 1e-5


def test_nystrom_eigenvalues_approach_the_operator_eigenvalues() -> None:
    est = nystrom_eigenvalues(brownian, 40)
    assert min(est) > 0
    for j in range(1, 5):
        assert abs(est[j - 1] - brownian_eigenvalue(j)) < 0.02 * brownian_eigenvalue(j) + 1e-4
