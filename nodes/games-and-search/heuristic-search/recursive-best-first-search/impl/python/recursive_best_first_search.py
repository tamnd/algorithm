# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-best-first-search/. The authors are listed in prov/TDF1Y3.jsonl.

"""RBFS, recursive best-first search (Korf 1993), with a check for cycles.

The code follows Korf's pseudocode and the page. Each call RBFS(n, F(n), B)
keeps the stored values F of the children of n, explores the child of least
F with the bound min(B, second least F), and returns the least stored value
of its children when that value exceeds B. A child inherits the stored value
of its parent when the parent was explored before (f(n) < F(n)).

The search is a tree search: a successor that is already on the current
path is skipped, so on a finite graph the tree of paths is finite. The
recursion depth is the length of the current path, so this code is for
problems whose paths stay well under the Python limit of about 1000 frames.
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
    expansions: list = field(default_factory=list)  # (path tuple, f) of each expansion
    generated: int = 0  # successor pairs looked at
    max_depth: int = 0  # longest current path, in states


def recursive_best_first_search(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, Number]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], Number],
) -> SearchResult:
    """Find a cheapest path from start to a goal in space linear in its depth.

    Precondition: positive costs, finitely many successors per state, a
    finite graph, and an admissible h. Then the returned cost is optimal.
    Cost: O(b d) stored values for paths of at most d states and at most b
    successors per state; the time has no bound in terms of A*.
    """
    res = SearchResult(None, None)
    path: list = []
    on_path: set = set()

    def rbfs(n, g, Fn, B):
        f = g + h(n)
        if f > B:  # @line L3
            return f
        if is_goal(n):  # @line L4
            res.path, res.cost = path + [n], g
            return None
        path.append(n)
        on_path.add(n)
        res.max_depth = max(res.max_depth, len(path))
        res.expansions.append((tuple(path), f))
        kids = []
        for i, (m, c) in enumerate(successors(n)):  # @line L5
            res.generated += 1
            if m in on_path:
                continue
            fm = g + c + h(m)
            Fm = max(Fn, fm) if f < Fn else fm  # @line L7
            kids.append([Fm, i, m, g + c])
        out: Optional[Number] = INF  # @line L6
        if kids:
            kids.sort(key=lambda k: (k[0], k[1]))
            while kids[0][0] <= B and kids[0][0] < INF:  # @line L8
                alt = kids[1][0] if len(kids) > 1 else INF  # @line L9
                v = rbfs(kids[0][2], kids[0][3], kids[0][0], min(B, alt))  # @line L10
                if v is None:
                    out = None
                    break
                kids[0][0] = v
                kids.sort(key=lambda k: (k[0], k[1]))
            else:
                out = kids[0][0]  # @line L11
        path.pop()
        on_path.discard(n)
        return out

    rbfs(start, 0, h(start), INF)  # @line L1
    return res  # @line L2
