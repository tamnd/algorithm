# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-bisection-and-reconnection/. The authors are listed in prov/S23RH6.jsonl.

"""Tree bisection and reconnection (TBR) on unrooted binary trees.

A tree is an adjacency map {vertex: set of neighbors}. The leaves are 0 .. n - 1 (degree 1)
and every other vertex has degree 3. The topology of a tree is the set of its nontrivial
splits, each stored as the side that does not hold leaf 0.

A TBR move deletes an edge {u, v}. Each of the two parts that remain is made binary again:
an internal end vertex of degree 2 is suppressed. Then the parts are joined by a new edge.
Its end in a part is a new vertex on an edge of that part, or the leaf itself when the part
is one leaf.
"""

from typing import Callable, Dict, FrozenSet, List, Set, Tuple

Tree = Dict[int, Set[int]]
Topology = FrozenSet[FrozenSet[int]]
Attach = Tuple[int, int]  # an edge (p, q) to subdivide, or (leaf, -1) for a lone leaf


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


def gamma(tree: Tree, n: int) -> int:
    """Return the sum of |A| * |B| over the nontrivial splits A|B (Humphries and Wu 2013)."""
    return sum(len(s) * (n - len(s)) for s in topology(tree, n))


def _component(tree: Tree, start: int) -> Set[int]:
    seen = {start}
    stack = [start]
    while stack:
        v = stack.pop()
        for w in tree[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def _suppress(t: Tree, u: int, n: int) -> List[Attach]:
    """Make the part of u binary again and return its attachment points."""
    if u < n:  # a lone leaf
        return [(u, -1)]
    x, y = t[u]
    t[x].discard(u)
    t[y].discard(u)
    t[x].add(y)
    t[y].add(x)
    del t[u]
    part = _component(t, x)
    return [(p, q) for p in part for q in t[p] if p < q]


def _join(t: Tree, a: Attach, b: Attach, u: int, v: int) -> Tree:
    """Join attachment point a (new vertex u) to attachment point b (new vertex v)."""
    t2 = copy_tree(t)
    ends = []
    for (p, q), w in ((a, u), (b, v)):
        if q == -1:
            ends.append(p)
        else:
            t2[p].discard(q)
            t2[q].discard(p)
            t2[w] = {p, q}
            t2[p].add(w)
            t2[q].add(w)
            ends.append(w)
    t2[ends[0]].add(ends[1])
    t2[ends[1]].add(ends[0])
    return t2


def tbr_neighbors(tree: Tree, n: int) -> List[Tree]:
    """Return the distinct trees one TBR move away from the tree, without the tree itself.

    There are 4 * gamma(T) - (4n - 2)(n - 3) of them for n >= 4 (Humphries and Wu 2013).
    The loop tries O(n) bisections and O(n^2) reconnections of each, O(n^3) moves, and
    removes duplicates by topology at O(n^2) each, so O(n^5) time.
    """
    seen = {topology(tree, n)}
    out = []
    edges = [(u, v) for u in tree for v in tree[u] if u < v]
    for u, v in edges:  # @line L1
        t = copy_tree(tree)  # @line L2
        t[u].discard(v)
        t[v].discard(u)
        side_u = _suppress(t, u, n)  # @line L3
        side_v = _suppress(t, v, n)
        for a in side_u:  # @line L4
            for b in side_v:
                t2 = _join(t, a, b, u, v)  # @line L5
                key = topology(t2, n)  # @line L6
                if key not in seen:
                    seen.add(key)
                    out.append(t2)
    return out


def tbr_hill_climb(tree: Tree, n: int, score: Callable[[Tree], int]) -> Tuple[Tree, int]:
    """Steepest-descent local search with TBR moves. Return a tree that no TBR move improves."""
    best = tree
    best_score = score(best)
    while True:
        cand, cand_score = None, best_score
        for t in tbr_neighbors(best, n):
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
