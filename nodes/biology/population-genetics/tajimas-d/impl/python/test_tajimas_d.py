# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tajimas-d/. The authors are listed in prov/GAQA42.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from biostoch import check_mean, mean_var, poisson
from tajimas_d import (
    site_statistics,
    tajima_constants,
    tajimas_d,
    tajimas_d_from_stats,
    tajimas_d_limits,
)

EXAMPLE = ["100001", "100000", "010100", "001100", "001110"]


def simulate_sample(rng, n, theta):
    """A sample of n binary sequences from the neutral infinite-sites model
    without recombination. A lineage is the bit mask of the leaves below it;
    each mutation on it is a column with those leaves set to 1."""
    lineages = [1 << i for i in range(n)]
    columns = []
    while len(lineages) > 1:
        k = len(lineages)
        t = rng.expovariate(k * (k - 1) / 2.0)
        for lin in lineages:
            columns.extend([lin] * poisson(rng, theta * t / 2.0))
        i, j = rng.sample(range(k), 2)
        merged = lineages[i] | lineages[j]
        lineages = [x for idx, x in enumerate(lineages) if idx not in (i, j)]
        lineages.append(merged)
    return ["".join("1" if (c >> r) & 1 else "0" for c in columns)
            for r in range(n)]


def brute_pi(seqs):
    pairs = list(itertools.combinations(seqs, 2))
    return sum(sum(x != y for x, y in zip(a, b)) for a, b in pairs) / len(pairs)


def test_constants():
    k = tajima_constants(5)
    assert k["a1"] == Fraction(25, 12)
    assert k["c1"] == Fraction(1, 50)
    assert float(k["e1"]) == pytest.approx(0.0096)
    assert float(k["e2"]) == pytest.approx(0.0039325, abs=1e-7)
    k = tajima_constants(10)
    assert float(k["c1"]) == pytest.approx(0.0539216, abs=1e-7)
    assert float(k["c2"]) == pytest.approx(0.0472268, abs=1e-7)
    assert float(k["e1"]) == pytest.approx(0.0190605, abs=1e-7)
    assert float(k["e2"]) == pytest.approx(0.00494893, abs=1e-8)
    with pytest.raises(ValueError):
        tajima_constants(3)


def test_denominator_is_unbiased_for_the_variance():
    # E[S] = theta a1 and E[S(S-1)] = theta^2 (a1^2 + a2), so the expected
    # square of the denominator is c1 theta + c2 theta^2, exactly.
    for n in (4, 7, 12):
        k = tajima_constants(n)
        theta = Fraction(3, 2)
        lhs = k["e1"] * theta * k["a1"] + k["e2"] * theta ** 2 * (k["a1"] ** 2 + k["a2"])
        assert lhs == k["c1"] * theta + k["c2"] * theta ** 2


def test_example():
    s, pi = site_statistics(EXAMPLE)
    assert s == 6 and pi == pytest.approx(3.0)
    assert tajimas_d(EXAMPLE) == pytest.approx(0.286384, abs=1e-6)
    assert tajimas_d_from_stats(10, 10, 3.0) == pytest.approx(-0.670667, abs=1e-6)


def test_pi_matches_pairs():
    rng = random.Random(5)
    for _ in range(30):
        n = rng.randint(2, 9)
        seqs = ["".join(rng.choice("ACG") for _ in range(12)) for _ in range(n)]
        assert site_statistics(seqs)[1] == pytest.approx(brute_pi(seqs))
    assert site_statistics(["A", "C", "G", "G"]) == (1, pytest.approx(5 / 6))


def test_sign_and_limits():
    n = 10
    singletons = ["".join("1" if j == r else "0" for j in range(n)) for r in range(n)]
    assert tajimas_d(singletons) < 0
    half = ["1" * 8 if r < 5 else "0" * 8 for r in range(n)]
    assert tajimas_d(half) > 0
    low, high = tajimas_d_limits(n)
    assert low == pytest.approx(-2.18179, abs=1e-5)
    assert high == pytest.approx(2.87241, abs=1e-5)
    assert tajimas_d_limits(5)[0] == pytest.approx(-1.27572, abs=1e-5)
    assert tajimas_d_limits(5)[1] == pytest.approx(1.91357, abs=1e-5)
    big = 10 ** 7
    assert tajimas_d_from_stats(n, big, 2.0 * big / n) == pytest.approx(low, abs=1e-4)
    assert tajimas_d_from_stats(n, big, big * n / (2.0 * (n - 1))) == pytest.approx(high, abs=1e-4)
    assert tajimas_d_from_stats(n, 0, 0.0) is None
    assert tajimas_d(["AC", "AC", "AC", "AC"]) is None


def test_moments_under_the_neutral_model():
    rng = random.Random(1989)
    n, theta, reps = 10, 5.0, 15000
    k = tajima_constants(n)
    a1 = float(k["a1"])
    var_d = float(k["c1"]) * theta + float(k["c2"]) * theta ** 2
    var_pi = float(k["b1"]) * theta + float(k["b2"]) * theta ** 2
    assert var_pi == pytest.approx(9.012346, abs=1e-6)
    ds, d2, pi2, den = [], [], [], []
    for _ in range(reps):
        seqs = simulate_sample(rng, n, theta)
        s, pi = site_statistics(seqs)
        d = pi - s / a1
        ds.append(d)
        d2.append(d * d)
        pi2.append((pi - theta) ** 2)
        den.append(float(k["e1"]) * s + float(k["e2"]) * s * (s - 1))
    m, _ = mean_var(ds)
    assert check_mean(m, 0.0, var_d, reps)
    m, v = mean_var(d2)
    assert check_mean(m, var_d, v, reps)
    m, v = mean_var(pi2)
    assert check_mean(m, var_pi, v, reps)
    m, v = mean_var(den)
    assert check_mean(m, var_d, v, reps)
