# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/envy-cycle-elimination/. The authors are listed in prov/0PA93X.jsonl.

from fractions import Fraction
from typing import Callable, FrozenSet, Optional, Sequence

Valuation = Callable[[FrozenSet[int]], object]


def additive(values: Sequence[Sequence]) -> list[Valuation]:
    """Turn a matrix values[i][g] into additive valuation functions."""
    rows = [[Fraction(x) for x in row] for row in values]
    return [lambda s, r=r: sum((r[g] for g in s), Fraction(0)) for r in rows]


def envy_graph(vals: Sequence[Valuation], bundles: Sequence[FrozenSet[int]]) -> list[list[int]]:
    """out[i] lists the agents j whose bundle agent i values strictly more than its own."""
    n = len(bundles)
    own = [vals[i](bundles[i]) for i in range(n)]
    return [[j for j in range(n) if j != i and vals[i](bundles[j]) > own[i]] for i in range(n)]


def find_cycle(out: list[list[int]]) -> list[int]:
    """A cycle of the envy graph when every agent has an incoming edge.

    Walks backward from agent 0 along incoming edges until an agent
    repeats. Returns [c_0, ..., c_(k-1)] where c_(t+1) envies c_t and c_0
    envies c_(k-1).
    """
    n = len(out)
    pred = [-1] * n
    for i in range(n):
        for j in out[i]:
            if pred[j] < 0:
                pred[j] = i
    seen = {}
    walk = []
    x = 0
    while x not in seen:
        seen[x] = len(walk)
        walk.append(x)
        x = pred[x]
    return walk[seen[x]:]


def envy_cycle_elimination(
    vals: Sequence[Valuation], m: int, order: Optional[Sequence[int]] = None, stats: Optional[dict] = None
) -> list[FrozenSet[int]]:
    """Lipton, Markakis, Mossel and Saberi's envy-cycle elimination.

    vals[i] maps a frozenset of goods (from 0..m-1) to the value of agent i.
    Each valuation must be monotone: adding a good never lowers the value.
    The goods are given out in the given order (default 0..m-1). Each good
    goes to an agent that no one envies; when every agent is envied, the
    bundles turn along an envy cycle first. Ties go to the smallest agent
    index. Returns the bundles, which form an EF1 allocation. If stats is a
    dict, stats["rotations"] gets the number of cycle rotations.

    Cost: each good adds at most n - 1 envy edges and each rotation removes
    at least 2, so there are at most m(n-1)/2 rotations in total. Each envy
    graph needs n^2 value queries, so the run uses O(m n^3) value queries
    and O(m n^3) other steps.
    """
    n = len(vals)
    if n == 0:
        raise ValueError("at least one agent is needed")
    goods = list(range(m)) if order is None else list(order)
    if sorted(goods) != list(range(m)):
        raise ValueError("order must be a permutation of the goods")
    bundles = [frozenset() for _ in range(n)]  # @line L1
    rotations = 0
    for g in goods:  # @line L2
        out = envy_graph(vals, bundles)  # @line L3
        while True:
            indeg = [0] * n
            for i in range(n):
                for j in out[i]:
                    indeg[j] += 1
            if min(indeg) == 0:  # @line L4
                break
            cycle = find_cycle(out)  # @line L5
            k = len(cycle)
            old = {c: bundles[c] for c in cycle}
            for t in range(k):  # @line L6
                bundles[cycle[(t + 1) % k]] = old[cycle[t]]
            rotations += 1
            out = envy_graph(vals, bundles)  # @line L7
        i = indeg.index(0)  # @line L8
        bundles[i] = bundles[i] | {g}  # @line L9
    if stats is not None:
        stats["rotations"] = rotations
    return bundles  # @line L10
