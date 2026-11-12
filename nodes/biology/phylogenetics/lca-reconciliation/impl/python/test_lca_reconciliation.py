# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lca-reconciliation/. The authors are listed in prov/VSMQ48.jsonl.

import itertools
import random

from lca_reconciliation import (
    EulerLCA,
    children_of,
    duplications,
    events_of,
    lca_reconcile,
    postorder,
)


def random_rooted_tree(rng: random.Random, n_leaves: int, binary: bool):
    """Random rooted tree with n_leaves leaves, binary or with some polytomies."""
    parent, leaves = [-1], [0]
    while len(leaves) < n_leaves:
        t = leaves.pop(rng.randrange(len(leaves)))
        width = 2 if binary else min(rng.choice((2, 2, 3)), n_leaves - len(leaves))
        width = max(width, 2)
        for _ in range(width):
            parent.append(t)
            leaves.append(len(parent) - 1)
    return parent


def ancestors_or_self(parent, v):
    out = []
    while v >= 0:
        out.append(v)
        v = parent[v]
    return out


def naive_lca(parent, u, v):
    au = set(ancestors_or_self(parent, u))
    for w in ancestors_or_self(parent, v):
        if w in au:
            return w


def all_valid_mappings(gene_parent, species_parent, sigma):
    """Every mapping with M(leaf) = sigma(leaf) and M(g) an ancestor of, or
    equal to, M(child) for each child: the brute-force search space."""
    kids = children_of(gene_parent)
    order = postorder(gene_parent)
    internal = [g for g in order if kids[g]]

    def extend(i, m):
        if i == len(internal):
            yield dict(m)
            return
        g = internal[i]
        a, b = kids[g]
        low = naive_lca(species_parent, m[a], m[b])
        for s in ancestors_or_self(species_parent, low):
            m[g] = s
            yield from extend(i + 1, m)
        del m[g]

    start = {g: sigma[g] for g in order if not kids[g]}
    yield from extend(0, start)


def random_instance(rng):
    species = random_rooted_tree(rng, rng.randrange(2, 6), binary=rng.random() < 0.7)
    s_kids = children_of(species)
    s_leaves = [v for v in range(len(species)) if not s_kids[v]]
    gene = random_rooted_tree(rng, rng.randrange(2, 8), binary=True)
    g_kids = children_of(gene)
    sigma = {g: rng.choice(s_leaves) for g in range(len(gene)) if not g_kids[g]}
    return gene, species, sigma


def test_euler_lca_matches_naive() -> None:
    rng = random.Random(61)
    for _ in range(100):
        parent = random_rooted_tree(rng, rng.randrange(1, 15), binary=rng.random() < 0.5)
        lca = EulerLCA(parent)
        for u, v in itertools.product(range(len(parent)), repeat=2):
            assert lca.lca(u, v) == naive_lca(parent, u, v)


def test_lca_mapping_is_optimal_by_brute_force() -> None:
    rng = random.Random(62)
    for _ in range(300):
        gene, species, sigma = random_instance(rng)
        mapping, event, losses = lca_reconcile(gene, species, sigma)
        assert events_of(gene, species, mapping) == (duplications(event), losses)
        best_d = min_l = None
        for m in all_valid_mappings(gene, species, sigma):
            d, l = events_of(gene, species, m)
            assert duplications(event) <= d  # every LCA duplication is forced
            best_d = len(d) if best_d is None else min(best_d, len(d))
            if m != mapping:
                assert l > losses  # the LCA mapping is the unique loss minimizer
        assert len(duplications(event)) == best_d


def test_weighted_cost_unique_minimizer() -> None:
    rng = random.Random(63)
    for _ in range(150):
        gene, species, sigma = random_instance(rng)
        mapping, event, losses = lca_reconcile(gene, species, sigma)
        for cd, cl in ((1, 1), (3, 1), (1, 5), (0, 1)):
            mine = cd * len(duplications(event)) + cl * losses
            for m in all_valid_mappings(gene, species, sigma):
                d, l = events_of(gene, species, m)
                assert m == mapping or cd * len(d) + cl * l > mine


def test_small_example() -> None:
    # Species tree ((a,b),c): 0 root, 1 = ab, 2 = c, 3 = a, 4 = b.
    species = [-1, 0, 0, 1, 1]
    # Gene tree ((a1,b1),(a2,c1)): 0 root, 1, 2, leaves 3 a1, 4 b1, 5 a2, 6 c1.
    gene = [-1, 0, 0, 1, 1, 2, 2]
    sigma = {3: 3, 4: 4, 5: 3, 6: 2}
    mapping, event, losses = lca_reconcile(gene, species, sigma)
    assert mapping == {3: 3, 4: 4, 5: 3, 6: 2, 1: 1, 2: 0, 0: 0}
    assert duplications(event) == {0}
    assert losses == 2  # b is lost below node 2, and c is lost on the copy that leads to node 1
