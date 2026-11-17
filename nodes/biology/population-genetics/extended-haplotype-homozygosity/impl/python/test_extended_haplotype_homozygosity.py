# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-haplotype-homozygosity/. The authors are listed in prov/DC6Q95.jsonl.

import math
import random
from fractions import Fraction
from itertools import combinations

import pytest

from extended_haplotype_homozygosity import (carriers, ehh_curve, ihh_log_ratio, integrated_ehh,
                                             standardize)

EXAMPLE = ["01101", "01101", "01100", "11101", "00010", "10001", "01011", "10000"]
HAPS = [[int(c) for c in h] for h in EXAMPLE]
POS = [0.0, 0.1, 0.2, 0.3, 0.4]


def brute_ehh(haps, core, allele, j):
    """The fraction of pairs of carriers identical at all markers between core and j."""
    group = carriers(haps, core, allele)
    lo, hi = min(core, j), max(core, j)
    pairs = list(combinations(group, 2))
    same = sum(1 for a, b in pairs if haps[a][lo:hi + 1] == haps[b][lo:hi + 1])
    return Fraction(same, len(pairs))


def random_haps(rng, n, m, p=0.5):
    return [[1 if rng.random() < p else 0 for _ in range(m)] for _ in range(n)]


def test_example_curves():
    assert ehh_curve(HAPS, 2, 1) == [Fraction(1, 2), 1, 1, 1, Fraction(1, 2)]
    assert ehh_curve(HAPS, 2, 0) == [Fraction(1, 6), Fraction(1, 2), 1, Fraction(1, 3), 0]
    d = integrated_ehh(ehh_curve(HAPS, 2, 1), POS, 2)
    a = integrated_ehh(ehh_curve(HAPS, 2, 0), POS, 2)
    assert d.value == pytest.approx(0.35) and d.reached_left and d.reached_right
    assert a.value == pytest.approx(0.175) and a.reached_left and not a.reached_right
    assert ihh_log_ratio(HAPS, POS, 2) == pytest.approx(math.log(0.5))


def test_against_brute_force():
    rng = random.Random(2002)
    for _ in range(200):
        n, m = rng.randrange(3, 12), rng.randrange(1, 9)
        haps = random_haps(rng, n, m, rng.choice([0.2, 0.5, 0.8]))
        core = rng.randrange(m)
        for allele in (0, 1):
            if len(carriers(haps, core, allele)) < 2:
                with pytest.raises(ValueError):
                    ehh_curve(haps, core, allele)
                continue
            e = ehh_curve(haps, core, allele)
            assert e == [brute_ehh(haps, core, allele, j) for j in range(m)]
            # 1 at the core, and never larger away from it.
            assert e[core] == 1
            assert all(e[j] >= e[j - 1] for j in range(1, core + 1))
            assert all(e[j] <= e[j - 1] for j in range(core + 1, m))


def test_integration_rule():
    e = [Fraction(1, 10), Fraction(1, 2), Fraction(1), Fraction(1, 2), Fraction(1, 50), Fraction(1, 50)]
    pos = [0.0, 1.0, 3.0, 4.0, 6.0, 7.0]
    r = integrated_ehh(e, pos, 2)
    # Left: (1 + 1/2)/2 * 2 + (1/2 + 1/10)/2 * 1; right: (1 + 1/2)/2 * 1, then stop at 1/50.
    assert r.value == pytest.approx(1.5 + 0.3 + 0.75)
    assert r.reached_left and not r.reached_right
    assert integrated_ehh(e, pos, 2, cutoff=0.0).value == pytest.approx(1.5 + 0.3 + 0.75 + 0.52 + 0.02)
    with pytest.raises(ValueError):
        integrated_ehh(e, [0.0, 1.0, 1.0, 2.0, 3.0, 4.0], 2)


def test_mean_under_independent_markers():
    # With independent fair markers, two carriers agree at j markers next to
    # the core with probability 2^-j, so the mean of EHH is 2^-j exactly.
    rng = random.Random(7)
    reps, n, m, core = 400, 20, 6, 0
    sums = [[] for _ in range(m)]
    for _ in range(reps):
        haps = random_haps(rng, n, m)
        for h in haps:
            h[core] = 1
        e = ehh_curve(haps, core, 1)
        for j in range(m):
            sums[j].append(float(e[j]))
    for j in range(1, m):
        xs = sums[j]
        mean = sum(xs) / reps
        sd = math.sqrt(sum((x - mean) ** 2 for x in xs) / (reps - 1))
        assert abs(mean - 2.0 ** -j) <= 4 * sd / math.sqrt(reps) + 1e-12


def sweep_sample(rng, n_derived, n_ancestral, m, core, rate):
    """Derived carriers copy one founder haplotype; each copy keeps it on each
    side up to a break after an exponential number of markers, and has random
    alleles beyond. Ancestral carriers have random alleles."""
    founder = [rng.randrange(2) for _ in range(m)]
    haps = []
    for _ in range(n_derived):
        h = [rng.randrange(2) for _ in range(m)]
        left = core - int(rng.expovariate(rate))
        right = core + int(rng.expovariate(rate))
        for j in range(max(0, left), min(m, right + 1)):
            h[j] = founder[j]
        h[core] = 1
        haps.append(h)
    for _ in range(n_ancestral):
        h = [rng.randrange(2) for _ in range(m)]
        h[core] = 0
        haps.append(h)
    return haps


def test_sweep_gives_negative_scores():
    rng = random.Random(42)
    m, core = 41, 20
    pos = [0.01 * j for j in range(m)]
    scores = [ihh_log_ratio(sweep_sample(rng, 15, 15, m, core, 0.1), pos, core) for _ in range(40)]
    assert sum(1 for s in scores if s < 0) >= 36
    assert sum(scores) / len(scores) < -1.0


def test_standardize():
    rng = random.Random(5)
    freqs = [rng.random() for _ in range(400)]
    scores = [rng.gauss(3 * f, 1 + f) for f in freqs]
    z = standardize(scores, freqs, n_bins=4)
    for b in range(4):
        zs = [z[i] for i in range(400) if min(int(freqs[i] * 4), 3) == b]
        mean = sum(zs) / len(zs)
        var = sum((x - mean) ** 2 for x in zs) / (len(zs) - 1)
        assert abs(mean) < 1e-9 and abs(var - 1) < 1e-9
    lone = standardize([1.0, 2.0, 5.0], [0.1, 0.12, 0.9], n_bins=2)
    assert math.isnan(lone[2]) and lone[0] == pytest.approx(-math.sqrt(0.5))
