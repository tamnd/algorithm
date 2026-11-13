# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mex-function/. The authors are listed in prov/0H0WG2.jsonl.

"""The mex of a finite set of nonnegative integers is the smallest
nonnegative integer that is not in the set. This module computes it in time
linear in the size of the input, and uses it to compute Grundy values of
impartial games, first for subtraction games and then for any game given by
a move function."""

from functools import lru_cache
from typing import Callable, Hashable, Iterable, List, Sequence


def mex(values: Iterable[int]) -> int:
    """Return the smallest nonnegative integer not in values.

    The input may repeat values and may contain integers that are too large
    to matter. The answer is at most the number of distinct values, so a
    table of that size is enough: O(k) time and space for k input items."""
    items = list(values)
    k = len(items)
    present = [False] * (k + 1)
    for v in items:
        if v < 0:
            raise ValueError("mex is defined on nonnegative integers")
        if v <= k:
            present[v] = True
    m = 0
    while present[m]:
        m += 1
    return m


def mex_naive(values: Iterable[int]) -> int:
    """The definition, used as a reference in the tests."""
    s = set(values)
    m = 0
    while m in s:
        m += 1
    return m


def subtraction_grundy(moves: Sequence[int], n: int) -> List[int]:
    """Grundy values g(0), ..., g(n) of the subtraction game with the given
    move set: a move removes m tokens from one heap, for some m in moves
    with m at most the heap size."""
    g: List[int] = []
    for i in range(n + 1):
        g.append(mex(g[i - m] for m in moves if m <= i))
    return g


def grundy(position: Hashable, options: Callable[[Hashable], Iterable[Hashable]]) -> int:
    """Grundy value of a position of a finite impartial game, by recursion
    with a memo. options(p) lists the positions reachable in one move from
    p. The game graph must be acyclic."""

    @lru_cache(maxsize=None)
    def g(p: Hashable) -> int:
        return mex(g(q) for q in options(p))

    return g(position)
