# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regression-polynomial-chaos/. The authors are listed in prov/MZG7P5.jsonl.
import math
import random

import pytest

from regression_polynomial_chaos import (
    cholesky,
    design_row,
    forward,
    gram,
    ishigami,
    least_squares,
    loo_error,
    mean_variance,
    regression_pce,
    sample,
    sobol_from_coefficients,
    total_degree_set,
)


def small_problem(seed):
    rng = random.Random(seed)
    fams = ["uniform", "normal"]
    index = total_degree_set(2, 2)
    xs = [sample(fams, rng) for _ in range(15)]
    rows = [design_row(index, fams, x) for x in xs]
    y = [math.sin(x[0]) + 0.3 * x[1] ** 3 + 0.1 * rng.gauss(0, 1) for x in xs]
    return rows, y


def test_polynomial_in_the_span_is_recovered_exactly():
    rng = random.Random(5)
    fams = ["uniform", "normal"]
    index = total_degree_set(2, 3)
    true = [rng.uniform(-1, 1) for _ in index]

    def q(x):
        return sum(a * b for a, b in zip(design_row(index, fams, x), true))

    got_index, c, loo = regression_pce(q, fams, 3, 2 * len(index), random.Random(9))
    assert got_index == index
    assert max(abs(a - b) for a, b in zip(c, true)) < 1e-9
    assert loo < 1e-18


def test_loo_identity_matches_brute_force_refits():
    for seed in range(3):
        rows, y = small_problem(seed)
        c, low = least_squares(rows, y)
        fast = loo_error(rows, y, c, low)
        total = 0.0
        for i in range(len(y)):
            ci, _ = least_squares(rows[:i] + rows[i + 1 :], y[:i] + y[i + 1 :])
            total += (y[i] - sum(a * b for a, b in zip(rows[i], ci))) ** 2
        mean = sum(y) / len(y)
        var = sum((v - mean) ** 2 for v in y) / (len(y) - 1)
        assert abs(fast - total / len(y) / var) < 1e-9 * max(1.0, fast)


def test_hat_diagonal_sums_to_the_number_of_terms():
    rows, _ = small_problem(4)
    low = cholesky(gram(rows))
    h = [sum(v * v for v in forward(low, r)) for r in rows]
    assert abs(sum(h) - len(rows[0])) < 1e-10
    assert all(0.0 <= v <= 1.0 + 1e-12 for v in h)


def test_residual_is_orthogonal_to_every_basis_column():
    rows, y = small_problem(7)
    c, _ = least_squares(rows, y)
    res = [yi - sum(a * b for a, b in zip(r, c)) for r, yi in zip(rows, y)]
    for j in range(len(rows[0])):
        assert abs(sum(r[j] * e for r, e in zip(rows, res))) < 1e-10


def test_empirical_gram_matrix_tends_to_identity():
    rng = random.Random(2)
    index = total_degree_set(1, 3)
    rows = [design_row(index, ["uniform"], sample(["uniform"], rng)) for _ in range(4000)]
    g = gram(rows)
    n = len(rows)
    assert max(abs(g[i][j] / n - (1.0 if i == j else 0.0)) for i in range(4) for j in range(4)) < 0.15


def test_exponential_of_gaussian():
    _, c, loo = regression_pce(lambda x: math.exp(x[0]), ["normal"], 6, 200, random.Random(1))
    exact = [math.exp(0.5) / math.sqrt(math.factorial(n)) for n in range(7)]
    assert max(abs(a - b) for a, b in zip(c, exact)) < 0.05
    assert loo < 1e-3


def test_ishigami_sobol_indices():
    index, c, loo = regression_pce(ishigami, ["uniform"] * 3, 6, 252, random.Random(0))
    mean, _ = mean_variance(c)
    s, st = sobol_from_coefficients(index, c)
    assert abs(mean - 3.5) < 0.1
    assert abs(s[0] - 0.3139) < 0.02
    assert abs(s[1] - 0.4424) < 0.04
    assert abs(st[2] - 0.2437) < 0.03
    assert loo < 0.1


def test_too_few_runs_is_rejected():
    with pytest.raises(ValueError):
        regression_pce(ishigami, ["uniform"] * 3, 2, 9, random.Random(0))
