# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/russian-roulette/. The authors are listed in prov/QF25TE.jsonl.

import math
import random
from fractions import Fraction as Fr

from russian_roulette import expected_terms, mean_and_variance, outcomes, roulette, series

A = [Fr(3), Fr(1, 2), Fr(2), Fr(5, 4), Fr(1)]


def const(q: Fr):
    return lambda k, w: q


def test_single_step_is_unbiased_with_known_variance() -> None:
    for v in (Fr(1), Fr(7, 3)):
        for q in (Fr(1, 10), Fr(1, 2), Fr(1)):
            pairs = [(q, v / q), (1 - q, Fr(0))]
            m, var = mean_and_variance([(p, x) for p, x in pairs if p > 0])
            assert m == v
            assert var == v * v * (1 - q) / q


def test_finite_series_exact_expectation() -> None:
    lists = [const(Fr(1, 2)), lambda k, w: [Fr(1, 3), Fr(3, 4), Fr(1), Fr(1, 5)][k]]
    # a survival probability that depends on the weight is also unbiased
    lists.append(lambda k, w: max(Fr(1, 10), min(Fr(1), Fr(3, 4) / w)))
    for q in lists:
        pairs = outcomes(A, q)
        m, var = mean_and_variance(pairs)
        assert m == sum(A)
        assert var > 0  # the full sum has variance 0


def test_without_division_the_mean_is_too_small() -> None:
    q = [Fr(1, 3), Fr(3, 4), Fr(1), Fr(1, 5)]
    m, _ = mean_and_variance(outcomes(A, lambda k, w: q[k], divide=False))
    keep = [math.prod(q[:k], start=Fr(1)) for k in range(len(A))]
    assert m == sum(a * p for a, p in zip(A, keep))
    assert m == Fr(3) + Fr(1, 6) + Fr(1, 2) + Fr(1, 4) * Fr(5, 4) + Fr(1, 20)
    assert m < sum(A)


def test_zero_survival_loses_the_tail() -> None:
    # q = 0 before a nonzero term breaks the condition of unbiasedness.
    m, _ = mean_and_variance(outcomes(A, lambda k, w: Fr(0) if k == 2 else Fr(1, 2)))
    assert m == A[0] + A[1] + A[2]


def test_expected_number_of_terms() -> None:
    assert expected_terms(5, const(Fr(1, 2))) == 1 + Fr(1, 2) + Fr(1, 4) + Fr(1, 8) + Fr(1, 16)
    assert expected_terms(5, const(Fr(1))) == 5


def test_geometric_series_within_four_sigma() -> None:
    # sum of e rho^k is e / (1 - rho). With q = rho the estimate is e times the
    # number of terms, a geometric variable, with variance e^2 rho / (1 - rho)^2.
    e, rho, n = 1.5, 0.6, 20000
    rng = random.Random(11)
    vals = [series(lambda k: e * rho ** k, lambda k, w: rho, rng) for _ in range(n)]
    assert all(abs(v / e - round(v / e)) < 1e-9 for v in vals)
    sigma = e * math.sqrt(rho) / (1 - rho)
    assert abs(sum(vals) / n - e / (1 - rho)) <= 4 * sigma / math.sqrt(n)


def test_sampled_mean_matches_exact_mean() -> None:
    q = [0.25, 0.75, 1.0, 0.2]
    m, var = mean_and_variance(outcomes(A, lambda k, w: Fr(q[k]).limit_denominator()))
    rng = random.Random(5)
    n = 20000
    a = [float(x) for x in A]
    vals = [series(lambda k: a[k] if k < len(a) else 0.0, lambda k, w: q[k] if k < len(q) else 0.0, rng) for _ in range(n)]
    assert abs(sum(vals) / n - float(m)) <= 4 * math.sqrt(float(var) / n)


def test_roulette_step() -> None:
    rng = random.Random(0)
    n = 20000
    vals = [roulette(2.0, 0.25, rng) for _ in range(n)]
    assert set(vals) <= {0.0, 8.0}
    assert abs(sum(vals) / n - 2.0) <= 4 * math.sqrt(4.0 * 0.75 / 0.25 / n)
    assert roulette(2.0, 0.0, rng) == 0.0
    assert roulette(2.0, 1.0, rng) == 2.0
