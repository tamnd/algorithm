# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leslie-matrix/. The authors are listed in prov/V3XCAW.jsonl.
"""Tests of the Leslie model against the page example, exact Fraction
arithmetic, the closed forms, and random matrices with fixed seeds."""

import math
import random
from fractions import Fraction

import pytest

from leslie_matrix import (
    characteristic,
    euler_lotka_root,
    gcd_rule,
    is_primitive,
    leslie,
    net_reproductive_rate,
    power_iteration,
    project,
    reproductive_values,
    sensitivities,
    stable_distribution,
)

F = [0, 1.5, 1.0]
P = [0.5, 0.25]


def close(xs, ys, tol=1e-6):
    return len(xs) == len(ys) and all(abs(a - b) < tol for a, b in zip(xs, ys))


def matvec(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def test_page_projection_exact():
    Fq = [Fraction(0), Fraction(3, 2), Fraction(1)]
    Pq = [Fraction(1, 2), Fraction(1, 4)]
    path = project(Fq, Pq, [100, 0, 0], 5)
    assert path == [[0, 50, 0], [75, 0, Fraction(25, 2)], [Fraction(25, 2), Fraction(75, 2), 0],
                    [Fraction(225, 4), Fraction(25, 4), Fraction(75, 8)],
                    [Fraction(75, 4), Fraction(225, 8), Fraction(25, 16)]]
    assert [sum(n) for n in path] == [50, Fraction(175, 2), 50, Fraction(575, 8), Fraction(775, 16)]
    A = leslie(Fq, Pq)
    n = [100, 0, 0]
    for step in path:
        n = matvec(A, n)
        assert n == step
    assert characteristic(Fq, Pq) == [1, 0, Fraction(-3, 4), Fraction(-1, 8)]
    assert net_reproductive_rate(Fq, Pq) == Fraction(7, 8)


def test_page_eigen_values():
    lam = euler_lotka_root(F, P)
    assert abs(lam - math.cos(math.pi / 9)) < 1e-12
    for theta in (math.pi / 9, 7 * math.pi / 9, 13 * math.pi / 9):
        x = math.cos(theta)
        assert abs(x ** 3 - 0.75 * x - 0.125) < 1e-12
    assert abs(math.cos(7 * math.pi / 9) + 0.766044) < 1e-6
    assert abs(math.cos(13 * math.pi / 9) + 0.173648) < 1e-6
    assert close(stable_distribution(F, P), [0.597497, 0.317922, 0.084581])
    assert close(reproductive_values(F, P), [1, 1.879385, 1.064178])
    lam_p, w_p = power_iteration(F, P)
    assert abs(lam_p - lam) < 1e-10 and close(w_p, stable_distribution(F, P), tol=1e-9)


def test_eigenvectors_and_elasticities():
    A = leslie(F, P)
    lam = euler_lotka_root(F, P)
    w = stable_distribution(F, P)
    v = reproductive_values(F, P)
    assert close(matvec(A, w), [lam * x for x in w], tol=1e-12)
    At = [list(col) for col in zip(*A)]
    assert close(matvec(At, v), [lam * x for x in v], tol=1e-12)
    s, e = sensitivities(F, P)
    assert abs(sum(map(sum, e)) - 1) < 1e-12
    assert abs(e[0][1] - 0.394931) < 1e-6 and abs(e[0][2] - 0.070046) < 1e-6
    assert abs(e[1][0] - 0.464977) < 1e-6 and abs(e[2][1] - 0.070046) < 1e-6
    h = 1e-6
    for i, j in ((0, 1), (0, 2), (1, 0), (2, 1)):
        F2, P2 = list(F), list(P)
        if i == 0:
            F2[j] += h
        else:
            P2[j] += h
        assert abs((euler_lotka_root(F2, P2) - lam) / h - s[i][j]) < 1e-5


def test_random_matrices():
    rng = random.Random(71)
    for _ in range(300):
        k = rng.randint(2, 6)
        Fr = [rng.choice([0, rng.uniform(0, 3)]) for _ in range(k - 1)] + [rng.uniform(0.1, 3)]
        Pr = [rng.uniform(0.05, 1) for _ in range(k - 1)]
        lam = euler_lotka_root(Fr, Pr)
        coeffs = characteristic(Fr, Pr)
        assert abs(sum(c * lam ** (k - j) for j, c in enumerate(coeffs))) < 1e-9 * max(1, lam ** k)
        A = leslie(Fr, Pr)
        w = stable_distribution(Fr, Pr)
        assert close(matvec(A, w), [lam * x for x in w], tol=1e-9)
        r0 = net_reproductive_rate(Fr, Pr)
        assert (lam > 1) == (r0 > 1) and (lam < 1) == (r0 < 1)
        assert is_primitive(Fr, Pr) == gcd_rule(Fr, Pr)
        n = [1.0] + [0.0] * (k - 1)
        log_growth = 0.0
        for t in range(600):
            m = project(Fr, Pr, n, 1)[0]
            if t >= 300:
                log_growth += math.log(sum(m) / sum(n))
            n = [x / sum(m) for x in m]
        assert abs(log_growth / 300 - math.log(lam)) < 0.02


def test_imprimitive_example_cycles():
    Fq = [0, 0, Fraction(6)]
    Pq = [Fraction(1, 2), Fraction(1, 3)]
    assert not is_primitive(Fq, Pq) and not gcd_rule(Fq, Pq)
    assert net_reproductive_rate(Fq, Pq) == 1
    path = project(Fq, Pq, [6, 0, 0], 6)
    assert path[2] == [6, 0, 0] and path[5] == [6, 0, 0]
    assert path[0] == [0, 3, 0] and path[1] == [0, 0, 1]
    assert is_primitive(F, P)


def test_input_checks():
    with pytest.raises(ValueError):
        leslie([1, 2], [0.5, 0.5])
    with pytest.raises(ValueError):
        project(F, [1.5, 0.2], [1, 0, 0], 1)
    with pytest.raises(ValueError):
        euler_lotka_root([0, 0], [0.5])
    assert project(F, P, [1, 2, 3], 0) == []
