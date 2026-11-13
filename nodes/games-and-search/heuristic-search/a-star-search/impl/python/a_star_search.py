# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a-star-search/. The authors are listed in prov/6K9J0E.jsonl.

"""A* search (Hart, Nilsson and Raphael 1968) with OPEN and CLOSED lists.

The search follows the page pseudocode. OPEN is a binary heap with lazy
deletion: a state whose g drops is pushed again, and the old entry is skipped
when it comes out. Ties in f are broken toward the larger g, then first in,
first out.

Two switches give the variants that the page compares:
- reopen=False refuses a cheaper path to a CLOSED state (graph search
  without reopening). It is optimal for a consistent h, not in general.
- pathmax=True uses h(n') <- max(h(n'), h(n) - c(n, n')) when n' is put in
  OPEN (Mero 1984, rule 1), so f never drops from a parent to its child.
"""

import heapq
import itertools
from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional

Number = int | float | Fraction


@dataclass
class SearchResult:
    """The answer of a run, with the counts that the page uses."""

    path: Optional[list]  # states from the start to a goal, or None
    cost: Optional[Number]  # g of the goal, or None
    expanded: list = field(default_factory=list)  # states in the order of line L6
    popped_f: list = field(default_factory=list)  # f of each expanded state
    generated: int = 0  # successor pairs looked at, line L7
    pushed: int = 0  # entries put in OPEN, line L11 (the start included)
    reopenings: int = 0  # expansions of a state that was expanded before

    @property
    def expansions(self) -> int:
        return len(self.expanded)


def a_star_search(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, Number]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], Number],
    reopen: bool = True,
    pathmax: bool = False,
) -> SearchResult:
    """Find a cheapest path from start to a goal state.

    Precondition: edge costs are nonnegative, every state has finitely many
    successors, and h(s) >= 0. With reopen=True and an admissible h the
    returned cost is optimal on every finite graph; with a consistent h no
    state is expanded twice.
    Cost: O(E log E) time and O(V + E) space on a finite graph searched
    with a consistent h, where E counts the successor pairs looked at.
    """
    res = SearchResult(None, None)
    g: dict = {start: 0}  # @line L1
    parent: dict = {start: None}
    hv: dict = {start: h(start)}
    seq = itertools.count()
    heap = [(hv[start], 0, next(seq), start)]  # @line L2
    closed: set = set()
    ever_expanded: set = set()
    res.pushed = 1
    while heap:  # @line L3
        f, neg_g, _, n = heapq.heappop(heap)  # @line L4
        if -neg_g != g[n] or n in closed:
            continue  # a stale entry: n got a cheaper g later
        if is_goal(n):  # @line L5
            path = []
            s = n
            while s is not None:
                path.append(s)
                s = parent[s]
            res.path, res.cost = path[::-1], g[n]
            return res
        closed.add(n)  # @line L6
        res.expanded.append(n)
        res.popped_f.append(f)
        if n in ever_expanded:
            res.reopenings += 1
        ever_expanded.add(n)
        for m, c in successors(n):  # @line L7
            res.generated += 1
            ng = g[n] + c
            if m not in g or ng < g[m]:  # @line L8
                if m in closed and not reopen:
                    continue
                g[m] = ng  # @line L9
                parent[m] = n
                closed.discard(m)  # @line L10
                hm = h(m)
                if pathmax:
                    hm = max(hm, hv.get(m, hm), hv[n] - c)
                hv[m] = hm
                heapq.heappush(heap, (ng + hm, -ng, next(seq), m))  # @line L11
                res.pushed += 1
    return res  # @line L12


def effective_branching_factor(n: int, d: int, tol: Fraction = Fraction(1, 10**6)) -> Fraction:
    """The b* with n + 1 = 1 + b* + b*^2 + ... + b*^d, to within tol.

    n is the number of nodes generated (the root not counted) and d >= 1 the
    depth of the solution, with n >= d. The sum is increasing in b on b >= 0,
    so bisection on [1, n] finds the root. The result is exact for n = d
    (b* = 1); otherwise it is a midpoint at distance at most tol from b*.
    Cost: O(d log(n / tol)) operations on fractions.
    """
    if d < 1 or n < d:
        raise ValueError("need d >= 1 and n >= d")
    target = n + 1

    def total(b: Fraction) -> Fraction:
        s, p = Fraction(0), Fraction(1)
        for _ in range(d + 1):
            s += p
            p *= b
        return s

    if n == d:
        return Fraction(1)
    lo, hi = Fraction(1), Fraction(n)  # total(1) = d + 1 <= target <= total(n)
    while hi - lo > 2 * tol:
        mid = (lo + hi) / 2
        if total(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
