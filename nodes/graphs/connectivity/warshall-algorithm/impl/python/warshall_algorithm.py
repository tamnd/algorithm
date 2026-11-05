# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warshall-algorithm/. The authors are listed in prov/036P3Q.jsonl.


def warshall_algorithm(adj: list[list[int]]) -> list[list[bool]]:
    """Return the transitive closure R of a directed graph as an n x n Boolean matrix.

    The graph has vertices 0 .. n-1 and adjacency lists adj. Parallel arcs (repeated
    entries) and self-loops (v in adj[v]) are allowed. R[u][v] is True exactly when
    there is a walk of length at least 1 from u to v, so R[v][v] is True exactly
    when v lies on a cycle (a loop counts). Each row is kept as a Python int used as
    a bit vector, so line L5 is one OR of two rows.
    Time Theta(n^3) bit operations (n^3 / w word operations), space Theta(n^2) bits.
    """
    n = len(adj)
    row = [0] * n  # @line L1
    for u in range(n):
        for v in adj[u]:
            row[u] |= 1 << v
    for k in range(n):  # @line L2
        bit = 1 << k
        rk = row[k]
        for i in range(n):  # @line L3
            if row[i] & bit:  # @line L4
                row[i] |= rk  # @line L5
        # row[k] itself can change in pass k only by OR with itself, so rk stays valid.
    return [[bool(row[u] >> v & 1) for v in range(n)] for u in range(n)]  # @line L6
