# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-quickselect/. The authors are listed in prov/3SWVRD.jsonl.

import random
from typing import Callable, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

Trace = Callable[[int, int, int, T, int, int], None]


def randomized_quickselect(
    a: list[T],
    k: int,
    rng: random.Random | None = None,
    trace: Trace | None = None,
) -> T:
    """Return the element of rank k (0-based) of a, the item a sorted copy has at index k.

    Precondition: 0 <= k < len(a), and the items are totally ordered by <.
    The list a is permuted in place. Each round does one three-way comparison
    per item of the current range (two calls of <). Cost: expected at most 4n
    three-way comparisons on every input, O(n^2) in the worst case, O(1) extra space.
    If trace is given, it is called as trace(lo, hi, i, p, lt, gt) after each partition.
    """
    n = len(a)
    if not 0 <= k < n:
        raise IndexError("rank out of range")
    if rng is None:
        rng = random.Random()
    lo, hi = 0, n  # @line L1
    while True:  # @line L2
        i = rng.randrange(lo, hi)  # @line L3
        p = a[i]  # @line L4
        lt, gt = partition3(a, lo, hi, p)  # @line L5
        if trace is not None:
            trace(lo, hi, i, p, lt, gt)
        if k < lt:  # @line L6
            hi = lt
        elif k >= gt:  # @line L7
            lo = gt
        else:  # @line L8
            return a[k]


def partition3(a: list[T], lo: int, hi: int, p: T) -> tuple[int, int]:
    """Rearrange a[lo:hi] into the parts < p, == p and > p, and return their bounds (lt, gt).

    Afterwards a[lo:lt] < p, a[lt:gt] == p and a[gt:hi] > p. Cost: hi - lo three-way comparisons.
    """
    lt, i, gt = lo, lo, hi  # @line L9
    while i < gt:  # @line L10
        if a[i] < p:  # @line L11
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif p < a[i]:  # @line L12
            gt -= 1
            a[i], a[gt] = a[gt], a[i]
        else:  # @line L13
            i += 1
    return lt, gt  # @line L14
