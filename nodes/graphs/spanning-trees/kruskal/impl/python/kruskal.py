# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kruskal/. The authors are listed in prov/1DB0HR.jsonl.


def kruskal(n: int, edges: list[tuple[int, int, float]]) -> list[int]:
    """Return the indices of the edges of a minimum spanning forest.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge of weight w. Weights may tie, the graph may be disconnected, and
    parallel edges and self-loops are allowed. Ties are broken by the edge
    index, so the result is deterministic. If the graph is connected, the
    result has n - 1 edges and is a minimum spanning tree.

    Cost: O(m log m) for the sort plus O(m alpha(n)) for the union-find,
    where m = len(edges); O(n + m) extra space.
    """
    forest: list[int] = []  # @line L1
    parent = list(range(n))  # @line L2
    size = [1] * n

    def find_set(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path halving
            x = parent[x]
        return x

    order = sorted(range(len(edges)), key=lambda i: (edges[i][2], i))  # @line L3
    for i in order:  # @line L4
        u, v, _ = edges[i]
        ru, rv = find_set(u), find_set(v)
        if ru != rv:  # @line L5
            forest.append(i)  # @line L6
            if size[ru] < size[rv]:  # @line L7
                ru, rv = rv, ru
            parent[rv] = ru
            size[ru] += size[rv]
    return forest  # @line L8
