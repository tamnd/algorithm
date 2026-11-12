# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/astral/. The authors are listed in prov/AJ00YQ.jsonl.
"""ASTRAL: the species tree that shares the most quartets with the gene trees.

Taxa are the integers 0..n-1, and a set of taxa is a bitmask. A gene tree is
a pair (parent, taxon): parent[v] is the parent of node v (-1 at the root),
and taxon[v] is the taxon at leaf v. Gene trees are binary and complete;
the root may have two or three children, since gene trees are unrooted.

The dynamic program runs over a set of allowed clusters that is closed under
complement. With all subsets allowed it is exact; with the clusters of the
gene tree bipartitions it is the constrained search of ASTRAL.
"""

from collections import Counter
from itertools import combinations


def children_of(parent: list) -> list:
    kids = [[] for _ in parent]
    for v, p in enumerate(parent):
        if p >= 0:
            kids[p].append(v)
    return kids


def leaf_sets(parent: list, taxon: dict) -> list:
    """Bitmask of the taxa below each node, by an explicit postorder."""
    kids = children_of(parent)
    order, stack = [], [parent.index(-1)]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(kids[v])
    below = [0] * len(parent)
    for v in reversed(order):
        below[v] = 1 << taxon[v] if not kids[v] else 0
        for c in kids[v]:
            below[v] |= below[c]
    return below


def gene_tripartitions(gene, full: int) -> list:
    """The tripartition of the taxa at each internal node of an unrooted gene tree."""
    parent, taxon = gene
    kids = children_of(parent)
    below = leaf_sets(parent, taxon)
    out = []
    for v, ks in enumerate(kids):
        if not ks:
            continue
        parts = [below[c] for c in ks]
        if len(parts) == 2:
            parts.append(full & ~below[v])
        if len(parts) != 3:
            raise ValueError("gene trees must be binary")
        out.append(tuple(parts))
    return out


def count_tripartitions(genes, full: int) -> Counter:
    """Multiset of the tripartitions of all gene trees. Equal gene nodes in
    different gene trees are merged, as ASTRAL does."""
    counts = Counter()
    for g in genes:
        for tri in gene_tripartitions(g, full):
            counts[tuple(sorted(tri))] += 1
    return counts


def tripartition_weight(tri: tuple, gene_tris: Counter) -> int:
    """Number of (gene, quartet) pairs ab|cd with a, b in two different parts
    of tri and c, d in the third, where the gene tree shows ab|cd. Each such
    quartet is counted at the one gene node that has c, d in one part and
    a, b in the two others."""
    total = 0
    for g, mult in gene_tris.items():
        inter = [[(s & q).bit_count() for q in g] for s in tri]
        here = 0
        for k in range(3):
            i, j = (x for x in range(3) if x != k)
            for r in range(3):
                p, q = (x for x in range(3) if x != r)
                pairs = inter[i][p] * inter[j][q] + inter[i][q] * inter[j][p]
                m = inter[k][r]
                here += m * (m - 1) // 2 * pairs
        total += mult * here
    return total


def gene_clusters(genes, full: int) -> set:
    """Both sides of every bipartition of the gene trees, plus singletons."""
    allowed = {1 << t for t in range(full.bit_length())}
    for parent, taxon in genes:
        for s in leaf_sets(parent, taxon):
            if s and s != full:
                allowed.add(s)
                allowed.add(full & ~s)
    return allowed


def astral(genes, n: int, allowed=None):
    """Return (score, clusters): the quartet score of the best species tree
    whose bipartitions are all in the allowed set, and the clusters of that
    tree rooted at the split of the full set."""
    full = (1 << n) - 1
    if allowed is None:
        allowed = set(range(1, full + 1))
    allowed = set(allowed) | {full} | {1 << t for t in range(n)}
    gene_tris = count_tripartitions(genes, full)
    value, best = {}, {}
    for a in sorted(allowed, key=int.bit_count):  # @line L1
        if a.bit_count() == 1:
            value[a] = 0  # @line L2
            continue
        low = a & -a
        top = None
        for a1 in allowed:
            a2 = a & ~a1
            # a1 holds the lowest taxon of a, so each split is tried once
            if a1 & a != a1 or a1 == a or not a1 & low:
                continue
            if a1 not in value or a2 not in value:
                continue
            w = tripartition_weight((a1, a2, full & ~a), gene_tris)
            score = value[a1] + value[a2] + w  # @line L3
            if top is None or score > top:
                top, best[a] = score, (a1, a2)  # @line L4
        if top is not None:
            value[a] = top
    clusters, stack = [], [full]  # @line L5
    while stack:
        a = stack.pop()
        clusters.append(a)
        if a in best:
            stack.extend(best[a])
    return value[full] // 2, clusters  # @line L6


def splits_of_clusters(clusters, n: int) -> frozenset:
    """Nontrivial bipartitions of a tree, each as the side without taxon 0."""
    full = (1 << n) - 1
    out = set()
    for c in clusters:
        s = c if not c & 1 else full & ~c
        if 2 <= s.bit_count() <= n - 2:
            out.add(s)
    return frozenset(out)


def gene_splits(gene, n: int) -> frozenset:
    return splits_of_clusters(leaf_sets(*gene), n)


def quartet_topology(splits: frozenset, quad: tuple):
    """The bitmask of the pair that holds quad[0] in the quartet topology of
    the tree, or None if the tree leaves the quartet unresolved."""
    a = quad[0]
    four = sum(1 << t for t in quad)
    for x in quad[1:]:
        pair = (1 << a) | (1 << x)
        rest = four & ~pair
        if any(s & four in (pair, rest) for s in splits):
            return pair
    return None


def quartet_score(species_splits: frozenset, genes, n: int) -> int:
    """The quartet support of a species tree, counted quartet by quartet."""
    gs = [gene_splits(g, n) for g in genes]
    total = 0
    for quad in combinations(range(n), 4):
        q = quartet_topology(species_splits, quad)
        total += sum(1 for s in gs if quartet_topology(s, quad) == q)
    return total
