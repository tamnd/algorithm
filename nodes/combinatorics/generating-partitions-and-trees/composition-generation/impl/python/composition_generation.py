# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/composition-generation/. The authors are listed in prov/45NXTX.jsonl.

from collections.abc import Iterator


def compositions(n: int) -> Iterator[tuple[int, ...]]:
    """Yield the compositions of n in lexicographic order.

    The first composition is (1, ..., 1) and the last one is (n,). The
    generator keeps the parts in one array a[1..m] and changes it in place;
    the yield copies it, which costs O(m) for each composition.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:  # @line L1
        yield ()
        return
    a = [1] * (n + 1)  # @line L2: a[0] is unused, as in the pseudocode
    m = n
    while True:  # @line L3
        yield tuple(a[1 : m + 1])  # @line L4
        if m == 1:  # @line L5
            return
        t = a[m] - 1  # @line L6
        m -= 1  # @line L7
        a[m] += 1
        while t > 0:  # @line L8
            m += 1
            a[m] = 1
            t -= 1


def extra_writes(n: int) -> int:
    """Run the algorithm without visits and return the number of runs of the loop body of line L8."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    a = [1] * (n + 1)
    m = n
    runs = 0
    while m != 1:
        t = a[m] - 1
        m -= 1
        a[m] += 1
        while t > 0:
            runs += 1
            m += 1
            a[m] = 1
            t -= 1
    return runs
