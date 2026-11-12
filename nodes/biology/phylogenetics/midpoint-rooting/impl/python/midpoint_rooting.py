# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midpoint-rooting/. The authors are listed in prov/7VS8ZC.jsonl.

"""Midpoint rooting of an unrooted tree with branch lengths.

A tree is a dict that maps each vertex to a dict {neighbour: length}. Lengths
are non-negative numbers (int, Fraction or float); use int or Fraction for
exact answers. Leaves are the vertices of degree 1.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Hashable

Tree = dict[Hashable, dict[Hashable, object]]


def distances_from(tree: Tree, s: Hashable) -> tuple[dict, dict]:
    """Distances and parent pointers from s, by an explicit-stack traversal."""
    dist = {s: 0}
    parent = {s: None}
    stack = [s]
    while stack:
        v = stack.pop()
        for w, length in tree[v].items():
            if w not in dist:
                dist[w] = dist[v] + length
                parent[w] = v
                stack.append(w)
    return dist, parent


def leaves(tree: Tree) -> list[Hashable]:
    return [v for v, nb in tree.items() if len(nb) == 1]


def midpoint(tree: Tree) -> tuple[Hashable, Hashable, object, object]:
    """Return (u, v, t, D): the root is on edge u-v at distance t from u, and D is the diameter.

    When t = 0 the root is the vertex u itself.
    """
    ls = leaves(tree)
    if len(ls) < 2:
        raise ValueError("need at least two leaves")
    da, _ = distances_from(tree, ls[0])  # @line L1
    b = max(ls, key=lambda x: da[x])  # @line L2 (a leaf farthest from ls[0])
    db, parent = distances_from(tree, b)  # @line L3
    c = max(ls, key=lambda x: db[x])  # @line L4 (a leaf farthest from b)
    D = db[c]  # @line L5
    half = D / 2 if isinstance(D, float) else Fraction(D) / 2
    if c == b:  # every leaf is at distance 0 from b
        return b, b, 0, D
    x = c  # @line L6 (walk from c towards b)
    while db[parent[x]] > half:  # @line L7
        x = parent[x]
    u = parent[x]  # @line L8 (db[u] <= half < db[x])
    return u, x, half - db[u], D


def root_tree(tree: Tree, u: Hashable, v: Hashable, t) -> tuple[Hashable, dict, dict]:
    """Insert the root at distance t from u on edge u-v. Return (root, children, length).

    If t = 0 the root is u. Otherwise a new vertex "ROOT" is placed on the edge.
    length[w] is the length of the edge from w to its parent.
    """
    children: dict = {}
    length: dict = {}
    if t == 0:
        root = u
        starts = [(w, u, tree[u][w]) for w in tree[u]]
    else:
        root = "ROOT"
        starts = [(u, root, t), (v, root, tree[u][v] - t)]
    children[root] = []
    stack = list(starts)
    while stack:
        w, p, ell = stack.pop()
        children[p].append(w)
        length[w] = ell
        children[w] = []
        for z, lz in tree[w].items():
            if z != p and not (root == "ROOT" and {w, z} == {u, v}):
                stack.append((z, w, lz))
    return root, children, length


def clusters(root: Hashable, children: dict) -> set[frozenset]:
    """The clusters of the internal vertices of a rooted tree, the root excluded."""
    order = []
    stack = [root]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(children[v])
    below: dict = {}
    out = set()
    for v in reversed(order):
        if children[v]:
            below[v] = frozenset().union(*(below[c] for c in children[v]))
            if v != root:
                out.add(below[v])
        else:
            below[v] = frozenset([v])
    return out
