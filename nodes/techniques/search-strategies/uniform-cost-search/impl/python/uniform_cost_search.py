# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uniform-cost-search/. The authors are listed in prov/81NJ23.jsonl.

import heapq
import itertools
from collections.abc import Callable, Hashable, Iterable
from typing import NamedTuple, Optional, TypeVar

S = TypeVar("S", bound=Hashable)


class Node(NamedTuple):
    state: Hashable
    parent: Optional["Node"]
    g: float


def _path(n: Node) -> list:
    out = []
    m: Optional[Node] = n
    while m is not None:
        out.append(m.state)
        m = m.parent
    out.reverse()
    return out


def uniform_cost_search(
    start: S,
    successors: Callable[[S], Iterable[tuple[S, float]]],
    is_goal: Callable[[S], bool],
) -> Optional[tuple[list[S], float]]:
    """Return (path, cost) of a cheapest path from start to a goal, or None.

    successors(s) yields pairs (next_state, cost) with cost >= 0. States must be
    hashable. The goal test is done when a node leaves the frontier, so the cost
    is optimal. The search stops on every finite space, and on an infinite space
    with a finite branching factor when the costs are at least some eps > 0 and
    a goal is reachable. Cost: O((V + E) log V) on an explicit graph with V
    reachable states and E transitions; O(N log N) for N generated nodes.
    """
    tie = itertools.count()  # breaks ties in the heap by insertion order
    node = Node(start, None, 0)  # @line L1
    frontier: list[tuple[float, int, Node]] = [(0, next(tie), node)]  # @line L2
    reached: dict[Hashable, Node] = {start: node}  # @line L3
    while frontier:  # @line L4
        _, _, n = heapq.heappop(frontier)  # @line L5
        if n.g > reached[n.state].g:  # @line L6
            continue
        if is_goal(n.state):  # @line L7
            return _path(n), n.g
        for s2, c in successors(n.state):  # @line L8
            if c < 0:
                raise ValueError("uniform-cost search needs non-negative action costs")
            g2 = n.g + c  # @line L9
            old = reached.get(s2)
            if old is None or g2 < old.g:  # @line L10
                reached[s2] = Node(s2, n, g2)  # @line L11
                heapq.heappush(frontier, (g2, next(tie), reached[s2]))  # @line L12
    return None  # @line L13
