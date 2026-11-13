# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-expansion-a-star/. The authors are listed in prov/JA3VM9.jsonl.

"""PEA*, partial expansion A* (Yoshizumi, Miura and Ishida 2000).

Each state in OPEN has a stored value F, which starts at f = g + h. When a
state n of least F is expanded, the code makes all its children but stores
only those with f <= F(n) + C, for the cutoff C >= 0. If some child was not
stored, n goes back to OPEN with F(n) = the least f of those children;
otherwise n is closed. A cheaper path to a state resets its F to its new f
and puts it back in OPEN (reopening). C = infinity stores every child, which
is A*. OPEN is a binary heap with lazy deletion; ties in F go to the larger g,
then first in, first out.
"""

import heapq
import itertools
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
    expansions: int = 0  # times a state of OPEN that is not a goal was expanded
    generated: int = 0  # children made, line L7
    stored_f: list = field(default_factory=list)  # f of each state put in OPEN, line L11
    max_open: int = 0  # largest size of OPEN


def partial_expansion_a_star(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, Number]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], Number],
    cutoff: Number = 0,
) -> SearchResult:
    """Find a cheapest path from start to a goal, storing few surplus nodes.

    Precondition: nonnegative costs, finitely many successors per state, an
    admissible h and cutoff >= 0. Then the returned cost is optimal.
    Cost: with cutoff 0, no stored state has f > C*; each state can be
    expanded once for each distinct f value of its children.
    """
    res = SearchResult(None, None)
    g: dict = {start: 0}  # @line L1
    parent: dict = {start: None}
    F: dict = {start: h(start)}
    open_set = {start}
    seq = itertools.count()
    heap = [(F[start], 0, next(seq), start)]  # @line L2
    res.stored_f.append(F[start])
    while heap:  # @line L3
        key, neg_g, _, n = heapq.heappop(heap)  # @line L4
        if n not in open_set or key != F[n] or -neg_g != g[n]:
            continue  # a stale entry
        open_set.discard(n)
        if is_goal(n):  # @line L5
            path, s = [], n
            while s is not None:
                path.append(s)
                s = parent[s]
            res.path, res.cost = path[::-1], g[n]
            return res
        res.expansions += 1
        rest = INF  # @line L6
        for m, c in successors(n):  # @line L7
            res.generated += 1
            gm = g[n] + c
            fm = gm + h(m)  # @line L8
            if fm > key + cutoff:  # @line L9
                rest = min(rest, fm)
                continue
            if m not in g or gm < g[m]:  # @line L10
                g[m], parent[m], F[m] = gm, n, fm  # @line L11
                open_set.add(m)
                heapq.heappush(heap, (fm, -gm, next(seq), m))
                res.stored_f.append(fm)
        if rest < INF:  # @line L12
            F[n] = rest
            open_set.add(n)
            heapq.heappush(heap, (rest, -g[n], next(seq), n))
        res.max_open = max(res.max_open, len(open_set))
    return res  # @line L13
