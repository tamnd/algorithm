# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-interchange/. The authors are listed in prov/57633W.jsonl.

"""Nearest-neighbor interchange (NNI) on unrooted binary trees, and a hill climb that uses it.

A tree is an adjacency map {vertex: set of neighbors}. The leaves are 0 .. n - 1 and have
degree 1. Every other vertex is internal and has degree 3. For n >= 4 leaves the tree has
n - 2 internal vertices, 2n - 3 edges and n - 3 internal edges.

The topology of a tree is the set of its nontrivial splits. Each split is stored as the side
that does not hold leaf 0. Two trees with the same leaf labels are the same unrooted tree
exactly when they have the same set of splits.
"""

from typing import Callable, Dict, FrozenSet, Iterator, List, Set, Tuple

Tree = Dict[int, Set[int]]
Topology = FrozenSet[FrozenSet[int]]


def copy_tree(tree: Tree) -> Tree:
    """Return a deep copy of the adjacency map."""
    return {v: set(nb) for v, nb in tree.items()}


def leaf_count(tree: Tree) -> int:
    """Return the number of leaves (vertices of degree 1)."""
    return sum(1 for nb in tree.values() if len(nb) == 1)


def splits(tree: Tree, n: int) -> List[FrozenSet[int]]:
    """Return the leaf set below each edge, seen from leaf 0, for all 2n - 3 edges.

    Each set is the side of the edge that does not hold leaf 0. Cost O(n^2) for the sets.
    Uses an explicit stack, so deep trees do not hit the recursion limit.
    """
    parent = {0: -1}
    order = [0]
    stack = [0]
    while stack:
        v = stack.pop()
        for w in tree[v]:
            if w not in parent:
                parent[w] = v
                order.append(w)
                stack.append(w)
    below: Dict[int, Set[int]] = {}
    for v in reversed(order):
        s = {v} if v < n else set()
        for w in tree[v]:
            if parent.get(w) == v:
                s |= below[w]
        below[v] = s
    return [frozenset(below[v]) for v in order[1:]]


def topology(tree: Tree, n: int) -> Topology:
    """Return the set of nontrivial splits (both sides with at least 2 leaves)."""
    return frozenset(s for s in splits(tree, n) if 2 <= len(s) <= n - 2)


def internal_edges(tree: Tree) -> Iterator[Tuple[int, int]]:
    """Yield each edge {u, v} with both ends internal, once, as (u, v) with u < v."""
    for u, nb in tree.items():
        if len(nb) == 3:
            for v in nb:
                if u < v and len(tree[v]) == 3:
                    yield u, v


def nni_neighbors(tree: Tree) -> List[Tree]:
    """Return the 2(n - 3) trees one NNI away from an unrooted binary tree.

    For each internal edge {u, v}, let a, b be the other neighbors of u and c, d the other
    neighbors of v. The two moves exchange b with c, and b with d. Cost O(n) per neighbor
    for the copy, so O(n^2) in total.
    """
    out = []
    for u, v in internal_edges(tree):  # @line L1
        a, b = sorted(tree[u] - {v})  # @line L2
        c, d = sorted(tree[v] - {u})
        for x in (c, d):  # @line L3
            t = copy_tree(tree)
            t[u].discard(b)  # @line L4
            t[b].discard(u)
            t[v].discard(x)
            t[x].discard(v)
            t[u].add(x)  # @line L5
            t[x].add(u)
            t[v].add(b)
            t[b].add(v)
            out.append(t)  # @line L6
    return out


def nni_hill_climb(tree: Tree, score: Callable[[Tree], int]) -> Tuple[Tree, int]:
    """Steepest-descent local search with NNI moves. Return a tree that no NNI improves.

    score is the objective to minimize, for example a parsimony length. Each round scores
    all 2(n - 3) neighbors and moves to the best one if it is strictly better. The score
    drops by at least 1 in each round when it is an integer, so the loop stops.
    """
    best = tree  # @line L7
    best_score = score(best)
    while True:  # @line L8
        cand = None
        cand_score = best_score
        for t in nni_neighbors(best):  # @line L9
            s = score(t)
            if s < cand_score:  # @line L10
                cand, cand_score = t, s
        if cand is None:  # @line L11
            return best, best_score  # @line L12
        best, best_score = cand, cand_score  # @line L13


def all_trees(n: int) -> List[Tree]:
    """Return all (2n - 5)!! unrooted binary trees on leaves 0 .. n - 1, for n >= 3.

    Built by inserting leaf k on each edge of each tree on the leaves 0 .. k - 1.
    """
    start: Tree = {0: {n}, 1: {n}, 2: {n}, n: {0, 1, 2}}
    trees = [start]
    for k in range(3, n):
        nxt = []
        for t in trees:
            new = max(t) + 1
            for x, y in [(x, y) for x in t for y in t[x] if x < y]:
                t2 = copy_tree(t)
                t2[x].discard(y)
                t2[y].discard(x)
                t2[new] = {x, y, k}
                t2[x].add(new)
                t2[y].add(new)
                t2[k] = {new}
                nxt.append(t2)
        trees = nxt
    return trees
