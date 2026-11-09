# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-combination-generation/. The authors are listed in prov/PHDE76.jsonl.

from collections.abc import Iterator


def rec_combinations(n: int, k: int) -> Iterator[tuple[int, ...]]:
    """Yield the k-subsets of [n] as increasing tuples, in lexicographic order."""
    if k < 0:
        return
    a: list[int] = []  # @line L1: the stack a[1..m], with m = len(a)

    def choose(i: int) -> Iterator[tuple[int, ...]]:
        m = len(a)
        if m == k:  # @line L2
            yield tuple(a)
            return
        if n - i + 1 < k - m:  # @line L3
            return
        a.append(i)  # @line L4
        yield from choose(i + 1)  # @line L5
        a.pop()  # @line L6
        yield from choose(i + 1)  # @line L7

    yield from choose(1)


def count_calls(n: int, k: int) -> int:
    """Return the number of calls of CHOOSE that rec_combinations(n, k) makes."""
    calls = 0
    m = 0

    def choose(i: int) -> None:
        nonlocal calls, m
        calls += 1
        if m == k:
            return
        if n - i + 1 < k - m:
            return
        m += 1
        choose(i + 1)
        m -= 1
        choose(i + 1)

    choose(1)
    return calls
