# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rand-index/. The authors are listed in prov/C0AH5H.jsonl.

import itertools
import random
from fractions import Fraction

from rand_index import pair_counts, rand_index, rand_index_naive

# Manning, Raghavan and Schutze, Introduction to Information Retrieval, Figure 16.4:
# three clusters of 17 points, classes x, o and d (diamond).
IIR_CLUSTERS = [1] * 6 + [2] * 6 + [3] * 5
IIR_CLASSES = list("xxxxxo") + list("xooood") + list("xxddd")


def test_iir_example() -> None:
    assert pair_counts(IIR_CLUSTERS, IIR_CLASSES) == (20, 20, 24, 72)
    assert rand_index(IIR_CLUSTERS, IIR_CLASSES) == Fraction(92, 136)


def test_against_definition() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randrange(0, 12)
        u = [rng.randrange(4) for _ in range(n)]
        v = [rng.randrange(3) for _ in range(n)]
        assert rand_index(u, v) == rand_index_naive(u, v)
        assert rand_index(u, v) == rand_index(v, u)


def test_label_names_do_not_matter() -> None:
    u = [0, 0, 1, 1, 2, 2, 2]
    v = [1, 0, 0, 1, 1, 2, 2]
    renamed = ["b" if x == 0 else "c" if x == 1 else "a" for x in u]
    assert rand_index(u, v) == rand_index(renamed, v)


def test_extremes() -> None:
    u = [0, 0, 1, 1, 2]
    assert rand_index(u, u) == 1
    assert rand_index([0] * 4, [0, 1, 2, 3]) == 0
    assert rand_index([], []) == 1
    assert rand_index([5], [9]) == 1


def test_mean_under_permutations_is_not_constant() -> None:
    # The mean of the Rand index under random relabeling depends on the cluster sizes,
    # which is the reason for the adjusted Rand index.
    def mean_ri(u, v):
        perms = list(itertools.permutations(v))
        return sum(rand_index(u, p) for p in perms) / len(perms)

    assert mean_ri([0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1]) == Fraction(13, 25)
    assert mean_ri([0, 0, 1, 1, 2, 2], [0, 0, 1, 1, 2, 2]) == Fraction(17, 25)
