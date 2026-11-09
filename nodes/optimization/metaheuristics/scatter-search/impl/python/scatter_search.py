# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scatter-search/. The authors are listed in prov/GRJBJP.jsonl.

import random
from dataclasses import dataclass
from fractions import Fraction

Bits = tuple[int, ...]


@dataclass(frozen=True)
class Knapsack:
    """A 0-1 knapsack instance: maximize the value of the packed items within the capacity."""

    values: list[int]
    weights: list[int]
    capacity: int

    def value(self, x: Bits) -> int:
        return sum(v for v, b in zip(self.values, x) if b)

    def weight(self, x: Bits) -> int:
        return sum(w for w, b in zip(self.weights, x) if b)

    def ratio_order(self) -> list[int]:
        """Items by value per unit weight, best first, ties to the lowest index."""
        return sorted(range(len(self.values)), key=lambda i: (-Fraction(self.values[i], self.weights[i]), i))

    def rank(self, x: Bits) -> tuple[int, Bits]:
        """The order used to sort solutions: higher value first, then the smaller bit string."""
        return (-self.value(x), x)


def repair(k: Knapsack, x: Bits) -> Bits:
    """Remove packed items, worst ratio first, until the weight is within the capacity."""
    y = list(x)
    load = k.weight(x)
    for i in reversed(k.ratio_order()):
        if load <= k.capacity:
            break
        if y[i]:
            y[i] = 0
            load -= k.weights[i]
    return tuple(y)


def improve(k: Knapsack, x: Bits) -> Bits:
    """Add items, best ratio first, whenever they fit. Needs a feasible x; the result is maximal."""
    y = list(x)
    load = k.weight(x)
    for i in k.ratio_order():
        if not y[i] and load + k.weights[i] <= k.capacity:
            y[i] = 1
            load += k.weights[i]
    return tuple(y)


def hamming(x: Bits, y: Bits) -> int:
    return sum(a != b for a, b in zip(x, y))


def scatter_search(
    k: Knapsack, pool_size: int, b1: int, b2: int, rng: random.Random
) -> tuple[Bits, int, list[list[Bits]]]:
    """Scatter search for 0-1 knapsack (Glover; Laguna and Martí).

    Builds pool_size random solutions, repairs and improves them, and forms a
    reference set of the b1 best plus b2 most diverse ones. Each round combines
    every pair with a new member by rounding the midpoint up (union) and down
    (intersection), repairs and improves the children, and lets a child replace
    the worst member when it is better and not already present. Stops when the
    reference set does not change. Returns (best, value, the reference sets of
    all rounds, the first one included).
    """
    if pool_size < 1 or b1 < 1 or b2 < 0:
        raise ValueError("need pool_size >= 1, b1 >= 1 and b2 >= 0")
    n = len(k.values)
    pool: list[Bits] = []
    for _ in range(pool_size):  # @line L1
        z = improve(k, repair(k, tuple(rng.randint(0, 1) for _ in range(n))))
        if z not in pool:
            pool.append(z)
    pool.sort(key=k.rank)
    ref = pool[:b1]  # @line L2
    rest = pool[b1:]
    while rest and len(ref) < b1 + b2:
        far = max(rest, key=lambda z: (min(hamming(z, r) for r in ref), -rest.index(z)))
        ref.append(far)
        rest.remove(far)
    history = [list(ref)]
    new = set(ref)
    while True:  # @line L3
        children: list[Bits] = []  # @line L4
        for i in range(len(ref)):  # @line L5
            for j in range(i + 1, len(ref)):
                x, y = ref[i], ref[j]
                if x not in new and y not in new:
                    continue
                up = tuple(a | b for a, b in zip(x, y))  # @line L6
                down = tuple(a & b for a, b in zip(x, y))
                for z in (up, down):
                    children.append(improve(k, repair(k, z)))  # @line L7
        new = set()
        for z in sorted(set(children), key=k.rank):  # @line L8
            worst = max(ref, key=k.rank)
            if z not in ref and k.value(z) > k.value(worst):  # @line L9
                ref[ref.index(worst)] = z
                new.add(z)
        if not new:  # @line L10
            break
        history.append(list(ref))
    best = min(ref, key=k.rank)
    return best, k.value(best), history  # @line L11
