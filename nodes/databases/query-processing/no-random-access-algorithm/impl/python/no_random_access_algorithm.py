# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-random-access-algorithm/. The authors are listed in prov/29R7VV.jsonl.

"""No-random-access algorithm (NRA) of Fagin, Lotem and Naor for top-k.

The database is a list of m lists. Each list holds the same N objects as
(object, grade) pairs, sorted by grade from high to low. Grades are at least
`floor` (0 by default). The aggregation t maps a tuple of m grades to a score
and must be monotone.

NRA uses sorted access only. For each seen object R it keeps the grades read
so far and two bounds on t(R):
  W(R) = t(known grades, floor for the missing ones)        (worst case)
  B(R) = t(known grades, last grade read in each list for the missing ones)
An object not yet seen has W = t(floor, ..., floor) and B = t(last grades).
After each round, T is the set of k seen objects with the largest W, ties
broken by the larger B, and M is the smallest W in T. NRA stops when no
object outside T can have a score above M.

The output is the set T. NRA may stop before it knows the exact scores, so
each object is returned with its bounds (W, B).

stats gets "depth", "sorted" and "random" (always 0).
"""

from collections.abc import Callable, Hashable, Sequence

Grade = float
Database = Sequence[Sequence[tuple[Hashable, Grade]]]


def no_random_access(lists: Database, t: Callable[[tuple], Grade], k: int,
                     stats: dict | None = None,
                     floor: Grade = 0) -> list[tuple[Hashable, Grade, Grade]]:
    """Return k (object, W, B) triples whose objects form a top-k set."""
    m = len(lists)
    n = len(lists[0]) if m else 0
    if any(len(lst) != n for lst in lists):
        raise ValueError("all lists must hold the same objects")
    k = max(0, min(k, n))
    known: dict[Hashable, list] = {}
    bottom: list[Grade] = [floor] * m
    top: list[tuple[Hashable, Grade, Grade]] = []
    depth = sorted_acc = 0  # @line L1
    while depth < n and k > 0:  # @line L2
        for i in range(m):  # @line L3
            obj, g = lists[i][depth]
            sorted_acc += 1
            if g < floor:
                raise ValueError("grades must be at least floor")
            known.setdefault(obj, [None] * m)[i] = g
            bottom[i] = g
        depth += 1  # @line L4
        bounds = []
        for obj, xs in known.items():  # @line L5
            w = t(tuple(floor if x is None else x for x in xs))
            b = t(tuple(bottom[i] if x is None else x for i, x in enumerate(xs)))
            bounds.append((w, b, obj))
        bounds.sort(key=lambda e: (-e[0], -e[1]))  # @line L6
        top = [(obj, w, b) for w, b, obj in bounds[:k]]
        if len(top) < k:
            continue
        m_k = top[-1][1]
        others_ok = all(b <= m_k for _, b, _ in bounds[k:])  # @line L7
        unseen_ok = len(known) == n or t(tuple(bottom)) <= m_k
        if others_ok and unseen_ok:
            break
    if stats is not None:
        stats.update(depth=depth, sorted=sorted_acc, random=0)
    return top  # @line L8
