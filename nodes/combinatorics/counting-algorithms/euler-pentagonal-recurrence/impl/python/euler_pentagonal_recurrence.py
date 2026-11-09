# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-pentagonal-recurrence/. The authors are listed in prov/SBKFAF.jsonl.


def partition_numbers(n: int, mod: int | None = None) -> list[int]:
    """Return [p(0), ..., p(n)], exactly or modulo mod.

    p(m) is the number of partitions of m. With mod = None the values are
    exact Python integers. With an integer mod >= 1 they are residues in
    [0, mod).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if mod is not None and mod < 1:
        raise ValueError("mod must be at least 1")
    p = [0] * (n + 1)
    p[0] = 1 if mod is None else 1 % mod  # @line L1
    for m in range(1, n + 1):  # @line L2
        s = 0  # @line L3
        j = 1
        g = 1  # g = j(3j - 1)/2
        while g <= m:  # @line L4
            c = 1 if j % 2 == 1 else -1  # @line L5
            s += c * p[m - g]  # @line L6
            if g + j <= m:  # @line L7: g + j = j(3j + 1)/2
                s += c * p[m - g - j]
            g += 3 * j + 1  # @line L8: the next pentagonal number
            j += 1
        p[m] = s if mod is None else s % mod  # @line L9
    return p  # @line L10


def partition_number(n: int, mod: int | None = None) -> int:
    """Return p(n), exactly or modulo mod. p(n) = 0 for n < 0."""
    if n < 0:
        return 0
    return partition_numbers(n, mod)[n]
