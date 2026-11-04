# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bidirectional-search/. The authors are listed in prov/921J83.jsonl.

from collections.abc import Callable, Hashable, Iterable
from typing import Optional, TypeVar

S = TypeVar("S", bound=Hashable)


def _join(meet: S, parent_f: dict, parent_b: dict) -> list[S]:
    """Path start .. meet from the forward parents, then meet .. goal from the backward parents."""
    left = []
    x: Optional[S] = meet
    while x is not None:
        left.append(x)
        x = parent_f[x]
    left.reverse()
    x = parent_b[meet]
    while x is not None:
        left.append(x)
        x = parent_b[x]
    return left


def bidirectional_search(
    start: S,
    goal: S,
    successors: Callable[[S], Iterable[S]],
    predecessors: Callable[[S], Iterable[S]],
    trace: Optional[list] = None,
) -> Optional[list[S]]:
    """Bidirectional breadth-first search on a graph with unit action costs.

    Precondition: predecessors(v) lists each u with v in successors(u).
    Expands one full layer at a time, on the side with the smaller frontier,
    and returns a shortest path [start, ..., goal] or None if goal cannot be
    reached. If trace is a list, ("f" or "b", layer size) is appended for each
    layer expanded.
    Cost: O(b^(d/2)) nodes generated and stored when both directions have
    branching factor b and the distance is d; O(V + E) on an explicit graph.
    """
    if start == goal:  # @line L1
        return [start]
    parent_f: dict = {start: None}  # @line L2
    parent_b: dict = {goal: None}
    front_f, front_b = [start], [goal]  # @line L3
    while front_f and front_b:  # @line L4
        if len(front_f) <= len(front_b):  # @line L5
            side, front, parent, other, nbrs = "f", front_f, parent_f, parent_b, successors
        else:
            side, front, parent, other, nbrs = "b", front_b, parent_b, parent_f, predecessors
        if trace is not None:
            trace.append((side, len(front)))
        nxt = []  # @line L6
        for u in front:  # @line L7
            for v in nbrs(u):  # @line L8
                if v in parent:  # @line L9
                    continue
                parent[v] = u  # @line L10
                if v in other:  # @line L11
                    return _join(v, parent_f, parent_b)
                nxt.append(v)  # @line L12
        if side == "f":  # @line L13
            front_f = nxt
        else:
            front_b = nxt
    return None  # @line L14
