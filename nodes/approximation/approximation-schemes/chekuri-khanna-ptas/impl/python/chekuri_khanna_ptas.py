# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chekuri-khanna-ptas/. The authors are listed in prov/K6B73V.jsonl.

"""The guessing step of the Chekuri and Khanna PTAS for multiple knapsack.

The candidate sets are built as in the paper: a guess O of the optimum,
profits rounded down to powers of (1 + delta), one class per profit, and a
bounded tuple (k_1, ..., k_h) that fixes how many of the smallest items of
each class to take. The packing step of the paper (block structure, LP and
GAP rounding) is replaced by an exact search, so this code is meant for
small instances and for checking the bounds, not for large inputs.
"""

from fractions import Fraction
from typing import Iterator, Optional, Union

Number = Union[int, Fraction, float]


def _ceil(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


def _floor_log(x: Fraction, base: Fraction) -> int:
    """Return the largest e >= 0 with base**e <= x, for x >= 1 and base > 1."""
    e, power = 0, base
    while power <= x:
        e, power = e + 1, power * base
    return e


def profit_classes(
    sizes: list[int], profits: list[int], kept: list[int], big_o: Fraction, delta: Fraction
) -> tuple[list[list[int]], list[Fraction]]:
    """Return (classes, a) for one guess O.

    Items with profit below delta * O / n are dropped. Each other profit is
    rounded down to (delta * O / n) * (1 + delta)**e. classes[r] holds the
    items with the r-th exponent, smallest size first, and a[r] is their
    rounded profit.
    """
    n = len(kept)
    unit = delta * big_o / n
    by_exp: dict[int, list[int]] = {}
    for i in kept:
        if profits[i] >= unit:  # @line L4
            e = _floor_log(Fraction(profits[i]) / unit, 1 + delta)  # @line L5
            by_exp.setdefault(e, []).append(i)
    exps = sorted(by_exp)
    classes = [sorted(by_exp[e], key=lambda i: (sizes[i], i)) for e in exps]  # @line L6
    a = [unit * (1 + delta) ** e for e in exps]
    return classes, a


def _count_vectors(
    classes: list[list[int]], a: list[Fraction], g: Fraction, budget: int
) -> Iterator[list[int]]:
    """Yield each distinct vector (c_1, ..., c_h) with c_r = ceil(k_r g / a_r)
    for some k with k_1 + ... + k_h <= budget and c_r <= |S_r|."""
    h = len(classes)

    def k_min(r: int, c: int) -> Optional[int]:
        if c == 0:
            return 0
        k = ((c - 1) * a[r] / g).numerator // ((c - 1) * a[r] / g).denominator + 1
        return k if _ceil(k * g / a[r]) == c else None

    def walk(r: int, left: int, acc: list[int]) -> Iterator[list[int]]:
        if r == h:
            yield list(acc)
            return
        for c in range(len(classes[r]) + 1):
            k = k_min(r, c)
            if k is None:
                continue
            if k > left:
                break
            acc.append(c)
            yield from walk(r + 1, left - k, acc)
            acc.pop()

    yield from walk(0, budget, [])


def candidate_sets(
    sizes: list[int], profits: list[int], capacities: list[int], delta: Number
) -> Iterator[tuple[Fraction, int, int, list[int]]]:
    """Yield (O, h, D, U) for every guess O and every candidate set U.

    U is a sorted list of 0-based item indices. h is the number of profit
    classes and D the bound on k_1 + ... + k_h for this guess, so the number
    of sets U for one O is at most C(D + h, h).
    """
    d = Fraction(delta)
    if not 0 < d <= Fraction(1, 3):
        raise ValueError("delta must be in (0, 1/3]")
    top = max(capacities, default=0)
    kept = [i for i in range(len(sizes)) if sizes[i] <= top]  # @line L1
    if not kept:
        return
    n = len(kept)
    p_max = max(profits[i] for i in kept)
    big_j = 0
    while (1 + d) ** big_j < n:  # @line L2
        big_j += 1
    for j in range(big_j + 1):  # @line L3
        big_o = p_max * (1 + d) ** j
        classes, a = profit_classes(sizes, profits, kept, big_o, d)
        h = len(classes)
        g = d * d * big_o / h  # @line L7
        budget = int((1 + d) * h / (d * d))
        for c in _count_vectors(classes, a, g, budget):  # @line L8
            chosen = [i for r in range(h) for i in classes[r][: c[r]]]  # @line L9
            yield big_o, h, budget, sorted(chosen)


def pack_exact(
    sizes: list[int], capacities: list[int], items: list[int]
) -> Optional[list[list[int]]]:
    """Return a packing of all the given items, one list per knapsack, or
    None if there is none. Exact backtracking search, largest item first."""
    order = sorted(items, key=lambda i: (-sizes[i], i))
    free = list(capacities)
    bins: list[list[int]] = [[] for _ in capacities]

    def place(t: int) -> bool:
        if t == len(order):
            return True
        x = order[t]
        tried = set()
        for b in range(len(free)):
            if free[b] >= sizes[x] and free[b] not in tried:
                tried.add(free[b])
                free[b] -= sizes[x]
                bins[b].append(x)
                if place(t + 1):
                    return True
                bins[b].pop()
                free[b] += sizes[x]
        return False

    if not place(0):
        return None
    return [sorted(b) for b in bins]


def chekuri_khanna_ptas(
    sizes: list[int], profits: list[int], capacities: list[int], eps: Number
) -> list[list[int]]:
    """Return a feasible packing, one sorted list of 0-based item indices
    per knapsack, of profit at least (1 - eps) times the optimum.

    The guessing step runs with delta = eps / 3, which gives the bound
    (1 - 2 delta - delta^2) OPT >= (1 - eps) OPT. Precondition: positive
    integer sizes, profits and capacities, 0 < eps <= 1.
    """
    e = Fraction(eps)
    if not 0 < e <= 1:
        raise ValueError("eps must be in (0, 1]")
    best: list[list[int]] = [[] for _ in capacities]
    best_profit = 0
    seen: set[tuple[int, ...]] = set()
    for _, _, _, chosen in candidate_sets(sizes, profits, capacities, e / 3):
        key = tuple(chosen)
        value = sum(profits[i] for i in chosen)
        if key in seen or value <= best_profit:
            continue
        seen.add(key)
        packing = pack_exact(sizes, capacities, chosen)  # @line L10
        if packing is not None:
            best, best_profit = packing, value
    return best  # @line L11
