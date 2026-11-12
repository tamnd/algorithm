# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lca-reconciliation/. The authors are listed in prov/VSMQ48.jsonl.
"""LCA reconciliation of a gene tree with a species tree.

Trees are parent lists: parent[v] is the parent of node v and parent[root]
is -1. The gene tree is binary. sigma maps each gene leaf to the species
leaf it was sampled from. The species tree gets constant-time LCA queries
from an Euler tour and a sparse table of range minima.
"""


def children_of(parent: list) -> list:
    kids = [[] for _ in parent]
    for v, p in enumerate(parent):
        if p >= 0:
            kids[p].append(v)
    return kids


def postorder(parent: list) -> list:
    kids = children_of(parent)
    order, stack = [], [parent.index(-1)]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(kids[v])
    order.reverse()
    return order


class EulerLCA:
    """LCA by an Euler tour and a sparse table: O(m log m) setup, O(1) queries."""

    def __init__(self, parent: list):
        kids = children_of(parent)
        root = parent.index(-1)
        self.depth = [0] * len(parent)
        self.first = [0] * len(parent)
        tour = []
        stack = [(root, 0)]
        while stack:
            v, i = stack.pop()
            if i == 0:
                self.first[v] = len(tour)
            tour.append(v)
            if i < len(kids[v]):
                stack.append((v, i + 1))
                c = kids[v][i]
                self.depth[c] = self.depth[v] + 1
                stack.append((c, 0))
        self.tour = tour
        self.table = [tour[:]]
        span = 1
        while 2 * span <= len(tour):
            prev = self.table[-1]
            row = []
            for i in range(len(tour) - 2 * span + 1):
                a, b = prev[i], prev[i + span]
                row.append(a if self.depth[a] <= self.depth[b] else b)
            self.table.append(row)
            span *= 2

    def lca(self, u: int, v: int) -> int:
        i, j = sorted((self.first[u], self.first[v]))
        k = (j - i + 1).bit_length() - 1
        a, b = self.table[k][i], self.table[k][j - (1 << k) + 1]
        return a if self.depth[a] <= self.depth[b] else b


def lca_reconcile(gene_parent: list, species_parent: list, sigma: dict):
    """Return (mapping, event, losses) of the LCA reconciliation, where
    event[g] is "duplication" or "speciation" for each internal gene node."""
    lca = EulerLCA(species_parent)  # @line L1
    kids = children_of(gene_parent)
    mapping, event, losses = {}, {}, 0
    for g in postorder(gene_parent):  # @line L2
        if not kids[g]:
            mapping[g] = sigma[g]  # @line L3
            continue
        a, b = kids[g]
        m = lca.lca(mapping[a], mapping[b])  # @line L4
        mapping[g] = m
        dup = m == mapping[a] or m == mapping[b]
        if dup:  # @line L5
            event[g] = "duplication"
        else:
            event[g] = "speciation"  # @line L6
        for c in (a, b):  # @line L7
            losses += lca.depth[mapping[c]] - lca.depth[m] - 1 + dup
    return mapping, event, losses  # @line L8


def duplications(event: dict) -> set:
    return {g for g, e in event.items() if e == "duplication"}


def events_of(gene_parent: list, species_parent: list, mapping: dict):
    """Duplications and losses of any valid mapping, with the usual rule:
    g is a speciation iff its children map strictly below M(g) into two
    different child subtrees, that is, M(g) is their LCA and equals neither."""
    lca = EulerLCA(species_parent)
    kids = children_of(gene_parent)
    dups, losses = set(), 0
    for g in range(len(gene_parent)):
        if not kids[g]:
            continue
        a, b = kids[g]
        m = mapping[g]
        speciation = lca.lca(mapping[a], mapping[b]) == m and m not in (mapping[a], mapping[b])
        if not speciation:
            dups.add(g)
        for c in (a, b):
            losses += lca.depth[mapping[c]] - lca.depth[m] - 1 + (not speciation)
    return dups, losses
