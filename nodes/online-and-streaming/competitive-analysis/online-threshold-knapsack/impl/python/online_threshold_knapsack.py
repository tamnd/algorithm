# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-threshold-knapsack/. The authors are listed in prov/RRVVVX.jsonl.

import math


def psi(z: float, L: float, U: float) -> float:
    """Threshold on value density when a fraction z of the capacity is used.

    Psi(z) = L for z <= c and (U e / L)^z * (L / e) for z >= c, where
    c = 1 / (1 + ln(U / L)). It rises from L at z = c to U at z = 1.
    """
    c = 1 / (1 + math.log(U / L))
    if z <= c:
        return L
    return (U * math.e / L) ** z * (L / math.e)


class OnlineThresholdKnapsack:
    """Online knapsack with capacity 1, value densities in [L, U] and small items.

    Each item is (weight, value) with weight in (0, 1]. The item is taken if
    its density value/weight is at least psi(z) for the current used
    fraction z, and if it fits.
    """

    def __init__(self, L: float, U: float) -> None:
        if not 0 < L <= U:
            raise ValueError("need 0 < L <= U")
        self.L, self.U = L, U
        self.c = 1 / (1 + math.log(U / L))  # @line L1
        self.z = 0.0
        self.value = 0.0
        self.taken: list[int] = []
        self.t = 0

    def arrive(self, weight: float, value: float) -> bool:  # @line L2
        """Decide on the next item for good; return True if it is taken."""
        i = self.t
        self.t += 1
        threshold = psi(self.z, self.L, self.U)  # @line L3
        # a relative slack of 1e-12 keeps densities equal to L from being lost to rounding
        if value >= threshold * weight * (1 - 1e-12) and self.z + weight <= 1 + 1e-12:  # @line L4
            self.taken.append(i)  # @line L5
            self.z += weight
            self.value += value
            return True
        return False

    def result(self) -> list[int]:
        return self.taken  # @line L6


def threshold_knapsack(items: list[tuple[float, float]], L: float, U: float) -> list[int]:
    """Run the algorithm on a list of (weight, value) items and return the taken indices."""
    alg = OnlineThresholdKnapsack(L, U)
    for w, v in items:
        alg.arrive(w, v)
    return alg.result()


def fractional_opt(items: list[tuple[float, float]]) -> float:
    """Optimum of the fractional knapsack with capacity 1, an upper bound on OPT."""
    room, total = 1.0, 0.0
    for w, v in sorted(items, key=lambda it: it[1] / it[0], reverse=True):
        take = min(w, room)
        total += v * take / w
        room -= take
        if room <= 0:
            break
    return total


def guarantee(L: float, U: float, eps: float) -> float:
    """Bound on OPT / ALG for items of weight at most eps.

    For U > L and eps <= 1 - c it is (1 + ln(U/L)) * (U e / L)^(2 eps). For U = L the
    algorithm takes each item that fits, and the bound is 1 / (1 - eps).
    """
    if U == L:
        return 1 / (1 - eps)
    c = 1 / (1 + math.log(U / L))
    if eps > 1 - c:
        raise ValueError("the bound needs eps <= 1 - c")
    return (1 + math.log(U / L)) * (U * math.e / L) ** (2 * eps)
