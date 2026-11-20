# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-intrusive-spectral-projection/. The authors are listed in prov/K2M34Y.jsonl.
import math
import random

from non_intrusive_spectral_projection import (
    basis_1d,
    evaluate,
    gauss_rule,
    ishigami,
    jacobi_eigen,
    mean_variance,
    nisp,
    sobol_from_coefficients,
    total_degree_set,
)


def moment(family, k):
    if k % 2:
        return 0.0
    if family == "uniform":
        return 1.0 / (k + 1)
    return float(math.prod(range(k - 1, 0, -2)))


def test_jacobi_eigen_diagonalizes():
    rng = random.Random(3)
    n = 6
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            a[i][j] = a[j][i] = rng.uniform(-1, 1)
    vals, v = jacobi_eigen(a)
    for k in range(n):
        av = [sum(a[i][j] * v[j][k] for j in range(n)) for i in range(n)]
        assert all(abs(av[i] - vals[k] * v[i][k]) < 1e-12 for i in range(n))


def test_gauss_rules_are_exact_to_degree_2m_minus_1():
    for family in ("uniform", "normal"):
        for m in range(1, 9):
            xs, ws = gauss_rule(family, m)
            assert abs(sum(ws) - 1.0) < 1e-13
            for k in range(2 * m):
                q = sum(w * x**k for x, w in zip(xs, ws))
                size = sum(w * abs(x) ** k for x, w in zip(xs, ws))
                assert abs(q - moment(family, k)) < 1e-12 * max(1.0, size)


def test_basis_is_orthonormal():
    for family in ("uniform", "normal"):
        xs, ws = gauss_rule(family, 10)
        for a in range(8):
            for b in range(8):
                g = sum(w * basis_1d(family, x, 8)[a] * basis_1d(family, x, 8)[b] for x, w in zip(xs, ws))
                assert abs(g - (1.0 if a == b else 0.0)) < 1e-11


def test_polynomial_is_recovered_exactly():
    rng = random.Random(11)
    fams = ["uniform", "normal"]
    index = total_degree_set(2, 4)
    true = [rng.uniform(-1, 1) for _ in index]

    def q(x):
        return evaluate(index, true, fams, x)

    got_index, got, runs = nisp(q, fams, 4, 5)
    assert got_index == index
    assert runs == 25
    assert max(abs(a - b) for a, b in zip(got, true)) < 1e-12


def test_exponential_of_gaussian():
    _, c, _ = nisp(lambda x: math.exp(x[0]), ["normal"], 5, 12)
    exact = [math.exp(0.5) / math.sqrt(math.factorial(n)) for n in range(6)]
    assert max(abs(a - b) for a, b in zip(c, exact)) < 1e-6
    mean, var = mean_variance(c)
    assert abs(mean - math.exp(0.5)) < 1e-10
    captured = sum(math.e / math.factorial(n) for n in range(1, 6))
    assert abs(var - captured) < 1e-5


def test_ishigami_moments_and_sobol_indices():
    index, c, runs = nisp(ishigami, ["uniform"] * 3, 8, 9)
    assert runs == 729
    mean, var = mean_variance(c)
    assert abs(mean - 3.5) < 1e-6
    assert abs(var - 13.844588) < 0.06
    s, st = sobol_from_coefficients(index, c)
    assert abs(s[0] - 0.3139) < 0.002
    assert abs(s[1] - 0.4424) < 0.002
    assert abs(s[2]) < 1e-12
    assert abs(st[2] - 0.2437) < 0.002


def test_aliasing_with_too_few_points():
    # degree 4 expansion of x^6 with a 3 point rule: the projection is wrong
    _, c_bad, _ = nisp(lambda x: x[0] ** 6, ["uniform"], 4, 3)
    _, c_good, _ = nisp(lambda x: x[0] ** 6, ["uniform"], 4, 6)
    assert abs(c_good[0] - 1.0 / 7.0) < 1e-13
    assert max(abs(a - b) for a, b in zip(c_bad, c_good)) > 1e-2
