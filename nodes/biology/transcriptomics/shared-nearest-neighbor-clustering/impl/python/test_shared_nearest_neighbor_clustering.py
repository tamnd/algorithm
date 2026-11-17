# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shared-nearest-neighbor-clustering/. The authors are listed in prov/6JJNPV.jsonl.

import math
import random

import pytest

from rq3lin import knn
from shared_nearest_neighbor_clustering import (
    aggregate,
    local_moving,
    louvain,
    modularity,
    relabel,
    snn_cluster,
    snn_graph,
)

PAGE = [(0, 0), (1, 0), (0, 1), (1, 1), (2.6, 0.5), (4, 0), (5, 0), (4, 1), (5, 1)]


def partitions(n):
    """All set partitions of range(n) as restricted growth strings."""
    def rec(prefix, top):
        if len(prefix) == n:
            yield list(prefix)
            return
        for c in range(top + 2):
            prefix.append(c)
            yield from rec(prefix, max(top, c))
            prefix.pop()
    yield from rec([0], 0) if n else iter([[]])


def best_modularity(adj, resolution=1.0):
    return max(modularity(adj, p, resolution) for p in partitions(len(adj)))


def modularity_by_edges(adj, labels, resolution=1.0):
    """sum over communities of L_c / m - gamma (d_c / 2m)^2, from the unordered edge list."""
    m = sum(w for i, row in enumerate(adj) for j, w in row.items() if i < j)
    d, L = {}, {}
    for i, row in enumerate(adj):
        c = labels[i]
        d[c] = d.get(c, 0.0) + sum(row.values())
        for j, w in row.items():
            if i < j and labels[j] == c:
                L[c] = L.get(c, 0.0) + w
    return sum(L.get(c, 0.0) / m - resolution * (d[c] / (2 * m)) ** 2 for c in d)


def random_graph(rng, n, p):
    adj = [dict() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                w = rng.choice([0.25, 0.5, 1.0])
                adj[i][j] = adj[j][i] = w
    return adj


def ari(a, b):
    n = len(a)
    pairs = {}
    for x, y in zip(a, b):
        pairs[(x, y)] = pairs.get((x, y), 0) + 1
    ca, cb = {}, {}
    for x in a:
        ca[x] = ca.get(x, 0) + 1
    for y in b:
        cb[y] = cb.get(y, 0) + 1

    def c2(v):
        return v * (v - 1) / 2

    s = sum(c2(v) for v in pairs.values())
    sa = sum(c2(v) for v in ca.values())
    sb = sum(c2(v) for v in cb.values())
    exp = sa * sb / c2(n)
    return (s - exp) / ((sa + sb) / 2 - exp)


def test_page_example():
    assert knn(PAGE, 3)[4] == [5, 7, 1]
    g = snn_graph(PAGE, 3)
    assert math.isclose(g[4][1], 1 / 7) and math.isclose(g[4][5], 1 / 3) and math.isclose(g[4][7], 1 / 3)
    assert g[0][1] == 1.0 and g[5][6] == 1.0
    labels, levels = louvain(g)
    assert labels == [0, 0, 0, 0, 1, 1, 1, 1, 1]
    assert len(levels) == 1
    q = modularity(g, labels)
    assert math.isclose(q, 0.4874932629455092, rel_tol=1e-12)
    # The other place for the bridge cell 4 is worse, and here Louvain finds the best partition.
    assert modularity(g, [0, 0, 0, 0, 0, 1, 1, 1, 1]) < q
    assert math.isclose(q, best_modularity(g), rel_tol=1e-12)


def test_jaccard_weight_bounds():
    rng = random.Random(1)
    pts = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(40)]
    for k in (1, 3, 6):
        g = snn_graph(pts, k)
        nb = knn(pts, k)
        for i, row in enumerate(g):
            for j, w in row.items():
                assert j in nb[i] or i in nb[j]
                assert 1 / (2 * k + 1) - 1e-15 <= w <= 1.0
            assert all(j in row for j in nb[i])


def test_modularity_matches_the_edge_formula():
    rng = random.Random(2)
    for _ in range(30):
        g = random_graph(rng, 8, 0.4)
        if not any(g):
            continue
        lab = [rng.randrange(3) for _ in range(8)]
        for gamma in (0.5, 1.0, 2.0):
            assert math.isclose(modularity(g, lab, gamma), modularity_by_edges(g, lab, gamma), abs_tol=1e-12)


