# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cluster-purity/. The authors are listed in prov/4PZFVQ.jsonl.
"""Purity of a clustering against ground truth classes."""

from collections import Counter, defaultdict
from fractions import Fraction
from typing import Hashable, Sequence


def purity(clusters: Sequence[Hashable], classes: Sequence[Hashable]) -> Fraction:
    """(1/n) * sum over clusters of the count of its most common class. O(n) time.

    The arguments are not symmetric: the first one is the clustering, the second one
    the ground truth. Purity of an empty input is 1 by convention.
    """
    if len(clusters) != len(classes):
        raise ValueError("the two labelings must have the same length")
    n = len(clusters)
    if n == 0:
        return Fraction(1)
    table: dict[Hashable, Counter] = defaultdict(Counter)
    for c, y in zip(clusters, classes):
        table[c][y] += 1
    return Fraction(sum(max(row.values()) for row in table.values()), n)


def majority_labels(clusters: Sequence[Hashable], classes: Sequence[Hashable]) -> dict:
    """The class that each cluster is assigned to (its most common class)."""
    table: dict[Hashable, Counter] = defaultdict(Counter)
    for c, y in zip(clusters, classes):
        table[c][y] += 1
    return {c: row.most_common(1)[0][0] for c, row in table.items()}
