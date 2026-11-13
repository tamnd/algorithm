# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bidirectional-heuristic-search/. The authors are listed in prov/C7VG9R.jsonl.

"""MM, bidirectional heuristic search that meets in the middle (Holte et al. 2016).

A forward search from the start uses h_f, an estimate of the cost to the
goal, and a backward search from the goal uses h_b, an estimate of the cost
from the start, over the predecessor function. A node n of a direction has
the priority pr(n) = max(g(n) + h(n), 2 g(n)). Each step expands, in the
direction of the least priority C, a node of priority C (ties: smaller g,
then first in). U is the cost of the best path found where the two
searches touch. The search stops when
    U <= max(C, fmin_f, fmin_b, gmin_f + gmin_b + eps),
where eps is a lower bound on the cost of every action.

U is updated when a generated node has a g value in the other direction,
that is when it is in the other OPEN or the other CLOSED. The paper tests
only the other OPEN; the extra test can only find a path sooner. For
clarity the code scans OPEN for each minimum, which costs O(n) per step.
"""

import itertools
from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
INF = float("inf")


@dataclass
class SearchResult:
    path: Optional[list]  # states from the start to the goal, or None
    cost: Optional[Number]  # U at the end, or None
    expanded_f: list = field(default_factory=list)  # forward expansions, in order
    expanded_b: list = field(default_factory=list)  # backward expansions, in order
    gs_f: list = field(default_factory=list)  # g_f of each forward expansion
    gs_b: list = field(default_factory=list)  # g_b of each backward expansion

    @property
    def expansions(self) -> int:
        return len(self.expanded_f) + len(self.expanded_b)


class _Side:
    def __init__(self, root, nbrs, h, seq):
        self.g: dict = {root: 0}
        self.parent: dict = {root: None}
        self.open: dict = {root: next(seq)}  # state -> insertion number
        self.closed: set = set()
        self.nbrs, self.h = nbrs, h

    def pr(self, n):
        return max(self.g[n] + self.h(n), 2 * self.g[n])

    def best(self):
        return min(self.open, key=lambda n: (self.pr(n), self.g[n], self.open[n]))


def mm_search(
    start: Hashable,
    goal: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, Number]]],
    predecessors: Callable[[Hashable], Iterable[tuple[Hashable, Number]]],
    h_f: Callable[[Hashable], Number],
    h_b: Callable[[Hashable], Number],
    eps: Number = 0,
) -> SearchResult:
    """Find a cheapest path from start to goal with MM.

    Precondition: positive costs, each at least eps >= 0; h_f(n) is at most
    the cost from n to goal and h_b(n) at most the cost from start to n.
    Then the returned cost is optimal, every forward expansion has
    g_f <= C*/2 and f_f <= C*, and the same holds backward.
    """
    res = SearchResult(None, None)
    seq = itertools.count()
    fw = _Side(start, successors, h_f, seq)  # @line L1
    bw = _Side(goal, predecessors, h_b, seq)
    U, meet = (0, start) if start == goal else (INF, None)  # @line L2
    while fw.open and bw.open:  # @line L3
        nf, nb = fw.best(), bw.best()
        C = min(fw.pr(nf), bw.pr(nb))  # @line L4
        fmin_f = min(fw.g[n] + fw.h(n) for n in fw.open)
        fmin_b = min(bw.g[n] + bw.h(n) for n in bw.open)
        gmin_f = min(fw.g[n] for n in fw.open)
        gmin_b = min(bw.g[n] for n in bw.open)
        if U <= max(C, fmin_f, fmin_b, gmin_f + gmin_b + eps):  # @line L5
            break
        if C == fw.pr(nf):  # @line L6
            side, other, n = fw, bw, nf
            res.expanded_f.append(n)
            res.gs_f.append(fw.g[n])
        else:
            side, other, n = bw, fw, nb
            res.expanded_b.append(n)
            res.gs_b.append(bw.g[n])
        del side.open[n]  # @line L7
        side.closed.add(n)
        for c, cost in side.nbrs(n):  # @line L8
            gc = side.g[n] + cost
            if c in side.g and side.g[c] <= gc:  # @line L9
                continue
            side.open.pop(c, None)  # @line L10
            side.closed.discard(c)
            side.g[c], side.parent[c] = gc, n  # @line L11
            side.open[c] = next(seq)
            if c in other.g and gc + other.g[c] < U:  # @line L12
                U, meet = gc + other.g[c], c
    if U == INF:
        return res  # @line L13
    left, s = [], meet
    while s is not None:
        left.append(s)
        s = fw.parent[s]
    right, s = [], bw.parent[meet]
    while s is not None:
        right.append(s)
        s = bw.parent[s]
    res.path, res.cost = left[::-1] + right, U
    return res  # @line L14
