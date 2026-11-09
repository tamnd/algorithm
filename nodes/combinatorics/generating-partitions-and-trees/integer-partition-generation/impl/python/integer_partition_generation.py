# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/integer-partition-generation/. The authors are listed in prov/E69C97.jsonl.

from collections.abc import Iterator


def partitions(n: int) -> Iterator[tuple[int, ...]]:
    """Yield the partitions of n in reverse lexicographic order.

    Each partition is a tuple of parts in non-increasing order. The generator
    keeps the parts in one array a[1..m] and changes it in place; the yield
    copies it, which costs O(m) for each partition.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:  # @line L1
        yield ()
        return
    a = [0] * (n + 2)  # a[0] is unused, as in the pseudocode
    a[1], m = n, 1  # @line L2
    q = 1 if n > 1 else 0  # @line L3: q is the index of the last part > 1
    while True:  # @line L4
        yield tuple(a[1 : m + 1])  # @line L5
        if q == 0:  # @line L6
            return
        if a[q] == 2:  # @line L7
            a[q] = 1  # @line L8
            m += 1
            a[m] = 1
            q -= 1
        else:  # @line L9
            x = a[q] - 1  # @line L10
            s = m - q + 1
            a[q] = x
            m = q
            while s > x:  # @line L11
                m += 1
                a[m] = x
                s -= x
            m += 1  # @line L12
            a[m] = s
            q = m if s > 1 else m - 1  # @line L13


def step_counts(n: int) -> tuple[int, int, int]:
    """Run the algorithm without visits.

    Return (the number of steps that take the branch of line L7, the number
    that take the branch of line L9, the total number of runs of the loop
    body of line L11).
    """
    if n <= 1:
        return 0, 0, 0
    a = [0] * (n + 2)
    a[1], m, q = n, 1, 1
    fast = general = inner = 0
    while q != 0:
        if a[q] == 2:
            fast += 1
            a[q] = 1
            m += 1
            a[m] = 1
            q -= 1
        else:
            general += 1
            x = a[q] - 1
            s = m - q + 1
            a[q] = x
            m = q
            while s > x:
                inner += 1
                m += 1
                a[m] = x
                s -= x
            m += 1
            a[m] = s
            q = m if s > 1 else m - 1
    return fast, general, inner
