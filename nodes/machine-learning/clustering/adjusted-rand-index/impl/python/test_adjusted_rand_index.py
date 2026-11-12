# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjusted-rand-index/. The authors are listed in prov/W19B99.jsonl.

import itertools
import random
from fractions import Fraction

from adjusted_rand_index import adjusted_rand_index, comb2, contingency

IIR_CLUSTERS = [1] * 6 + [2] * 6 + [3] * 5
IIR_CLASSES = list("xxxxxo") + list("xooood") + list("xxddd")


def index_s(u, v):
    cells, _, _ = contingency(u, v)
    return sum(comb2(m) for m in cells.values())


def set_partitions(n):
    """All labelings in restricted growth form: one per set partition of n items."""
    out = []

    def grow(prefix, top):
        if len(prefix) == n:
            out.append(tuple(prefix))
            return
        for c in range(top + 2):
            grow(prefix + [c], max(top, c))

    grow([], -1)
    return out


def test_expectation_by_all_permutations() -> None:
    # Under the permutation model, v is relabeled by a uniform random permutation of the
    # items, with its cluster sizes fixed. Each distinct arrangement of v is equally likely.
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randrange(2, 8)
        u = [rng.randrange(3) for _ in range(n)]
        v = [rng.randrange(3) for _ in range(n)]
        arrangements = set(itertools.permutations(v))
        mean_s = Fraction(sum(index_s(u, p) for p in arrangements), len(arrangements))
        _, rows, cols = contingency(u, v)
        su = sum(comb2(m) for m in rows.values())
        sv = sum(comb2(m) for m in cols.values())
        assert mean_s == Fraction(su * sv, comb2(n))
        mean_ari = sum(adjusted_rand_index(u, p) for p in arrangements) / len(arrangements)
        degenerate = su == sv and su in (0, comb2(n))
        assert mean_ari == (1 if degenerate else 0)


def test_equals_adjusted_rand() -> None:
    # ARI = (RI - E[RI]) / (1 - E[RI]) with the Rand index RI = (C(n,2) + 2S - A - B) / C(n,2).
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randrange(2, 15)
        u = [rng.randrange(4) for _ in range(n)]
        v = [rng.randrange(4) for _ in range(n)]
        _, rows, cols = contingency(u, v)
        a = sum(comb2(m) for m in rows.values())
        b = sum(comb2(m) for m in cols.values())
        p = comb2(n)
        ri = Fraction(p + 2 * index_s(u, v) - a - b, p)
        eri = Fraction(p + 2 * Fraction(a * b, p) - a - b, p)
        if eri != 1:
            assert adjusted_rand_index(u, v) == (ri - eri) / (1 - eri)


def test_examples() -> None:
    assert adjusted_rand_index(IIR_CLUSTERS, IIR_CLASSES) == Fraction(60, 247)
    assert adjusted_rand_index([0, 0, 1, 1], [0, 1, 0, 1]) == Fraction(-1, 2)
    assert adjusted_rand_index([0, 0, 1, 1, 2, 2], [5, 5, 3, 3, 4, 4]) == 1


def test_degenerate_cases() -> None:
    assert adjusted_rand_index([], []) == 1
    assert adjusted_rand_index([1], [2]) == 1
    assert adjusted_rand_index([0, 0, 0], [1, 1, 1]) == 1
    assert adjusted_rand_index([0, 1, 2], [2, 0, 1]) == 1
    # One side trivial, the other not: the denominator is not 0, and the value is 0.
    assert adjusted_rand_index([0, 0, 0, 0], [0, 0, 1, 1]) == 0
    assert adjusted_rand_index([0, 1, 2, 3], [0, 0, 1, 1]) == 0


def test_range_on_all_pairs_of_partitions() -> None:
    for n in range(2, 7):
        parts = set_partitions(n)
        values = [adjusted_rand_index(p, q) for p in parts for q in parts]
        assert max(values) == 1
        assert min(values) >= Fraction(-1, 2)
        for p in parts:
            for q in parts:
                if adjusted_rand_index(p, q) == 1:
                    assert p == q
