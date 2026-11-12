# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/astral/. The authors are listed in prov/AJ00YQ.jsonl.

import random
from itertools import combinations

from astral import (
    astral,
    count_tripartitions,
    gene_clusters,
    gene_splits,
    quartet_score,
    quartet_topology,
    splits_of_clusters,
    tripartition_weight,
)


def all_unrooted_trees(n: int):
    """Every unrooted binary tree on taxa 0..n-1, by stepwise addition, as an
    edge list with leaves 0..n-1 and internal nodes from n up."""
    trees = [[(0, n), (1, n), (2, n)]]
    for leaf in range(3, n):
        grown = []
        for edges in trees:
            w = n + leaf - 2
            for e, (u, v) in enumerate(edges):
                grown.append(edges[:e] + edges[e + 1:] + [(u, w), (w, v), (w, leaf)])
        trees = grown
    return trees


def to_gene(edges, n: int):
    """Parent list of an unrooted tree, hung from its internal node n."""
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    size = max(adj) + 1
    parent = [None] * size
    parent[n] = -1
    stack = [n]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if parent[v] is None:
                parent[v] = u
                stack.append(v)
    return parent, {v: v for v in range(n)}


TREES = {n: all_unrooted_trees(n) for n in range(4, 8)}
TREE_SPLITS = {n: [gene_splits(to_gene(e, n), n) for e in TREES[n]] for n in TREES}


def random_gene(rng: random.Random, n: int):
    return to_gene(rng.choice(TREES[n]), n)


def brute_force_best(genes, n: int, allowed_splits=None) -> int:
    """Best quartet score over all (2n-5)!! unrooted binary species trees."""
    quads = list(combinations(range(n), 4))
    shown = [[quartet_topology(gene_splits(g, n), q) for q in quads] for g in genes]
    best = None
    for splits in TREE_SPLITS[n]:
        if allowed_splits is not None and not splits <= allowed_splits:
            continue
        mine = [quartet_topology(splits, q) for q in quads]
        score = sum(t == m for gs in shown for t, m in zip(gs, mine))
        best = score if best is None else max(best, score)
    return best


def naive_weight(tri, genes, n: int) -> int:
    total = 0
    for g in genes:
        s = gene_splits(g, n)
        for quad in combinations(range(n), 4):
            pair = quartet_topology(s, quad)
            rest = sum(1 << t for t in quad) & ~pair
            for together, apart in ((pair, rest), (rest, pair)):
                k = [i for i in range(3) if tri[i] & together == together]
                if k:
                    others = [tri[i] for i in range(3) if i != k[0]]
                    if all((apart & o).bit_count() == 1 for o in others):
                        total += 1
    return total


def test_tripartition_weight_matches_quartet_count() -> None:
    rng = random.Random(71)
    for _ in range(40):
        n = rng.randrange(4, 8)
        genes = [random_gene(rng, n) for _ in range(rng.randrange(1, 4))]
        labels = [rng.randrange(3) for _ in range(n)]
        tri = tuple(sum(1 << t for t in range(n) if labels[t] == i) for i in range(3))
        tris = count_tripartitions(genes, (1 << n) - 1)
        assert sum(tris.values()) == len(genes) * (n - 2)
        assert tripartition_weight(tri, tris) == naive_weight(tri, genes, n)


def test_exact_dp_matches_brute_force() -> None:
    rng = random.Random(72)
    assert [len(TREES[n]) for n in range(4, 8)] == [3, 15, 105, 945]
    for trial in range(25):
        n = 7 if trial < 2 else rng.randrange(4, 7)
        genes = [random_gene(rng, n) for _ in range(rng.randrange(1, 5))]
        score, clusters = astral(genes, n)
        assert score == quartet_score(splits_of_clusters(clusters, n), genes, n)
        assert score == brute_force_best(genes, n)


def test_constrained_dp_matches_brute_force_on_its_space() -> None:
    rng = random.Random(73)
    for _ in range(20):
        n = rng.randrange(5, 8)
        genes = [random_gene(rng, n) for _ in range(rng.randrange(1, 4))]
        allowed = gene_clusters(genes, (1 << n) - 1)
        score, clusters = astral(genes, n, allowed)
        splits = splits_of_clusters(clusters, n)
        assert splits <= splits_of_clusters(allowed, n)
        assert score == quartet_score(splits, genes, n)
        assert score == brute_force_best(genes, n, splits_of_clusters(allowed, n))
        assert score <= astral(genes, n)[0]


def simulate_msc(rng: random.Random, species):
    """Gene tree under the multispecies coalescent. species is a list of
    (left, right, height) for internal nodes in order of height, with leaves
    0..n-1 at height 0; returns a rooted gene tree with one copy per taxon."""
    n = len(species) + 1
    parent, taxon = [], {}
    lineages = {}
    for t in range(n):
        parent.append(-1)
        taxon[t] = t
        lineages[t] = [t]
    heights = {t: 0.0 for t in range(n)}
    up = {}
    for idx, (left, right, h) in enumerate(species):
        up[left] = up[right] = n + idx
        heights[n + idx] = h
    root = n + len(species) - 1
    for idx, (left, right, h) in enumerate(species):
        node = n + idx
        merged = []
        for child in (left, right):
            live, t = lineages.pop(child), heights[child]
            while len(live) > 1:
                k = len(live)
                t += rng.expovariate(k * (k - 1) / 2)
                if t >= h:
                    break
                a, b = rng.sample(range(k), 2)
                new = len(parent)
                parent.append(-1)
                parent[live[a]] = parent[live[b]] = new
                live = [x for i, x in enumerate(live) if i not in (a, b)] + [new]
            merged.extend(live)
        lineages[node] = merged
    live = lineages[root]
    while len(live) > 1:
        a, b = rng.sample(range(len(live)), 2)
        new = len(parent)
        parent.append(-1)
        parent[live[a]] = parent[live[b]] = new
        live = [x for i, x in enumerate(live) if i not in (a, b)] + [new]
    return parent, taxon


def test_recovers_species_tree_under_msc() -> None:
    # Caterpillar ((((0,1),2),3),4) with inner branches of 0.3 coalescent units.
    species = [(0, 1, 1.0), (5, 2, 1.3), (6, 3, 1.6), (7, 4, 1.9)]
    n = 5
    true_splits = splits_of_clusters([0b00011, 0b00111, 0b01111], n)
    rng = random.Random(74)
    genes = [simulate_msc(rng, species) for _ in range(300)]
    discordant = sum(1 for g in genes if gene_splits(g, n) != true_splits)
    assert discordant > 100  # most gene trees disagree with the species tree
    for allowed in (None, gene_clusters(genes, (1 << n) - 1)):
        score, clusters = astral(genes, n, allowed)
        assert splits_of_clusters(clusters, n) == true_splits
