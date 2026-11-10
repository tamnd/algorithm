# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mst-preorder-walk-tsp/. The authors are listed in prov/98SJR0.jsonl.

from typing import Sequence


def prim_parents(cost: Sequence[Sequence[float]], root: int = 0) -> tuple[list[int], list[int]]:
    """Prim's algorithm on the complete graph with an array, in O(n^2) time.

    Return (parent, order): parent[v] is the tree parent of v (-1 for the root), and order lists
    the vertices in the order in which Prim adds them. Ties go to the smaller vertex number.
    """
    n = len(cost)
    in_tree = [False] * n
    key: list[float | None] = [None] * n
    parent = [-1] * n
    order: list[int] = []
    key[root] = 0
    for _ in range(n):
        u = -1
        for v in range(n):
            kv = key[v]
            if not in_tree[v] and kv is not None:
                ku = key[u] if u >= 0 else None
                if ku is None or kv < ku:
                    u = v
        in_tree[u] = True
        order.append(u)
        for v in range(n):
            kv = key[v]
            if not in_tree[v] and (kv is None or cost[u][v] < kv):
                key[v] = cost[u][v]
                parent[v] = u
    return parent, order


def mst_preorder_tour(cost: Sequence[Sequence[float]], root: int = 0) -> list[int]:
    """Return the preorder of a minimum spanning tree rooted at root, as a tour.

    Precondition: cost is a symmetric n x n matrix of non-negative numbers. With the triangle
    inequality the tour costs at most 2 (1 - 1/n) OPT. The children of a vertex are visited in
    the order in which Prim adds them. Time O(n^2) and extra space O(n).
    """
    n = len(cost)
    if n == 0:
        return []
    parent, order = prim_parents(cost, root)  # @line L1
    children: list[list[int]] = [[] for _ in range(n)]
    for v in order:
        if parent[v] >= 0:
            children[parent[v]].append(v)
    tour: list[int] = []  # @line L2
    stack = [root]
    while stack:  # @line L3
        v = stack.pop()  # @line L4
        tour.append(v)  # @line L5
        stack.extend(reversed(children[v]))  # @line L6
    return tour  # @line L7


def tour_cost(cost: Sequence[Sequence[float]], tour: list[int]) -> float:
    """The cost of the closed tour, including the edge from the last vertex back to the first."""
    k = len(tour)
    return sum(cost[tour[i]][tour[(i + 1) % k]] for i in range(k)) if k > 1 else 0
