# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sorted-neighborhood-method/. The authors are listed in prov/7P2CSB.jsonl.
"""The sorted neighborhood method (SNM) of Hernandez and Stolfo, with several passes.

Records are any values. A key function maps a record to a sortable value, and
match(r, s) is the pairwise rule (the "equational theory" of the paper). One
pass sorts the records by its key and compares each record with the w - 1
records before it in the sorted order. The multi-pass method runs one pass per
key, takes the union of the matched pairs, and returns the connected
components (the transitive closure) as clusters of record numbers.
"""


def snm_pass(records, key, match, w):
    """One pass. Return (set of matched pairs (i, j) with i < j, number of match calls)."""
    n = len(records)
    order = sorted(range(n), key=lambda i: (key(records[i]), i))  # @line L3
    pairs = set()
    calls = 0
    for p in range(n):  # @line L4
        for q in range(max(0, p - w + 1), p):  # @line L5
            calls += 1
            a, b = order[q], order[p]
            if match(records[a], records[b]):  # @line L6
                pairs.add((min(a, b), max(a, b)))  # @line L6
    return pairs, calls


def expected_calls(n, w):
    """The number of match calls of one pass: (w - 1) n - w (w - 1) / 2 for n >= w."""
    if w <= 1:
        return 0
    if n <= w:
        return n * (n - 1) // 2
    return (w - 1) * n - w * (w - 1) // 2


class UnionFind:
    """Union by size with path halving, for the closure of line L7."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]


def clusters_from_pairs(n, pairs):
    """Connected components of the graph on 0 .. n - 1 with the given edges, sorted."""
    uf = UnionFind(n)
    for a, b in sorted(pairs):
        uf.union(a, b)
    groups = {}
    for i in range(n):
        groups.setdefault(uf.find(i), []).append(i)
    return sorted(groups.values())


def sorted_neighborhood(records, keys, match, w):
    """Multi-pass SNM. Return (clusters, matched pairs, total match calls)."""
    pairs = set()  # @line L1
    calls = 0
    for key in keys:  # @line L2
        found, c = snm_pass(records, key, match, w)
        pairs |= found
        calls += c
    clusters = clusters_from_pairs(len(records), pairs)  # @line L7
    return clusters, pairs, calls  # @line L8


def all_pairs(records, match):
    """The baseline that compares every pair: the result SNM approximates."""
    pairs = set()
    n = len(records)
    for a in range(n):
        for b in range(a + 1, n):
            if match(records[a], records[b]):
                pairs.add((a, b))
    return pairs


def pair_set(clusters):
    """All pairs (i, j), i < j, that share a cluster."""
    out = set()
    for c in clusters:
        c = sorted(c)
        for x in range(len(c)):
            for y in range(x + 1, len(c)):
                out.add((c[x], c[y]))
    return out


def precision_recall(found_clusters, true_clusters):
    """Pairwise precision and recall of found clusters against the true ones."""
    found = pair_set(found_clusters)
    true = pair_set(true_clusters)
    hit = len(found & true)
    precision = hit / len(found) if found else 1.0
    recall = hit / len(true) if true else 1.0
    return precision, recall
