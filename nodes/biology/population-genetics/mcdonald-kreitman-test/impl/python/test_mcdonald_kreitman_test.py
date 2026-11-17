# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcdonald-kreitman-test/. The authors are listed in prov/4QSXZX.jsonl.

import math
import random
from fractions import Fraction

import pytest

from bioseq import CODON_TABLE, STOPS
from mcdonald_kreitman_test import classify_codons, fisher_exact, mk_summary, mk_test, mk_test_from_counts

SENSE = sorted(c for c in CODON_TABLE if c not in STOPS)


def brute_fisher(table):
    (a, b), (c, d) = table
    r1, r2, c1 = a + b, c + d, a + c
    n = r1 + r2

    def prob(k):
        return Fraction(math.comb(r1, k) * math.comb(r2, c1 - k), math.comb(n, c1))

    obs = prob(a)
    return sum(prob(k) for k in range(0, c1 + 1) if k <= r1 and c1 - k <= r2 and prob(k) <= obs)


def test_fisher_known_values():
    assert fisher_exact([[4, 0], [0, 4]], exact=True) == Fraction(1, 35)
    assert fisher_exact([[7, 2], [3, 8]], exact=True) == Fraction(293, 4199)
    assert fisher_exact([[12, 5], [7, 16]]) == pytest.approx(0.02384, abs=1e-5)
    assert fisher_exact([[0, 0], [0, 0]]) == 1.0
    with pytest.raises(ValueError):
        fisher_exact([[1, -1], [0, 0]])


def test_fisher_against_brute_force():
    rng = random.Random(3)
    for _ in range(300):
        t = [[rng.randrange(12) for _ in range(2)] for _ in range(2)]
        assert fisher_exact(t, exact=True) == brute_fisher(t)
        # The test does not depend on the orientation of the table.
        assert fisher_exact([[t[0][1], t[0][0]], [t[1][1], t[1][0]]], exact=True) == brute_fisher(t)
        assert fisher_exact([t[1], t[0]], exact=True) == brute_fisher(t)


def test_adh_table():
    r = mk_test_from_counts(7, 17, 2, 42)
    assert r.p_value == pytest.approx(8206423 / 1120001480)
    assert r.neutrality_index == pytest.approx(34 / 294)
    assert r.alpha == pytest.approx(1 - 34 / 294)
    assert mk_summary(0, 5, 3, 4) == (None, None)


def test_small_alignment():
    a = ["ATGGCTTTACCTGAAAAA", "ATGGCCTTACCTGAAAAA", "ATGGCTTTACCTGAAAGA"]
    b = ["ATGGCTCTACCTGATAAA", "ATGGCTCTACCTGATAAA"]
    # Codon 2 GCT/GCC: polymorphic, synonymous. Codon 6 AAA/AGA: polymorphic,
    # nonsynonymous. Codon 3 TTA/CTA: fixed, synonymous. Codon 5 GAA/GAT: fixed,
    # nonsynonymous.
    assert classify_codons(a, b) == (1, 1, 1, 1, 0)
    r = mk_test(a, b)
    assert r.p_value == 1.0 and r.neutrality_index == 1.0 and r.alpha == 0.0


def test_skips_and_errors():
    # Two varying positions in one codon, and a gap.
    a = ["TTTGCT", "TTTGCT"]
    b = ["GTAGC-", "GTAGC-"]
    assert classify_codons(a, b) == (0, 0, 0, 0, 2)
    # A site polymorphic in B and different from A counts as a polymorphism.
    assert classify_codons(["CTT"], ["CTC", "CTA"]) == (0, 0, 0, 1, 0)
    with pytest.raises(ValueError):
        classify_codons(["TAA"], ["TAT"])
    with pytest.raises(ValueError):
        classify_codons(["ATGA"], ["ATGA"])
    with pytest.raises(ValueError):
        classify_codons([], ["ATG"])


def test_counts_cover_all_codons():
    rng = random.Random(8)
    for _ in range(50):
        anc = [rng.choice(SENSE) for _ in range(40)]
        seqs = []
        for _ in range(6):
            s = []
            for c in anc:
                if rng.random() < 0.2:
                    i = rng.randrange(3)
                    d = c[:i] + rng.choice([x for x in "ACGT" if x != c[i]]) + c[i + 1:]
                    c = d if d not in STOPS else c
                s.append(c)
            seqs.append("".join(s))
        dn, ds, pn, ps, skipped = classify_codons(seqs[:3], seqs[3:])
        invariant = sum(1 for k in range(40) if len({s[3 * k:3 * k + 3] for s in seqs}) == 1)
        assert dn + ds + pn + ps + skipped + invariant == 40


def rejection_rate(rng, reps, f_fixed, f_poly, d=20, p=30):
    hits = 0
    for _ in range(reps):
        dn = sum(rng.random() < f_fixed for _ in range(d))
        pn = sum(rng.random() < f_poly for _ in range(p))
        if fisher_exact([[dn, d - dn], [pn, p - pn]]) <= 0.05:
            hits += 1
    return hits / reps


def test_level_under_the_null_and_power():
    rng = random.Random(1991)
    reps = 2000
    rate = rejection_rate(rng, reps, 0.7, 0.7)
    # Fisher's test is conservative: the rate is at most the level, up to noise.
    assert rate <= 0.05 + 4 * math.sqrt(0.05 * 0.95 / reps)
    power = rejection_rate(rng, 500, 0.95, 0.5)
    assert power > 0.5
