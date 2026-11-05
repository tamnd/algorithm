# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reverse-delete/. The authors are listed in prov/WC91FF.jsonl.


def reverse_delete(n: int, edges: list[tuple[int, int, float]]) -> list[int]:
    """Return the indices of the edges of a minimum spanning forest, in increasing order.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge of weight w. Weights may be negative and may tie, the graph may be
    disconnected, and parallel edges and self-loops are allowed. The edges
    are scanned by non-increasing weight, and among equal weights by
    decreasing index. If the graph is connected, the result has n - 1 edges
    and is a minimum spanning tree.

    Cost: O(m log m) for the sort plus O(n + m) for each of the m
    connectivity tests, so O(m (n + m)) time in the worst case, and
    O(n + m) extra space, where m = len(edges).
    """
    alive = [True] * len(edges)  # @line L1
    adj: list[list[int]] = [[] for _ in range(n)]
    for i, (u, v, _) in enumerate(edges):
        adj[u].append(i)
        if v != u:
            adj[v].append(i)

    def connected_without(s: int, t: int, skip: int) -> bool:
        """Is there a path from s to t that uses only live edges other than skip?"""
        if s == t:
            return True
        seen = [False] * n
        seen[s] = True
        stack = [s]
        while stack:
            x = stack.pop()
            for i in adj[x]:
                if i == skip or not alive[i]:
                    continue
                a, b, _ = edges[i]
                y = b if a == x else a
                if not seen[y]:
                    if y == t:
                        return True
                    seen[y] = True
                    stack.append(y)
        return False

    order = sorted(range(len(edges)), key=lambda i: (edges[i][2], i), reverse=True)  # @line L2
    for i in order:  # @line L3
        u, v, _ = edges[i]
        if connected_without(u, v, i):  # @line L4
            alive[i] = False  # @line L5
    return [i for i in range(len(edges)) if alive[i]]  # @line L6
