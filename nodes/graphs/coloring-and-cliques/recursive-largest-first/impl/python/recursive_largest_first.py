# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-largest-first/. The authors are listed in prov/8E77R4.jsonl.

from collections.abc import Sequence


def recursive_largest_first(adj: Sequence[Sequence[int]]) -> list[int]:
    """Color the vertices 0 .. n-1 of a simple undirected graph by Leighton's RLF rule.

    adj[v] lists the neighbours of v (each edge is in both lists). Color classes are
    built one at a time. U holds the uncolored vertices, P the candidates for the
    current class and W the uncolored vertices that already have a neighbour in it.
    The first member is the vertex of P with the most neighbours in U; each later
    member is the vertex of P with the most neighbours in W, ties broken by the
    fewest neighbours in P and then by the smaller index. Returns the colors 1 .. k.
    Time O(n^2 + k m) for k colors, extra space O(n).
    """
    n = len(adj)
    c = [0] * n
    in_u = [True] * n
    u_size = n
    k = 0  # @line L1
    where = [0] * n  # 0: not in U, 1: in P, 2: in W
    d_w = [0] * n  # neighbours in W
    d_p = [0] * n  # neighbours in P
    while u_size > 0:  # @line L2
        k += 1  # @line L3: P <- U, W <- empty
        for x in range(n):
            where[x] = 1 if in_u[x] else 0
            d_w[x] = 0
        for x in range(n):
            d_p[x] = sum(1 for y in adj[x] if in_u[y])
        p_size = u_size
        v = -1  # @line L4: most neighbours in U (= in P now), smaller index first
        for x in range(n):
            if where[x] == 1 and (v < 0 or d_p[x] > d_p[v]):
                v = x
        while True:  # @line L5
            c[v] = k  # @line L6
            where[v] = 0
            in_u[v] = False
            u_size -= 1
            p_size -= 1
            for y in adj[v]:
                d_p[y] -= 1
            for x in adj[v]:  # @line L7
                if where[x] == 1:
                    where[x] = 2
                    p_size -= 1
                    for y in adj[x]:
                        d_p[y] -= 1
                        d_w[y] += 1
            if p_size == 0:  # @line L8
                break
            v = -1  # @line L9
            for x in range(n):
                if where[x] == 1 and (
                    v < 0
                    or d_w[x] > d_w[v]
                    or (d_w[x] == d_w[v] and d_p[x] < d_p[v])
                ):
                    v = x
    return c  # @line L10
