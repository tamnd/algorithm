# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/odd-even-transposition-sort/. The authors are listed in prov/QRMS1F.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def round_pairs(n: int, t: int) -> list[tuple[int, int]]:
    """Return the comparators (i, i + 1) of round t, for t = 1, 2, ..."""
    s = (t - 1) % 2  # @line L2
    return [(i, i + 1) for i in range(s, n - 1, 2)]  # @line L3


def odd_even_transposition_sort(a: list[T]) -> None:
    """Sort a in place in n rounds. The pairs of one round are disjoint,
    so this loop is a sequential simulation of the parallel rounds."""
    n = len(a)
    for t in range(1, n + 1):  # @line L1
        for i, j in round_pairs(n, t):
            if a[j] < a[i]:  # @line L5: exchange only on a strict inversion
                a[i], a[j] = a[j], a[i]  # @line L4


def rounds_until_sorted(a: list[T]) -> int:
    """Return the first round after which a copy of a is sorted (0 if it is sorted)."""
    b = list(a)
    n = len(b)
    t = 0
    while any(b[i + 1] < b[i] for i in range(n - 1)):
        t += 1
        for i, j in round_pairs(n, t):
            if b[j] < b[i]:
                b[i], b[j] = b[j], b[i]
    return t
