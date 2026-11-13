# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beam-search/. The authors are listed in prov/WJE1MW.jsonl.

"""Beam search: breadth-first search that keeps the k best states of each layer.

The code follows the page pseudocode. A layer is the set of states kept at
one depth. The candidates of the next layer are the successors of the layer
that are not in SEEN (the states kept in earlier layers). If a candidate is
a goal, the search returns the cheapest such candidate. Otherwise it keeps
the k candidates of least f = g + h; ties go to the candidate generated
first. width=None keeps every candidate, which is breadth-first search.
"""

from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SearchResult:
    path: Optional[list]  # states from the start to a goal, or None
    cost: Optional[int]  # cost of that path, or None
    layers: list = field(default_factory=list)  # the kept layers, in order
    generated: int = 0  # successor pairs looked at
    pruned: int = 0  # candidates dropped by the width limit


def beam_search(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, int]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], int],
    width: Optional[int] = None,
) -> SearchResult:
    """Search with a beam of the given width; return a path or failure.

    Precondition: width >= 1 or None, nonnegative costs, finitely many
    successors per state. On a finite graph the search stops. A returned path
    is a real path to a goal; failure does not prove that no goal is
    reachable unless width is None.
    Cost: at most k b successor pairs and one sort of at most k b candidates
    per layer, where b bounds the number of successors. Each layer adds new
    states to SEEN, so there are at most n layers on a graph of n states.
    """
    if width is not None and width < 1:
        raise ValueError("the width must be at least 1")
    res = SearchResult(None, None)
    g = {start: 0}
    parent = {start: None}

    def path_to(s):
        p = []
        while s is not None:
            p.append(s)
            s = parent[s]
        return p[::-1]

    if is_goal(start):  # @line L1
        res.path, res.cost = [start], 0
        return res
    layer = [start]  # @line L2
    seen = {start}
    res.layers.append(list(layer))
    while layer:  # @line L3
        cand: dict = {}  # @line L4
        for n in layer:  # @line L5
            for m, c in successors(n):
                res.generated += 1
                if m in seen:
                    continue
                if m not in cand or g[n] + c < cand[m][0]:  # @line L6
                    order = cand[m][1] if m in cand else len(cand)
                    cand[m] = (g[n] + c, order, n)
        goals = [m for m in cand if is_goal(m)]  # @line L7
        if goals:
            best = min(goals, key=lambda m: (cand[m][0], cand[m][1]))
            for m, (gm, _, p) in cand.items():
                g[m], parent[m] = gm, p
            res.path, res.cost = path_to(best), cand[best][0]
            return res
        ranked = sorted(cand, key=lambda m: (cand[m][0] + h(m), cand[m][1]))  # @line L8
        keep = ranked if width is None else ranked[:width]
        res.pruned += len(ranked) - len(keep)
        for m in keep:
            g[m], parent[m] = cand[m][0], cand[m][2]
        layer = keep
        seen.update(keep)  # @line L9
        if layer:
            res.layers.append(list(layer))
    return res  # @line L10
