# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-graphical-model/. The authors are listed in prov/65EW3P.jsonl.

import itertools
import math
import random
from fractions import Fraction

from gaussian_graphical_model import (conditional_covariance, edges_of, graphical_lasso, inverse,
                                      matmul, partial_correlation, sub)


def random_precision(p, rng, density=0.5):
    """A sparse, strictly diagonally dominant (so positive definite) integer matrix."""
    t = [[Fraction(0)] * p for _ in range(p)]
    for i, j in itertools.combinations(range(p), 2):
        if rng.random() < density:
            t[i][j] = t[j][i] = Fraction(rng.choice([-3, -2, -1, 1, 2, 3]))
    for i in range(p):
        t[i][i] = sum(abs(x) for x in t[i]) + rng.randint(1, 4)
    return t


def separated(p, edges, A, B, S):
    adj = {v: set() for v in range(p)}
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    seen, stack = set(A), list(A)
    while stack:
        v = stack.pop()
        if v in B:
            return False
        for w in adj[v] - seen - set(S):
            seen.add(w)
            stack.append(w)
    return True


def test_precision_zero_iff_zero_conditional_covariance():
    rng = random.Random(1972)
    for _ in range(30):
        p = rng.randint(2, 5)
        theta = random_precision(p, rng)
        sigma = inverse(theta)
        for i, j in itertools.combinations(range(p), 2):
            rest = [k for k in range(p) if k not in (i, j)]
            c = conditional_covariance(sigma, [i, j], rest)
            # Cov(X_ij | rest) is the inverse of the 2x2 block of Theta
            assert c == inverse(sub(theta, [i, j], [i, j]))
            assert (c[0][1] == 0) == (theta[i][j] == 0)
            # the partial correlation is the correlation of the conditional covariance
            pc = float(c[0][1]) / math.sqrt(float(c[0][0] * c[1][1]))
            assert abs(pc - partial_correlation([[float(x) for x in r] for r in theta], i, j)) < 1e-12


def test_global_markov_property_from_the_zeros():
    rng = random.Random(7)
    for _ in range(20):
        p = rng.randint(3, 5)
        theta = random_precision(p, rng, 0.4)
        sigma = inverse(theta)
        edges = edges_of(theta)
        for lab in itertools.product(range(4), repeat=p):
            A = [v for v in range(p) if lab[v] == 0]
            B = [v for v in range(p) if lab[v] == 1]
            S = [v for v in range(p) if lab[v] == 2]
            if A and B and separated(p, edges, A, B, S):
                c = conditional_covariance(sigma, A + B, S)
                assert all(c[a][len(A) + b] == 0 for a in range(len(A)) for b in range(len(B)))


def test_marginal_zero_is_not_conditional_zero():
    # chain 0 - 1 - 2: Theta_02 = 0 but Sigma_02 != 0
    theta = [[Fraction(2), Fraction(-1), Fraction(0)], [Fraction(-1), Fraction(2), Fraction(-1)],
             [Fraction(0), Fraction(-1), Fraction(2)]]
    sigma = inverse(theta)
    assert sigma[0][2] == Fraction(1, 4)
    assert conditional_covariance(sigma, [0, 2], [1])[0][1] == 0


def sample_cov(sigma, n, rng):
    p = len(sigma)
    lo = [[0.0] * p for _ in range(p)]  # Cholesky factor
    for i in range(p):
        for j in range(i + 1):
            s = sigma[i][j] - sum(lo[i][k] * lo[j][k] for k in range(j))
            lo[i][j] = math.sqrt(s) if i == j else s / lo[j][j]
    acc = [[0.0] * p for _ in range(p)]
    for _ in range(n):
        z = [rng.gauss(0, 1) for _ in range(p)]
        x = [sum(lo[i][k] * z[k] for k in range(i + 1)) for i in range(p)]
        for i in range(p):
            for j in range(p):
                acc[i][j] += x[i] * x[j]
    return [[a / n for a in row] for row in acc]


def test_rho_zero_gives_the_inverse():
    rng = random.Random(1)
    theta = random_precision(4, rng, 0.7)
    s = [[float(x) for x in r] for r in inverse(theta)]
    est, _ = graphical_lasso(s, 0.0)
    for i in range(4):
        for j in range(4):
            assert abs(est[i][j] - float(theta[i][j])) < 1e-6


def test_kkt_conditions_and_support_recovery():
    p = 5
    true = [[1.0 if i == j else (0.4 if abs(i - j) == 1 else 0.0) for j in range(p)] for i in range(p)]
    sigma = [[float(x) for x in r] for r in inverse([[Fraction(x).limit_denominator() for x in r] for r in true])]
    s = sample_cov(sigma, 3000, random.Random(2008))
    rho = 0.2
    theta, w = graphical_lasso(s, rho)
    # W is the inverse of Theta
    prod = matmul(w, theta)
    assert all(abs(prod[i][j] - (i == j)) < 1e-6 for i in range(p) for j in range(p))
    # stationarity: W - S = rho * subgradient of |Theta|
    for i in range(p):
        assert abs(w[i][i] - s[i][i] - rho) < 1e-9
        for j in range(p):
            if i != j:
                if abs(theta[i][j]) > 1e-7:
                    assert abs(w[i][j] - s[i][j] - rho * math.copysign(1, theta[i][j])) < 1e-6
                else:
                    assert abs(w[i][j] - s[i][j]) <= rho + 1e-6
    assert edges_of(theta, 1e-6) == {(i, i + 1) for i in range(p - 1)}


def test_large_rho_gives_a_diagonal_precision():
    rng = random.Random(5)
    s = [[float(x) for x in r] for r in inverse(random_precision(4, rng, 0.8))]
    rho = max(abs(s[i][j]) for i in range(4) for j in range(4) if i != j)
    theta, _ = graphical_lasso(s, rho)
    assert edges_of(theta, 1e-12) == set()
    for i in range(4):
        assert abs(theta[i][i] - 1 / (s[i][i] + rho)) < 1e-9
