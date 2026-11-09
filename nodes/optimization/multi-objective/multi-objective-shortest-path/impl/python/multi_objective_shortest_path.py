# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-objective-shortest-path/. The authors are listed in prov/BMDG74.jsonl.

"""The label-setting method of Martins (1984) for multi-objective shortest paths.

All objectives are minimized. The graph is directed, given as a list of arcs
(u, v, cost), where cost is a tuple of p >= 1 nonnegative numbers. The method
returns, for each distinct nondominated cost vector of an s-t path, one path
with that cost. Labels are taken from a heap in lexicographic order of their
cost vectors; a label taken from the heap is permanent and is never removed.
"""

import heapq
from typing import Dict, Hashable, List, Sequence, Tuple

Arc = Tuple[Hashable, Hashable, Sequence]


def weakly_dominates(a: Sequence, b: Sequence) -> bool:
    return all(x <= y for x, y in zip(a, b))


def martins(arcs: Sequence[Arc], s: Hashable, t: Hashable) -> List[Tuple[Tuple, List]]:
    """Return a list of (cost, path) pairs, one for each nondominated cost
    vector of an s-t path, sorted by cost. A path is a list of vertices."""
    out: Dict[Hashable, List[Tuple[Hashable, Tuple]]] = {}
    p = None
    for u, v, c in arcs:
        c = tuple(c)
        if any(x < 0 for x in c):
            raise ValueError("arc costs must be nonnegative")
        if p is None:
            p = len(c)
        out.setdefault(u, []).append((v, c))
    if p is None:
        return [((), [s])] if s == t else []
    zero = tuple(0 for _ in range(p))
    # A label is [cost, vertex, predecessor label id, alive].
    labels: List[list] = [[zero, s, -1, True]]  # @line L1
    temp: Dict[Hashable, List[int]] = {s: [0]}  # @line L1
    perm: Dict[Hashable, List[int]] = {}  # @line L1
    heap = [(zero, 0)]  # @line L1
    while heap:  # @line L2
        y, lid = heapq.heappop(heap)  # @line L3
        lab = labels[lid]  # @line L3
        if not lab[3]:  # @line L3
            continue  # @line L3
        v = lab[1]  # @line L4
        temp[v].remove(lid)  # @line L4
        perm.setdefault(v, []).append(lid)  # @line L4
        for w, c in out.get(v, []):  # @line L5
            y2 = tuple(a + b for a, b in zip(y, c))  # @line L6
            near = perm.get(w, []) + temp.get(w, [])  # @line L7
            if any(weakly_dominates(labels[j][0], y2) for j in near):  # @line L7
                continue  # @line L7
            keep = []  # @line L8
            for j in temp.get(w, []):  # @line L8
                if weakly_dominates(y2, labels[j][0]):  # @line L8
                    labels[j][3] = False  # @line L8
                else:  # @line L8
                    keep.append(j)  # @line L8
            labels.append([y2, w, lid, True])  # @line L9
            keep.append(len(labels) - 1)  # @line L9
            temp[w] = keep  # @line L9
            heapq.heappush(heap, (y2, len(labels) - 1))  # @line L9
    result = []  # @line L10
    for lid in perm.get(t, []):  # @line L10
        path = []  # @line L10
        j = lid  # @line L10
        while j != -1:  # @line L10
            path.append(labels[j][1])  # @line L10
            j = labels[j][2]  # @line L10
        result.append((labels[lid][0], path[::-1]))  # @line L10
    result.sort(key=lambda r: r[0])
    return result
