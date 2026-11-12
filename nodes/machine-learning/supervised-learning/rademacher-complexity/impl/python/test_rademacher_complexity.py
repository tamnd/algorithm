# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rademacher-complexity/. The authors are listed in prov/3MG65J.jsonl.

import random
from fractions import Fraction
from itertools import product

from rademacher_complexity import (
    apply_coordinatewise, linear_unit_ball_bound, linear_unit_ball_exact, massart_bound,
    monte_carlo_tolerance, rademacher_exact, rademacher_monte_carlo, threshold_vectors,
)


def test_exact_values_by_hand():
    assert rademacher_exact([(1, -1, 1, 1)]) == 0
    assert rademacher_exact(list(product((-1, 1), repeat=4))) == 1
    assert rademacher_exact([(1, 1, 1, 1), (-1, -1, -1, -1)]) == Fraction(3, 8)


def test_thresholds_exact_values():
    assert rademacher_exact(threshold_vectors([1, 2, 3, 4])) == Fraction(19, 32)
    assert rademacher_exact(threshold_vectors(list(range(10)))) == Fraction(1067, 2560)


def test_monte_carlo_agrees_with_enumeration():
    rng = random.Random(2002)
    for A in (threshold_vectors(list(range(8))),
              [tuple(rng.choice((-1, 1)) for _ in range(10)) for _ in range(6)],
              [tuple(Fraction(rng.randint(-3, 3), 3) for _ in range(9)) for _ in range(5)]):
        exact = float(rademacher_exact(A))
        est = rademacher_monte_carlo(A, 4000, random.Random(5))
        assert abs(est - exact) <= monte_carlo_tolerance(A, 4000, 1e-6)


def test_massart_bound_holds():
    rng = random.Random(3)
    for _ in range(30):
        n = rng.randint(2, 10)
        A = [tuple(rng.randint(-2, 2) for _ in range(n)) for _ in range(rng.randint(2, 8))]
        assert float(rademacher_exact(A)) <= massart_bound(A) + 1e-12


def test_contraction_lemma_on_a_finite_set():
    def ramp(t):  # 1-Lipschitz
        return min(Fraction(1), max(Fraction(0), 1 - t))
    rng = random.Random(4)
    for _ in range(30):
        n = rng.randint(2, 9)
        A = [tuple(Fraction(rng.randint(-4, 4), 2) for _ in range(n)) for _ in range(5)]
        assert rademacher_exact(apply_coordinatewise(ramp, A)) <= rademacher_exact(A)
        double = apply_coordinatewise(lambda t: 2 * t, A)  # 2-Lipschitz, equality
        assert rademacher_exact(double) == 2 * rademacher_exact(A)


def test_linear_class_bound():
    rng = random.Random(6)
    for _ in range(10):
        n = rng.randint(2, 10)
        xs = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(n)]
        r = max(sum(c * c for c in x) ** 0.5 for x in xs)
        exact = linear_unit_ball_exact(xs)
        assert exact <= linear_unit_ball_bound(xs) + 1e-12 <= r / n ** 0.5 + 2e-12
