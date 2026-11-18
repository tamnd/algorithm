# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/similarity-flooding/. The authors are listed in prov/BY6RCV.jsonl.

"""Similarity flooding (Melnik, Garcia-Molina and Rahm 2002).

A graph is a list of edges (source, label, target). Nodes are strings or any
values with a total order. The result of the fixpoint is a dict from map pairs
(a, b), with a a node of A and b a node of B, to a similarity in [0, 1].
"""

from collections import defaultdict
from math import sqrt

Edge = tuple  # (source, label, target)

FORMULAS = ("basic", "A", "B", "C")


def pairwise_connectivity_graph(ga, gb):
    """The edges ((a, b), l, (a2, b2)) for each pair of edges a -l-> a2 in A and b -l-> b2 in B."""
    by_label = defaultdict(list)
    for b, label, b2 in sorted(set(gb)):
        by_label[label].append((b, b2))
    out = []
    for a, label, a2 in sorted(set(ga)):
        for b, b2 in by_label.get(label, ()):
            out.append(((a, b), label, (a2, b2)))
    return out


def propagation_graph(ga, gb):
    """The induced propagation graph: a dict from each node x to a list of (y, w).

    Each edge x -l-> y of the pairwise connectivity graph gives a forward edge
    x -> y with weight 1 / (number of l-edges out of x) and a backward edge
    y -> x with weight 1 / (number of l-edges into y).
    """
    pcg = pairwise_connectivity_graph(ga, gb)  # @line L1
    n_out = defaultdict(int)
    n_in = defaultdict(int)
    for x, label, y in pcg:
        n_out[(x, label)] += 1
        n_in[(y, label)] += 1
    prop = defaultdict(list)
    for x, label, y in pcg:  # @line L2
        prop[x].append((y, 1.0 / n_out[(x, label)]))  # @line L3
        prop[y].append((x, 1.0 / n_in[(y, label)]))
    return prop


def _phi(prop, nodes, vec):
    """phi(vec)(y) = sum of w * vec(x) over the edges x -> y with weight w."""
    res = {x: 0.0 for x in nodes}
    for x in nodes:
        v = vec[x]
        if v:
            for y, w in prop.get(x, ()):
                res[y] += w * v
    return res


def flood(ga, gb, sigma0, formula="basic", eps=1e-9, max_iter=1000):
    """Run the fixpoint. Return (sigma, iterations)."""
    if formula not in FORMULAS:
        raise ValueError("unknown formula " + repr(formula))
    prop = propagation_graph(ga, gb)
    nodes = set(prop)
    for x, edges in prop.items():
        nodes.update(y for y, _ in edges)
    nodes.update(sigma0)
    nodes = sorted(nodes)
    s0 = {x: float(sigma0.get(x, 0.0)) for x in nodes}  # @line L4
    sigma = dict(s0)
    it = 0
    while True:  # @line L5
        if formula == "basic":  # @line L6
            base, arg = sigma, sigma
        elif formula == "A":
            base, arg = s0, sigma
        elif formula == "B":
            base, arg = None, {x: s0[x] + sigma[x] for x in nodes}
        else:
            both = {x: s0[x] + sigma[x] for x in nodes}
            base, arg = both, both
        ph = _phi(prop, nodes, arg)
        new = {x: (base[x] if base is not None else 0.0) + ph[x] for x in nodes}  # @line L7
        top = max(new.values(), default=0.0)
        if top > 0:
            new = {x: v / top for x, v in new.items()}  # @line L8
        res = sqrt(sum((new[x] - sigma[x]) ** 2 for x in nodes))  # @line L9
        sigma = new
        it += 1
        if res < eps or it >= max_iter:  # @line L10
            return sigma, it


def stable_filter(sigma, threshold=0.0):
    """A stable marriage on the pairs with similarity at least threshold.

    Nodes of A propose to nodes of B in decreasing order of similarity; ties are
    broken by the node order. Each node is in at most one pair.
    """
    prefs_a = defaultdict(list)
    rank_b = defaultdict(dict)
    for (a, b), v in sigma.items():
        if v >= threshold and v > 0:
            prefs_a[a].append((-v, b))
            rank_b[b][a] = (-v, a)
    for a in prefs_a:
        prefs_a[a].sort()
    nxt = {a: 0 for a in prefs_a}
    engaged = {}  # b -> a
    free = sorted(prefs_a, reverse=True)
    while free:  # @line L11
        a = free.pop()
        if nxt[a] >= len(prefs_a[a]):
            continue
        _, b = prefs_a[a][nxt[a]]
        nxt[a] += 1
        cur = engaged.get(b)
        if cur is None:
            engaged[b] = a
        elif rank_b[b][a] < rank_b[b][cur]:
            engaged[b] = a
            free.append(cur)
        else:
            free.append(a)
    return sorted((a, b) for b, a in engaged.items())  # @line L12


def similarity_flooding(ga, gb, sigma0, formula="basic", threshold=0.0, eps=1e-9, max_iter=1000):
    """Return (pairs, sigma): the filtered pairs and the final similarities."""
    sigma, _ = flood(ga, gb, sigma0, formula, eps, max_iter)
    return stable_filter(sigma, threshold), sigma
