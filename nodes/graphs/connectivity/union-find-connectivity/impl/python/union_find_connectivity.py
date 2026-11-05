# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/union-find-connectivity/. The authors are listed in prov/TDTBHE.jsonl.


def union_find_connectivity(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Return comp, where comp[v] is the root of the set of v after all unions.

    The vertices are 0 .. n-1 and edges is a list of pairs (u, v). The direction
    of a pair is ignored, so for a directed graph the result is the weak
    components. Self-loops and parallel edges are allowed. Two vertices get the
    same comp value exactly when they are joined by a path. Union by rank and
    path compression give O(n + m alpha(n)) time; extra space O(n).
    """
    parent = list(range(n))  # @line L1
    rank = [0] * n

    def find(x: int) -> int:
        r = x
        while parent[r] != r:  # @line L7
            r = parent[r]
        while parent[x] != r:  # @line L8
            parent[x], x = r, parent[x]
        return r  # @line L9

    def link(a: int, b: int) -> None:
        if rank[a] < rank[b]:  # @line L10
            a, b = b, a
        parent[b] = a  # @line L11
        if rank[a] == rank[b]:  # @line L12
            rank[a] += 1

    for u, v in edges:  # @line L2
        a, b = find(u), find(v)  # @line L3
        if a != b:  # @line L4
            link(a, b)
    comp = [find(v) for v in range(n)]  # @line L5
    return comp  # @line L6
