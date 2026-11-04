# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aks-sorting-network/. The authors are listed in prov/9EWBX0.jsonl.

"""Seiferas's version of the AKS sorting network.

The network keeps its registers in bags, one bag for each node of a complete
binary tree, and repeats one stage: separate the items of each bag, send a
few items from each end back to the parent, and send the two halves of the
rest down to the children. The capacities shrink with time, and at the end
every item lies in a small subtree to which it is native.

The separator is pluggable. The default is an exact separator (a Batcher
odd-even merge network on the bag), which is correct for every n but not of
constant depth. The functions expander_halver and halver_error build and
measure the constant-depth epsilon-halvers that the O(log n) depth needs.
"""

import random
from fractions import Fraction
from functools import lru_cache
from itertools import product
from typing import Callable, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

# Seiferas's parameters (A = 10, lambda = 1/100, nu = 13/20); with an exact
# separator (epsilon = 0) they satisfy all of his constraints.
A = Fraction(10)
LAM = Fraction(1, 100)
NU = Fraction(13, 20)

Comparator = tuple[int, int]  # (i, j): the minimum goes to register i
Separator = Callable[[list[int]], list[Comparator]]


def _oem(m: int) -> list[tuple[int, int]]:
    """Comparators (p, q), p < q, of odd-even merge sort on positions 0 .. m - 1."""
    size = 1
    while size < m:
        size *= 2
    net: list[tuple[int, int]] = []

    def merge(lo: int, w: int, r: int) -> None:
        s = 2 * r
        if s < w:
            merge(lo, w, s)
            merge(lo + r, w, s)
            net.extend((i, i + r) for i in range(lo + r, lo + w - r, s))
        else:
            net.append((lo, lo + r))

    def sort(lo: int, w: int) -> None:
        if w > 1:
            sort(lo, w // 2)
            sort(lo + w // 2, w // 2)
            merge(lo, w, 1)

    sort(0, size)
    return [(p, q) for p, q in net if q < m]


def exact_separator(regs: list[int]) -> list[Comparator]:
    """Sort the registers regs, in this order, with an odd-even merge network."""
    return [(regs[p], regs[q]) for p, q in _oem(len(regs))]


def aks_network(n: int, separate: Separator = exact_separator) -> tuple[list[Comparator], list[int]]:
    """Return (comparators, order) of the network for n = 2^k >= 2 registers.

    After the comparators run, out[r] = register order[r] holds the item of
    rank r.
    """
    levels = n.bit_length() - 1  # lg n
    leaf = levels - 1  # depth of the bags of pairs
    net: list[Comparator] = []
    bags: dict[tuple[int, int], list[int]] = {(0, 0): list(range(n))}  # @line L1
    t = 0
    while n * NU**t * A**leaf >= 1 / LAM:  # @line L2
        new: dict[tuple[int, int], list[int]] = {}
        for (d, i), regs in bags.items():  # @line L3
            if not regs:
                continue
            b = n * NU**t * A**d  # @line L4
            net.extend(separate(regs))  # @line L5
            rest = regs
            if d > 0:
                k = int(LAM * b)  # @line L6
                if 2 * k >= len(regs):
                    up, rest = regs, []
                else:
                    up, rest = regs[:k] + regs[len(regs) - k :], regs[k : len(regs) - k]
                if len(rest) % 2 == 1:  # @line L7
                    mid = len(rest) // 2
                    up, rest = up + [rest[mid]], rest[:mid] + rest[mid + 1 :]
                new.setdefault((d - 1, i // 2), []).extend(up)
            if rest:
                if d == leaf:
                    raise AssertionError("a leaf bag must evacuate items downward")
                h = len(rest) // 2  # @line L8
                new.setdefault((d + 1, 2 * i), []).extend(rest[:h])
                new.setdefault((d + 1, 2 * i + 1), []).extend(rest[h:])
        bags = new
        t += 1  # @line L9
    k = 0
    while (1 / LAM) * (1 / A) ** (k + 1) >= 1:
        k += 1
    top = max(leaf - k, 0)
    width = n >> top
    order = [0] * n
    for i in range(1 << top):  # @line L10
        regs = [r for (d, j), rs in bags.items() if d >= top and j >> (d - top) == i for r in rs]
        if any(rs for (d, _), rs in bags.items() if d < top):
            raise AssertionError("a bag above the final subtrees is not empty")
        if len(regs) != width:
            raise AssertionError("a final subtree holds the wrong number of items")
        net.extend(exact_separator(regs))
        order[i * width : (i + 1) * width] = regs
    return net, order


@lru_cache(maxsize=None)
def _cached_network(n: int) -> tuple[tuple[Comparator, ...], tuple[int, ...]]:
    net, order = aks_network(n)
    return tuple(net), tuple(order)


def stages(n: int) -> int:
    """Return the number of separation stages of the network for n = 2^k registers."""
    leaf = n.bit_length() - 2
    t = 0
    while n * NU**t * A**leaf >= 1 / LAM:
        t += 1
    return t


def aks_sorting_network(a: list[T]) -> None:
    """Sort a in place, in non-decreasing order, with the bag network of Seiferas.

    The length is padded to a power of 2 (at least 2) with a top element that
    is larger than every item.
    """
    n = len(a)
    if n < 2:
        return
    size = 2
    while size < n:
        size *= 2
    top = object()
    x: list[object] = list(a) + [top] * (size - n)

    def less(u: object, v: object) -> bool:
        if v is top:
            return u is not top
        if u is top:
            return False
        return u < v  # type: ignore[operator]

    net, order = _cached_network(size)
    for i, j in net:
        if less(x[j], x[i]):  # @line L11
            x[i], x[j] = x[j], x[i]
    a[:] = [x[r] for r in order[:n]]  # type: ignore[misc]


def expander_halver(m: int, d: int, seed: int) -> list[list[Comparator]]:
    """Return d layers; layer s compares wire u with wire m + p_s(u) for a random permutation p_s.

    The union of the d perfect matchings is a d-regular bipartite graph
    between the halves 0 .. m - 1 and m .. 2m - 1, and each comparator puts
    the minimum on the first half.
    """
    rng = random.Random(seed)
    layers = []
    for _ in range(d):
        p = list(range(m))
        rng.shuffle(p)
        layers.append([(u, m + p[u]) for u in range(m)])
    return layers


def halver_error(layers: list[list[Comparator]], m: int) -> Fraction:
    """Return the smallest epsilon for which the layers form an epsilon-halver on 2m wires.

    By the zero-one principle it is enough to try all 0-1 inputs: for z <= m
    zeros, count the zeros that end in the second half, and for z >= m, the
    ones that end in the first half.
    """
    worst = Fraction(0)
    for bits in product((0, 1), repeat=2 * m):
        x = list(bits)
        for layer in layers:
            for i, j in layer:
                if x[i] > x[j]:
                    x[i], x[j] = x[j], x[i]
        zeros = x.count(0)
        if 0 < zeros <= m:
            worst = max(worst, Fraction(x[m:].count(0), zeros))
        ones = 2 * m - zeros
        if 0 < ones <= m:
            worst = max(worst, Fraction(x[:m].count(1), ones))
    return worst
