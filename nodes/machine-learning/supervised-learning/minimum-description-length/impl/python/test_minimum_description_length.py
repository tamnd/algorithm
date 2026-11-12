# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-description-length/. The authors are listed in prov/71J32F.jsonl.

import math
import random
from fractions import Fraction
from itertools import product

from minimum_description_length import (bin_counts, code_length, code_parts, code_probability, dirichlet_marginal,
                                        mdl_select, sample)


def test_kraft_holds_with_equality_for_each_model() -> None:
    for b, n in ((1, 3), (2, 3), (3, 2)):
        for j in range(b + 1):
            k = 2 ** j
            total = sum((code_probability(list(xs), b, k) for xs in product(range(2 ** b), repeat=n)), Fraction(0))
            assert total == Fraction(1, b + 1)


def test_code_length_is_minus_log_probability() -> None:
    rng = random.Random(2)
    for _ in range(50):
        b = rng.randint(1, 6)
        xs = [rng.randrange(2 ** b) for _ in range(rng.randint(1, 30))]
        k = 2 ** rng.randint(0, b)
        p = code_probability(xs, b, k)
        assert abs(code_length(xs, b, k) - (-math.log2(p.numerator) + math.log2(p.denominator))) < 1e-9


def test_two_part_code_equals_bayes_evidence() -> None:
    rng = random.Random(3)
    for _ in range(50):
        b = rng.randint(1, 5)
        xs = [rng.randrange(2 ** b) for _ in range(rng.randint(1, 25))]
        k = 2 ** rng.randint(0, b)
        assert code_probability(xs, b, k) == dirichlet_marginal(xs, b, k)
        # The same evidence, built one point at a time with Laplace's rule of succession.
        width = 2 ** b // k
        seen = [0] * k
        p = Fraction(1, b + 1)
        for t, x in enumerate(xs):
            p *= Fraction(seen[x // width] + 1, t + k) * Fraction(1, width)
            seen[x // width] += 1
        assert p == code_probability(xs, b, k)


def test_cost_over_maximum_likelihood_is_at_most_the_count_code() -> None:
    rng = random.Random(4)
    for _ in range(50):
        b = rng.randint(1, 8)
        xs = [rng.randrange(2 ** b) for _ in range(rng.randint(1, 300))]
        k = 2 ** rng.randint(0, b)
        n = len(xs)
        _, counts, labels, positions = code_parts(xs, b, k)
        ml = -sum(v * math.log2(v / n) for v in bin_counts(xs, 2 ** b, k) if v)
        assert labels <= ml + 1e-9
        assert labels + counts - ml <= math.log2(math.comb(n + k - 1, k - 1)) + 1e-9
        assert positions == n * math.log2(2 ** b / k)


def test_selection_on_fixed_seeds() -> None:
    b = 8
    xs = sample(1000, b, [1.0], random.Random(1))
    assert mdl_select(xs, b)[0] == 1
    for n in (200, 1000):
        xs = sample(n, b, [0.45, 0.05, 0.1, 0.4], random.Random(1))
        assert mdl_select(xs, b)[0] == 4
