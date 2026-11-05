# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dinkelbach-algorithm/. The authors are listed in prov/VSSWCG.jsonl.

from fractions import Fraction
from typing import Callable, Hashable, List, Tuple, TypeVar

X = TypeVar("X", bound=Hashable)


def dinkelbach(
    min_param: Callable[[Fraction], X],
    num: Callable[[X], int],
    den: Callable[[X], int],
    x0: X,
) -> Tuple[X, Fraction]:
    """Return (x, ratio) with x minimizing num(x) / den(x) over a finite set.

    min_param(lam) must return a solution that minimizes num - lam * den
    over the set, and den must be positive on the set. The arithmetic is exact,
    with fractions, so the stopping test F(lam) >= 0 is exact.
    """
    x = x0  # @line L1
    while True:  # @line L2
        lam = Fraction(num(x), den(x))  # @line L3
        y = min_param(lam)  # @line L4
        if num(y) - lam * den(y) >= 0:  # @line L5
            return x, lam
        x = y  # @line L6


def dinkelbach_trace(
    min_param: Callable[[Fraction], X],
    num: Callable[[X], int],
    den: Callable[[X], int],
    x0: X,
) -> List[Tuple[X, Fraction, Fraction]]:
    """Run the same iteration and return the list of (x_k, lambda_k, F(lambda_k))."""
    out = []
    x = x0
    while True:
        lam = Fraction(num(x), den(x))
        y = min_param(lam)
        f = num(y) - lam * den(y)
        out.append((x, lam, f))
        if f >= 0:
            return out
        x = y


def best_ratio_subset(items: List[Tuple[int, int]], k: int) -> Tuple[Tuple[int, ...], Fraction]:
    """Choose k items (c, t), t > 0, minimizing sum(c) / sum(t), by Dinkelbach's algorithm."""
    if not 1 <= k <= len(items):
        raise ValueError("need 1 <= k <= len(items)")

    def num(s: Tuple[int, ...]) -> int:
        return sum(items[i][0] for i in s)

    def den(s: Tuple[int, ...]) -> int:
        return sum(items[i][1] for i in s)

    def min_param(lam: Fraction) -> Tuple[int, ...]:
        order = sorted(range(len(items)), key=lambda i: (items[i][0] - lam * items[i][1], i))
        return tuple(sorted(order[:k]))

    return dinkelbach(min_param, num, den, tuple(range(k)))
