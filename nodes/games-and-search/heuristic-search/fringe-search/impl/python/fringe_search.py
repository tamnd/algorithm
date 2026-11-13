# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fringe-search/. The authors are listed in prov/YG7MJ1.jsonl.

"""Fringe search (Bjornsson, Enzenberger, Holte and Schaeffer 2005).

The fringe is one doubly linked list of states. A pass walks it from left
to right with the threshold flim. A state with f > flim stays in the list
(the "later" part) and gives a candidate for the next threshold. A state
with f <= flim is expanded and removed; each child with a new or cheaper g
is moved to the place just after it (the "now" part), so the same pass
visits it. A cache holds g and the parent of each state seen. Children are
inserted from right to left, so they are visited in the order of
successors().
"""

from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
INF = float("inf")


@dataclass
class SearchResult:
    path: Optional[list]  # states from the start to a goal, or None
    cost: Optional[Number]  # g of the goal, or None
    thresholds: list = field(default_factory=list)  # flim of each pass
    expanded: list = field(default_factory=list)  # states in the order of expansion
    visits: int = 0  # list entries looked at, all passes

    @property
    def reexpansions(self) -> int:
        return len(self.expanded) - len(set(self.expanded))


def fringe_search(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, Number]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], Number],
) -> SearchResult:
    """Find a cheapest path from start to a goal without a priority queue.

    Precondition: positive costs, finitely many successors per state, and an
    admissible h. Then the returned cost is optimal; on a finite graph with
    no reachable goal the search returns failure.
    Cost: O(n) space for the list and the cache, n the states seen.
    """
    res = SearchResult(None, None)
    HEAD = object()  # sentinel: nxt[HEAD] is the first state of the list
    nxt: dict = {HEAD: start}  # @line L1
    prv: dict = {start: HEAD}
    nxt[start] = None
    cache: dict = {start: (0, None)}  # @line L2
    flim = h(start)

    def unlink(s):
        p, q = prv.pop(s), nxt.pop(s)
        nxt[p] = q
        if q is not None:
            prv[q] = p

    def link_after(a, s):
        q = nxt[a]
        nxt[a], prv[s], nxt[s] = s, a, q
        if q is not None:
            prv[q] = s

    while nxt[HEAD] is not None:  # @line L3
        res.thresholds.append(flim)
        fmin = INF  # @line L4
        node = nxt[HEAD]
        while node is not None:  # @line L5
            res.visits += 1
            g, _ = cache[node]
            f = g + h(node)
            if f > flim:  # @line L6
                fmin = min(fmin, f)
                node = nxt[node]
                continue
            if is_goal(node):  # @line L7
                path, s = [], node
                while s is not None:
                    path.append(s)
                    s = cache[s][1]
                res.path, res.cost = path[::-1], g
                return res
            res.expanded.append(node)
            for child, c in reversed(list(successors(node))):  # @line L8
                gc = g + c
                if child in cache and gc >= cache[child][0]:  # @line L9
                    continue
                if child in prv:  # @line L10
                    unlink(child)
                link_after(node, child)  # @line L11
                cache[child] = (gc, node)  # @line L12
            after = nxt[node]
            unlink(node)  # @line L13
            node = after
        flim = fmin  # @line L14
    return res  # @line L15
