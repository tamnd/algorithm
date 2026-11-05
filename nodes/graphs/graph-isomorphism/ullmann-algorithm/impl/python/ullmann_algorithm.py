# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ullmann-algorithm/. The authors are listed in prov/GMKCZG.jsonl.
"""Ullmann's algorithm for subgraph isomorphism, with the refinement procedure.

Graphs are undirected and simple, given as (n, edges) with vertices 0..n-1, and may carry
integer vertex labels. G1 is the pattern (k vertices), G2 the host (n vertices). Rows of the
candidate matrix are Python integers used as bit sets over host vertices. The search uses an
explicit stack instead of recursion.
"""

from collections.abc import Iterator

Graph = tuple[int, list[tuple[int, int]]]


def _adj(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    a: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        a[u].add(v)
        a[v].add(u)
    return a


def refine(m: list[int], adj1: list[set[int]], nbmask2: list[int]) -> bool:
    """Ullmann's refinement in place: clear m[i] bit j when some neighbor x of i has no candidate
    among the neighbors of j. Returns False when a row becomes empty.
    Cost: O(k * n * d1) bit-set operations per pass, at most k * n passes.
    """
    # @line L8
    changed = True
    while changed:
        changed = False
        # @line L9
        for i in range(len(m)):
            row = m[i]
            bits = row
            while bits:
                low = bits & -bits
                j = low.bit_length() - 1
                bits ^= low
                # @line L10
                for x in adj1[i]:
                    if m[x] & nbmask2[j] == 0:
                        row &= ~low
                        changed = True
                        break
            m[i] = row
            if row == 0:
                return False
        # @line L11
    return True


def ullmann_matches(g1: Graph, g2: Graph, induced: bool = False,
                    labels1: list[int] | None = None, labels2: list[int] | None = None) -> Iterator[list[int]]:
    """Yield every injective map f (f[i] is the host vertex of pattern vertex i) that keeps edges,
    and also non-edges when induced is True. Cost: exponential in the worst case;
    O(k^2 n) words of memory for the stack of matrices.
    """
    k, e1 = g1
    n, e2 = g2
    if k > n:
        return
    if k == 0:
        yield []
        return
    adj1, adj2 = _adj(k, e1), _adj(n, e2)
    nbmask2 = [sum(1 << y for y in adj2[j]) for j in range(n)]
    lab1 = labels1 if labels1 is not None else [0] * k
    lab2 = labels2 if labels2 is not None else [0] * n
    # @line L1
    m0 = [sum(1 << j for j in range(n) if lab1[i] == lab2[j] and len(adj1[i]) <= len(adj2[j])) for i in range(k)]
    # @line L2
    if not refine(m0, adj1, nbmask2):
        return
    # @line L3
    stack: list[tuple[int, list[int], int]] = [(0, m0, m0[0])]
    while stack:
        i, m, todo = stack.pop()
        # @line L4
        if todo == 0:
            continue
        low = todo & -todo
        j = low.bit_length() - 1
        stack.append((i, m, todo ^ low))
        # @line L5
        m2 = list(m)
        m2[i] = low
        for r in range(i + 1, k):
            m2[r] &= ~low
        # @line L6
        if not refine(m2, adj1, nbmask2):
            continue
        # @line L7
        if i == k - 1:
            f = [m2[r].bit_length() - 1 for r in range(k)]
            if all(f[y] in adj2[f[x]] for x, y in e1) and (
                    not induced or all((f[b] in adj2[f[a]]) == (b in adj1[a])
                                       for a in range(k) for b in range(a + 1, k))):
                yield f
            continue
        stack.append((i + 1, m2, m2[i + 1]))


def ullmann_count(g1: Graph, g2: Graph, induced: bool = False) -> int:
    """Number of embeddings. Cost: as ullmann_matches over the whole search."""
    return sum(1 for _ in ullmann_matches(g1, g2, induced))


def ullmann_isomorphic(g1: Graph, g2: Graph) -> bool:
    """Graph isomorphism as an induced embedding between graphs of equal size. Cost: as ullmann_matches."""
    if g1[0] != g2[0] or len(g1[1]) != len(g2[1]):
        return False
    return next(ullmann_matches(g1, g2, True), None) is not None
