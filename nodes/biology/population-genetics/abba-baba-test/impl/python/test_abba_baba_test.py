# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/abba-baba-test/. The authors are listed in prov/7E0M5A.jsonl.

import math
import random

import pytest

from abba_baba_test import (abba_baba, block_jackknife, block_sums, count_patterns, d_from_counts, polarize,
                            site_terms)


def simulate_sites(rng, n_sites, t_internal, gamma, t_intro):
    """Site patterns of four single sequences from a three-taxon gene tree model.

    Species tree ((P1, P2), P3) with an internal branch of t_internal coalescent
    units. With probability gamma a site's P2 lineage comes from P3 (introgression),
    where it can join the P3 lineage during t_intro units before the root. A lineage
    pair that does not join in time ends up in a random one of the three pairings
    (incomplete lineage sorting). One derived mutation falls on the internal branch
    of the gene tree with probability 0.3, else on a tip, so sites are ABBA, BABA,
    BBAA or a singleton pattern.
    """
    seqs = ([], [], [], [])
    for _ in range(n_sites):
        if rng.random() < gamma:
            pair = (2, 3) if rng.random() < 1 - math.exp(-t_intro) else rng.choice([(1, 2), (1, 3), (2, 3)])
        else:
            pair = (1, 2) if rng.random() < 1 - math.exp(-t_internal) else rng.choice([(1, 2), (1, 3), (2, 3)])
        derived = set(pair) if rng.random() < 0.3 else {rng.choice([1, 2, 3])}
        for idx in range(3):
            seqs[idx].append("T" if idx + 1 in derived else "C")
        seqs[3].append("C")
    return seqs


def brute_counts(p1, p2, p3, out):
    pats = ["".join("A" if x == a else "B" for x in (y1, y2, y3, a)) for y1, y2, y3, a in zip(p1, p2, p3, out)]
    return pats.count("ABBA"), pats.count("BABA")


def test_counts_by_hand():
    p1 = "AACGTA"
    p2 = "GACGTT"
    p3 = "GTCATT"
    o = "AAGATA"
    # site 0: A G G | A -> ABBA ; site 1: A A T | A -> AAB.. no ; site 2: C C C | G -> BBBA no
    # site 3: G G A | A -> BBAA no ; site 4: T T T | T -> no ; site 5: A T T | A -> ABBA
    assert count_patterns(p1, p2, p3, o) == (2, 0)
    assert count_patterns(p2, p1, p3, o) == (0, 2)


def test_counts_against_brute_force():
    rng = random.Random(1)
    for _ in range(20):
        seqs = ["".join(rng.choice("AC") for _ in range(200)) for _ in range(4)]
        assert count_patterns(*seqs) == brute_counts(*seqs)


def test_frequency_terms_match_counts():
    rng = random.Random(2)
    seqs = simulate_sites(rng, 500, 0.5, 0.0, 1.0)
    rows = polarize(*seqs)
    a = sum(site_terms(*r)[0] for r in rows)
    b = sum(site_terms(*r)[1] for r in rows)
    assert (a, b) == count_patterns(*seqs)


def test_frequency_terms_by_hand():
    x, y = site_terms(0.2, 0.6, 0.5, 0.1)
    assert x == pytest.approx(0.8 * 0.6 * 0.5 * 0.9)
    assert y == pytest.approx(0.2 * 0.4 * 0.5 * 0.9)
    # The numerator is p3 (1 - p4) (p2 - p1).
    assert x - y == pytest.approx(0.5 * 0.9 * (0.6 - 0.2))


def test_antisymmetry():
    rng = random.Random(3)
    freqs = [tuple(rng.random() for _ in range(3)) + (0.0,) for _ in range(300)]
    swapped = [(b, a, c, d) for a, b, c, d in freqs]
    d1, se1, z1 = abba_baba(freqs, 30)
    d2, se2, z2 = abba_baba(swapped, 30)
    assert d1 == pytest.approx(-d2)
    assert se1 == pytest.approx(se2)
    assert z1 == pytest.approx(-z2)


def test_jackknife_of_mean_is_standard_error():
    rng = random.Random(4)
    vals = [rng.gauss(0, 1) for _ in range(12)]
    est, se, loo = block_jackknife(vals, lambda xs: sum(xs) / len(xs))
    mean = sum(vals) / 12
    s2 = sum((v - mean) ** 2 for v in vals) / 11
    assert est == pytest.approx(mean)
    assert se == pytest.approx(math.sqrt(s2 / 12))


def test_jackknife_leave_one_out_values():
    blocks = [(3.0, 1.0), (2.0, 2.0), (4.0, 0.0), (1.0, 1.0)]
    est, se, loo = block_jackknife(blocks, lambda bs: d_from_counts(sum(a for a, _ in bs), sum(b for _, b in bs)))
    assert est == pytest.approx((10 - 4) / 14)
    assert loo == pytest.approx([(7 - 3) / 10, (8 - 2) / 10, (6 - 4) / 10, (9 - 3) / 12])
    mean = sum(loo) / 4
    assert se == pytest.approx(math.sqrt(0.75 * sum((v - mean) ** 2 for v in loo)))


def test_null_model_gives_small_z():
    rng = random.Random(5)
    seqs = simulate_sites(rng, 20000, 0.3, 0.0, 1.0)
    d, se, z = abba_baba(polarize(*seqs), 500)
    assert abs(z) < 3
    abba, baba = count_patterns(*seqs)
    assert abba > 300 and baba > 300  # incomplete lineage sorting makes both patterns common


def test_introgression_gives_positive_d():
    rng = random.Random(6)
    seqs = simulate_sites(rng, 20000, 0.3, 0.1, 1.0)
    d, se, z = abba_baba(polarize(*seqs), 500)
    assert d > 0.1
    assert z > 5


def test_block_sums_and_errors():
    freqs = [(0.0, 1.0, 1.0, 0.0)] * 5 + [(1.0, 0.0, 1.0, 0.0)] * 2
    assert block_sums(freqs, 3) == [(3.0, 0.0), (2.0, 1.0), (0.0, 1.0)]
    with pytest.raises(ValueError):
        block_sums(freqs, 0)
    with pytest.raises(ValueError):
        d_from_counts(0, 0)
    with pytest.raises(ValueError):
        block_jackknife([(1.0, 0.0)], lambda bs: 0.0)
    # Sites with three alleles are dropped.
    assert polarize("AT", "CT", "GA", "AA") == [(1.0, 1.0, 0.0, 0.0)]
