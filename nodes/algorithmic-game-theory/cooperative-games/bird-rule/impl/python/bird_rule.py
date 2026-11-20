# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bird-rule/. The authors are listed in prov/7MY1TF.jsonl.
"""Bird's rule for minimum cost spanning tree games (Bird 1976).

The input is a symmetric cost matrix c on the vertices 0, 1, ..., n. Vertex 0 is the
source and vertices 1 to n are the players. The rule grows a tree from the source with
Prim's algorithm and charges each player the cost of the edge by which the tree reaches
it. The charges add up to the cost of a minimum spanning tree, and they are in the core
of the game c(S) = cost of a minimum spanning tree on S and the source.

Ties are broken by the smallest vertex index, so the output is deterministic. The time is
O(n^2) and the extra space is O(n).
"""


def _check(cost):
    size = len(cost)
    if size == 0:
        raise ValueError("the cost matrix must contain the source")
    for row in cost:
        if len(row) != size:
            raise ValueError("the cost matrix must be square")
    for u in range(size):
        for v in range(u + 1, size):
            if cost[u][v] != cost[v][u]:
                raise ValueError("the cost matrix must be symmetric")
    return size - 1


def bird(cost):
    """Return (x, parent): x[v] is the charge of player v and parent[v] the vertex
    that connects v in the Prim tree from the source 0. x[0] = 0 and parent[0] = None."""
    n = _check(cost)
    dist = [None] * (n + 1)
    parent = [None] * (n + 1)
    for v in range(1, n + 1):  # @line L1
        dist[v] = cost[0][v]
        parent[v] = 0
    in_tree = [False] * (n + 1)  # @line L2
    in_tree[0] = True
    x = [0] * (n + 1)
    for _ in range(n):  # @line L3
        v = None
        for w in range(1, n + 1):  # @line L4
            if not in_tree[w] and (v is None or dist[w] < dist[v]):
                v = w
        x[v] = dist[v]  # @line L5
        in_tree[v] = True
        for w in range(1, n + 1):  # @line L6
            if not in_tree[w] and cost[v][w] < dist[w]:
                dist[w] = cost[v][w]
                parent[w] = v
    return x, parent  # @line L7


def coalition_cost(cost, coalition):
    """c(S): the cost of a minimum spanning tree on S and the source, by Prim's algorithm."""
    nodes = [0] + sorted(set(coalition))
    best = {v: cost[0][v] for v in nodes[1:]}
    total = 0
    while best:
        v = min(best, key=lambda w: (best[w], w))
        total += best.pop(v)
        for w in best:
            if cost[v][w] < best[w]:
                best[w] = cost[v][w]
    return total
