# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subtree-prune-and-regraft/. The authors are listed in prov/PCRYBM.jsonl.

"""Subtree prune and regraft (SPR) on unrooted binary trees, and a hill climb that uses it.

A tree is an adjacency map {vertex: set of neighbors}. The leaves are 0 .. n - 1 (degree 1)
and every other vertex has degree 3. The topology of a tree is the set of its nontrivial
splits, each stored as the side that does not hold leaf 0.

An SPR move cuts an edge {u, v} with u internal. The part that holds v is the pruned subtree.
The vertex u now has degree 2, so it is suppressed: its two other neighbors are joined. Then
a new vertex subdivides an edge of the rest of the tree and is joined to v.
"""

from typing import Callable, Dict, FrozenSet, List, Set, Tuple

Tree = Dict[int, Set[int]]
Topology = FrozenSet[FrozenSet[int]]


def copy_tree(tree: Tree) -> Tree:
    """Return a deep copy of the adjacency map."""
    return {v: set(nb) for v, nb in tree.items()}


def splits(tree: Tree, n: int) -> List[FrozenSet[int]]:
    """Return, for each edge, the side that does not hold leaf 0. Explicit stack, O(n^2)."""
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
    """Return the set of nontrivial splits of the tree."""
    return frozenset(s for s in splits(tree, n) if 2 <= len(s) <= n - 2)


def component(tree: Tree, start: int) -> Set[int]:
    """Return the vertices reachable from start."""
    seen = {start}
    stack = [start]
    while stack:
        v = stack.pop()
        for w in tree[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def spr_neighbors(tree: Tree, n: int) -> List[Tree]:
    """Return the distinct trees one SPR move away from the tree, without the tree itself.

    For n >= 4 there are exactly 2(n - 3)(2n - 7) of them (Allen and Steel 2001). The loop
    tries all O(n) cuts and all O(n) regraft edges, O(n^2) moves, and removes duplicates by
    topology at O(n^2) each, so O(n^4) time in total.
    """
    seen = {topology(tree, n)}
    out = []
    for u in tree:  # @line L1
        if len(tree[u]) != 3:
            continue
        for v in tree[u]:
            t = copy_tree(tree)  # @line L2
            t[u].discard(v)
            t[v].discard(u)
            x, y = t[u]  # @line L3
            t[x].discard(u)
            t[y].discard(u)
            t[x].add(y)
            t[y].add(x)
            del t[u]
            rest = component(t, x)
            for p in rest:  # @line L4
                for q in t[p]:
                    if p < q:
                        t2 = copy_tree(t)  # @line L5
                        t2[p].discard(q)
                        t2[q].discard(p)
                        t2[u] = {p, q, v}
                        t2[p].add(u)
                        t2[q].add(u)
                        t2[v].add(u)
                        key = topology(t2, n)  # @line L6
                        if key not in seen:
                            seen.add(key)
                            out.append(t2)
    return out


def spr_hill_climb(tree: Tree, n: int, score: Callable[[Tree], int]) -> Tuple[Tree, int]:
    """Steepest-descent local search with SPR moves. Return a tree that no SPR move improves."""
    best = tree
    best_score = score(best)
    while True:
        cand, cand_score = None, best_score
        for t in spr_neighbors(best, n):
            s = score(t)
            if s < cand_score:
                cand, cand_score = t, s
        if cand is None:
            return best, best_score
        best, best_score = cand, cand_score


def all_trees(n: int) -> List[Tree]:
    """Return all (2n - 5)!! unrooted binary trees on leaves 0 .. n - 1, for n >= 3."""
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
