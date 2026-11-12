# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stepwise-addition/. The authors are listed in prov/3VNTRD.jsonl.

"""Stepwise addition: build an unrooted binary tree by adding one taxon at a time at the
position that gives the best score so far.

A tree is an adjacency map {vertex: set of neighbors}. Taxa are the integers 0 .. n - 1 and
are leaves. Internal vertices get the ids n, n + 1, ... in the order they are made.
The score here is the Fitch parsimony length of DNA or other characters, a number to minimize,
but any function of the partial tree can take its place.
"""

import random
from typing import Callable, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple

Tree = Dict[int, Set[int]]


def copy_tree(tree: Tree) -> Tree:
    """Return a deep copy of the adjacency map."""
    return {v: set(nb) for v, nb in tree.items()}


def edges(tree: Tree) -> List[Tuple[int, int]]:
    """Return each edge once, as (x, y) with x < y, in a fixed order."""
    return sorted((x, y) for x in tree for y in tree[x] if x < y)


def insert_leaf(tree: Tree, edge: Tuple[int, int], leaf: int, new: int) -> Tree:
    """Return a copy of the tree with the edge subdivided by vertex new, and leaf joined to it."""
    x, y = edge
    t = copy_tree(tree)
    t[x].discard(y)
    t[y].discard(x)
    t[new] = {x, y, leaf}
    t[x].add(new)
    t[y].add(new)
    t[leaf] = {new}
    return t


def fitch_score(tree: Tree, n: int, seqs: Sequence[str]) -> int:
    """Fitch parsimony length of the taxa in the tree. O(k m) for k leaves and m sites."""
    root = min(v for v in tree if v < n)
    parent = {root: -1}
    order = [root]
    stack = [root]
    while stack:
        v = stack.pop()
        for w in tree[v]:
            if w not in parent:
                parent[w] = v
                order.append(w)
                stack.append(w)
    total = 0
    for j in range(len(seqs[0])):
        sets: Dict[int, Set[str]] = {}
        for v in reversed(order[1:]):
            kids = [w for w in tree[v] if parent.get(w) == v]
            if not kids:
                sets[v] = {seqs[v][j]}
                continue
            a, b = sets[kids[0]], sets[kids[1]]
            if a & b:
                sets[v] = a & b
            else:
                sets[v] = a | b
                total += 1
        if seqs[root][j] not in sets[order[1]]:
            total += 1
    return total


def stepwise_addition(order: Sequence[int], n: int, score: Callable[[Tree], int]) -> Tuple[Tree, int]:
    """Add the taxa in the given order, each at the edge that gives the lowest score.

    Precondition: order lists at least 3 distinct taxa from 0 .. n - 1. Ties go to the first
    edge in sorted order. Step k tries 2k - 5 edges, so a run scores 3 + 5 + ... + (2n - 5)
    = (n - 2)^2 - 1 candidate trees over k = 4 .. n.
    """
    a, b, c = order[0], order[1], order[2]
    tree: Tree = {a: {n}, b: {n}, c: {n}, n: {a, b, c}}  # @line L1
    best_score = score(tree)
    nxt = n + 1
    for leaf in order[3:]:  # @line L2
        best: Optional[Tree] = None  # @line L3
        best_score = None
        for e in edges(tree):  # @line L4
            cand = insert_leaf(tree, e, leaf, nxt)  # @line L5
            s = score(cand)
            if best_score is None or s < best_score:  # @line L6
                best, best_score = cand, s
        tree = best  # @line L7
        nxt += 1
    return tree, best_score  # @line L8


def random_addition(n: int, score: Callable[[Tree], int], replicates: int, rng: random.Random) -> Tuple[Tree, int]:
    """Run stepwise addition with random taxon orders and keep the best tree."""
    best: Optional[Tuple[Tree, int]] = None
    for _ in range(replicates):
        order = list(range(n))
        rng.shuffle(order)
        t, s = stepwise_addition(order, n, score)
        if best is None or s < best[1]:
            best = (t, s)
    assert best is not None
    return best


def all_trees_by_addition(n: int) -> List[Tree]:
    """Return all (2n - 5)!! unrooted binary trees on taxa 0 .. n - 1 by full addition."""
    trees = [{0: {n}, 1: {n}, 2: {n}, n: {0, 1, 2}}]
    for leaf in range(3, n):
        new = n + leaf - 2
        trees = [insert_leaf(t, e, leaf, new) for t in trees for e in edges(t)]
    return trees


def topology(tree: Tree, n: int) -> FrozenSet[FrozenSet[int]]:
    """Return the set of nontrivial splits, each as the side without the smallest taxon."""
    leaves = sorted(v for v in tree if v < n)
    root = leaves[0]
    parent = {root: -1}
    order = [root]
    stack = [root]
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
    k = len(leaves)
    return frozenset(frozenset(below[v]) for v in order[1:] if 2 <= len(below[v]) <= k - 2)
