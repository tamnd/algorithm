# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lawler-chromatic-number/. The authors are listed in prov/E447F2.jsonl.

from collections.abc import Iterator, Sequence


def maximal_independent_sets(nbr: Sequence[int], s: int) -> Iterator[int]:
    """Yield each maximal independent set of the subgraph induced by the bitmask s.

    nbr[v] is the bitmask of the neighbours of v. This is Bron-Kerbosch on the
    complement, with the Tomita pivot, so it takes O(3^(k/3)) steps for k = |s|,
    up to a factor polynomial in k. The empty set is yielded once when s is empty.
    """
    stack = [(0, s, 0)]  # (R, P, X): R is independent, P and X are its candidates
    while stack:
        r, p, x = stack.pop()
        if p == 0:
            if x == 0:
                yield r
            continue
        # pivot u in P or X with the most candidates that are not its neighbours,
        # that is, the fewest P-vertices left after removing u's non-neighbours
        best, u = -1, -1
        px = p | x
        while px:
            w = (px & -px).bit_length() - 1
            px &= px - 1
            c = (p & ~nbr[w] & ~(1 << w)).bit_count()
            if c > best:
                best, u = c, w
        branch = p & (nbr[u] | (1 << u))  # vertices that are not non-neighbours of u
        while branch:
            v = (branch & -branch).bit_length() - 1
            branch &= branch - 1
            keep = ~(nbr[v] | (1 << v))
            stack.append((r | (1 << v), p & keep, x & keep))
            p &= ~(1 << v)
            x |= 1 << v


def lawler_chromatic_number(adj: Sequence[Sequence[int]]) -> tuple[int, list[int]]:
    """Return (chi, c): the chromatic number of the graph and an optimal coloring.

    adj[v] lists the neighbours of v in a simple undirected graph on 0 .. n-1.
    c[v] is in 1 .. chi and adjacent vertices get different colors. Time
    O(2.4423^n) up to a polynomial factor, space Theta(2^n).
    """
    n = len(adj)
    nbr = [0] * n
    for v in range(n):
        for w in adj[v]:
            nbr[v] |= 1 << w
    full = (1 << n) - 1
    inf = n + 1
    best = [0] * (1 << n)  # @line L1: best[0] = 0 for the empty set
    choice = [0] * (1 << n)
    for s in range(1, full + 1):  # @line L2: subsets before supersets
        best[s] = inf  # @line L3
        for i in maximal_independent_sets(nbr, s):  # @line L4
            if best[s & ~i] + 1 < best[s]:  # @line L5
                best[s] = best[s & ~i] + 1
                choice[s] = i
    c = [0] * n
    s, k = full, 0
    while s:
        k += 1
        i = choice[s]
        for v in range(n):
            if i >> v & 1:
                c[v] = k
        s &= ~i
    return best[full], c  # @line L6
