# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/day-algorithm/. The authors are listed in prov/WDM8Q2.jsonl.

"""Day's cluster-table algorithm for the Robinson-Foulds distance.

A rooted tree is a pair (root, children): children maps each internal vertex
to the list of its children, and a vertex that is not a key (or has an empty
list) is a leaf. Leaves are the taxon names. Each internal vertex must have at
least two children.

An unrooted tree is a dict that maps each vertex to the list of its
neighbours; its leaves (degree 1) are the taxa. Internal vertices have degree
at least 3.

All traversals use explicit stacks, so the cost is O(n) time and space and
deep trees do not hit the recursion limit.
"""

from __future__ import annotations

from typing import Hashable

Rooted = tuple[Hashable, dict[Hashable, list[Hashable]]]
Unrooted = dict[Hashable, list[Hashable]]


def postorder(root: Hashable, children: dict) -> list[Hashable]:
    """The vertices in postorder (children left to right, then the parent)."""
    out = []
    stack = [(root, False)]
    while stack:
        v, done = stack.pop()
        if done or not children.get(v):
            out.append(v)
        else:
            stack.append((v, True))
            for c in reversed(children[v]):
                stack.append((c, False))
    return out


def cluster_table(t1: Rooted) -> tuple[dict[Hashable, int], list, int]:
    """Number the leaves of t1 in postorder and build the table X.

    Return (num, X, c1): num maps each leaf to its number, X[i] is the interval
    (lo, hi) stored in row i or None, and c1 is the number of internal vertices.
    """
    root, ch = t1
    order = postorder(root, ch)
    num: dict[Hashable, int] = {}
    lo: dict[Hashable, int] = {}
    hi: dict[Hashable, int] = {}
    for v in order:  # @line L1 (number the leaves left to right)
        if not ch.get(v):
            num[v] = lo[v] = hi[v] = len(num)
    n = len(num)
    X: list = [None] * n  # @line L2
    last_child = {root}
    for v in ch:
        if ch[v]:
            last_child.add(ch[v][-1])
    c1 = 0
    for v in order:  # @line L3
        kids = ch.get(v)
        if not kids:
            continue
        if len(kids) < 2:
            raise ValueError("an internal vertex has fewer than two children")
        c1 += 1
        lo[v], hi[v] = lo[kids[0]], hi[kids[-1]]  # @line L4 (the cluster of v is [lo, hi])
        if v in last_child:  # @line L5
            row = lo[v]
        else:  # @line L6
            row = hi[v]
        if X[row] is not None:
            raise AssertionError("two clusters in one row")  # cannot happen, see the proof
        X[row] = (lo[v], hi[v])
    return num, X, c1


def shared_clusters(t2: Rooted, num: dict, X: list) -> tuple[int, int]:
    """Count the internal vertices of t2 whose cluster is in the table. Return (shared, c2)."""
    root, ch = t2
    lo: dict[Hashable, int] = {}
    hi: dict[Hashable, int] = {}
    size: dict[Hashable, int] = {}
    shared = c2 = 0  # @line L7
    seen = 0
    for v in postorder(root, ch):  # @line L8
        kids = ch.get(v)
        if not kids:
            if v not in num:
                raise ValueError(f"leaf {v!r} is not in the first tree")
            lo[v] = hi[v] = num[v]
            size[v] = 1
            seen += 1
            continue
        if len(kids) < 2:
            raise ValueError("an internal vertex has fewer than two children")
        c2 += 1
        lo[v] = min(lo[c] for c in kids)  # @line L9
        hi[v] = max(hi[c] for c in kids)
        size[v] = sum(size[c] for c in kids)
        a, b = lo[v], hi[v]
        if b - a + 1 == size[v] and (X[a] == (a, b) or X[b] == (a, b)):  # @line L10
            shared += 1
    if seen != len(num):
        raise ValueError("the two trees have different leaf sets")
    return shared, c2


def rf_rooted(t1: Rooted, t2: Rooted) -> int:
    """The Robinson-Foulds distance of two rooted trees: the size of the symmetric difference of their cluster sets."""
    num, X, c1 = cluster_table(t1)
    shared, c2 = shared_clusters(t2, num, X)
    return (c1 - shared) + (c2 - shared)  # @line L11 (the root cluster is shared and adds 0)


def root_at_leaf(tree: Unrooted, r: Hashable) -> Rooted:
    """Root an unrooted tree at the neighbour u of leaf r and drop r.

    The clusters of the result are the sides without r of the splits of the
    tree, except the trivial split of r, whose side is the root cluster.
    """
    if len(tree[r]) != 1:
        raise ValueError(f"{r!r} is not a leaf")
    u = tree[r][0]
    children: dict[Hashable, list[Hashable]] = {}
    stack = [(u, r)]
    while stack:
        v, p = stack.pop()
        kids = [w for w in tree[v] if w != p]
        if kids:
            children[v] = kids
            stack.extend((w, v) for w in kids)
    return u, children


def rf_unrooted(tree1: Unrooted, tree2: Unrooted) -> int:
    """The Robinson-Foulds distance of two unrooted trees: the size of the symmetric difference of their split sets."""
    leaves1 = sorted((v for v, nb in tree1.items() if len(nb) == 1), key=repr)
    if len(leaves1) < 3:
        return 0
    r = leaves1[0]
    if r not in tree2 or len(tree2[r]) != 1:
        raise ValueError("the two trees have different leaf sets")
    return rf_rooted(root_at_leaf(tree1, r), root_at_leaf(tree2, r))


# -- the reference: direct comparison of split sets -----------------------------


def splits_direct(tree: Unrooted) -> set[frozenset]:
    """Every nontrivial split, as the side that does not hold the smallest leaf. O(n^2) time."""
    leaves = sorted((v for v, nb in tree.items() if len(nb) == 1), key=repr)
    r = leaves[0]
    out = set()
    for u in tree:
        for v in tree[u]:
            side = set()
            seen = {u, v}
            stack = [v]
            while stack:
                w = stack.pop()
                if len(tree[w]) == 1:
                    side.add(w)
                for z in tree[w]:
                    if z not in seen:
                        seen.add(z)
                        stack.append(z)
            if r not in side and 2 <= len(side) <= len(leaves) - 2:
                out.add(frozenset(side))
    return out


def rf_direct(tree1: Unrooted, tree2: Unrooted) -> int:
    return len(splits_direct(tree1) ^ splits_direct(tree2))


def clusters_direct(t: Rooted) -> set[frozenset]:
    root, ch = t
    out = set()
    for v in ch:
        if ch[v]:
            leaves = set()
            stack = [v]
            while stack:
                w = stack.pop()
                if ch.get(w):
                    stack.extend(ch[w])
                else:
                    leaves.add(w)
            out.add(frozenset(leaves))
    return out
