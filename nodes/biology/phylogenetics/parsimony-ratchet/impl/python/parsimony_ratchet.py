# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parsimony-ratchet/. The authors are listed in prov/GM2NX0.jsonl.

"""The parsimony ratchet of Nixon (1999) with TBR branch swapping and weighted Fitch scoring.

A tree is an adjacency map {vertex: set of neighbors} on n >= 4 taxa 0 .. n - 1 (the leaves,
degree 1); every other vertex has degree 3. seqs[i] is the character string of taxon i, all
of the same length m. A weight vector w gives a positive integer weight w[j] to character j.
The length of a tree is sum_j w[j] * (Fitch changes of character j on the tree).
"""

import random
from typing import Dict, Iterator, List, Optional, Sequence, Set, Tuple

Tree = Dict[int, Set[int]]


def copy_tree(tree: Tree) -> Tree:
    return {v: set(nb) for v, nb in tree.items()}


def fitch_changes(tree: Tree, seqs: Sequence[str]) -> List[int]:
    """Return the Fitch number of changes of each character. O(n m) time, explicit stack."""
    n = len(seqs)
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
    kids = {v: [w for w in tree[v] if parent.get(w) == v] for v in order}
    out = []
    for j in range(len(seqs[0])):
        sets: Dict[int, Set[str]] = {}
        c = 0
        for v in reversed(order[1:]):
            if v < n:
                sets[v] = {seqs[v][j]}
                continue
            a, b = sets[kids[v][0]], sets[kids[v][1]]
            if a & b:
                sets[v] = a & b
            else:
                sets[v] = a | b
                c += 1
        if seqs[0][j] not in sets[order[1]]:
            c += 1
        out.append(c)
    return out


def length(tree: Tree, seqs: Sequence[str], w: Sequence[int]) -> int:
    """Weighted parsimony length of the tree."""
    return sum(wi * ci for wi, ci in zip(w, fitch_changes(tree, seqs)))


def _component(tree: Tree, start: int) -> Set[int]:
    seen = {start}
    stack = [start]
    while stack:
        v = stack.pop()
        for x in tree[v]:
            if x not in seen:
                seen.add(x)
                stack.append(x)
    return seen


def _suppress(t: Tree, u: int, n: int) -> List[Tuple[int, int]]:
    if u < n:
        return [(u, -1)]
    x, y = t[u]
    t[x].discard(u)
    t[y].discard(u)
    t[x].add(y)
    t[y].add(x)
    del t[u]
    part = _component(t, x)
    return [(p, q) for p in part for q in t[p] if p < q]


def tbr_moves(tree: Tree, n: int) -> Iterator[Tree]:
    """Yield the result of every TBR move (with repeats, and with the tree itself).

    There are O(n^3) moves and each costs O(n) to build.
    """
    for u, v in [(u, v) for u in tree for v in tree[u] if u < v]:
        t = copy_tree(tree)
        t[u].discard(v)
        t[v].discard(u)
        side_u = _suppress(t, u, n)
        side_v = _suppress(t, v, n)
        for a in side_u:
            for b in side_v:
                t2 = copy_tree(t)
                ends = []
                for (p, q), z in ((a, u), (b, v)):
                    if q == -1:
                        ends.append(p)
                    else:
                        t2[p].discard(q)
                        t2[q].discard(p)
                        t2[z] = {p, q}
                        t2[p].add(z)
                        t2[q].add(z)
                        ends.append(z)
                t2[ends[0]].add(ends[1])
                t2[ends[1]].add(ends[0])
                yield t2


def tbr_search(tree: Tree, seqs: Sequence[str], w: Sequence[int]) -> Tuple[Tree, int]:
    """Steepest-descent TBR search under weights w, holding one tree.

    Returns a tree that no TBR move makes shorter under w, and its length.
    """
    n = len(seqs)
    best, best_len = tree, length(tree, seqs, w)
    while True:
        cand: Optional[Tree] = None
        cand_len = best_len
        for t in tbr_moves(best, n):
            s = length(t, seqs, w)
            if s < cand_len:
                cand, cand_len = t, s
        if cand is None:
            return best, best_len
        best, best_len = cand, cand_len


def stepwise_start(seqs: Sequence[str], w: Sequence[int], rng: random.Random) -> Tree:
    """A random-addition-sequence Wagner tree: add taxa in random order at their best edge."""
    n = len(seqs)
    order = list(range(n))
    rng.shuffle(order)
    order.remove(0)
    order.insert(0, 0)  # keep taxon 0 in the tree so that fitch_changes can root there
    a, b, c = order[:3]
    tree: Tree = {a: {n}, b: {n}, c: {n}, n: {a, b, c}}
    nxt = n + 1
    for k in range(3, n):
        leaf = order[k]
        best, best_len = None, None
        for x, y in sorted((x, y) for x in tree for y in tree[x] if x < y):
            t = copy_tree(tree)
            t[x].discard(y)
            t[y].discard(x)
            t[nxt] = {x, y, leaf}
            t[x].add(nxt)
            t[y].add(nxt)
            t[leaf] = {nxt}
            s = length(t, seqs, w)  # Fitch reads only the taxa already in the tree
            if best_len is None or s < best_len:
                best, best_len = t, s
        tree = best
        nxt += 1
    return tree


def parsimony_ratchet(
    seqs: Sequence[str],
    iterations: int,
    fraction: float,
    rng: random.Random,
    start: Optional[Tree] = None,
) -> Tuple[Tree, int]:
    """Nixon's ratchet. Return the shortest tree found under unit weights and its length.

    Each iteration doubles the weight of a random subset of the characters (each one with
    probability fraction), runs a TBR search under the perturbed weights from the current
    tree, then runs a TBR search under the original weights from the tree it found.
    """
    m = len(seqs[0])
    w = [1] * m
    if start is None:
        start = stepwise_start(seqs, w, rng)
    tree, s = tbr_search(start, seqs, w)  # @line L1
    best_tree, best_len = tree, s  # @line L2
    for _ in range(iterations):  # @line L3
        w2 = [2 * wj if rng.random() < fraction else wj for wj in w]  # @line L4
        tree, _ = tbr_search(tree, seqs, w2)  # @line L5
        tree, s = tbr_search(tree, seqs, w)  # @line L6
        if s < best_len:  # @line L7
            best_tree, best_len = tree, s
    return best_tree, best_len  # @line L8
