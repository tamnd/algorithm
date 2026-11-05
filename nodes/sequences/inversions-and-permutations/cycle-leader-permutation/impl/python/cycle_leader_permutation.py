# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cycle-leader-permutation/. The authors are listed in prov/J8DYW4.jsonl.

from typing import MutableSequence, Sequence, TypeVar

T = TypeVar("T")


def apply_permutation(a: MutableSequence[T], p: MutableSequence[int]) -> MutableSequence[T]:
    """Move a[i] to position p[i] in place, for a permutation p of 0..n-1.

    p is marked by bitwise complement while the cycles are moved and is
    restored before returning.
    """
    n = len(a)
    if len(p) != n:
        raise ValueError("a and p must have the same length")
    for i in range(n):  # @line L1
        if p[i] >= 0:  # @line L2
            x, j = a[i], p[i]  # @line L3
            while j != i:  # @line L4
                x, a[j] = a[j], x  # @line L5
                k = p[j]  # @line L6
                p[j] = ~p[j]
                j = k
            a[i] = x  # @line L7
            p[i] = ~p[i]
    for i in range(n):  # @line L8
        p[i] = ~p[i]
    return a  # @line L9


def apply_permutation_readonly(a: MutableSequence[T], p: Sequence[int]) -> MutableSequence[T]:
    """Move a[i] to position p[i] in place without writing p."""
    n = len(a)
    if len(p) != n:
        raise ValueError("a and p must have the same length")
    for i in range(n):  # @line L10
        j = p[i]  # @line L11
        while j > i:
            j = p[j]
        if j == i:  # @line L12
            x, j = a[i], p[i]  # @line L13
            while j != i:  # @line L14
                x, a[j] = a[j], x
                j = p[j]
            a[i] = x  # @line L15
    return a  # @line L16


def leader_reads(p: Sequence[int]) -> int:
    """Number of reads of p made by the leader test of apply_permutation_readonly."""
    total = 0
    for i in range(len(p)):
        j = p[i]
        total += 1
        while j > i:
            j = p[j]
            total += 1
    return total
