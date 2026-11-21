# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/datafly/. The authors are listed in prov/JK6NEV.jsonl.
"""Sweeney's Datafly heuristic for k-anonymity by full-domain generalization and row suppression.

A table is a list of rows. Each row is a tuple of d quasi-identifier values.
A hierarchy for attribute a is a list of dicts: hierarchy[a][l] maps each raw
value of attribute a to its value at level l, hierarchy[a][0] is the identity,
and the last level maps every value of the attribute to one value.
"""

from collections import Counter
from typing import Hashable, Sequence

Row = tuple[Hashable, ...]
Hierarchy = Sequence[Sequence[dict[Hashable, Hashable]]]


def datafly(table: Sequence[Row], hierarchy: Hierarchy, k: int) -> tuple[tuple[int, ...], list[int]]:
    """Return (v, s): the generalization vector chosen by Datafly and the sorted indices of the
    rows to suppress. The table generalized by v, without the rows in s, is k-anonymous,
    and s has at most k rows.

    Precondition: k >= 1, every row has d values, and the top level of each hierarchy
    maps all values of its attribute to one value.
    Cost: at most h + 1 rounds, where h is the sum of the hierarchy heights, and
    O(n d) expected time per round for n rows and d attributes.
    """
    d = len(hierarchy)
    v = [0] * d  # @line L1
    while True:  # @line L2
        gen = [tuple(hierarchy[a][v[a]][row[a]] for a in range(d)) for row in table]  # @line L3
        counts = Counter(gen)
        s = [i for i, g in enumerate(gen) if counts[g] < k]  # @line L4
        if len(s) <= k:  # @line L5
            break
        distinct = [len({g[a] for g in gen}) for a in range(d)]
        best = max(range(d), key=lambda a: (distinct[a], -a))  # @line L6
        v[best] += 1  # @line L7
    return tuple(v), s  # @line L8
