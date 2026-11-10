# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probability-proportional-to-size-sampling/. The authors are listed in prov/G2PZNC.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from pps_sampling import (
    hansen_hurwitz,
    horvitz_thompson,
    ht_variance,
    inclusion_probabilities,
    integer_form,
    poisson_sample,
    pps_with_replacement,
    systematic_from_start,
    systematic_pps,
    systematic_pps_float,
)

# The example of the page.
X = [2, 3, 5, 4, 6]
Y = [5, 6, 11, 9, 12]
TOTAL = 43
N_SAMPLE = 2


def law_systematic(a, d, n):
    """All D starts are equally likely: the exact law of the sample."""
    law = {}
    for t in range(d):
        s = tuple(systematic_from_start(a, d, n, t))
        law[s] = law.get(s, F(0)) + F(1, d)
    return law


def test_example() -> None:
    pi = inclusion_probabilities(X, N_SAMPLE)
    assert pi == [F(1, 5), F(3, 10), F(1, 2), F(2, 5), F(3, 5)]
    a, d, n = integer_form(pi)
    assert (a, d, n) == ([2, 3, 5, 4, 6], 10, 2)
    samples = [systematic_from_start(a, d, n, t) for t in range(d)]
    assert samples[3] == [1, 3]
    assert horvitz_thompson([1, 3], Y, pi) == F(85, 2)  # 20 + 22.5
    ests = [horvitz_thompson(s, Y, pi) for s in samples]
    assert [float(e) for e in ests] == [47.5, 47.5, 42.5, 42.5, 40.0, 42.0, 42.0, 42.0, 42.0, 42.0]
    mean = sum(ests) / d
    assert mean == TOTAL
    assert sum((e - mean) ** 2 for e in ests) / d == F(11, 2)


def test_systematic_inclusion_exact() -> None:
    rng = random.Random(1952)
    for _ in range(300):
        size = rng.randint(1, 7)
        n = rng.randint(1, size)
        x = [rng.randint(1, 12) for _ in range(size)]
        pi = inclusion_probabilities(x, n)
        assert sum(pi) == n and all(0 < p <= 1 for p in pi)
        a, d, nn = integer_form(pi)
        assert nn == n
        law = law_systematic(a, d, n)
        for s in law:
            assert len(s) == n and len(set(s)) == n
        for i in range(size):
            assert sum(pr for s, pr in law.items() if i in s) == pi[i]
        # Horvitz-Thompson is unbiased.
        y = [rng.randint(-5, 20) for _ in range(size)]
        assert sum(pr * horvitz_thompson(s, y, pi) for s, pr in law.items()) == sum(y)


def test_ht_variance_formula() -> None:
    pi = inclusion_probabilities(X, N_SAMPLE)
    a, d, n = integer_form(pi)
    law = law_systematic(a, d, n)
    pij = {}
    for s, pr in law.items():
        for i, j in itertools.combinations(sorted(s), 2):
            pij[(i, j)] = pij.get((i, j), F(0)) + pr
    assert ht_variance(Y, pi, pij) == F(11, 2)
    # Units 1 and 2 (0-based 0 and 1) are never together: no unbiased variance estimate.
    assert (0, 1) not in pij


def test_zero_variance_when_proportional() -> None:
    y = [7 * v for v in X]
    pi = inclusion_probabilities(X, N_SAMPLE)
    a, d, n = integer_form(pi)
    assert {horvitz_thompson(s, y, pi) for s in law_systematic(a, d, n)} == {sum(y)}
    assert {hansen_hurwitz([i, j], X, y) for i in range(5) for j in range(5)} == {sum(y)}


