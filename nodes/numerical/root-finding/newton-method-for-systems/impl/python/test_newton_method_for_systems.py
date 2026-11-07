# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-method-for-systems/. The authors are listed in prov/EB6BTR.jsonl.

import math
import random
from decimal import Decimal, getcontext
from fractions import Fraction

from newton_method_for_systems import (forward_difference_jacobian, newton_system,
                                       norm_inf, solve)


def F(v):
    return [v[0] ** 2 + v[1] ** 2 - 4, v[0] * v[1] - 1]


def J(v):
    return [[2 * v[0], 2 * v[1]], [v[1], v[0]]]


def exact_root():
    getcontext().prec = 60
    s3 = Decimal(3).sqrt()
    return (2 + s3).sqrt(), (2 - s3).sqrt()


def dec(q):
    return Decimal(q.numerator) / Decimal(q.denominator)


def test_circle_hyperbola_example():
    r = newton_system(F, J, [2.0, 0.0])
    assert r.reason == "converged"
    assert (r.iterations, r.f_evals, r.j_evals) == (6, 6, 6)
    X, Y = exact_root()
    assert r.x[0] == float(X) and abs(Decimal(r.x[1]) - Y) <= Decimal(2) ** -53
    assert r.steps[0] == 0.5


def test_observed_order_two_in_exact_arithmetic():
    X, Y = exact_root()
    x = [Fraction(2), Fraction(0)]
    errs = []
    for _ in range(7):
        errs.append(max(abs(dec(x[0]) - X), abs(dec(x[1]) - Y)))
        s = solve(J(x), [-t for t in F(x)])
        x = [x[0] + s[0], x[1] + s[1]]
    ratios = [errs[k + 1] / errs[k] ** 2 for k in range(6)]
    assert all(Decimal("0.2") < q < Decimal("0.75") for q in ratios)
    assert abs(ratios[5] - Decimal(2).sqrt() / 2) < Decimal("1e-6")
    # observed order log(e2/e1)/log(e1/e0) close to 2
    q = (errs[6] / errs[5]).ln() / (errs[5] / errs[4]).ln()
    assert abs(q - 2) < Decimal("0.01")


def test_exact_root_with_fractions():
    # F(x, y) = (x + y - 3, x - y - 1) is linear: one step lands on (2, 1)
    G = lambda v: [v[0] + v[1] - 3, v[0] - v[1] - 1]
    JG = lambda v: [[1, 1], [1, -1]]
    r = newton_system(G, JG, [Fraction(10), Fraction(-7)])
    assert r.x == [2, 1] and r.reason == "root"
    assert (r.iterations, r.f_evals, r.j_evals) == (2, 2, 1)


def test_start_at_root():
    r = newton_system(F, J, [Fraction(2), Fraction(0)], max_iter=1)
    assert r.reason == "kmax reached" and r.x == [2, Fraction(1, 2)] and r.f_evals == 1
    G = lambda v: [v[0] - 1, v[1] - 2]
    r = newton_system(G, lambda v: [[1, 0], [0, 1]], [1, 2])
    assert r.reason == "root" and (r.f_evals, r.j_evals) == (1, 0)


def test_singular_jacobian():
    # J(0, y) is singular for F(x, y) = (x^2 + y^2 - 4, x y - 1)
    r = newton_system(F, J, [0.0, 0.0])
    assert r.reason == "singular" and r.f_evals == 1 and r.j_evals == 1
    r = newton_system(F, J, [Fraction(1), Fraction(1)])
    assert r.reason == "singular"


def test_singular_root_is_linear_and_needs_absolute_tolerance():
    G = lambda v: [v[0] ** 2, v[1]]
    JG = lambda v: [[2 * v[0], 0.0], [0.0, 1.0]]
    r = newton_system(G, JG, [1.0, 1.0], max_iter=100)
    assert r.reason == "kmax reached" and r.x[0] == 2.0 ** -100
    for a, b in zip(r.steps[1:], r.steps[2:]):
        assert b == a / 2
    r = newton_system(G, JG, [1.0, 1.0], tol_abs=1e-8, max_iter=100)
    assert r.reason == "converged" and r.iterations == 27


def test_no_solution_fails_or_stops():
    # x^2 + y^2 + 1 = 0, x - y = 0 has no real solution
    G = lambda v: [v[0] ** 2 + v[1] ** 2 + 1, v[0] - v[1]]
    JG = lambda v: [[2 * v[0], 2 * v[1]], [1.0, -1.0]]
    r = newton_system(G, JG, [1.0, 1.0], max_iter=50)
    assert not r.converged
    assert r.f_evals <= 50


def test_nan_and_inf():
    G = lambda v: [math.log(v[0]) if v[0] > 0 else float("nan"), v[1]]
    JG = lambda v: [[1 / v[0], 0.0], [0.0, 1.0]]
    r = newton_system(G, JG, [10.0, 1.0])
    assert r.reason == "failure"
    H = lambda v: [math.exp(v[0]) - 1, v[1]]
    JH = lambda v: [[math.exp(v[0]), 0.0], [0.0, 1.0]]
    r = newton_system(H, JH, [-800.0, 0.0])
    assert r.reason in ("singular", "failure")


def test_freudenstein_roth_from_standard_start():
    G = lambda v: [-13 + v[0] + ((5 - v[1]) * v[1] - 2) * v[1],
                   -29 + v[0] + ((v[1] + 1) * v[1] - 14) * v[1]]
    JG = lambda v: [[1.0, 10 * v[1] - 3 * v[1] ** 2 - 2],
                    [1.0, 3 * v[1] ** 2 + 2 * v[1] - 14]]
    r = newton_system(G, JG, [0.5, -2.0])
    assert r.converged and abs(r.x[0] - 5) < 1e-12 and abs(r.x[1] - 4) < 1e-12
    assert r.iterations == 44


def test_finite_difference_jacobian():
    jac = forward_difference_jacobian(F)
    r = newton_system(F, jac, [2.0, 0.0])
    assert r.converged and norm_inf([r.x[0] - 1.9318516525781366,
                                     r.x[1] - 0.5176380902050416]) <= 2.3e-16
    assert jac.calls == 3 * r.j_evals


def test_solve_pivoting_exact():
    a = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(1)]]
    assert solve(a, [Fraction(2), Fraction(3)]) == [1, 2]
    assert solve([[1, 2], [2, 4]], [1, 2]) is None


def test_random_well_conditioned_systems():
    rng = random.Random(20261108)
    for _ in range(500):
        n = rng.randint(1, 4)
        z = [rng.uniform(-2, 2) for _ in range(n)]
        c = [rng.uniform(-0.3, 0.3) for _ in range(n)]
        # F_i(x) = x_i - z_i + c_i (x_i - z_i)^2 + 0.1 * sum_j (x_j - z_j)^3 / n
        def G(v, z=z, c=c, n=n):
            d = [v[i] - z[i] for i in range(n)]
            t = sum(dj ** 3 for dj in d) / (10 * n)
            return [d[i] + c[i] * d[i] ** 2 + t for i in range(n)]

        def JG(v, z=z, c=c, n=n):
            d = [v[i] - z[i] for i in range(n)]
            return [[(1 + 2 * c[i] * d[i] if i == j else 0) + 3 * d[j] ** 2 / (10 * n)
                     for j in range(n)] for i in range(n)]

        x0 = [z[i] + rng.uniform(-0.5, 0.5) for i in range(n)]
        r = newton_system(G, JG, x0)
        assert r.converged
        assert norm_inf([r.x[i] - z[i] for i in range(n)]) <= 1e-14
        assert r.f_evals <= 10 and r.f_evals == r.iterations
