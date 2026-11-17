# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-gene-coexpression-network-analysis/. The authors are listed in prov/WN4DQ5.jsonl.

import itertools
import math
import random
import statistics

import pytest

from weighted_gene_coexpression_network_analysis import (
    adjacency,
    average_linkage,
    correlation_matrix,
    cut_tree,
    eigengene,
    pearson,
    scale_free_fit,
    standardize,
    topological_overlap,
    wgcna,
)

PAGE_A = [
    [1.0, 0.9, 0.8, 0.0],
    [0.9, 1.0, 0.7, 0.1],
    [0.8, 0.7, 1.0, 0.0],
    [0.0, 0.1, 0.0, 1.0],
]


def random_adjacency(rng, n):
    a = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            a[i][j] = a[j][i] = rng.random()
    return a


def tom_brute(a):
    """The definition, entry by entry, with sets of neighbours written out."""
    n = len(a)
    out = [[1.0] * n for _ in range(n)]
    for i, j in itertools.permutations(range(n), 2):
        others = [u for u in range(n) if u not in (i, j)]
        l_ij = sum(a[i][u] * a[u][j] for u in others)
        k_i = sum(a[i][u] for u in range(n) if u != i)
        k_j = sum(a[j][u] for u in range(n) if u != j)
        out[i][j] = (l_ij + a[i][j]) / (min(k_i, k_j) + 1 - a[i][j])
    return out


def test_pearson_matches_statistics():
    rng = random.Random(71)
    for _ in range(50):
        x = [rng.gauss(0, 1) for _ in range(8)]
        y = [rng.gauss(0, 1) + 0.5 * v for v in x]
        assert math.isclose(pearson(x, y), statistics.correlation(x, y), rel_tol=1e-12)
    with pytest.raises(ValueError):
        pearson([1, 1, 1], [1, 2, 3])


def test_adjacency_unsigned_and_signed():
    r = [[1.0, -0.5], [-0.5, 1.0]]
    assert adjacency(r, 2)[0][1] == 0.25
    assert adjacency(r, 2, signed=True)[0][1] == 0.0625
    assert adjacency(r, 2)[0][0] == 1.0


def test_page_example():
    t = topological_overlap(PAGE_A)
    # k = (1.7, 1.7, 1.5, 0.1); l_12 = 0.8 * 0.7 + 0 * 0.1 = 0.56
    assert math.isclose(t[0][1], (0.56 + 0.9) / (1.7 + 1 - 0.9), rel_tol=1e-12)
    assert math.isclose(t[0][3], (0.09 + 0.0) / (0.1 + 1 - 0.0), rel_tol=1e-12)


def test_tom_matches_brute_force_and_lies_in_unit_interval():
    rng = random.Random(72)
    for _ in range(50):
        n = rng.randint(2, 9)
        a = random_adjacency(rng, n)
        t = topological_overlap(a)
        b = tom_brute(a)
        for i in range(n):
            for j in range(n):
                assert math.isclose(t[i][j], b[i][j], rel_tol=1e-12)
                assert t[i][j] == t[j][i]
                assert -1e-15 <= t[i][j] <= 1 + 1e-15


def test_tom_extremes():
    full = [[1.0] * 5 for _ in range(5)]
    assert all(math.isclose(v, 1.0) for row in topological_overlap(full) for v in row)
    empty = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    t = topological_overlap(empty)
    assert all(t[i][j] == 0.0 for i in range(4) for j in range(4) if i != j)


def brute_average_linkage(d):
    """Recompute every cluster distance as the mean of the pairwise distances."""
    clusters = [(i,) for i in range(len(d))]
    heights = []
    sets = []
    while len(clusters) > 1:
        best = None
        for x, y in itertools.combinations(range(len(clusters)), 2):
            a, b = clusters[x], clusters[y]
            h = sum(d[i][j] for i in a for j in b) / (len(a) * len(b))
            if best is None or h < best[0]:
                best = (h, x, y)
        h, x, y = best
        new = tuple(sorted(clusters[x] + clusters[y]))
        clusters = [c for i, c in enumerate(clusters) if i not in (x, y)] + [new]
        heights.append(h)
        sets.append(new)
    return heights, sets


def test_average_linkage_matches_brute_force_and_is_monotone():
    rng = random.Random(73)
    for _ in range(60):
        n = rng.randint(2, 10)
        d = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d[i][j] = d[j][i] = rng.random()
        merges = average_linkage(d)
        heights, sets = brute_average_linkage(d)
        assert [m[3] for m in merges] == sets
        for m, h in zip(merges, heights):
            assert math.isclose(m[2], h, rel_tol=1e-12)
        assert all(merges[t][2] <= merges[t + 1][2] + 1e-12 for t in range(len(merges) - 1))


