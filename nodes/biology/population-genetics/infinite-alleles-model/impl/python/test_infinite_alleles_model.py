# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/infinite-alleles-model/. The authors are listed in prov/AWDSAS.jsonl.

import random
from fractions import Fraction

from biostoch import check_mean, chi2_sf, mean_var
from infinite_alleles_model import (
    allele_counts,
    allele_profile,
    ewens_probability,
    expected_alleles,
    homozygosity,
    homozygosity_after,
    homozygosity_equilibrium,
    homozygosity_step,
    hoppe_urn,
    partitions,
    simulate,
)


def test_equilibrium_is_fixed_point():
    for two_n, u in ((20, Fraction(1, 20)), (100, Fraction(1, 1000)), (7, Fraction(1, 3))):
        F = homozygosity_equilibrium(two_n, u)
        assert homozygosity_step(F, two_n, u) == F
    # N = 50, u = 0.001, theta = 0.2: F* = 0.833125 against 1 / (1 + theta) = 0.833333.
    F = homozygosity_equilibrium(100, Fraction(1, 1000))
    assert abs(float(F) - 0.833125) < 5e-7
    assert abs(float(F) - 1 / 1.2) < 3e-4


def test_recursion_converges():
    two_n, u = 20, Fraction(1, 20)
    F = homozygosity_after(two_n, u, 200)
    assert abs(float(F - homozygosity_equilibrium(two_n, u))) < 1e-12
    # Without mutation the homozygosity only rises: 1 - F_t = (1 - 1/(2N))^t (1 - F_0).
    assert homozygosity_after(10, 0, 3, Fraction(0)) == 1 - Fraction(9, 10) ** 3


def test_simulated_homozygosity_matches_recursion():
    rng = random.Random(1964)
    two_n, u, gens, reps = 20, 0.05, 60, 10000
    values = [homozygosity(simulate(rng, two_n, u, gens)) for _ in range(reps)]
    m, v = mean_var(values)
    mu = float(homozygosity_after(two_n, Fraction(1, 20), gens))
    assert check_mean(m, mu, v, reps)
    assert abs(mu - float(homozygosity_equilibrium(two_n, Fraction(1, 20)))) < 1e-4


def test_no_mutation_keeps_labels():
    rng = random.Random(3)
    pop = simulate(rng, 12, 0.0, 30, start=list(range(12)))
    assert set(pop) <= set(range(12))
    assert sum(allele_counts(pop)) == 12


def test_ewens_formula_values():
    # n = 3, theta = 2: (3,0,0), (1,1,0), (0,0,1) have 1/3, 1/2, 1/6.
    assert ewens_probability((3, 0, 0), 2) == Fraction(1, 3)
    assert ewens_probability((1, 1, 0), 2) == Fraction(1, 2)
    assert ewens_probability((0, 0, 1), 2) == Fraction(1, 6)
    # theta = 1 gives the cycle types of a uniform random permutation.
    assert ewens_probability((0, 2, 0, 0), 1) == Fraction(1, 8)
    for n, theta in ((6, Fraction(3, 2)), (8, 1), (5, Fraction(1, 7))):
        total = sum(ewens_probability(allele_profile(p, n), theta) for p in partitions(n))
        assert total == 1


def test_hoppe_urn_matches_ewens():
    rng = random.Random(1972)
    n, theta, reps = 4, 1.0, 100000
    counts = {}
    for _ in range(reps):
        a = allele_profile(allele_counts(hoppe_urn(rng, n, theta)), n)
        counts[a] = counts.get(a, 0) + 1
    stat = 0.0
    parts = list(partitions(n))
    for p in parts:
        a = allele_profile(p, n)
        e = reps * float(ewens_probability(a, 1))
        stat += (counts.get(a, 0) - e) ** 2 / e
    assert sum(counts.values()) == reps and len(counts) <= len(parts)
    assert chi2_sf(stat, len(parts) - 1) > 0.001


def test_expected_number_of_alleles():
    assert expected_alleles(3, 1) == Fraction(11, 6)
    assert abs(float(expected_alleles(10, 2)) - 4.03975) < 5e-6
    rng = random.Random(5)
    n, theta, reps = 10, 2.0, 40000
    ks = [len(set(hoppe_urn(rng, n, theta))) for _ in range(reps)]
    m, _ = mean_var(ks)
    var = sum(theta * i / (theta + i) ** 2 for i in range(n))
    assert check_mean(m, float(expected_alleles(n, 2)), var, reps)


def test_invalid():
    for bad in ((0, 0.1, 1), (10, 1.5, 1), (10, 0.1, -1)):
        try:
            simulate(random.Random(0), *bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    try:
        hoppe_urn(random.Random(0), 5, 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
