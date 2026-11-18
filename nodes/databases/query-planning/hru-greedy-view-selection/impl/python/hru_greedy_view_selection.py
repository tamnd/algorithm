# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hru-greedy-view-selection/. The authors are listed in prov/TY6PHM.jsonl.
"""The greedy view selection algorithm of Harinarayan, Rajaraman and Ullman (SIGMOD 1996).

A lattice of views has a top view, which is always stored, and a relation
"w can be answered from v" (w <= v). In the linear cost model, the cost of
answering w from a set S of stored views is the size of the smallest view
in S that w can be answered from. The benefit of a view v for S is

    B(v, S) = sum over w <= v of max(0, C_S(w) - |v|),

the total saving when v is added to S. The greedy algorithm adds, k times,
the view with the largest benefit. Each query w can have a weight (its
frequency); the default weight is 1.

`greedy_views` is the algorithm of the paper. `greedy_per_space` picks by
benefit per unit of space, the variant for a space limit.
"""

from itertools import combinations
from typing import Dict, Hashable, Iterable, List, Optional, Sequence, Set, Tuple

View = Hashable


class Lattice:
    """Views with sizes, the top view, and for each view the views below it."""

    def __init__(self, sizes: Dict[View, float], edges: Iterable[Tuple[View, View]],
                 top: View, weights: Optional[Dict[View, float]] = None):
        """`edges` holds pairs (v, w) where w can be answered from v directly."""
        self.size = dict(sizes)
        self.top = top
        self.views: List[View] = sorted(self.size, key=repr)
        children: Dict[View, List[View]] = {v: [] for v in self.views}
        for v, w in edges:
            if v not in self.size or w not in self.size:
                raise ValueError("an edge names an unknown view")
            children[v].append(w)
        self.below: Dict[View, Set[View]] = {}
        for v in self.views:
            seen = {v}
            stack = [v]
            while stack:
                for w in children[stack.pop()]:
                    if w not in seen:
                        seen.add(w)
                        stack.append(w)
            self.below[v] = seen
        if self.below[top] != set(self.views):
            raise ValueError("every view must be answerable from the top view")
        self.weight = {v: 1 for v in self.views}
        if weights:
            self.weight.update(weights)

    def costs(self, stored: Iterable[View]) -> Dict[View, float]:
        """C_S(w) for every view w: the smallest stored view that answers w."""
        stored = set(stored) | {self.top}
        cost = {}
        for w in self.views:
            cost[w] = min(self.size[u] for u in stored if w in self.below[u])
        return cost

    def total_cost(self, stored: Iterable[View]) -> float:
        cost = self.costs(stored)
        return sum(self.weight[w] * cost[w] for w in self.views)

    def benefit_of_set(self, stored: Iterable[View]) -> float:
        """The saving of a set over storing the top view alone."""
        return self.total_cost([]) - self.total_cost(stored)


def _benefit(lat: Lattice, cost: Dict[View, float], v: View) -> float:
    s = lat.size[v]
    return sum(lat.weight[w] * (cost[w] - s) for w in lat.below[v] if cost[w] > s)


def greedy_views(lat: Lattice, k: int) -> Tuple[List[View], List[float]]:
    """Pick k views (besides the top view) by largest benefit.

    Returns the views in the order of choice and the benefit of each choice.
    Ties go to the view that comes first in the sorted order of views.
    """
    stored = {lat.top}  # @line L1
    cost = lat.costs(stored)
    picks: List[View] = []
    gains: List[float] = []
    for _ in range(k):  # @line L2
        best, best_b = None, -1.0
        for v in lat.views:
            if v in stored:
                continue
            b = _benefit(lat, cost, v)  # @line L3
            if b > best_b:  # @line L4
                best, best_b = v, b
        if best is None:
            break
        stored.add(best)  # @line L5
        picks.append(best)
        gains.append(best_b)
        s = lat.size[best]
        for w in lat.below[best]:
            if cost[w] > s:
                cost[w] = s
    return picks, gains  # @line L6


def greedy_per_space(lat: Lattice) -> List[Tuple[View, float, float]]:
    """Pick views by largest benefit per unit of space, while some benefit is positive.

    Returns (view, space used so far, benefit so far) after each choice.
    """
    stored = {lat.top}
    cost = lat.costs(stored)
    out = []
    space = 0.0
    total = 0.0
    while True:
        best, best_r = None, 0.0
        for v in lat.views:
            if v in stored:
                continue
            r = _benefit(lat, cost, v) / lat.size[v]
            if r > best_r:
                best, best_r = v, r
        if best is None:
            return out
        b = _benefit(lat, cost, best)
        stored.add(best)
        space += lat.size[best]
        total += b
        out.append((best, space, total))
        for w in lat.below[best]:
            if cost[w] > lat.size[best]:
                cost[w] = lat.size[best]


def best_k_views(lat: Lattice, k: int) -> Tuple[float, Tuple[View, ...]]:
    """The largest benefit of k views, by trying every set of k views."""
    others = [v for v in lat.views if v != lat.top]
    best = (-1.0, ())
    for c in combinations(others, min(k, len(others))):
        b = lat.benefit_of_set(c)
        if b > best[0]:
            best = (b, c)
    return best


def best_within_space(lat: Lattice, space: float) -> float:
    """The largest benefit of a set of views of total size at most `space`, by brute force."""
    others = [v for v in lat.views if v != lat.top]
    best = 0.0
    for m in range(1, len(others) + 1):
        for c in combinations(others, m):
            if sum(lat.size[v] for v in c) <= space:
                best = max(best, lat.benefit_of_set(c))
    return best


def greedy_bound(k: int) -> float:
    """1 - (1 - 1/k)^k, the guarantee of Theorem 4.1 of the paper."""
    return 1 - (1 - 1 / k) ** k


def cube_lattice(dims: Sequence[str], size_of) -> Lattice:
    """The data cube lattice: one view per subset of the dimensions.

    The view on a set A answers the view on every subset of A. `size_of`
    maps a frozenset of dimensions to the size of that view.
    """
    subsets = [frozenset(c) for m in range(len(dims) + 1) for c in combinations(dims, m)]
    sizes = {s: size_of(s) for s in subsets}
    edges = [(a, a - {x}) for a in subsets for x in a]
    return Lattice(sizes, edges, frozenset(dims))
