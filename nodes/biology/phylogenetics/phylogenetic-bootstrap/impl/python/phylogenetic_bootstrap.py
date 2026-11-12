# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phylogenetic-bootstrap/. The authors are listed in prov/3RY3K8.jsonl.

"""Felsenstein's nonparametric bootstrap for the splits of a phylogenetic tree.

The data are n aligned sequences of length m (seqs[i][j] is the state of taxon i at site j).
An estimator maps an alignment to a list of equally good trees. Each tree is given by its
set of nontrivial splits, and each split is the frozenset of taxa on the side without taxon 0.
When the estimator returns t tied trees, each one counts 1/t. The support of a split is the
mean count over the bootstrap replicates.

The estimator used in the tests is exhaustive maximum parsimony with Fitch scoring, which is
exact but takes (2n - 5)!! tree scores, so it fits only small n.
"""

import random
from fractions import Fraction
from typing import Callable, Dict, FrozenSet, List, Sequence, Set

Split = FrozenSet[int]
Topology = FrozenSet[Split]
Estimator = Callable[[Sequence[str]], List[Topology]]


def resample_columns(seqs: Sequence[str], rng: random.Random) -> List[str]:
    """Draw m site indices uniformly with replacement and return the new alignment."""
    m = len(seqs[0])
    idx = [rng.randrange(m) for _ in range(m)]
    return ["".join(s[j] for j in idx) for s in seqs]


def bootstrap_support(seqs: Sequence[str], estimate: Estimator, replicates: int, rng: random.Random) -> Dict[Split, float]:
    """Return the bootstrap support of every split seen in any replicate.

    Cost: replicates times the cost of one estimate, plus O(m n) per replicate to resample.
    """
    counts: Dict[Split, Fraction] = {}  # @line L1
    for _ in range(replicates):  # @line L2
        data = resample_columns(seqs, rng)  # @line L3
        trees = estimate(data)  # @line L4
        share = Fraction(1, len(trees))
        for t in trees:  # @line L5
            for s in t:
                counts[s] = counts.get(s, Fraction(0)) + share
    return {s: float(c / replicates) for s, c in counts.items()}  # @line L6


# ---------------------------------------------------------------- an exact estimator


def all_topologies(n: int) -> List[List[Set[int]]]:
    """Return all (2n - 5)!! unrooted binary trees on 0 .. n - 1 as adjacency lists."""
    start = {0: {n}, 1: {n}, 2: {n}, n: {0, 1, 2}}
    trees = [start]
    for k in range(3, n):
        nxt = []
        for t in trees:
            new = n + k - 2
            for x, y in sorted((x, y) for x in t for y in t[x] if x < y):
                t2 = {v: set(nb) for v, nb in t.items()}
                t2[x].discard(y)
                t2[y].discard(x)
                t2[new] = {x, y, k}
                t2[x].add(new)
                t2[y].add(new)
                t2[k] = {new}
                nxt.append(t2)
        trees = nxt
    return trees


def _rooted_order(tree, n):
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
    return order, kids


def tree_splits(tree, n: int) -> Topology:
    """Return the nontrivial splits of a tree as sides without taxon 0."""
    order, kids = _rooted_order(tree, n)
    below: Dict[int, Set[int]] = {}
    for v in reversed(order):
        s = {v} if v < n else set()
        for w in kids[v]:
            s |= below[w]
        below[v] = s
    return frozenset(frozenset(below[v]) for v in order[1:] if 2 <= len(below[v]) <= n - 2)


def fitch_length(tree, seqs: Sequence[str]) -> int:
    """Fitch parsimony length. O(n m)."""
    n = len(seqs)
    order, kids = _rooted_order(tree, n)
    total = 0
    for j in range(len(seqs[0])):
        sets: Dict[int, Set[str]] = {}
        for v in reversed(order[1:]):
            if v < n:
                sets[v] = {seqs[v][j]}
                continue
            a, b = sets[kids[v][0]], sets[kids[v][1]]
            if a & b:
                sets[v] = a & b
            else:
                sets[v] = a | b
                total += 1
        if seqs[0][j] not in sets[order[1]]:
            total += 1
    return total


def exhaustive_parsimony(seqs: Sequence[str]) -> List[Topology]:
    """Return all most parsimonious trees, by scoring every tree. For n up to about 7."""
    n = len(seqs)
    trees = all_topologies(n)
    lens = [fitch_length(t, seqs) for t in trees]
    best = min(lens)
    return [tree_splits(t, n) for t, s in zip(trees, lens) if s == best]
