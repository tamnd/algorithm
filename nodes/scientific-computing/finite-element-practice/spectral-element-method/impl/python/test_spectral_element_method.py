# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-element-method/. The authors are listed in prov/6Q7T79.jsonl.

import math
import random

import spectral_element_method as S

PI = math.pi


def u(x):
    return math.sin(PI * x) * math.exp(x)


def f(x):  # -u'' + u
    d2 = math.exp(x) * ((1 - PI * PI) * math.sin(PI * x) + 2 * PI * math.cos(PI * x))
    return -d2 + u(x)


PROBE = [i / 97 for i in range(98)]


def max_error(E, n):
    breaks = [i / E for i in range(E + 1)]
    _, U = S.sem_solve(breaks, n, f, 1.0)
    return max(abs(S.evaluate(breaks, n, U, x) - u(x)) for x in PROBE)


def test_hand_example_one_quadratic_element():
    xs, ws = S.gll(2)
    assert xs == [-1.0, 0.0, 1.0]
    assert max(abs(a - b) for a, b in zip(ws, (1 / 3, 4 / 3, 1 / 3))) < 1e-15
    D = S.derivative_matrix(xs)
    want = [[-1.5, 2.0, -0.5], [-0.5, 0.0, 0.5], [0.5, -2.0, 1.5]]
    assert max(abs(D[i][j] - want[i][j]) for i in range(3) for j in range(3)) < 1e-15
    points, U = S.sem_solve([0.0, 1.0], 2, lambda x: 1.0)
    assert points == [0.0, 0.5, 1.0]
    assert abs(U[1] - 0.125) < 1e-15  # u = x (1 - x) / 2


def test_gll_rule():
    xs, ws = S.gll(4)
    r = math.sqrt(3 / 7)
    assert max(abs(a - b) for a, b in zip(xs, (-1, -r, 0, r, 1))) < 1e-15
    assert max(abs(a - b) for a, b in zip(ws, (0.1, 49 / 90, 32 / 45, 49 / 90, 0.1))) < 1e-15
    for n in (3, 6, 9):
        xs, ws = S.gll(n)
        assert abs(sum(ws) - 2) < 1e-14
        for d in range(2 * n):  # exact up to degree 2n - 1
            exact = 0.0 if d % 2 else 2 / (d + 1)
            assert abs(sum(w * x ** d for x, w in zip(xs, ws)) - exact) < 1e-13
        d = 2 * n  # not exact at degree 2n
        assert abs(sum(w * x ** d for x, w in zip(xs, ws)) - 2 / (d + 1)) > 1e-6


def test_derivative_matrix_is_exact_for_degree_n():
    rng = random.Random(4)
    for n in (3, 7, 12):
        xs, _ = S.gll(n)
        D = S.derivative_matrix(xs)
        coef = [rng.uniform(-1, 1) for _ in range(n + 1)]
        p = [sum(c * x ** k for k, c in enumerate(coef)) for x in xs]
        dp = [sum(k * c * x ** (k - 1) for k, c in enumerate(coef) if k) for x in xs]
        got = [sum(D[i][j] * p[j] for j in range(n + 1)) for i in range(n + 1)]
        assert max(abs(a - b) for a, b in zip(got, dp)) < 1e-10


def test_diagonal_mass_is_the_row_sum_of_the_exact_mass():
    n = 5
    xs, ws = S.gll(n)
    fine_x, fine_w = S.gll(n + 1)  # exact for degree 2n + 1 >= 2n
    basis = [[S.lagrange_eval(xs, [1.0 if k == j else 0.0 for k in range(n + 1)], t) for t in fine_x]
             for j in range(n + 1)]
    exact = [[sum(w * a * b for w, a, b in zip(fine_w, basis[i], basis[j])) for j in range(n + 1)]
             for i in range(n + 1)]
    for i in range(n + 1):
        assert abs(sum(exact[i]) - ws[i]) < 1e-14  # the GLL mass lumps the exact mass
    assert max(abs(exact[i][j]) for i in range(n + 1) for j in range(n + 1) if i != j) > 1e-3


def test_exponential_convergence_in_the_degree():
    errs = [max_error(1, n) for n in (4, 8, 12)]
    assert errs[0] > 1e-3
    assert errs[1] < 1e-5
    assert errs[2] < 1e-9
    assert max_error(2, 10) < 1e-10


def test_algebraic_order_in_h_at_fixed_degree():
    e1, e2 = max_error(8, 2), max_error(16, 2)
    assert 2.7 < math.log2(e1 / e2) < 3.3  # h^(N+1) with N = 2
