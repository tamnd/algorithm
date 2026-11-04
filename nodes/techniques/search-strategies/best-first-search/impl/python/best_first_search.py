# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-first-search/. The authors are listed in prov/MQ3R69.jsonl.

import heapq
import itertools
from collections.abc import Callable, Hashable, Iterable
from typing import NamedTuple, Optional, TypeVar

S = TypeVar("S", bound=Hashable)


class Node(NamedTuple):
    state: Hashable
    parent: Optional["Node"]
    g: float
    depth: int


def path_of(n: Node) -> list:
    """The states from the root to n."""
    out = []
    m: Optional[Node] = n
    while m is not None:
        out.append(m.state)
        m = m.parent
    out.reverse()
    return out


def best_first_search(
    start: S,
    successors: Callable[[S], Iterable[tuple[S, float]]],
    is_goal: Callable[[S], bool],
    f: Callable[[Node], float],
    trace: Optional[list] = None,
) -> Optional[tuple[list[S], float]]:
    """Graph-search best-first search with evaluation function f.

    Returns (path, cost) for the first goal node removed from the frontier, or
    None when no goal is reachable. successors(s) yields (next_state, cost)
    pairs with cost >= 0; f(node) reads node.state, node.g and node.depth.
    A state is added again only on a strictly cheaper path (by g). Ties in f
    are broken by insertion order. If trace is a list, the state of each
    expanded node is appended to it. With f = g + h for an admissible h the
    result is a cheapest path. Cost: O(N log N) for N generated nodes.
    """
    tie = itertools.count()
    node = Node(start, None, 0, 0)  # @line L1
    frontier: list[tuple[float, int, Node]] = [(f(node), next(tie), node)]  # @line L2
    reached: dict[Hashable, Node] = {start: node}  # @line L3
    while frontier:  # @line L4
        _, _, n = heapq.heappop(frontier)  # @line L5
        if n is not reached[n.state]:  # @line L6
            continue
        if is_goal(n.state):  # @line L7
            return path_of(n), n.g
        if trace is not None:
            trace.append(n.state)
        for s2, c in successors(n.state):  # @line L8
            if c < 0:
                raise ValueError("best-first search needs non-negative action costs")
            child = Node(s2, n, n.g + c, n.depth + 1)  # @line L9
            old = reached.get(s2)
            if old is None or child.g < old.g:  # @line L10
                reached[s2] = child  # @line L11
                heapq.heappush(frontier, (f(child), next(tie), child))  # @line L12
    return None  # @line L13
