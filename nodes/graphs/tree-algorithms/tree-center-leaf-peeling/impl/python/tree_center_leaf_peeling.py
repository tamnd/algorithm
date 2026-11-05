# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-center-leaf-peeling/. The authors are listed in prov/R9M66X.jsonl.


def tree_center(n: int, edges: list[tuple[int, int]]) -> tuple[list[int], int]:
    """Return (centre, rounds) of a free, unweighted tree on the vertices 0 .. n-1.

    The centre is the sorted list of the one or two vertices of smallest
    eccentricity. rounds is the number of peeling rounds; the radius is rounds
    when the centre has one vertex and rounds + 1 when it has two (for n >= 2).
    Precondition: n >= 1 and edges are the n - 1 edges of a tree.
    Time and extra space Theta(n); no recursion.
    """
    if n <= 2:  # @line L1
        return list(range(n)), 0
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    deg = [len(a) for a in adj]  # @line L2
    leaves = [v for v in range(n) if deg[v] == 1]  # @line L3
    left = n
    rounds = 0
    while left > 2:  # @line L4
        left -= len(leaves)  # @line L5
        rounds += 1
        nxt: list[int] = []  # @line L6
        for u in leaves:  # @line L7
            deg[u] = 0  # @line L8
            for v in adj[u]:  # @line L9
                if deg[v] > 0:
                    deg[v] -= 1  # @line L10
                    if deg[v] == 1:  # @line L11
                        nxt.append(v)
        leaves = nxt  # @line L12
    return sorted(leaves), rounds  # @line L13
