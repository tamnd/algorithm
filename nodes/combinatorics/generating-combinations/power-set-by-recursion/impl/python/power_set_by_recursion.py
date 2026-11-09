# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-set-by-recursion/. The authors are listed in prov/198V88.jsonl.

from collections.abc import Iterator


def subsets_counter(n: int) -> Iterator[tuple[int, ...]]:
    """Yield the bit vectors x[0..n-1] of all subsets of [n] in binary counting order.

    x[j] = 1 means that element j + 1 is in the subset. Each vector is yielded as a copy.
    """
    x = [0] * (n + 1)  # @line L1: x[n] is the sentinel
    while True:  # @line L2
        yield tuple(x[:n])  # @line L3
        j = 0  # @line L4
        while x[j] == 1:  # @line L5
            x[j] = 0
            j += 1
        if j == n:  # @line L6
            return
        x[j] = 1  # @line L7


def subsets_recursive(n: int) -> Iterator[tuple[int, ...]]:
    """Yield the same list as subsets_counter, by the include or exclude recursion."""
    x = [0] * n

    def extend(i: int) -> Iterator[tuple[int, ...]]:
        if i == 0:  # @line L9
            yield tuple(x)
            return
        x[i - 1] = 0  # @line L10
        yield from extend(i - 1)
        x[i - 1] = 1  # @line L11
        yield from extend(i - 1)

    yield from extend(n)  # @line L8


def as_set(x: tuple[int, ...]) -> list[int]:
    """Return the sorted elements of the subset with bit vector x."""
    return [j + 1 for j, bit in enumerate(x) if bit]


def counter_writes(n: int) -> int:
    """Return the number of bits that the 2^n - 1 increments write, the final scan not included."""
    x = [0] * (n + 1)
    writes = 0
    while True:
        j = 0
        cleared = 0
        while x[j] == 1:
            x[j] = 0
            j += 1
            cleared += 1
        if j == n:
            return writes
        x[j] = 1
        writes += cleared + 1