def test_aggregation_keeps_modularity():
    rng = random.Random(3)
    for _ in range(30):
        g = random_graph(rng, 9, 0.35)
        if not any(g):
            continue
        comm = relabel([rng.randrange(4) for _ in range(9)])
        h = aggregate(g, comm)
        assert math.isclose(modularity(g, comm), modularity(h, list(range(len(h)))), abs_tol=1e-12)
        assert math.isclose(sum(map(lambda r: sum(r.values()), g)), sum(map(lambda r: sum(r.values()), h)))


def test_local_moving_ends_in_a_local_optimum():
    rng = random.Random(4)
    for _ in range(25):
        g = random_graph(rng, 8, 0.4)
        if not any(g):
            continue
        comm, _ = local_moving(g)
        q = modularity(g, comm)
        assert q >= modularity(g, list(range(8))) - 1e-12
        for i in range(8):
            for c in set(comm[j] for j in g[i]):
                trial = comm[:]
                trial[i] = c
                assert modularity(g, trial) <= q + 1e-9


def test_louvain_against_exhaustive_search():
    """Louvain is a heuristic: never above the optimum, and measured to reach it on most small graphs."""
    rng = random.Random(5)
    hits = total = 0
    for _ in range(30):
        n = rng.randint(4, 8)
        g = random_graph(rng, n, 0.45)
        if not any(g):
            continue
        labels, levels = louvain(g)
        q, best = modularity(g, labels), best_modularity(g)
        assert q <= best + 1e-12
        qs = [modularity(g, lv) for lv in levels]
        assert all(b > a for a, b in zip([modularity(g, list(range(n)))] + qs, qs))
        total += 1
        hits += math.isclose(q, best, abs_tol=1e-9)
    assert total >= 25 and hits >= 0.8 * total


def test_components_are_never_merged():
    a = snn_graph([(0, 0), (1, 0), (0, 1)], 2)
    g = [dict(r) for r in a] + [{4: 1.0}, {3: 1.0}]
    labels, _ = louvain(g)
    assert labels[0] == labels[1] == labels[2] != labels[3] == labels[4]


def test_resolution_zero_gives_the_connected_components():
    rng = random.Random(6)
    for _ in range(20):
        g = random_graph(rng, 9, 0.2)
        if not any(g):
            continue
        labels, _ = louvain(g, resolution=0.0)
        comp = list(range(9))

        def find(x):
            while comp[x] != x:
                x = comp[x]
            return x

        for i, row in enumerate(g):
            for j in row:
                comp[find(i)] = find(j)
        roots = [find(i) for i in range(9)]
        for i in range(9):
            for j in range(9):
                if g[i] and g[j]:
                    assert (labels[i] == labels[j]) == (roots[i] == roots[j])


def test_empty_graph_and_errors():
    assert louvain([dict(), dict()])[0] == [0, 1]
    with pytest.raises(ValueError):
        snn_graph([(0, 0), (1, 1)], 2)


def test_gaussian_clusters_measured():
    """A measurement: 3 groups of 40 cells in 20 dimensions, PCA to 5.

    With k = 15 the groups come back exactly. With k = 10 one group is split in
    two, but no cluster mixes two groups: a smaller k gives more clusters.
    """
    rng = random.Random(2015)
    centers = [[rng.gauss(0, 1.2) for _ in range(20)] for _ in range(3)]
    X, truth = [], []
    for c in range(3):
        for _ in range(40):
            X.append([m + rng.gauss(0, 1) for m in centers[c]])
            truth.append(c)
    assert ari(snn_cluster(X, k=15, n_pcs=5), truth) > 0.95
    labels = snn_cluster(X, k=10, n_pcs=5)
    assert len(set(labels)) > 3
    assert all(len({t for t, l in zip(truth, labels) if l == c}) == 1 for c in set(labels))
    # Edges between groups get smaller Jaccard weights than edges inside groups.
    from rq3lin import pca_fit, pca_project
    mu, axes, _ = pca_fit(X, 5)
    g = snn_graph(pca_project(X, mu, axes), 10)
    inside = [w for i, r in enumerate(g) for j, w in r.items() if truth[i] == truth[j]]
    across = [w for i, r in enumerate(g) for j, w in r.items() if truth[i] != truth[j]]
    if across:
        assert sum(across) / len(across) < 0.6 * sum(inside) / len(inside)
