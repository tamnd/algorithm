# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-mst-method/. The authors are listed in prov/AA7K7S.jsonl.

from typing import Callable

# A cut chooser gets the tree label of each vertex and the labels of the
# trees that some edge leaves, and returns a set of tree labels S. The cut is
# (union of the trees in S, the rest). Any such set respects A.
CutChooser = Callable[[list[int], list[int]], set[int]]


def first_open_tree(comp: list[int], open_trees: list[int]) -> set[int]:
    """The default choice: the open tree with the smallest label."""
    return {min(open_trees)}


def generic_mst(
    n: int, edges: list[tuple[int, int, float]], choose_cut: CutChooser = first_open_tree
) -> list[int]:
    """Return the indices of the edges of a minimum spanning forest, in the order added.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge. Weights may tie (a light edge is then the one with the least
    (w, i)); the graph may be disconnected. choose_cut is the free choice of
    the method: it must return a set of tree labels that some edge leaves.

    Cost: at most n - 1 iterations of O(n + m) each, so O(n (n + m)) time
    besides choose_cut; O(n + m) extra space.
    """
    a: list[int] = []  # @line L1
    while True:
        comp = _labels(n, edges, a)
        open_trees = sorted({comp[x] for u, v, _ in edges if comp[u] != comp[v] for x in (u, v)})
        if not open_trees:  # @line L2
            return a  # @line L6
        s = choose_cut(comp, open_trees)  # @line L3
        light = None
        for i, (u, v, w) in enumerate(edges):  # @line L4
            if (comp[u] in s) != (comp[v] in s):
                if light is None or (w, i) < (edges[light][2], light):
                    light = i
        if light is None:
            raise ValueError("choose_cut returned a cut that no edge crosses")
        a.append(light)  # @line L5


def _labels(n: int, edges: list[tuple[int, int, float]], a: list[int]) -> list[int]:
    """Label each vertex with the smallest vertex of its tree in (V, a)."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for i in a:
        u, v, _ = edges[i]
        adj[u].append(v)
        adj[v].append(u)
    comp = [-1] * n
    for s in range(n):
        if comp[s] < 0:
            comp[s] = s
            stack = [s]
            while stack:
                x = stack.pop()
                for y in adj[x]:
                    if comp[y] < 0:
                        comp[y] = s
                        stack.append(y)
    return comp
