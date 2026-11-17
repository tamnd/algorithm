# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fagin-algorithm/. The authors are listed in prov/2544V4.jsonl.

"""Fagin's algorithm (FA) for the top k objects under a monotone aggregation.

The database is a list of m lists. Each list holds the same N objects as
(object, grade) pairs, sorted by grade from high to low. The aggregation t
maps a tuple of m grades to a score and must be monotone: raising any grade
never lowers the score.

FA reads the lists by sorted access in parallel, one depth at a time, until at
least k objects have been seen in every list. Then it fetches the missing
grades of every seen object by random access and returns the k seen objects
with the highest scores.

stats gets "depth", "sorted" and "random" (the numbers of accesses).
"""

import heapq
from collections.abc import Callable, Hashable, Sequence

Grade = float
Database = Sequence[Sequence[tuple[Hashable, Grade]]]


def fagin(lists: Database, t: Callable[[tuple], Grade], k: int,
          stats: dict | None = None) -> list[tuple[Hashable, Grade]]:
    """Return k (object, score) pairs with the highest scores, best first."""
    m = len(lists)
    n = len(lists[0]) if m else 0
    if any(len(lst) != n for lst in lists):
        raise ValueError("all lists must hold the same objects")
    k = max(0, min(k, n))
    seen: dict[Hashable, dict[int, Grade]] = {}
    matches = 0
    depth = sorted_acc = random_acc = 0  # @line L1
    while matches < k and depth < n:  # @line L2
        for i in range(m):  # @line L3
            obj, g = lists[i][depth]
            sorted_acc += 1
            fields = seen.setdefault(obj, {})
            fields[i] = g
            if len(fields) == m:
                matches += 1
        depth += 1  # @line L4
    index = [None] * m        # built lazily: the random access interface
    scores = {}
    for obj, fields in seen.items():  # @line L5
        for i in range(m):
            if i not in fields:
                if index[i] is None:
                    index[i] = dict(lists[i])
                fields[i] = index[i][obj]
                random_acc += 1
        scores[obj] = t(tuple(fields[i] for i in range(m)))  # @line L6
    top = heapq.nlargest(k, scores.items(), key=lambda p: p[1])  # @line L7
    if stats is not None:
        stats.update(depth=depth, sorted=sorted_acc, random=random_acc)
    return top
