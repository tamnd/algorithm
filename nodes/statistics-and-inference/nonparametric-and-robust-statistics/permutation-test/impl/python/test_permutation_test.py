# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/permutation-test/. The authors are listed in prov/KSN49K.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from permutation_test import mean_difference, permutation_test, sign_flip_test

# Darwin's Zea mays data from Fisher, The Design of Experiments, Section 21:
# crossed minus self-fertilized height in each of 15 pairs, in eighths of an inch.
DARWIN = [49, -67, 8, 16, 6, 23, 28, 41, 14, 29, 56, 24, 75, 60, -48]

# Survival times in days of 16 mice, Efron and Tibshirani (1993), Table 2.1.
TREATMENT = [94, 197, 16, 38, 99, 141, 23]
CONTROL = [52, 104, 146, 10, 51, 30, 40, 27, 46]


def all_permutations_p(x, y, alternative):
    """Brute force: the fraction of all N! orderings whose statistic is at least as extreme."""
    z, m = list(x) + list(y), len(x)
    t_obs = mean_difference(z[:m], z[m:])
    hits = total = 0
    for w in itertools.permutations(z):
        t = mean_difference(w[:m], w[m:])
        if alternative == "greater":
            hits += t >= t_obs
        elif alternative == "less":
            hits += t <= t_obs
        else:
            hits += abs(t) >= abs(t_obs)
        total += 1
    return Fraction(hits, total)


@pytest.mark.parametrize("alternative", ["greater", "less", "two-sided"])
def test_exact_matches_all_permutations(alternative):
    rng = random.Random(3)
    for n_total in range(2, 8):
        for m in range(1, n_total):
            z = [Fraction(rng.randint(-6, 6), rng.randint(1, 3)) for _ in range(n_total)]
            got = permutation_test(z[:m], z[m:], alternative=alternative)
            assert got == all_permutations_p(z[:m], z[m:], alternative)


def test_darwin_sign_flip():
    assert sum(DARWIN) == 314
    assert sign_flip_test(DARWIN) == Fraction(1726, 32768)
    assert sign_flip_test(DARWIN, alternative="greater") == Fraction(863, 32768)


def test_sign_flip_brute_force():
    rng = random.Random(5)
    for n in range(1, 9):
        d = [rng.randint(-5, 5) for _ in range(n)]
        hits = sum(abs(sum(s * v for s, v in zip(signs, d))) >= abs(sum(d))
                   for signs in itertools.product((1, -1), repeat=n))
        assert sign_flip_test(d) == Fraction(hits, 2**n)


def test_mouse_data_exact():
    assert mean_difference(TREATMENT, CONTROL) == Fraction(1930, 63)
    assert permutation_test(TREATMENT, CONTROL) == Fraction(1613, 11440)
    assert permutation_test(TREATMENT, CONTROL, alternative="two-sided") == Fraction(3184, 11440)


def test_monte_carlo_formula():
    b = 1000
    got = permutation_test(TREATMENT, CONTROL, b=b, rng=random.Random(1))
    rng = random.Random(1)
    z, m = TREATMENT + CONTROL, len(TREATMENT)
    t_obs = mean_difference(TREATMENT, CONTROL)
    count = 0
    for _ in range(b):
        w = z[:]
        rng.shuffle(w)
        count += mean_difference(w[:m], w[m:]) >= t_obs
    assert got == Fraction(1 + count, 1 + b)
    assert got == Fraction(134, 1001)
    assert got > 0


def test_exact_level_by_enumeration():
    """Under H0 every split is equally likely; P(p <= alpha) <= alpha for every alpha."""
    z = [Fraction(v) for v in (3, 8, 1, 9, 4, 12, 7, 5)]
    m = 4
    splits = list(itertools.combinations(range(8), m))
    pvals = []
    for chosen in splits:
        x = [z[i] for i in chosen]
        y = [z[i] for i in range(8) if i not in chosen]
        pvals.append(permutation_test(x, y))
    k = len(splits)
    assert k == math.comb(8, 4)
    for alpha in (Fraction(1, 70), Fraction(1, 20), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2)):
        size = Fraction(sum(p <= alpha for p in pvals), k)
        assert size <= alpha
    # Distinct sums except for ties: the size at an attainable level is exact.
    assert Fraction(sum(p <= Fraction(1, 70) for p in pvals), k) == Fraction(1, 70)


def test_monte_carlo_size():
    rng = random.Random(11)
    r, b, alpha = 3000, 19, 0.05
    rejections = 0
    for _ in range(r):
        z = [rng.gauss(0.0, 1.0) for _ in range(10)]
        p = permutation_test(z[:5], z[5:], b=b, rng=rng)
        rejections += p <= alpha
    rate = rejections / r
    assert rate <= alpha + 4 * math.sqrt(alpha * (1 - alpha) / r)
    assert rate >= alpha - 4 * math.sqrt(alpha * (1 - alpha) / r) - 1 / math.comb(10, 5)


def test_float_tolerance_keeps_observed_split():
    x, y = [0.1, 0.2, 0.3], [0.7, 0.05, 0.4]
    p = permutation_test(x, y, alternative="two-sided")
    assert p >= Fraction(1, math.comb(6, 3))


def test_errors():
    with pytest.raises(ValueError):
        permutation_test([1], [2], alternative="bigger")
    with pytest.raises(ValueError):
        permutation_test([], [1, 2])
    with pytest.raises(ValueError):
        permutation_test([1], [2], b=10)
