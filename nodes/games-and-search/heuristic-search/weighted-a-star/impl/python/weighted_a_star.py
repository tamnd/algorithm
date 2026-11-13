# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-a-star/. The authors are listed in prov/887HFH.jsonl.

"""Weighted A*: best-first search on f = g + w h with a weight w >= 1.

OPEN is a binary heap with lazy deletion: a state whose g drops is pushed
again and the old entry is skipped. Ties in f go to the larger g, then first
in, first out. Use an int or a Fraction for w so that keys compare exactly.

reopen=True puts a CLOSED state back in OPEN when a cheaper path to it is
found. reopen=False ignores such paths; the cost bound w C* still holds when
h is consistent.
"""

import heapq
import itertools
from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]


@dataclass
class SearchResult:
    path: Optional[list]  # states from the start to a goal, or None
    cost: Optional[Number]  # g of the goal, or None
    expanded: list = field(default_factory=list)  # states in the order of line L6
    generated: int = 0  # successor pairs looked at, line L7
    reopenings: int = 0  # expansions of a state that was expanded before


def weighted_a_star(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, Number]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], Number],
    w: Number = 1,
    reopen: bool = True,
) -> SearchResult:
    """Find a path from start to a goal of cost at most w times the least cost.

    Precondition: w >= 1, costs are nonnegative, every state has finitely
    many successors, and h is admissible (consistent if reopen=False).
    Cost: O(m log m) time and O(n + m) space on a finite graph searched
    without reopening, where m counts the successor pairs looked at.
    """
    if w < 1:
        raise ValueError("the weight must be at least 1")
    res = SearchResult(None, None)
    g: dict = {start: 0}  # @line L1
    parent: dict = {start: None}
    seq = itertools.count()
    heap = [(w * h(start), 0, next(seq), start)]  # @line L2
    closed: set = set()
    ever: set = set()
    while heap:  # @line L3
        _, neg_g, _, n = heapq.heappop(heap)  # @line L4
        if -neg_g != g[n] or n in closed:
            continue  # a stale entry
        if is_goal(n):  # @line L5
            path, s = [], n
            while s is not None:
                path.append(s)
                s = parent[s]
            res.path, res.cost = path[::-1], g[n]
            return res
        closed.add(n)  # @line L6
        res.expanded.append(n)
        if n in ever:
            res.reopenings += 1
        ever.add(n)
        for m, c in successors(n):  # @line L7
            res.generated += 1
            ng = g[n] + c
            if m not in g or ng < g[m]:  # @line L8
                if m in closed and not reopen:
                    continue
                g[m] = ng  # @line L9
                parent[m] = n
                closed.discard(m)  # @line L10
                heapq.heappush(heap, (ng + w * h(m), -ng, next(seq), m))  # @line L11
    return res  # @line L12
