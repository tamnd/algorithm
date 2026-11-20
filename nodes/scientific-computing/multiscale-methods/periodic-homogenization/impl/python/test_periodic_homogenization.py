# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/periodic-homogenization/. The authors are listed in prov/W15DY8.jsonl.
import math
import random
from fractions import Fraction

from periodic_homogenization import (
    cell_problem_1d,
    cell_problem_2d,
    corrector_gradient,
    homogenized_solve_1d,
)


def a_sin(y):
    return 2 + math.sin(2 * math.pi * y)


def harmonic(values):
    return len(values) / sum(1 / v for v in values)


def simpson(g, lo, hi, m):
    h = (hi - lo) / m
    s = g(lo) + g(hi)
    for i in range(1, m):
        s += (4 if i % 2 else 2) * g(lo + i * h)
    return s * h / 3


def exact_u_eps(eps, x, m=4000):
    """u for -(a(x / eps) u')' = 1, u(0) = u(1) = 0: a u' = C - x, so u(x) = int_0^x (C - s) / a(s / eps) ds."""
    inv = simpson(lambda s: 1 / a_sin(s / eps), 0.0, 1.0, m)
    mom = simpson(lambda s: s / a_sin(s / eps), 0.0, 1.0, m)
    c = mom / inv
    k = max(2, 2 * round(m * x / 2))
    return simpson(lambda s: (c - s) / a_sin(s / eps), 0.0, x, k), c


def test_1d_cell_problem_gives_the_harmonic_mean_exactly():
    rng = random.Random(3)
    a = [Fraction(rng.randint(1, 9), rng.randint(1, 4)) for _ in range(12)]
    a_star, chi = cell_problem_1d(a)
    assert a_star == Fraction(len(a)) / sum(1 / v for v in a)
    assert sum(chi) == 0
    assert a_star <= sum(a) / len(a)


def test_two_phase_1d_by_hand():
    a_star, _ = cell_problem_1d([Fraction(1), Fraction(4)])
    assert a_star == Fraction(8, 5)


def test_sine_coefficient_gives_sqrt3():
    for n in (16, 32, 64):
        a = [a_sin((k + 0.5) / n) for k in range(n)]
        a_star, _ = cell_problem_1d(a)
        assert abs(a_star - math.sqrt(3)) < 1e-6
    a_star, _ = cell_problem_1d([a_sin((k + 0.5) / 64) for k in range(64)])
    assert abs(a_star - 1.7320508075688772) < 1e-12


def test_laminate_2d_is_harmonic_across_and_arithmetic_along():
    n = 4
    a = [[Fraction(1) if i < n // 2 else Fraction(4) for i in range(n)] for _ in range(n)]
    A, chi1, chi2 = cell_problem_2d(a)
    assert A == [[Fraction(8, 5), 0], [0, Fraction(5, 2)]]
    assert all(c == 0 for c in chi2)
    assert sum(chi1) == 0


def test_random_2d_cell_is_symmetric_and_within_the_bounds():
    rng = random.Random(7)
    n = 6
    a = [[rng.uniform(1.0, 10.0) for _ in range(n)] for _ in range(n)]
    A, _, _ = cell_problem_2d(a)
    flat = [v for row in a for v in row]
    lower, upper = harmonic(flat), sum(flat) / len(flat)
    assert abs(A[0][1] - A[1][0]) < 1e-12
    for d in range(2):
        assert lower - 1e-12 <= A[d][d] <= upper + 1e-12
    assert A[0][0] * A[1][1] - A[0][1] ** 2 > 0


def test_homogenized_solution_at_the_midpoint():
    u0 = homogenized_solve_1d(math.sqrt(3), 1.0, 8)
    assert abs(u0[4] - 1 / (8 * math.sqrt(3))) < 1e-14
    exact = homogenized_solve_1d(Fraction(2), Fraction(1), 4)
    assert exact == [0, Fraction(3, 64), Fraction(1, 16), Fraction(3, 64), 0]


def test_u_eps_converges_to_u0_at_rate_eps():
    a_star = math.sqrt(3)
    errors = []
    for eps in (1 / 4, 1 / 8, 1 / 16, 1 / 32):
        err = 0.0
        for x in [0.05 + 0.9 * k / 37 for k in range(38)]:
            u, _ = exact_u_eps(eps, x)
            err = max(err, abs(u - x * (1 - x) / (2 * a_star)))
        errors.append(err)
    for e1, e2 in zip(errors, errors[1:]):
        assert 1.5 < e1 / e2 < 2.6


def test_corrector_fixes_the_gradient():
    a_star = math.sqrt(3)
    for eps in (1 / 8, 1 / 32):
        _, c = exact_u_eps(eps, 0.5)
        plain, corrected = 0.0, 0.0
        for x in (0.1, 0.23, 0.37, 0.61, 0.83):
            du_eps = (c - x) / a_sin(x / eps)
            du0 = (0.5 - x) / a_star
            plain = max(plain, abs(du_eps - du0))
            corrected = max(corrected, abs(du_eps - corrector_gradient(a_sin, a_star, du0, x, eps)))
        assert plain > 0.05
        assert corrected < eps
