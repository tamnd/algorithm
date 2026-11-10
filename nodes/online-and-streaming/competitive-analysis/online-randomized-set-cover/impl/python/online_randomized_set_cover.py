# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-randomized-set-cover/. The authors are listed in prov/68PE88.jsonl.

import math
import random
from collections.abc import Hashable, Mapping


def fractional_step(x: dict, members: list, costs: Mapping, d: int, iters: int = 100) -> float:
    """Raise y_j until the members' x sum to 1, with dx_i/dy = (x_i + 1/d)/c_i.

    The rate of x_i depends only on x_i, so after a raise of size t,
    x_i(t) = (x_i + 1/d) * exp(t / c_i) - 1/d. The sum is increasing in t,
    and t is found by bisection. Returns t, the increase of y_j.
    """
    def total(t: float) -> float:
        return sum((x[i] + 1 / d) * math.exp(t / costs[i]) - 1 / d for i in members)

    if total(0.0) >= 1:
        return 0.0
    lo, hi = 0.0, 1.0
    while total(hi) < 1:
        hi *= 2
    for _ in range(iters):
        mid = (lo + hi) / 2
        if total(mid) < 1:
            lo = mid
        else:
            hi = mid
    for i in members:
        x[i] = (x[i] + 1 / d) * math.exp(hi / costs[i]) - 1 / d
    return hi


class OnlineRandomizedSetCover:
    """Online set cover by a fractional primal-dual step and threshold rounding.

    `sets` maps each set name to its elements and `costs` to its cost; the set
    system is known in advance, the elements that must be covered arrive one
    at a time. Each set draws k = ceil(2 ln n) uniform values once, and its
    threshold is their minimum; a set is taken when its fractional value
    reaches the threshold. An element left uncovered gets its cheapest set.
    """

    def __init__(self, sets: Mapping[Hashable, frozenset], costs: Mapping[Hashable, float], rng: random.Random) -> None:
        self.sets = {s: frozenset(e) for s, e in sets.items()}
        self.costs = dict(costs)
        self.ground = frozenset().union(*self.sets.values()) if self.sets else frozenset()
        n = max(1, len(self.ground))
        self.k = max(1, math.ceil(2 * math.log(n)))
        self.containing: dict = {}
        for s, elems in self.sets.items():
            for e in elems:
                self.containing.setdefault(e, []).append(s)
        self.d = max((len(v) for v in self.containing.values()), default=1)
        self.x = {s: 0.0 for s in self.sets}  # @line L1
        self.theta = {s: min(rng.random() for _ in range(self.k)) for s in self.sets}  # @line L2
        self.chosen: set = set()
        self.y: dict = {}
        self.history: list[tuple[Hashable, dict]] = []
        self.fallbacks = 0

    def arrive(self, e: Hashable) -> set:  # @line L3
        """Cover element e; return the sets added for it."""
        members = self.containing.get(e)  # @line L4
        if not members:
            raise ValueError(f"no set contains {e!r}")
        self.y[e] = self.y.get(e, 0.0) + fractional_step(self.x, members, self.costs, self.d)  # @line L5
        self.history.append((e, {s: self.x[s] for s in members}))
        added = set()
        for s in members:
            if s not in self.chosen and self.x[s] >= self.theta[s]:  # @line L6
                added.add(s)
        self.chosen |= added
        if not any(s in self.chosen for s in members):  # @line L7
            s = min(members, key=lambda t: (self.costs[t], str(t)))  # @line L8
            added.add(s)
            self.chosen.add(s)
            self.fallbacks += 1
        return added

    def cost(self) -> float:
        return sum(self.costs[s] for s in self.chosen)  # @line L9

    def fractional_cost(self) -> float:
        return sum(self.costs[s] * self.x[s] for s in self.sets)

    def dual_value(self) -> float:
        return sum(self.y.values())


def expected_threshold_cost(x: Mapping, costs: Mapping, k: int) -> float:
    """Exact expected cost of the sets taken by thresholds, given the final x."""
    return sum(costs[s] * (1 - (1 - min(1.0, v)) ** k) for s, v in x.items())


def uncovered_probability(snapshot: Mapping, k: int) -> float:
    """Probability that thresholds leave an element uncovered, given its sets' x at arrival."""
    p = 1.0
    for v in snapshot.values():
        p *= (1 - min(1.0, v)) ** k
    return p
