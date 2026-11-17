# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/watterson-estimator/. The authors are listed in prov/BFZ8DK.jsonl.

import random
from fractions import Fraction

import pytest

from biostoch import check_mean, mean_var, poisson
from watterson_estimator import (
    harmonic,
    harmonic2,
    segregating_sites,
    theta_squared_from_count,
    watterson_from_count,
    watterson_theta,
    watterson_variance,
    watterson_variance_estimate,
)

EXAMPLE = ["100001", "100000", "010100", "001100", "001110"]


def sample_segregating_sites(rng, n, theta):
    """S under the neutral infinite-sites model: a Kingman total branch
    length L, then S ~ Poisson(theta L / 2)."""
    total = 0.0
    for k in range(n, 1, -1):
        total += k * rng.expovariate(k * (k - 1) / 2.0)
    return poisson(rng, theta * total / 2.0)


def test_harmonic_numbers():
    assert harmonic(2) == 1
    assert harmonic(5) == Fraction(25, 12)
    assert abs(float(harmonic(10)) - 2.828968) < 1e-6
    assert abs(float(harmonic2(10)) - 1.539768) < 1e-6
    with pytest.raises(ValueError):
        harmonic(1)


def test_example_matrix():
    assert segregating_sites(EXAMPLE) == 6
    assert watterson_from_count(6, 5) == Fraction(72, 25)
    assert watterson_theta(EXAMPLE) == pytest.approx(2.88)
    assert watterson_theta(EXAMPLE, per_site=True) == pytest.approx(0.48)


def test_dna_and_missing_data():
    seqs = ["ACGTAC", "ACGTTC", "ACNTAG", "AC-TAC"]
    # Site 3 has only G and missing values; sites 5 and 6 segregate.
    assert segregating_sites(seqs) == 2
    # A site with three alleles counts once.
    assert segregating_sites(["A", "C", "G"]) == 1
    # Invariant sites do not change S.
    assert segregating_sites([s + "GGG" for s in EXAMPLE]) == 6


def test_order_does_not_matter():
    rng = random.Random(7)
    rows = ["".join(rng.choice("ACGT") for _ in range(30)) for _ in range(8)]
    s = segregating_sites(rows)
    perm = list(range(30))
    rng.shuffle(perm)
    cols = ["".join(r[j] for j in perm) for r in rows]
    assert segregating_sites(list(reversed(rows))) == s
    assert segregating_sites(cols) == s


def test_bad_input():
    with pytest.raises(ValueError):
        segregating_sites(["ACG"])
    with pytest.raises(ValueError):
        segregating_sites(["ACG", "AC"])
    with pytest.raises(ValueError):
        watterson_from_count(-1, 4)


def test_unbiased_under_the_neutral_model():
    rng = random.Random(2024)
    n, theta, reps = 10, 5.0, 20000
    counts = [sample_segregating_sites(rng, n, theta) for _ in range(reps)]
    estimates = [float(watterson_from_count(s, n)) for s in counts]
    m, _ = mean_var(estimates)
    var = watterson_variance(theta, n)
    assert abs(var - 6.577362) < 1e-5
    assert check_mean(m, theta, var, reps)
    # The sample variance of theta_W against Watterson's formula.
    sq = [(x - theta) ** 2 for x in estimates]
    m2, v2 = mean_var(sq)
    assert check_mean(m2, var, v2, reps)
    # S (S - 1) / (a_n^2 + b_n) is unbiased for theta^2.
    t2 = [float(theta_squared_from_count(s, n)) for s in counts]
    m3, v3 = mean_var(t2)
    assert check_mean(m3, theta * theta, v3, reps)
    # The estimate of the variance is unbiased for it.
    ve = [watterson_variance_estimate(s, n) for s in counts]
    m4, v4 = mean_var(ve)
    assert check_mean(m4, var, v4, reps)


def test_two_sequences():
    rng = random.Random(11)
    theta, reps = 1.5, 20000
    xs = [float(watterson_from_count(sample_segregating_sites(rng, 2, theta), 2))
          for _ in range(reps)]
    m, _ = mean_var(xs)
    assert check_mean(m, theta, theta + theta * theta, reps)
