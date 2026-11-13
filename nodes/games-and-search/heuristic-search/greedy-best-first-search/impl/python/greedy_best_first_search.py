# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-best-first-search/. The authors are listed in prov/TT8WY1.jsonl.

"""Greedy best-first search: always expand the open state of least h.

The graph search follows the page pseudocode. REACHED holds every state that
was ever put in OPEN, so each state enters OPEN at most once and the first
path found to it is kept. Ties in h are broken first in, first out.

tree=True drops REACHED. This is the tree search of the page, which can run
forever on a graph with a cycle.
max_expansions stops a run after that many expansions (None means no limit).
"""

import heapq
import itertools
from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SearchResult:
    path: Optional[list]  # states from the start to a goal, or None
    cost: Optional[int]  # cost of that path, or None
    expanded: list = field(default_factory=list)  # states in the order of expansion
    generated: int = 0  # successor pairs looked at
    stopped: bool = False  # True when max_expansions ended the run


def greedy_best_first_search(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, int]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], int],
    tree: bool = False,
    max_expansions: Optional[int] = None,
) -> SearchResult:
    """Find some path from start to a goal, guided by h only.

    Precondition: every state has finitely many successors and costs are
    nonnegative. In graph mode on a finite graph the search stops, and it
    returns a path exactly when a goal can be reached.
    Cost: O(m log n) time and O(n) space in graph mode, where n states are
    reached and m successor pairs are looked at.
    """
    res = SearchResult(None, None)
    seq = itertools.count()
    # Tree mode stores whole nodes (state, g, parent node) because a state can
    # occur many times; graph mode stores one parent per state.
    root = (start, 0, None)  # @line L1
    heap = [(h(start), next(seq), root)]  # @line L2
    reached = {start}
    while heap:  # @line L3
        if max_expansions is not None and len(res.expanded) >= max_expansions:
            res.stopped = True
            return res
        _, _, node = heapq.heappop(heap)  # @line L4
        n, g, _ = node
        if is_goal(n):  # @line L5
            path = []
            x = node
            while x is not None:
                path.append(x[0])
                x = x[2]
            res.path, res.cost = path[::-1], g
            return res
        res.expanded.append(n)
        for m, c in successors(n):  # @line L6
            res.generated += 1
            if tree or m not in reached:  # @line L7
                reached.add(m)  # @line L8
                heapq.heappush(heap, (h(m), next(seq), (m, g + c, node)))  # @line L9
    return res  # @line L10
