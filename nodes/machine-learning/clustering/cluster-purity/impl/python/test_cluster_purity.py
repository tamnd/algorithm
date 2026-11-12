# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cluster-purity/. The authors are listed in prov/4PZFVQ.jsonl.

import random
from collections import Counter
from fractions import Fraction

from cluster_purity import majority_labels, purity

IIR_CLUSTERS = [1] * 6 + [2] * 6 + [3] * 5
IIR_CLASSES = list("xxxxxo") + list("xooood") + list("xxddd")


def test_iir_example() -> None:
    assert purity(IIR_CLUSTERS, IIR_CLASSES) == Fraction(12, 17)
    assert majority_labels(IIR_CLUSTERS, IIR_CLASSES) == {1: "x", 2: "o", 3: "d"}
    # Purity is not symmetric in its two arguments.
    assert purity([0, 0, 0, 0], ["a", "a", "b", "b"]) == Fraction(1, 2)
    assert purity(["a", "a", "b", "b"], [0, 0, 0, 0]) == 1


def test_singletons_and_one_cluster() -> None:
    assert purity(list(range(17)), IIR_CLASSES) == 1
    assert purity([0] * 17, IIR_CLASSES) == Fraction(8, 17)
    assert purity([], []) == 1


def test_against_definition_and_bounds() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randrange(1, 30)
        cl = [rng.randrange(5) for _ in range(n)]
        y = [rng.randrange(3) for _ in range(n)]
        p = purity(cl, y)
        # The definition by pairs of (cluster, class) counts.
        want = sum(max(sum(1 for i in range(n) if cl[i] == c and y[i] == t) for t in set(y)) for c in set(cl))
        assert p == Fraction(want, n)
        # The lower bound: the share of the largest class.
        assert p >= Fraction(max(Counter(y).values()), n)
        # Splitting a cluster never lowers purity.
        split = [c if i % 2 else c + 100 for i, c in enumerate(cl)]
        assert purity(split, y) >= p