def test_cut_tree_labels():
    d = [[0, 1, 9, 9, 9], [1, 0, 9, 9, 9], [9, 9, 0, 2, 9], [9, 9, 2, 0, 9], [9, 9, 9, 9, 0]]
    merges = average_linkage(d)
    assert cut_tree(merges, 5, 2.5) == [1, 1, 2, 2, 3]
    assert cut_tree(merges, 5, 2.5, min_size=2) == [1, 1, 2, 2, 0]
    assert cut_tree(merges, 5, 0.5) == [1, 2, 3, 4, 5]
    assert cut_tree(merges, 5, 100) == [1] * 5


def test_eigengene_of_a_rank_one_module():
    rng = random.Random(74)
    pattern = [rng.gauss(0, 1) for _ in range(7)]
    expr = [[c * p + b for p in pattern] for c, b in ((1.0, 3.0), (2.5, -1.0), (0.3, 0.0), (4.0, 2.0))]
    v = eigengene(expr)
    z = standardize(pattern)
    norm = math.sqrt(sum(t * t for t in z))
    for a, b in zip(v, z):
        assert math.isclose(a, b / norm, rel_tol=1e-9, abs_tol=1e-12)


def test_eigengene_is_the_top_eigenvector():
    rng = random.Random(75)
    expr = [[rng.gauss(0, 1) for _ in range(6)] for _ in range(9)]
    v = eigengene(expr)
    x = [standardize(row) for row in expr]
    c = [[sum(row[s] * row[t] for row in x) for t in range(6)] for s in range(6)]
    cv = [sum(c[s][t] * v[t] for t in range(6)) for s in range(6)]
    lam = sum(a * b for a, b in zip(v, cv))
    assert math.isclose(sum(t * t for t in v), 1.0, rel_tol=1e-12)
    for a, b in zip(cv, v):
        assert math.isclose(a, lam * b, rel_tol=1e-6, abs_tol=1e-9)
    for _ in range(200):
        u = [rng.gauss(0, 1) for _ in range(6)]
        nu = math.sqrt(sum(t * t for t in u))
        u = [t / nu for t in u]
        cu = [sum(c[s][t] * u[t] for t in range(6)) for s in range(6)]
        assert sum(a * b for a, b in zip(u, cu)) <= lam + 1e-9


def test_scale_free_fit_matches_a_direct_regression():
    rng = random.Random(76)
    k = [rng.paretovariate(1.5) for _ in range(400)]
    r2, slope = scale_free_fit(k)
    lo, hi = min(k), max(k)
    w = (hi - lo) / 10
    bins = {}
    for v in k:
        bins.setdefault(min(int((v - lo) / w), 9), []).append(v)
    xs = [math.log10(statistics.mean(vs)) for _, vs in sorted(bins.items())]
    ys = [math.log10(len(vs) / 400) for _, vs in sorted(bins.items())]
    fit = statistics.linear_regression(xs, ys)
    assert math.isclose(slope, fit.slope, rel_tol=1e-9)
    assert math.isclose(r2, statistics.correlation(xs, ys) ** 2, rel_tol=1e-9)
    assert slope < 0


def test_planted_modules_measurement():
    # A measurement with a fixed seed: two modules of 8 genes, each driven by
    # its own hidden factor, and 4 noise genes, over 20 samples.
    rng = random.Random(77)
    samples = 20
    f1 = [rng.gauss(0, 1) for _ in range(samples)]
    f2 = [rng.gauss(0, 1) for _ in range(samples)]
    expr = []
    for f in (f1, f2):
        for _ in range(8):
            c = rng.choice([1.0, -1.0]) * rng.uniform(0.8, 1.2)
            expr.append([c * x + rng.gauss(0, 0.3) for x in f])
    for _ in range(4):
        expr.append([rng.gauss(0, 1) for _ in range(samples)])
    labels, eig = wgcna(expr, beta=6, height=0.8, min_size=4)
    first, second = set(labels[:8]), set(labels[8:16])
    assert len(first) == 1 and len(second) == 1 and first != second and 0 not in first | second
    assert all(lab == 0 for lab in labels[16:])
    for lab, f in ((labels[0], f1), (labels[8], f2)):
        assert abs(pearson(eig[lab], f)) > 0.95
    r = correlation_matrix(expr)
    assert r[0][1] == r[1][0]
