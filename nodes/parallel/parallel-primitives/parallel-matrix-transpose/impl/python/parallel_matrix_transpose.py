# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-matrix-transpose/. The authors are listed in prov/A6Y79E.jsonl.

"""In-place fork-join matrix transpose, run sequentially with work and span counters.

Cost model: a swap, or a call that returns at once, costs 1. A group of k parallel tasks
adds k - 1 to the work and ceil(lg k) to the span. An optional trace records the cells
in the order that a run on one processor touches them, for a cache simulation.
"""

from collections import OrderedDict
from dataclasses import dataclass
from typing import Any

Matrix = list[list[Any]]


@dataclass(frozen=True)
class Cost:
    work: int
    span: int


def ceil_lg(k: int) -> int:
    return (k - 1).bit_length() if k > 1 else 0


def par(costs: list[Cost]) -> Cost:
    k = len(costs)
    return Cost(sum(c.work for c in costs) + k - 1, ceil_lg(k) + max(c.span for c in costs))


UNIT = Cost(1, 1)


class Transposer:
    def __init__(self, a: Matrix, trace: list[tuple[int, int]] | None = None) -> None:
        self.a = a
        self.trace = trace
        self.swaps = 0

    def _swap(self, i: int, j: int, k: int, l: int) -> None:
        a = self.a
        a[i][j], a[k][l] = a[k][l], a[i][j]
        self.swaps += 1
        if self.trace is not None:
            self.trace.append((i, j))
            self.trace.append((k, l))

    def transpose(self, r: int, n: int) -> Cost:
        """Transpose the n x n block at (r, r) in place; n is a power of 2."""
        if n == 1:  # @line L1
            return UNIT
        h = n // 2  # @line L2
        t11 = self.transpose(r, h)  # @line L3: spawn
        t22 = self.transpose(r + h, h)  # @line L4: spawn
        s = self.swap_t(r, r + h, r + h, r, h)  # @line L5
        return par([t11, t22, s])  # @line L6: sync

    def swap_t(self, i: int, j: int, k: int, l: int, n: int) -> Cost:
        """Swap the n x n block X at (i, j) with the transpose of the block Y at (k, l)."""
        if n == 1:  # @line L7
            self._swap(i, j, k, l)
            return UNIT
        h = n // 2  # @line L8
        c1 = self.swap_t(i, j, k, l, h)  # @line L9: X11 with Y11
        c2 = self.swap_t(i, j + h, k + h, l, h)  # X12 with Y21
        c3 = self.swap_t(i + h, j, k, l + h, h)  # @line L10: X21 with Y12
        c4 = self.swap_t(i + h, j + h, k + h, l + h, h)  # X22 with Y22
        return par([c1, c2, c3, c4])  # @line L11: sync

    def swap_rect(self, i: int, j: int, k: int, l: int, p: int, q: int) -> Cost:
        """Swap the p x q block X at (i, j) with the transpose of the q x p block Y at (k, l).

        Any p and q: halve the larger side, as in the cache-oblivious transpose.
        """
        if p == 0 or q == 0:
            return UNIT
        if p == 1 and q == 1:
            self._swap(i, j, k, l)
            return UNIT
        if p >= q:
            p1 = p // 2
            return par([self.swap_rect(i, j, k, l, p1, q), self.swap_rect(i + p1, j, k, l + p1, p - p1, q)])
        q1 = q // 2
        return par([self.swap_rect(i, j, k, l, p, q1), self.swap_rect(i, j + q1, k + q1, l, p, q - q1)])

    def transpose_any(self, r: int, n: int) -> Cost:
        """Transpose the n x n block at (r, r) in place, for any n >= 0."""
        if n <= 1:
            return UNIT
        h = n // 2
        t11 = self.transpose_any(r, h)
        t22 = self.transpose_any(r + h, n - h)
        s = self.swap_rect(r, r + h, r + h, r, h, n - h)
        return par([t11, t22, s])


def transpose(a: Matrix, trace: list[tuple[int, int]] | None = None) -> tuple[Cost, int]:
    """Transpose a square matrix in place. Returns the cost and the number of swaps."""
    n = len(a)
    t = Transposer(a, trace)
    if n == 0:
        return UNIT, 0
    if n & (n - 1) == 0:
        cost = t.transpose(0, n)
    else:
        cost = t.transpose_any(0, n)
    return cost, t.swaps


def transpose_rows(a: Matrix, trace: list[tuple[int, int]] | None = None) -> None:
    """The plain loop: for each i and each j > i, swap a[i][j] with a[j][i]."""
    n = len(a)
    t = Transposer(a, trace)
    for i in range(n):
        for j in range(i + 1, n):
            t._swap(i, j, j, i)


def lru_misses(trace: list[tuple[int, int]], n: int, lines: int, line_words: int) -> int:
    """Count the misses of a fully associative LRU cache on a row-major n x n matrix."""
    cache: OrderedDict[int, None] = OrderedDict()
    misses = 0
    for i, j in trace:
        block = (i * n + j) // line_words
        if block in cache:
            cache.move_to_end(block)
        else:
            misses += 1
            cache[block] = None
            if len(cache) > lines:
                cache.popitem(last=False)
    return misses
