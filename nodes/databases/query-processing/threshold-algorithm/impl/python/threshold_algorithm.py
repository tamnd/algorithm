# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threshold-algorithm/. The authors are listed in prov/7GGJ22.jsonl.

"""Threshold algorithm (TA) of Fagin, Lotem and Naor for top-k aggregation.

The database is a list of m lists. Each list holds the same N objects as
(object, grade) pairs, sorted by grade from high to low. The aggregation t
maps a tuple of m grades to a score and must be monotone.

TA reads the lists by sorted access in parallel. When it sees an object, it
gets the object's other grades by random access and computes its score. It
keeps only the k best objects seen. After each round it computes the
threshold tau = t(last grade read in each list), and stops as soon as k
objects with score at least tau have been seen.

As in the paper, an object is looked up again each time it is seen under
sorted access and is not among the current k best; this keeps the buffer at
k objects.

stats gets "depth", "sorted" and "random".
"""

import heapq
import itertools
from collections.abc import Callable, Hashable, Sequence

Grade = float
Database = Sequence[Sequence[tuple[Hashable, Grade]]]


def threshold_algorithm(lists: Database, t: Callable[[tuple], Grade], k: int,
                        stats: dict | None = None) -> list[tuple[Hashable, Grade]]:
    """Return k (object, score) pairs with the highest scores, best first."""
    m = len(lists)
    n = len(lists[0]) if m else 0
    if any(len(lst) != n for lst in lists):
        raise ValueError("all lists must hold the same objects")
    k = max(0, min(k, n))
    index: list[dict | None] = [None] * m      # the random access interface
    tie = itertools.count()
    best: list[tuple[Grade, int, Hashable]] = []   # min-heap of the k best seen
    members: set[Hashable] = set()
    depth = sorted_acc = random_acc = 0  # @line L1
    while depth < n and k > 0:  # @line L2
        bottom = []
        for i in range(m):  # @line L3
            obj, g = lists[i][depth]  # @line L4
            sorted_acc += 1
            bottom.append(g)
            if obj in members:
                continue
            grades = []
            for j in range(m):  # @line L5
                if j == i:
                    grades.append(g)
                else:
                    if index[j] is None:
                        index[j] = dict(lists[j])
                    grades.append(index[j][obj])
                    random_acc += 1
            score = t(tuple(grades))
            if len(best) < k:  # @line L6
                heapq.heappush(best, (score, next(tie), obj))
                members.add(obj)
            elif score > best[0][0]:
                _, _, out = heapq.heapreplace(best, (score, next(tie), obj))
                members.discard(out)
                members.add(obj)
        tau = t(tuple(bottom))  # @line L7
        depth += 1  # @line L8
        if len(best) == k and best[0][0] >= tau:  # @line L9
            break
    if stats is not None:
        stats.update(depth=depth, sorted=sorted_acc, random=random_acc)
    return [(obj, s) for s, _, obj in sorted(best, key=lambda e: (-e[0], e[1]))]  # @line L10
