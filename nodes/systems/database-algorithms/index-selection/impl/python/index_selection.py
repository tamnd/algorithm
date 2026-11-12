# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/index-selection/. The authors are listed in prov/BFQ09A.jsonl.

"""Index selection under a space budget: greedy by benefit per space, and exact search.

A workload has queries q with a weight w_q and a cost base_q without any index.
A candidate index i has a size s_i, a maintenance cost m_i (the extra cost of
the workload's updates when i exists), and a cost cost(q, i) for each query
that can use it. A query uses the best one index of the configuration, or none:

    Cost(q, S) = min(base_q, min over i in S of cost(q, i))
    Total(S)   = sum over q of w_q * Cost(q, S) + sum over i in S of m_i

The problem is to choose S with sum of s_i at most the budget that minimizes
Total(S). This is the model of single-index atomic configurations of
Chaudhuri and Narasayya (1997), with the optimizer's estimates given as a table.
"""

from fractions import Fraction
from itertools import combinations
from typing import Dict, FrozenSet, List, Sequence, Tuple


class Workload:
    def __init__(self, queries: Sequence[Tuple[int, int]],
                 indexes: Sequence[Tuple[str, int, int]],
                 cost: Dict[Tuple[int, str], int]) -> None:
        """queries: (weight, base cost); indexes: (name, size, maintenance);
        cost: (query number, index name) -> cost of the query with that index."""
        self.queries = list(queries)
        self.names = [name for name, _, _ in indexes]
        self.size = {name: s for name, s, _ in indexes}
        self.maint = {name: m for name, _, m in indexes}
        self.cost = dict(cost)
        if any(s <= 0 for s in self.size.values()):
            raise ValueError("sizes must be positive")

    def query_cost(self, q: int, config: FrozenSet[str]) -> int:
        best = self.queries[q][1]
        for i in config:
            c = self.cost.get((q, i))
            if c is not None and c < best:
                best = c
        return best

    def total(self, config) -> int:
        config = frozenset(config)
        return (sum(w * self.query_cost(q, config) for q, (w, _) in enumerate(self.queries))
                + sum(self.maint[i] for i in config))

    def benefit(self, config) -> int:
        """Total cost saved against no index at all (maintenance included)."""
        return self.total(frozenset()) - self.total(config)

    def used(self, config) -> int:
        return sum(self.size[i] for i in config)


def greedy(wl: Workload, budget: int) -> Tuple[FrozenSet[str], List[str]]:
    """Add the index with the largest marginal benefit per unit of space that
    fits, while some index fits and has a positive marginal benefit."""
    chosen: FrozenSet[str] = frozenset()                                  # @line L1
    order: List[str] = []
    current = wl.total(chosen)
    while True:                                                           # @line L2
        best, best_ratio = None, None
        for i in wl.names:                                                # @line L3
            if i in chosen or wl.used(chosen) + wl.size[i] > budget:      # @line L4
                continue                                                  # @line L4
            gain = current - wl.total(chosen | {i})                       # @line L5
            ratio = Fraction(gain, wl.size[i])                            # @line L5
            if gain > 0 and (best_ratio is None or ratio > best_ratio):   # @line L6
                best, best_ratio = i, ratio                               # @line L6
        if best is None:                                                  # @line L7
            return chosen, order                                          # @line L7
        chosen = chosen | {best}                                          # @line L8
        order.append(best)
        current = wl.total(chosen)


def best_of_greedy_and_single(wl: Workload, budget: int) -> FrozenSet[str]:
    """The better of greedy and the best single index that fits."""
    g, _ = greedy(wl, budget)
    best = g
    for i in wl.names:
        if wl.size[i] <= budget and wl.total({i}) < wl.total(best):
            best = frozenset({i})
    return best


def brute_force(wl: Workload, budget: int) -> FrozenSet[str]:
    """An optimal configuration, by trying every subset that fits.
    Ties go to fewer indexes, then to the first subset in name order."""
    best: FrozenSet[str] = frozenset()
    best_total = wl.total(best)
    for r in range(1, len(wl.names) + 1):
        for subset in combinations(wl.names, r):
            if wl.used(subset) <= budget:
                t = wl.total(subset)
                if t < best_total:
                    best, best_total = frozenset(subset), t
    return best


def from_knapsack(values: Sequence[int], sizes: Sequence[int]) -> Workload:
    """Item j becomes index Ij that serves only query j, saving values[j]."""
    queries = [(1, v) for v in values]
    indexes = [(f"I{j}", s, 0) for j, s in enumerate(sizes)]
    cost = {(j, f"I{j}"): 0 for j in range(len(values))}
    return Workload(queries, indexes, cost)


def from_max_coverage(n: int, sets: Sequence[Sequence[int]]) -> Workload:
    """Element e becomes a query of base cost 1; set j becomes an index of size 1
    that answers the queries of its elements at cost 0."""
    queries = [(1, 1)] * n
    indexes = [(f"S{j}", 1, 0) for j in range(len(sets))]
    cost = {(e, f"S{j}"): 0 for j, s in enumerate(sets) for e in s}
    return Workload(queries, indexes, cost)
