# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/value-function-approximation/. The authors are listed in prov/0BFJGH.jsonl.

import math
import random
from fractions import Fraction as F

from value_function_approximation import (
    d_norm2,
    projection_weights,
    semi_gradient_td0,
    solve,
    stationary_distribution,
    td_fixed_point,
    td_matrices,
    true_values,
)

P = [[F(1, 2), F(1, 2), F(0)], [F(1, 4), F(1, 2), F(1, 4)], [F(0), F(1, 2), F(1, 2)]]
R = [F(0), F(0), F(1)]
G = F(9, 10)
PHI = [[F(1), F(0)], [F(1), F(1)], [F(1), F(3)]]


def fl(m):
    return [[float(x) for x in row] for row in m]


def apply(phi, theta):
    return [sum(x * y for x, y in zip(row, theta)) for row in phi]


def test_worked_example_exact() -> None:
    mu = stationary_distribution(P)
    assert mu == [F(1, 4), F(1, 2), F(1, 4)]
    assert true_values(P, R, G) == [F(81, 44), F(9, 4), F(161, 44)]
    a, b = td_matrices(P, R, G, PHI, mu)
    assert a == [[F(1, 10), F(1, 8)], [F(1, 8), F(67, 80)]] and b == [F(1, 4), F(3, 4)]
    assert td_fixed_point(P, R, G, PHI, mu) == [F(185, 109), F(70, 109)]
    assert projection_weights(true_values(P, R, G), PHI, mu) == [F(1435, 836), F(131, 209)]


def test_td_fixed_point_solves_projected_bellman_equation() -> None:
    mu = stationary_distribution(P)
    theta = td_fixed_point(P, R, G, PHI, mu)
    v = apply(PHI, theta)
    tv = [R[s] + G * sum(P[s][t] * v[t] for t in range(3)) for s in range(3)]
    assert projection_weights(tv, PHI, mu) == theta


def test_error_bounds_exact() -> None:
    mu = stationary_distribution(P)
    v = true_values(P, R, G)
    vtd = apply(PHI, td_fixed_point(P, R, G, PHI, mu))
    pv = apply(PHI, projection_weights(v, PHI, mu))
    e_td = d_norm2([x - y for x, y in zip(vtd, v)], mu)
    e_pr = d_norm2([x - y for x, y in zip(pv, v)], mu)
    e_gap = d_norm2([x - y for x, y in zip(vtd, pv)], mu)
    assert e_td == e_pr + e_gap  # Pythagoras in the D norm
    assert e_td * (1 - G * G) <= e_pr  # ||V_TD - V|| <= ||Pi V - V|| / sqrt(1 - gamma^2)
    assert e_td * (1 - G) ** 2 <= e_pr  # the weaker 1 / (1 - gamma) bound
    assert e_td == F(217841, 23001616) and e_pr == F(169, 18392)


def test_a_is_positive_definite_on_random_chains() -> None:
    rng = random.Random(7)
    for _ in range(200):
        n, d = rng.randint(2, 5), rng.randint(1, 3)
        p = []
        for _ in range(n):
            w = [F(rng.randint(1, 5)) for _ in range(n)]
            p.append([x / sum(w) for x in w])
        mu = stationary_distribution(p)
        phi = [[F(rng.randint(-3, 3)) for _ in range(d)] for _ in range(n)]
        g = F(rng.randint(0, 99), 100)
        a, _ = td_matrices(p, [F(0)] * n, g, phi, mu)
        x = [F(rng.randint(-5, 5)) for _ in range(d)]
        quad = sum(x[i] * a[i][j] * x[j] for i in range(d) for j in range(d))
        assert quad >= (1 - g) * d_norm2(apply(phi, x), mu)


def test_expected_update_converges_to_fixed_point() -> None:
    mu = stationary_distribution(P)
    a, b = td_matrices(P, R, G, PHI, mu)
    a, b = fl(a), [float(x) for x in b]
    theta = [0.0, 0.0]
    for _ in range(3000):
        theta = [theta[i] + 0.5 * (b[i] - sum(a[i][j] * theta[j] for j in range(2))) for i in range(2)]
    assert all(abs(x - float(y)) < 1e-9 for x, y in zip(theta, [F(185, 109), F(70, 109)]))


def test_semi_gradient_td_reaches_fixed_point_with_seeds() -> None:
    target = [185 / 109, 70 / 109]
    runs = [semi_gradient_td0(fl(P), [0.0, 0.0, 1.0], 0.9, fl(PHI), 120000, 0.05, random.Random(s)) for s in range(4)]
    mean = [sum(t[k] for t in runs) / len(runs) for k in range(2)]
    assert all(abs(m - x) < 0.03 for m, x in zip(mean, target))
    assert all(math.dist(t, target) < 0.1 for t in runs)


def test_tabular_features_give_true_values() -> None:
    mu = stationary_distribution(P)
    eye = [[F(int(i == j)) for j in range(3)] for i in range(3)]
    assert td_fixed_point(P, R, G, eye, mu) == true_values(P, R, G)


def test_solve_rejects_singular() -> None:
    try:
        solve([[F(1), F(2)], [F(2), F(4)]], [F(1), F(1)])
    except ValueError:
        return
    raise AssertionError("expected ValueError")
