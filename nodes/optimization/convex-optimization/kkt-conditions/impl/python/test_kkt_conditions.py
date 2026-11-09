# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kkt-conditions/. The authors are listed in prov/MERSHB.jsonl.

import random
from fractions import Fraction

from kkt_conditions import kkt_violation, solve_linear, solve_qp_kkt

F = Fraction


def objective(Q, c, x):
    n = len(c)
    return sum(x[i] * Q[i][j] * x[j] for i in range(n) for j in range(n)) / 2 + sum(c[i] * x[i] for i in range(n))


def hildreth(Q, c, A, b, sweeps=200000, tol=1e-13):
    """Reference solver in floats: coordinate ascent on the dual (Hildreth, 1957).

    x(lam) = -Q^{-1}(c + A^T lam); the dual is a concave quadratic in lam >= 0.
    """
    n, m = len(c), len(b)
    cols = [solve_linear(Q, [F(int(i == j)) for i in range(n)]) for j in range(n)]
    Qinv = [[float(cols[j][i]) for j in range(n)] for i in range(n)]
    Af = [[float(v) for v in row] for row in A]
    cf = [float(v) for v in c]
    bf = [float(v) for v in b]
    QiAt = [[sum(Qinv[i][j] * Af[k][j] for j in range(n)) for k in range(m)] for i in range(n)]
    P = [[sum(Af[k][i] * QiAt[i][l] for i in range(n)) for l in range(m)] for k in range(m)]
    Qic = [sum(Qinv[i][j] * cf[j] for j in range(n)) for i in range(n)]
    h = [bf[k] + sum(Af[k][i] * Qic[i] for i in range(n)) for k in range(m)]
    lam = [0.0] * m
    for _ in range(sweeps):
        change = 0.0
        for k in range(m):
            grad = sum(P[k][l] * lam[l] for l in range(m)) + h[k]
            new = max(0.0, lam[k] - grad / P[k][k])
            change = max(change, abs(new - lam[k]))
            lam[k] = new
        if change < tol:
            break
    return [-(Qic[i] + sum(QiAt[i][k] * lam[k] for k in range(m))) for i in range(n)]


def test_worked_example():
    # minimize (x1-1)^2 + (x2-2)^2 - 5 = x1^2 + x2^2 - 2 x1 - 4 x2
    # subject to x1 + x2 <= 2, x1 >= 0, x2 >= 0
    Q = [[F(2), F(0)], [F(0), F(2)]]
    c = [F(-2), F(-4)]
    A = [[F(1), F(1)], [F(-1), F(0)], [F(0), F(-1)]]
    b = [F(2), F(0), F(0)]
    x, lam = solve_qp_kkt(Q, c, A, b)
    assert x == [F(1, 2), F(3, 2)]
    assert lam == [F(1), F(0), F(0)]
    assert kkt_violation(Q, c, A, b, x, lam) == 0
    assert objective(Q, c, x) + 5 == F(1, 2)


def test_unconstrained_minimum_inside():
    Q = [[F(2), F(0)], [F(0), F(2)]]
    c = [F(-2), F(-4)]
    A = [[F(1), F(1)]]
    b = [F(10)]
    x, lam = solve_qp_kkt(Q, c, A, b)
    assert x == [F(1), F(2)] and lam == [F(0)]


def test_infeasible():
    Q = [[F(1)]]
    c = [F(0)]
    A = [[F(1)], [F(-1)]]
    b = [F(0), F(-1)]  # x <= 0 and x >= 1
    assert solve_qp_kkt(Q, c, A, b) is None


def random_instance(rng, n, m):
    M = [[F(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
    Q = [[sum(M[k][i] * M[k][j] for k in range(n)) + (1 if i == j else 0) for j in range(n)] for i in range(n)]
    c = [F(rng.randint(-5, 5)) for _ in range(n)]
    A = []
    while len(A) < m:
        row = [F(rng.randint(-3, 3)) for _ in range(n)]
        if any(row):
            A.append(row)
    x0 = [F(rng.randint(-2, 2)) for _ in range(n)]
    b = [sum(A[k][j] * x0[j] for j in range(n)) + rng.randint(0, 3) for k in range(m)]
    return Q, c, A, b


def test_against_hildreth_and_random_points():
    rng = random.Random(7)
    for trial in range(60):
        n = rng.randint(1, 3)
        m = rng.randint(1, 5)
        Q, c, A, b = random_instance(rng, n, m)
        res = solve_qp_kkt(Q, c, A, b)
        assert res is not None  # x0 is feasible by construction
        x, lam = res
        assert kkt_violation(Q, c, A, b, x, lam) == 0
        ref = hildreth(Q, c, A, b)
        assert max(abs(float(x[i]) - ref[i]) for i in range(n)) < 1e-6
        fx = objective(Q, c, x)
        for _ in range(200):
            y = [F(rng.randint(-40, 40), 8) for _ in range(n)]
            if all(sum(A[k][j] * y[j] for j in range(n)) <= b[k] for k in range(m)):
                assert fx <= objective(Q, c, y)
