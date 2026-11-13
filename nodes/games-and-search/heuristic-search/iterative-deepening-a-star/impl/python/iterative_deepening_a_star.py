# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-deepening-a-star/. The authors are listed in prov/1ND9FV.jsonl.

"""IDA*, iterative-deepening A* (Korf 1985).

Each iteration is a depth-first search that cuts off every node with
f = g + h above the threshold T. The next threshold is the least f that was
cut off. The depth-first search uses an explicit stack of successor
iterators, so deep paths do not hit the Python recursion limit, and it skips
a successor that is already on the current path.
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
    cost: Optional[Number]  # cost of that path, or None
    thresholds: list = field(default_factory=list)  # T of each iteration
    expanded: list = field(default_factory=list)  # expanded[i] = states expanded in iteration i
    generated: int = 0  # successor pairs looked at, all iterations

    @property
    def expansions(self) -> int:
        return sum(len(e) for e in self.expanded)


def ida_star(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, Number]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], Number],
    max_iterations: Optional[int] = None,
) -> SearchResult:
    """Find a cheapest path from start to a goal with memory linear in its depth.

    Precondition: costs are at least some eps > 0, every state has finitely
    many successors and h is admissible. Then the returned cost is optimal.
    On a finite graph with no reachable goal the search returns failure.
    Cost: O(d) states on the path and O(b d) stack entries, for a path of
    d states and at most b successors per state.
    """
    res = SearchResult(None, None)
    if is_goal(start):
        res.path, res.cost = [start], 0
        return res
    T = h(start)  # @line L1
    while max_iterations is None or len(res.thresholds) < max_iterations:  # @line L2
        res.thresholds.append(T)
        exp: list = [start]
        res.expanded.append(exp)
        path, gs, on_path = [start], [0], {start}  # @line L3
        nxt = INF  # @line L10
        stack = [iter(successors(start))]
        while stack:
            try:
                m, c = next(stack[-1])  # @line L11
            except StopIteration:
                stack.pop()  # @line L16
                on_path.discard(path.pop())
                gs.pop()
                continue
            res.generated += 1
            if m in on_path:
                continue
            g = gs[-1] + c
            f = g + h(m)  # @line L7
            if f > T:  # @line L8
                nxt = min(nxt, f)  # @line L15
                continue
            if is_goal(m):  # @line L9
                res.path, res.cost = path + [m], g  # @line L14
                return res  # @line L4
            path.append(m)  # @line L12
            gs.append(g)
            on_path.add(m)
            stack.append(iter(successors(m)))  # @line L13
            exp.append(m)
        if nxt == INF:  # @line L5
            return res
        T = nxt  # @line L6
    return res