def test_hansen_hurwitz_exact() -> None:
    big_x = sum(X)
    p = [F(v, big_x) for v in X]
    for m in [1, 2, 3]:
        mean = var2 = F(0)
        for draws in itertools.product(range(5), repeat=m):
            pr = F(1)
            for i in draws:
                pr *= p[i]
            e = hansen_hurwitz(draws, X, Y)
            mean += pr * e
            var2 += pr * e * e
        assert mean == TOTAL
        one = sum(p[i] * (F(Y[i]) / p[i] - TOTAL) ** 2 for i in range(5))
        assert one == 10
        assert var2 - mean * mean == one / m


def test_simple_random_sample_is_worse() -> None:
    ests = [F(5, 2) * (Y[i] + Y[j]) for i, j in itertools.combinations(range(5), 2)]
    mean = sum(ests) / 10
    assert mean == TOTAL
    assert sum((e - mean) ** 2 for e in ests) / 10 == F(279, 4)  # 69.75 against 5.5


def test_poisson_sampling_exact() -> None:
    pi = inclusion_probabilities(X, N_SAMPLE)
    mean = F(0)
    for bits in itertools.product([0, 1], repeat=5):
        pr = F(1)
        for b, p in zip(bits, pi):
            pr *= p if b else 1 - p
        s = [i for i in range(5) if bits[i]]
        mean += pr * horvitz_thompson(s, Y, pi)
    assert mean == TOTAL


def test_take_all_units() -> None:
    pi = inclusion_probabilities([1, 1, 1, 10], 2)
    assert pi == [F(1, 3), F(1, 3), F(1, 3), F(1)]
    a, d, n = integer_form(pi)
    law = law_systematic(a, d, n)
    assert all(3 in s for s in law)


def test_wrong_variant_successive_sampling() -> None:
    # Draw n units one by one without replacement, each with probability proportional to size
    # among those left. The inclusion probabilities are not n x_i / X, so HT with those is biased.
    big_x = sum(X)
    pi_claimed = inclusion_probabilities(X, N_SAMPLE)
    pi_true = [F(0)] * 5
    mean = F(0)
    for i, j in itertools.permutations(range(5), 2):
        pr = F(X[i], big_x) * F(X[j], big_x - X[i])
        pi_true[i] += pr
        pi_true[j] += pr
        mean += pr * horvitz_thompson([i, j], Y, pi_claimed)
    assert pi_true != pi_claimed
    assert mean != TOTAL
    # With the true inclusion probabilities, HT is unbiased again.
    fixed = F(0)
    for i, j in itertools.permutations(range(5), 2):
        pr = F(X[i], big_x) * F(X[j], big_x - X[i])
        fixed += pr * horvitz_thompson([i, j], Y, pi_true)
    assert fixed == TOTAL


def test_random_runs() -> None:
    rng = random.Random(1943)
    pi = inclusion_probabilities(X, N_SAMPLE)
    a, d, n = integer_form(pi)
    counts = [0] * 5
    reps = 20000
    for _ in range(reps):
        for i in systematic_pps(a, d, n, rng):
            counts[i] += 1
    for c, p in zip(counts, pi):
        sd = (reps * p * (1 - p)) ** 0.5
        assert abs(c - reps * p) < 6 * sd
    counts = [0] * 5
    for _ in range(reps):
        s = systematic_pps_float([float(p) for p in pi], rng)
        assert len(s) == 2
        for i in s:
            counts[i] += 1
    for c, p in zip(counts, pi):
        assert abs(c - reps * p) < 6 * (reps * p * (1 - p)) ** 0.5
    est = sum(pps_with_replacement(X, Y, 2, rng) for _ in range(4000)) / 4000
    assert abs(float(est) - TOTAL) < 6 * (5.0 / 4000) ** 0.5
    sizes = [len(poisson_sample([float(p) for p in pi], rng)) for _ in range(4000)]
    assert 1.9 < sum(sizes) / 4000 < 2.1


def test_errors() -> None:
    with pytest.raises(ValueError):
        inclusion_probabilities([1, 2], 3)
    with pytest.raises(ValueError):
        systematic_pps([11, 9], 10, 2, random.Random(0))
