# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-map/. The authors are listed in prov/S8QNJR.jsonl.

"""Parallel map by fork-join splitting, with work and span counters.

Each split node (one spawn and one sync) costs 1 unit of work and span.
Item i costs cost(i) = (work, span); by default each call of f costs 1.
"""

from typing import Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def parallel_map(
    f: Callable[[T], U],
    a: list[T],
    cost: Callable[[int], tuple[int, int]] = lambda i: (1, 1),
) -> tuple[list[U], int, int]:
    """Return ([f(x) for x in a], work, span)."""
    n = len(a)
    b: list[U | None] = [None] * n  # @line L6

    def run(lo: int, hi: int) -> tuple[int, int]:
        if hi - lo == 1:  # @line L1
            b[lo] = f(a[lo])
            return cost(lo)
        mid = lo + (hi - lo + 1) // 2  # @line L2
        w1, s1 = run(lo, mid)  # @line L3: spawn
        w2, s2 = run(mid, hi)  # @line L4
        # @line L5: sync; the two halves wrote disjoint parts of b
        return w1 + w2 + 1, max(s1, s2) + 1

    work = span = 0
    if n > 0:  # @line L7
        work, span = run(0, n)
    return b, work, span  # @line L8


def blocked_map(f: Callable[[T], U], a: list[T], grain: int) -> tuple[list[U], int]:
    """Map with a grain size: ranges of at most `grain` items run serially.

    Returns the result and the number of split nodes.
    """
    n = len(a)
    b: list[U | None] = [None] * n
    splits = 0

    def run(lo: int, hi: int) -> None:
        nonlocal splits
        if hi - lo <= grain:
            for i in range(lo, hi):
                b[i] = f(a[i])
            return
        mid = lo + (hi - lo + 1) // 2
        splits += 1
        run(lo, mid)
        run(mid, hi)

    if n > 0:
        run(0, n)
    return b, splits
