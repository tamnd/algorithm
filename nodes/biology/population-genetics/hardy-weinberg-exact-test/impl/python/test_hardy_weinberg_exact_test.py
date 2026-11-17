# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hardy-weinberg-exact-test/. The authors are listed in prov/M4SDHR.jsonl.

import math
import random
from fractions import Fraction

import pytest

from hardy_weinberg_exact_test import (
    brute_force_distribution,
    chi_square_test,
    direct_probability,
    het_distribution,
    hwe_exact_test,
    simulate_null_counts,
)


def counts_with(n, n_A, h):
    """Genotype counts (n_AA, n_Aa, n_aa) with n_A copies of A and h heterozygotes."""
    return (n_A - h) // 2, h, (2 * n - n_A - h) // 2


def test_check_values_small_sample():
    # 10 individuals, 6 copies of the minor allele, 2 heterozygotes.
    dist = het_distribution(2, 2, 6, exact=True)
    assert dist == {0: Fraction(1, 323), 2: Fraction(42, 323), 4: Fraction(168, 323), 6: Fraction(112, 323)}
    assert hwe_exact_test(2, 2, 6, exact=True) == Fraction(43, 323)
    assert abs(hwe_exact_test(2, 2, 6) - 43 / 323) < 1e-12


def test_check_values_30_40_30():
    p = hwe_exact_test(30, 40, 30)
    assert abs(p - 0.04686) < 5e-6
    assert abs(p - float(hwe_exact_test(30, 40, 30, exact=True))) < 1e-12
    stat, p_chi = chi_square_test(30, 40, 30)
    assert abs(stat - 4.0) < 1e-12
    assert abs(p_chi - 0.0455003) < 1e-6


def test_recurrence_matches_closed_form():
    for n in range(1, 21):
        for n_A in range(0, 2 * n + 1):
            m = min(n_A, 2 * n - n_A)
            dist = het_distribution(*counts_with(n, n_A, m), exact=True)
            assert sum(dist.values()) == 1
            for h in range(0, m + 1):
                assert dist.get(h, Fraction(0)) == direct_probability(n, n_A, h)


def test_closed_form_matches_random_pairing():
    for n in range(1, 7):
        for n_A in range(0, 2 * n + 1):
            brute = brute_force_distribution(n, n_A)
            m = min(n_A, 2 * n - n_A)
            dist = het_distribution(*counts_with(n, n_A, m), exact=True)
            assert dist == brute


def test_float_matches_exact():
    rng = random.Random(2005)
    for _ in range(50):
        n = rng.randint(1, 200)
        n_A = rng.randint(0, 2 * n)
        m = min(n_A, 2 * n - n_A)
        h = rng.randrange(m % 2, m + 1, 2)
        g = counts_with(n, n_A, h)
        for alt in ("two-sided", "deficit", "excess"):
            pf = hwe_exact_test(*g, alternative=alt)
            pe = hwe_exact_test(*g, exact=True, alternative=alt)
            assert abs(pf - float(pe)) <= 1e-9


def test_p_value_is_valid_in_exact_arithmetic():
    # Under the null, P(p-value <= alpha) <= alpha for every alpha.
    n = 12
    alphas = [Fraction(k, 100) for k in range(1, 100)]
    for n_A in range(0, 2 * n + 1):
        m = min(n_A, 2 * n - n_A)
        law = het_distribution(*counts_with(n, n_A, m), exact=True)
        pv = {h: hwe_exact_test(*counts_with(n, n_A, h), exact=True) for h in law}
        for alpha in alphas:
            assert sum(law[h] for h in law if pv[h] <= alpha) <= alpha


def test_symmetry_and_one_sided_identity():
    rng = random.Random(7)
    for _ in range(30):
        n = rng.randint(1, 40)
        n_A = rng.randint(0, 2 * n)
        m = min(n_A, 2 * n - n_A)
        h = rng.randrange(m % 2, m + 1, 2)
        a, b, c = counts_with(n, n_A, h)
        assert hwe_exact_test(a, b, c, exact=True) == hwe_exact_test(c, b, a, exact=True)
        lo = hwe_exact_test(a, b, c, exact=True, alternative="deficit")
        hi = hwe_exact_test(a, b, c, exact=True, alternative="excess")
        assert lo + hi - het_distribution(a, b, c, exact=True)[b] == 1


def test_edge_cases():
    assert hwe_exact_test(5, 0, 0) == 1.0
    assert hwe_exact_test(0, 0, 7, exact=True) == 1
    assert hwe_exact_test(0, 1, 0, exact=True) == 1
    assert het_distribution(0, 1, 0, exact=True) == {1: 1}
    # A tie: h = 2 and h = 4 both have probability 16/33 when n = 6 and n_A = 4.
    assert het_distribution(1, 2, 3, exact=True) == {0: Fraction(1, 33), 2: Fraction(16, 33), 4: Fraction(16, 33)}
    assert hwe_exact_test(1, 2, 3, exact=True) == 1
    assert abs(hwe_exact_test(1, 2, 3) - 1.0) < 1e-12
    assert abs(hwe_exact_test(0, 4, 2) - 1.0) < 1e-12
    # All heterozygotes is the most extreme excess.
    assert hwe_exact_test(0, 10, 0, exact=True, alternative="excess") == direct_probability(10, 10, 10)


def test_invalid_input():
    with pytest.raises(ValueError):
        hwe_exact_test(0, 0, 0)
    with pytest.raises(ValueError):
        hwe_exact_test(-1, 2, 3)
    with pytest.raises(ValueError):
        hwe_exact_test(1, 2, 3, alternative="less")


def test_null_simulation():
    rng = random.Random(1949)
    n, n_A, reps, alpha = 50, 40, 2000, 0.05
    law = het_distribution(*counts_with(n, n_A, 0), exact=False)
    mu = sum(h * p for h, p in law.items())
    var = sum((h - mu) ** 2 * p for h, p in law.items())
    # Levene's mean of the heterozygote count.
    assert abs(mu - n_A * (2 * n - n_A) / (2 * n - 1)) < 1e-9
    total_h = 0
    rejections = 0
    for _ in range(reps):
        a, b, c = simulate_null_counts(rng, n, n_A)
        total_h += b
        rejections += hwe_exact_test(a, b, c) <= alpha
    z = 4
    assert abs(total_h / reps - mu) <= z * math.sqrt(var / reps)
    assert rejections / reps <= alpha + z * math.sqrt(alpha * (1 - alpha) / reps)
