# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hillis-steele-scan/. The authors are listed in prov/H3KT7W.jsonl.

"""The Hillis-Steele scan, simulated one synchronous round at a time.

Each round reads only the old array x and writes a new array y, as on a
PRAM with double buffering. The work is the number of applications of the
operator and the span is the number of rounds.
"""

from typing import Callable, TypeVar

T = TypeVar("T")


def hillis_steele_scan(op: Callable[[T, T], T], a: list[T]) -> tuple[list[T], int, int]:
    """Return (inclusive scan of a, work, rounds)."""
    x = list(a)  # @line L1
    n = len(x)
    d = 1  # @line L2
    work = rounds = 0
    while d < n:  # @line L3
        # @line L4: all n positions in parallel, reading only the old x
        y = [op(x[i - d], x[i]) if i >= d else x[i] for i in range(n)]  # @line L5
        work += n - d
        rounds += 1
        x = y  # @line L6
        d *= 2  # @line L7
    return x, work, rounds  # @line L8


def round_reads(n: int, d: int) -> tuple[list[int], list[int]]:
    """The cells read in the two EREW substeps of the round with distance d.

    In substep 1 processor i reads x[i]; in substep 2 processor i >= d reads
    x[i - d]. Returns the two lists of addresses, one entry per reader.
    """
    first = list(range(n))
    second = [i - d for i in range(d, n)]
    return first, second


def in_place_scan_wrong(op: Callable[[T, T], T], a: list[T]) -> list[T]:
    """A buggy version that updates x in place in increasing order of i.

    A later position then reads a value that was already updated in the
    same round. Used by the tests to show the pitfall.
    """
    x = list(a)
    n = len(x)
    d = 1
    while d < n:
        for i in range(d, n):
            x[i] = op(x[i - d], x[i])
        d *= 2
    return x
