# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lexicographic-combinations/. The authors are listed in prov/JMPMV6.jsonl.

from collections.abc import Iterator


def next_combination(a: list[int], n: int) -> bool:
    """Change the increasing list a over [n] to its lexicographic successor.

    Return False, and leave a unchanged, when a is the last list.
    """
    k = len(a)
    i = k  # @line L5: i is 1-based, a[i - 1] is the entry a_i
    while i >= 1 and a[i - 1] == n - k + i:  # @line L6
        i -= 1
    if i == 0:  # @line L7
        return False
    a[i - 1] += 1  # @line L8
    for j in range(i + 1, k + 1):  # @line L9
        a[j - 1] = a[j - 2] + 1
    return True


def lex_combinations(n: int, k: int) -> Iterator[tuple[int, ...]]:
    """Yield the k-subsets of [n] as increasing tuples, in lexicographic order."""
    if k < 0 or k > n:  # @line L1
        return
    a = list(range(1, k + 1))  # @line L2
    while True:  # @line L3
        yield tuple(a)  # @line L4
        if not next_combination(a, n):
            return


def scan_steps(n: int, k: int) -> tuple[int, int]:
    """Return (the total steps of line L6, the total writes of line L9) over the whole list."""
    if k < 0 or k > n:
        return 0, 0
    a = list(range(1, k + 1))
    steps = writes = 0
    while True:
        i = k
        while i >= 1 and a[i - 1] == n - k + i:
            i -= 1
            steps += 1
        if i == 0:
            return steps, writes
        a[i - 1] += 1
        for j in range(i + 1, k + 1):
            a[j - 1] = a[j - 2] + 1
            writes += 1
