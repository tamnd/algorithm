# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-partition-generation/. The authors are listed in prov/8CRTRG.jsonl.

from collections.abc import Iterator


def set_partitions(n: int) -> Iterator[tuple[int, ...]]:
    """Yield the restricted growth strings of length n in lexicographic order.

    Entry i - 1 of each tuple is the block number of element i, with blocks
    numbered from 0 in the order of their smallest elements. The generator
    changes one array in place; the yield copies it, which costs O(n).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:  # @line L1
        yield ()
        return
    a = [0] * (n + 1)  # @line L2: a[0] and b[0], b[1] are unused
    b = [0, 0] + [1] * (n - 1)  # b[j] = 1 + max(a[1..j-1]) for j >= 2
    while True:  # @line L3
        yield tuple(a[1:])  # @line L4
        j = n  # @line L5
        while j >= 2 and a[j] == b[j]:  # @line L6
            j -= 1
        if j == 1:  # @line L7
            return
        a[j] += 1  # @line L8
        c = max(b[j], a[j] + 1)
        for i in range(j + 1, n + 1):  # @line L9
            a[i] = 0
            b[i] = c


def to_blocks(rgs: tuple[int, ...]) -> list[list[int]]:
    """The blocks of the partition of {1, ..., n} that the string encodes."""
    k = max(rgs) + 1 if rgs else 0
    out: list[list[int]] = [[] for _ in range(k)]
    for i, v in enumerate(rgs, start=1):
        out[v].append(i)
    return out


def scan_steps(n: int) -> int:
    """Run the algorithm without visits and return the total number of runs of the loop body of line L6."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    a = [0] * (n + 1)
    b = [0, 0] + [1] * (n - 1)
    steps = 0
    while True:
        j = n
        while j >= 2 and a[j] == b[j]:
            steps += 1
            j -= 1
        if j == 1:
            return steps
        a[j] += 1
        c = max(b[j], a[j] + 1)
        for i in range(j + 1, n + 1):
            a[i] = 0
            b[i] = c
