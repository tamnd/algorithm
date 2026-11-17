# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/view-selection/. The authors are listed in prov/QEVP9Z.jsonl.
"""View selection in the lattice model of Harinarayan, Rajaraman and Ullman
(1996), with their greedy algorithm.

A lattice has views 0..m-1, a size |v| for each, a query frequency f(v),
and a relation "w can be answered from v" (v is an ancestor of w, and every
view is its own ancestor). One view, the top, can answer every view and is
always materialized. With the set S of materialized views, a query on w costs
C_S(w) = min{|v| : v in S, v is an ancestor of w} (the linear cost model).
The benefit of S is the drop in the total cost sum_w f(w) C_S(w) against
S = {top}. The greedy algorithm adds, k times, the view with the largest
benefit given the views chosen so far. Its benefit is at least
1 - (1 - 1/k)^k > 1 - 1/e of the best benefit of k views.
All arithmetic is exact (Fraction).
"""

from fractions import Fraction
from itertools import combinations
from typing import Dict, FrozenSet, Iterable, List, Sequence, Tuple


class Lattice:
    def __init__(self, size: Sequence, anc: Sequence[FrozenSet[int]], top: int,
                 freq: Sequence = ()) -> None:
        """anc[w] is the set of views from which w can be answered (w included)."""
        self.m = len(size)
        self.size = [Fraction(s) for s in size]
        self.anc = [frozenset(a) | {w} for w, a in enumerate(anc)]
        self.top = top
        self.freq = [Fraction(f) for f in freq] if freq else [Fraction(1)] * self.m
        assert all(top in a for a in self.anc)

    def cost(self, S: Iterable[int], w: int) -> Fraction:
        chosen = set(S) | {self.top}
        return min(self.size[v] for v in self.anc[w] if v in chosen)

    def total_cost(self, S: Iterable[int]) -> Fraction:
        S = list(S)
        return sum((self.freq[w] * self.cost(S, w) for w in range(self.m)), Fraction(0))

    def benefit(self, S: Iterable[int]) -> Fraction:
        return self.total_cost([]) - self.total_cost(S)


def cube(dims: Sequence[str], size: Dict[FrozenSet[str], int]) -> Tuple[Lattice, List[FrozenSet[str]]]:
    """The data cube lattice: one view per subset of the dimensions (its
    GROUP BY attributes); w can be answered from v when w's attributes are a
    subset of v's. The top view groups by all dimensions."""
    views = [frozenset(c) for r in range(len(dims), -1, -1) for c in combinations(dims, r)]
    anc = [frozenset(i for i, v in enumerate(views) if w <= v) for w in views]
    return Lattice([size[v] for v in views], anc, 0), views


def greedy(lat: Lattice, k: int) -> Tuple[List[int], List[Fraction]]:
    """Return the k chosen views in order, and the benefit of each choice."""
    S: List[int] = []  # @line L1
    gains: List[Fraction] = []
    cur = [lat.cost([], w) for w in range(lat.m)]  # C_S(w) for the current S
    for _ in range(k):  # @line L2
        best, best_gain = None, None
        for v in range(lat.m):  # @line L3
            if v == lat.top or v in S:
                continue
            gain = sum((lat.freq[w] * max(Fraction(0), cur[w] - lat.size[v])  # @line L4
                        for w in range(lat.m) if v in lat.anc[w]), Fraction(0))
            if best is None or gain > best_gain:  # @line L5
                best, best_gain = v, gain
        if best is None:
            break
        S.append(best)  # @line L6
        gains.append(best_gain)
        for w in range(lat.m):
            if best in lat.anc[w]:
                cur[w] = min(cur[w], lat.size[best])
    return S, gains  # @line L7


def optimal(lat: Lattice, k: int) -> Tuple[Fraction, Tuple[int, ...]]:
    """The largest benefit of at most k views, by trying all sets."""
    cand = [v for v in range(lat.m) if v != lat.top]
    best: Tuple[Fraction, Tuple[int, ...]] = (Fraction(0), ())
    for S in combinations(cand, min(k, len(cand))):
        b = lat.benefit(S)
        if b > best[0]:
            best = (b, S)
    return best


def greedy_ratio_bound(k: int) -> Fraction:
    """1 - (1 - 1/k)^k, the guarantee of the greedy algorithm for k views."""
    return 1 - (1 - Fraction(1, k)) ** k
