# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chow-liu-algorithm/. The authors are listed in prov/Q3KGA9.jsonl.

"""The Chow-Liu algorithm: the maximum-likelihood tree-structured Bayesian
network for discrete data, as a maximum weight spanning tree under empirical
mutual information weights (Kruskal with union-find).

data is a list of samples; each sample is a tuple of n small integers.
"""

import math
from collections import Counter
from fractions import Fraction


def mutual_information(data, i: int, j: int) -> float:
    """Empirical mutual information of variables i and j, in nats."""
    s = len(data)
    cij = Counter((x[i], x[j]) for x in data)
    ci = Counter(x[i] for x in data)
    cj = Counter(x[j] for x in data)
    return sum(c / s * math.log(c * s / (ci[a] * cj[b])) for (a, b), c in cij.items())


def chow_liu(data, n: int, root: int = 0):
    """Return (parent, cpt). parent[v] is the parent of v in the tree, or None for the root.

    cpt[v] maps (value of v, value of the parent) to the empirical P(x_v | x_parent);
    for the root the parent value is None.
    """
    # @line L1
    weight = {}
    for i in range(n):
        for j in range(i + 1, n):
            # @line L2
            weight[i, j] = mutual_information(data, i, j)
    # @line L3
    pairs = sorted(weight, key=lambda e: -weight[e])
    # @line L4
    up = list(range(n))
    tree = [[] for _ in range(n)]

    def find(a):
        while up[a] != a:
            up[a] = up[up[a]]
            a = up[a]
        return a
    # @line L5
    for i, j in pairs:
        # @line L6
        ri, rj = find(i), find(j)
        if ri != rj:
            # @line L7
            tree[i].append(j)
            tree[j].append(i)
            up[ri] = rj
    # @line L8
    parent = [None] * n
    seen, stack = {root}, [root]
    while stack:
        u = stack.pop()
        for w in tree[u]:
            if w not in seen:
                seen.add(w)
                parent[w] = u
                stack.append(w)
    # @line L9
    cpt = []
    for v in range(n):
        # @line L10
        p = parent[v]
        joint = Counter((x[v], None if p is None else x[p]) for x in data)
        marg = Counter(None if p is None else x[p] for x in data)
        cpt.append({k: Fraction(c, marg[k[1]]) for k, c in joint.items()})
    # @line L11
    return parent, cpt


def likelihood(data, parent) -> Fraction:
    """Exact likelihood of the data under the tree with maximum-likelihood tables."""
    out = Fraction(1)
    for v, p in enumerate(parent):
        joint = Counter((x[v], None if p is None else x[p]) for x in data)
        marg = Counter(None if p is None else x[p] for x in data)
        for (a, b), c in joint.items():
            out *= Fraction(c, marg[b]) ** c
    return out
