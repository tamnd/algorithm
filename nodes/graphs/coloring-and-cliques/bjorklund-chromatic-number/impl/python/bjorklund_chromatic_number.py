# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bjorklund-chromatic-number/. The authors are listed in prov/X7DPRF.jsonl.

from collections.abc import Sequence


def bjorklund_chromatic_number(adj: Sequence[Sequence[int]]) -> int:
    """Return the chromatic number of a simple undirected graph.

    adj[v] lists the neighbours of v (vertices 0 .. n-1, each edge in both lists,
    no self-loops). Subsets of the vertices are bitmasks. f[S] becomes the number
    of independent sets contained in S, the empty set included, and the number of
    k-tuples of independent sets whose union is all of V is
    sum over S of (-1)^(n - |S|) f[S]^k. The answer is the least k for which
    this number is positive. Time O(2^n n^2) and space O(2^n n) words.
    """
    n = len(adj)
    if n == 0:  # @line L1
        return 0
    nbr = [0] * n
    for v in range(n):
        for w in adj[v]:
            nbr[v] |= 1 << w
    full = 1 << n
    f = [0] * full
    f[0] = 1
    for s in range(1, full):  # @line L2
        v = (s & -s).bit_length() - 1
        rest = s & (s - 1)
        f[s] = 1 if f[rest] and not (nbr[v] & rest) else 0  # @line L3
    for v in range(n):  # @line L4
        bit = 1 << v
        for s in range(full):
            if s & bit:
                f[s] += f[s ^ bit]  # @line L5
    sign = [1 if (n - bin(s).count("1")) % 2 == 0 else -1 for s in range(full)]
    power = [1] * full
    for k in range(1, n + 1):  # @line L6
        total = 0
        for s in range(full):
            power[s] *= f[s]
            total += sign[s] * power[s]  # @line L7
        if total > 0:  # @line L8
            return k
    return n  # unreachable: the n singletons always cover V
