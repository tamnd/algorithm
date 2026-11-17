# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-reaction-method/. The authors are listed in prov/KRZQSZ.jsonl.
"""The next reaction method of Gibson and Bruck (2000).

A network with n species and m reactions is given by:
- stoich: the m change vectors (stoich[j][i] = S[i][j]);
- rate(j, x): the propensity a_j(x) of reaction j in state x;
- depends: depends[j] is the set of species indices that a_j reads.

Each reaction j has an absolute putative firing time tau[j] in an indexed
priority queue. After reaction mu fires, only the reactions in G[mu] (the
dependency graph) get a new propensity and a new time. The fired reaction
draws a new Exp(1) number; every other reaction reuses its clock: the
unused part of its unit-rate exponential, r = a_old (tau - t), gives
tau = t + r / a_new. When a propensity drops to 0, r is kept and the time
is infinite until the propensity is positive again.

Draw order: m numbers rng.expovariate(1.0) at the start, for j = 0, ...,
m - 1, then one rng.expovariate(1.0) for each event, for the fired reaction.
"""

from __future__ import annotations

import math
from typing import Callable, List, Sequence, Set, Tuple

State = Tuple[int, ...]


class IndexedMinHeap:
    """A binary min-heap of the keys key[0..m-1] with a position map, so
    that the key of any index can change in O(log m) time."""

    def __init__(self, keys: Sequence[float]):
        self.key = list(keys)
        self.heap = list(range(len(self.key)))
        self.pos = list(range(len(self.key)))
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._down(i)

    def top(self) -> Tuple[float, int]:
        j = self.heap[0]
        return self.key[j], j

    def update(self, j: int, k: float) -> None:
        old = self.key[j]
        self.key[j] = k
        if k < old:
            self._up(self.pos[j])
        elif k > old:
            self._down(self.pos[j])

    def _swap(self, p: int, q: int) -> None:
        h = self.heap
        h[p], h[q] = h[q], h[p]
        self.pos[h[p]] = p
        self.pos[h[q]] = q

    def _up(self, p: int) -> None:
        while p > 0:
            parent = (p - 1) // 2
            if self.key[self.heap[p]] < self.key[self.heap[parent]]:
                self._swap(p, parent)
                p = parent
            else:
                return

    def _down(self, p: int) -> None:
        n = len(self.heap)
        while True:
            c = 2 * p + 1
            if c >= n:
                return
            if c + 1 < n and self.key[self.heap[c + 1]] < self.key[self.heap[c]]:
                c += 1
            if self.key[self.heap[c]] < self.key[self.heap[p]]:
                self._swap(p, c)
                p = c
            else:
                return


def dependency_graph(stoich: Sequence[Sequence[int]], depends: Sequence[Set[int]]) -> List[List[int]]:
    """G[j] lists the reactions whose propensity can change when j fires:
    every k with a species in depends[k] that j changes, and j itself."""
    m = len(stoich)
    graph = []
    for j in range(m):
        changed = {i for i, d in enumerate(stoich[j]) if d != 0}
        out = [k for k in range(m) if k == j or changed & set(depends[k])]
        graph.append(out)
    return graph


def mass_action_rates(reactants: Sequence[Sequence[int]], rates: Sequence[float]):
    """Return (rate, depends) for stochastic mass action. reactants[j][i] is
    the number of molecules of species i that reaction j uses (0, 1 or 2);
    2X has propensity c x (x - 1) / 2."""
    def rate(j: int, x: State) -> float:
        a = rates[j]
        for i, k in enumerate(reactants[j]):
            if k == 1:
                a *= x[i]
            elif k == 2:
                a *= x[i] * (x[i] - 1) / 2.0
            elif k != 0:
                raise ValueError("only orders 0, 1 and 2 per species")
        return float(a)
    depends = [{i for i, k in enumerate(row) if k} for row in reactants]
    return rate, depends


def next_reaction_method(rng, x0: Sequence[int], stoich: Sequence[Sequence[int]],
                         rate: Callable[[int, State], float], depends: Sequence[Set[int]],
                         t_end: float, max_events: int = 10 ** 6):
    """Simulate one trajectory from x0 at time 0 up to time t_end.

    Returns (times, states, complete) as the direct method does.
    """
    m = len(stoich)
    t = 0.0  # @line L1
    x = tuple(int(v) for v in x0)
    graph = dependency_graph(stoich, depends)
    a = [0.0] * m
    clock = [0.0] * m  # the unused unit-rate time of a reaction with a = 0
    tau = [math.inf] * m
    for j in range(m):  # @line L2
        a[j] = rate(j, x)
        r = rng.expovariate(1.0)
        if a[j] > 0:
            tau[j] = t + r / a[j]
        else:
            clock[j] = r
    queue = IndexedMinHeap(tau)  # @line L3
    times = [t]
    states = [x]
    for _ in range(max_events):  # @line L4
        t_mu, mu = queue.top()  # @line L5
        if t_mu == math.inf or t_mu > t_end:  # @line L6
            return times, states, True
        t = t_mu  # @line L7
        nu = stoich[mu]
        x = tuple(x[i] + nu[i] for i in range(len(x)))
        times.append(t)
        states.append(x)
        for k in graph[mu]:  # @line L8
            a_new = rate(k, x)  # @line L9
            if a_new < 0:
                raise ValueError("propensities must be >= 0")
            if k == mu:  # @line L10
                r = rng.expovariate(1.0)
            elif a_new == a[k]:
                continue
            elif a[k] > 0:  # @line L11
                r = a[k] * (tau[k] - t)
            else:
                r = clock[k]
            a[k] = a_new
            if a_new > 0:
                tau[k] = t + r / a_new
            else:
                clock[k] = r
                tau[k] = math.inf
            queue.update(k, tau[k])  # @line L12
    return times, states, False
