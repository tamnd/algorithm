# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/em-haplotype-frequency-estimation/. The authors are listed in prov/5PQV9Z.jsonl.

import math
import random
from itertools import product

import pytest

from em_haplotype_frequency_estimation import (compatible_pairs, em_haplotype_frequencies, gene_count,
                                               log_likelihood, two_site_ld)

EXAMPLE = {(0, 0): 2, (0, 1): 1, (1, 0): 1, (1, 1): 3, (1, 2): 1, (2, 2): 2}


def example_genotypes():
    return [g for g, c in EXAMPLE.items() for _ in range(c)]


def brute_pairs(g):
    """All unordered pairs of haplotypes whose sum is g, by enumeration of all haplotypes."""
    m = len(g)
    haps = list(product((0, 1), repeat=m))
    out = set()
    for h in haps:
        for k in haps:
            if tuple(a + b for a, b in zip(h, k)) == tuple(g):
                out.add(tuple(sorted((h, k))))
    return out


def test_compatible_pairs_against_enumeration():
    for m in range(1, 5):
        for g in product((0, 1, 2), repeat=m):
            pairs = compatible_pairs(g)
            got = {tuple(sorted(pq)) for pq in pairs}
            assert len(got) == len(pairs)
            assert got == brute_pairs(g)
            het = sum(1 for x in g if x == 1)
            assert len(pairs) == (2 ** (het - 1) if het else 1)


def test_example_first_step_by_hand():
    p, trace = em_haplotype_frequencies(example_genotypes(), max_iter=1)
    assert p[(0, 0)] == pytest.approx(7.5 / 20)
    assert p[(0, 1)] == pytest.approx(3.5 / 20)
    assert p[(1, 0)] == pytest.approx(2.5 / 20)
    assert p[(1, 1)] == pytest.approx(6.5 / 20)


def test_example_converged_values():
    p, trace = em_haplotype_frequencies(example_genotypes(), tol=1e-15)
    assert p[(0, 0)] == pytest.approx(0.445269, abs=1e-6)
    assert p[(0, 1)] == pytest.approx(0.104731, abs=1e-6)
    assert p[(1, 0)] == pytest.approx(0.054731, abs=1e-6)
    assert p[(1, 1)] == pytest.approx(0.395269, abs=1e-6)
    assert trace[-1] == pytest.approx(-17.870215, abs=1e-6)
    d, dprime, r2 = two_site_ld(p)
    assert d == pytest.approx(0.170269, abs=1e-6)
    assert r2 == pytest.approx(0.468549, abs=1e-6)


def test_likelihood_never_decreases():
    rng = random.Random(7)
    for _ in range(20):
        m = rng.randint(2, 4)
        genos = [tuple(rng.randint(0, 2) for _ in range(m)) for _ in range(rng.randint(3, 15))]
        p, trace = em_haplotype_frequencies(genos, max_iter=60, tol=-1.0)
        for a, b in zip(trace, trace[1:]):
            assert b >= a - 1e-12


def two_site_grid_mle(genos, steps):
    """Maximize the two-site likelihood over p_11 on a grid, with the allele
    frequencies fixed at their sample values (every EM iterate has them)."""
    n = len(genos)
    pa = sum(g[0] for g in genos) / (2 * n)
    pb = sum(g[1] for g in genos) / (2 * n)
    lo = max(0.0, pa + pb - 1.0)
    hi = min(pa, pb)
    best = (-math.inf, None)
    for t in range(steps + 1):
        x = lo + (hi - lo) * t / steps
        p = {(1, 1): x, (1, 0): pa - x, (0, 1): pb - x, (0, 0): 1 - pa - pb + x}
        ll = log_likelihood(genos, p)
        if ll > best[0]:
            best = (ll, x)
    return best


def test_two_sites_against_grid():
    rng = random.Random(11)
    for case in range(15):
        genos = [tuple(rng.randint(0, 2) for _ in range(2)) for _ in range(rng.randint(5, 30))]
        if case == 0:
            genos = example_genotypes()
        p, trace = em_haplotype_frequencies(genos, max_iter=5000, tol=1e-13)
        ll_grid, x = two_site_grid_mle(genos, 4000)
        assert trace[-1] >= ll_grid - 1e-6


def test_kkt_conditions_three_sites():
    """At an interior fixed point the gradient of the log-likelihood is 2n for
    every haplotype with positive frequency, and at most 2n for the others."""
    rng = random.Random(5)
    haps = list(product((0, 1), repeat=3))
    freqs = [0.4, 0.05, 0.1, 0.05, 0.05, 0.15, 0.05, 0.15]
    genos = []
    for _ in range(80):
        h = rng.choices(haps, freqs)[0]
        k = rng.choices(haps, freqs)[0]
        genos.append(tuple(a + b for a, b in zip(h, k)))
    p, trace = em_haplotype_frequencies(genos, max_iter=20000, tol=1e-15)
    n = len(genos)
    grad = {h: 0.0 for h in p}
    for g in genos:
        pairs = compatible_pairs(g)
        tot = sum((1 if h == k else 2) * p[h] * p[k] for h, k in pairs)
        for h, k in pairs:
            if h == k:
                grad[h] += 2 * p[h] / tot
            else:
                grad[h] += 2 * p[k] / tot
                grad[k] += 2 * p[h] / tot
    for h, v in p.items():
        if v > 1e-6:
            assert grad[h] == pytest.approx(2 * n, rel=1e-4)
        else:
            assert grad[h] <= 2 * n * (1 + 1e-3)


def test_phase_known_equals_gene_counting():
    """When no genotype has two or more heterozygous sites, the phase is known,
    and the maximum likelihood estimate is the direct haplotype count."""
    rng = random.Random(3)
    haps = list(product((0, 1), repeat=3))
    pairs = []
    while len(pairs) < 40:
        h, k = rng.choice(haps), rng.choice(haps)
        if sum(1 for a, b in zip(h, k) if a != b) <= 1:
            pairs.append((h, k))
    genos = [tuple(a + b for a, b in zip(h, k)) for h, k in pairs]
    p, trace = em_haplotype_frequencies(genos, max_iter=5)
    want = gene_count(pairs)
    for h in set(p) | set(want):
        assert p.get(h, 0.0) == pytest.approx(want.get(h, 0.0), abs=1e-12)


def test_frequencies_sum_to_one_and_reject_bad_input():
    p, _ = em_haplotype_frequencies(example_genotypes())
    assert sum(p.values()) == pytest.approx(1.0, abs=1e-12)
    with pytest.raises(ValueError):
        compatible_pairs((0, 3))
    with pytest.raises(ValueError):
        em_haplotype_frequencies([])
