# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phylogenetic-bootstrap/. The authors are listed in prov/3RY3K8.jsonl.

import itertools
import math
import random
from fractions import Fraction

from phylogenetic_bootstrap import (
    all_topologies,
    bootstrap_support,
    exhaustive_parsimony,
    fitch_length,
    resample_columns,
    tree_splits,
)


def compositions(total, parts):
    """All vectors of parts nonnegative integers with the given sum."""
    for cut in itertools.combinations(range(total + parts - 1), parts - 1):
        prev = -1
        out = []
        for c in cut:
            out.append(c - prev - 1)
            prev = c
        out.append(total + parts - 2 - prev)
        yield out


def exact_support(seqs):
    """The ideal bootstrap: the expected count of each split over all m^m resamples.

    The estimate depends only on how many times each column is drawn, so the sum runs over
    the count vectors with multinomial weights m! / (c_1! ... c_m!) / m^m.
    """
    m = len(seqs[0])
    cache = {}
    total = {}
    for c in compositions(m, m):
        weight = Fraction(math.factorial(m), m**m)
        for x in c:
            weight /= math.factorial(x)
        data = ["".join(s[j] * c[j] for j in range(m)) for s in seqs]
        key = tuple(data)
        if key not in cache:
            cache[key] = exhaustive_parsimony(data)
        trees = cache[key]
        for t in trees:
            for s in t:
                total[s] = total.get(s, Fraction(0)) + weight / len(trees)
    return total


def test_compositions_weights_sum_to_one():
    m = 5
    w = Fraction(0)
    for c in compositions(m, m):
        x = Fraction(math.factorial(m), m**m)
        for k in c:
            x /= math.factorial(k)
        w += x
    assert w == 1
    assert sum(1 for _ in compositions(m, m)) == math.comb(2 * m - 1, m)


def test_resample_keeps_shape_and_uses_columns():
    rng = random.Random(1)
    seqs = ["ACGTA", "ACGTT", "AGGTC", "TCGTA"]
    cols = {"".join(s[j] for s in seqs) for j in range(5)}
    for _ in range(50):
        d = resample_columns(seqs, rng)
        assert [len(x) for x in d] == [5] * 4
        assert all("".join(x[j] for x in d) in cols for j in range(5))


def test_exhaustive_parsimony_against_direct_scan():
    rng = random.Random(2)
    for _ in range(20):
        seqs = ["".join(rng.choice("ACGT") for _ in range(6)) for _ in range(5)]
        best = exhaustive_parsimony(seqs)
        lens = {tree_splits(t, 5): fitch_length(t, seqs) for t in all_topologies(5)}
        low = min(lens.values())
        assert set(best) == {k for k, v in lens.items() if v == low}


def test_identical_columns_give_full_support():
    seqs = ["AAAA", "AAAA", "CCCC", "CCCC", "CCCC"]  # every site splits 01 | 234
    sup = bootstrap_support(seqs, exhaustive_parsimony, 20, random.Random(3))
    assert sup[frozenset({2, 3, 4})] == 1.0


def test_monte_carlo_matches_exact_bootstrap():
    seqs = ["AAAAC", "AAACC", "CCAAA", "CCCCA", "CACCA"]
    exact = exact_support(seqs)
    est = bootstrap_support(seqs, exhaustive_parsimony, 1500, random.Random(4))
    for s in set(exact) | set(est):
        e = float(exact.get(s, 0))
        # standard error is at most 0.5 / sqrt(1500) < 0.013; allow 4 of them
        assert abs(est.get(s, 0.0) - e) <= 0.052


def test_support_of_tree_splits_is_at_most_one_and_sums():
    rng = random.Random(5)
    seqs = ["".join(rng.choice("AC") for _ in range(8)) for _ in range(5)]
    sup = bootstrap_support(seqs, exhaustive_parsimony, 200, rng)
    assert all(0.0 <= v <= 1.0 for v in sup.values())
    # each replicate contributes exactly n - 3 = 2 splits in total
    assert abs(sum(sup.values()) - 2.0) < 1e-9
