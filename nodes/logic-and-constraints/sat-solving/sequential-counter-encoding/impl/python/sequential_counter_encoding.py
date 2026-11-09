# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-counter-encoding/. The authors are listed in prov/JYYPDZ.jsonl.

"""Sinz's sequential counter encoding of the cardinality constraint
x_1 + ... + x_n <= k into CNF.

The register variable s(i, j), for 1 <= i <= n-1 and 1 <= j <= k, is forced
true when at least j of x_1..x_i are true. For 1 <= k < n the result has
k(n-1) new variables and 2nk + n - 3k - 1 clauses. Literals are DIMACS ints.
"""


def at_most_k(xs: list[int], k: int, top: int) -> tuple[list[list[int]], int]:
    """Encode sum(xs) <= k. New variables are top+1, top+2, ...

    Returns (clauses, new top). xs are literals; k >= 0.
    """
    n = len(xs)
    if k >= n:
        return [], top
    if k == 0:
        return [[-x] for x in xs], top

    def s(i: int, j: int) -> int:  # 1-based register s(i, j)
        return top + (i - 1) * k + j

    x = [0] + list(xs)  # 1-based
    cl: list[list[int]] = [[-x[1], s(1, 1)]]  # @line L1
    cl += [[-s(1, j)] for j in range(2, k + 1)]  # @line L2
    for i in range(2, n):  # @line L3
        cl.append([-x[i], s(i, 1)])  # @line L4
        cl.append([-s(i - 1, 1), s(i, 1)])  # @line L5
        for j in range(2, k + 1):
            cl.append([-x[i], -s(i - 1, j - 1), s(i, j)])  # @line L6
            cl.append([-s(i - 1, j), s(i, j)])  # @line L7
        cl.append([-x[i], -s(i - 1, k)])  # @line L8
    cl.append([-x[n], -s(n - 1, k)])  # @line L9
    return cl, top + (n - 1) * k


def at_least_k(xs: list[int], k: int, top: int) -> tuple[list[list[int]], int]:
    """Encode sum(xs) >= k as 'at most len(xs) - k of the negations are true'."""
    if k <= 0:
        return [], top
    if k > len(xs):
        return [[]], top
    return at_most_k([-x for x in xs], len(xs) - k, top)
