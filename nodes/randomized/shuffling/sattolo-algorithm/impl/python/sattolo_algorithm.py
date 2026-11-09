# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sattolo-algorithm/. The authors are listed in prov/6WKJFK.jsonl.

import random
from typing import TypeVar

T = TypeVar("T")


def sattolo_shuffle(a: list[T], rng: random.Random) -> list[T]:
    """Rearrange a in place by a uniformly random cyclic permutation; return a.

    After the call, a[p] holds the item that was at position sigma(p), where
    sigma is uniform on the (n - 1)! permutations with one cycle of length n.
    With a = [0, 1, ..., n - 1] the result, read as p -> a[p], is that cycle.
    It makes n - 1 calls to rng.randrange: Theta(n) time, O(1) extra space.
    """
    for i in range(len(a) - 1, 0, -1):  # @line L1
        j = rng.randrange(i)  # @line L2
        a[i], a[j] = a[j], a[i]  # @line L3
    return a


def is_single_cycle(p: list[int]) -> bool:
    """Return True if the permutation p (as the map i -> p[i]) is one n-cycle."""
    n = len(p)
    if n == 0:
        return False
    seen, x, steps = set(), 0, 0
    while x not in seen:
        seen.add(x)
        x = p[x]
        steps += 1
    return x == 0 and steps == n


def cycle_from_order(order: list[int]) -> list[int]:
    """Turn an order (x0, ..., x_{n-1}) into the cycle x0 -> x1 -> ... -> x0.

    If the order is uniform, the cycle is uniform, since each n-cycle comes
    from exactly n orders (its n rotations).
    """
    n = len(order)
    p = [0] * n
    for k in range(n):
        p[order[k]] = order[(k + 1) % n]
    return p
