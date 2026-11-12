# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/agglomerative-clustering/. The authors are listed in prov/G398XN.jsonl.

import random
from fractions import Fraction

import pytest

from agglomerative_clustering import (
    LINKAGES,
    agglomerative_clustering,
    agglomerative_clustering_heap,
    lance_williams,
    merges_to_sets,
)


def sq(u, v):
    return sum((a - b) ** 2 for a, b in zip(u, v))


def mean(pts):
    return [Fraction(sum(c), len(pts)) for c in zip(*pts)]


def sse(pts):
    c = mean(pts)
    return sum(sq(p, c) for p in pts)


def direct(linkage, P, D, wa, wb):
    """The linkage of clusters A and B from the points. wa and wb map each
    point index to its weight 2^(-depth) in the merge tree of its cluster."""
    A, B = list(wa), list(wb)
    if linkage == "single":
        return min(D[i][j] for i in A for j in B)
    if linkage == "complete":
        return max(D[i][j] for i in A for j in B)
    if linkage == "average":
        return Fraction(sum(D[i][j] for i in A for j in B), len(A) * len(B))
    if linkage == "weighted":
        return sum(wa[i] * wb[j] * D[i][j] for i in A for j in B)
    if linkage == "centroid":
        return sq(mean([P[i] for i in A]), mean([P[j] for j in B]))
    if linkage == "median":
        ma = [sum(wa[i] * P[i][t] for i in A) for t in range(len(P[0]))]
        mb = [sum(wb[j] * P[j][t] for j in B) for t in range(len(P[0]))]
        return sq(ma, mb)
    assert linkage == "ward"
    return 2 * (sse([P[i] for i in A + B]) - sse([P[i] for i in A]) - sse([P[i] for i in B]))


def oracle(P, D, linkage):
    """Greedy agglomeration that recomputes each linkage from the points.
    Returns None when two pairs tie for the least value."""
    clusters = [{i: Fraction(1)} for i in range(len(P))]
    out = []
    while len(clusters) > 1:
        vals = []
        for x in range(len(clusters)):
            for y in range(x + 1, len(clusters)):
                vals.append((direct(linkage, P, D, clusters[x], clusters[y]), x, y))
        vals.sort(key=lambda t: t[0])
        if len(vals) > 1 and vals[0][0] == vals[1][0]:
            return None
        h, x, y = vals[0]
        a, b = clusters[x], clusters[y]
        out.append((frozenset(a), frozenset(b), h))
        new = {i: w / 2 for i, w in a.items()}
        new.update({j: w / 2 for j, w in b.items()})
        clusters = [c for t, c in enumerate(clusters) if t not in (x, y)] + [new]
    return out


def canon(triples):
    return sorted((tuple(sorted(a | b)), h) for a, b, h in triples)


def line(xs):
    return [[abs(a - b) for b in xs] for a in xs]


def test_worked_example():
    D = line([0, 2, 3, 7, 13, 21])
    assert agglomerative_clustering(D, "single") == [(1, 2, 1, 2), (0, 6, 2, 3), (3, 7, 4, 4), (4, 8, 6, 5), (5, 9, 8, 6)]
    assert agglomerative_clustering(D, "complete") == [(1, 2, 1, 2), (0, 6, 3, 3), (3, 4, 6, 2), (7, 8, 13, 5), (5, 9, 21, 6)]
    got = agglomerative_clustering(D, "average")
    assert [h for _, _, h, _ in got] == [1, Fraction(5, 2), Fraction(16, 3), 8, 14]
    assert [(a, b) for a, b, _, _ in got] == [(1, 2), (0, 6), (3, 7), (4, 5), (8, 9)]


def test_edges():
    for linkage in LINKAGES:
        assert agglomerative_clustering([], linkage) == []
        assert agglomerative_clustering([[0]], linkage) == []
        assert agglomerative_clustering([[0, 5], [5, 0]], linkage) == [(0, 1, 5, 2)]
    with pytest.raises(ValueError):
        agglomerative_clustering([[0]], "nearest")


def test_lance_williams_rows_against_points():
    rng = random.Random(7)
    for _ in range(300):
        pts = [[rng.randrange(-9, 10) for _ in range(2)] for _ in range(rng.randrange(3, 8))]
        D = [[sq(p, q) for q in pts] for p in pts]
        idx = list(range(len(pts)))
        rng.shuffle(idx)
        c1, c2 = sorted(rng.sample(range(1, len(idx)), 2))
        I, J, K = idx[:c1], idx[c1:c2], idx[c2:]
        for linkage in ("single", "complete", "average", "centroid", "ward"):
            w = lambda S: {i: Fraction(1) for i in S}
            want = direct(linkage, pts, D, w(K), w(I + J))
            got = lance_williams(
                linkage,
                direct(linkage, pts, D, w(K), w(I)),
                direct(linkage, pts, D, w(K), w(J)),
                direct(linkage, pts, D, w(I), w(J)),
                len(I), len(J), len(K),
            )
            assert got == want, linkage


def test_every_linkage_against_recomputation():
    rng = random.Random(11)
    checked = 0
    while checked < 250:
        n = rng.randrange(2, 8)
        P = [[rng.randrange(-20, 21) for _ in range(2)] for _ in range(n)]
        D = [[sq(p, q) for q in P] for p in P]
        linkage = LINKAGES[checked % len(LINKAGES)]
        want = oracle(P, D, linkage)
        if want is None:
            continue
        got = merges_to_sets(n, agglomerative_clustering(D, linkage))
        assert [(a | b, h) for a, b, h in got] == [(a | b, h) for a, b, h in want], linkage
        checked += 1


def test_heap_version_matches():
    rng = random.Random(3)
    for t in range(500):
        n = rng.randrange(0, 9)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randrange(1, 12)
        linkage = LINKAGES[t % len(LINKAGES)]
        assert agglomerative_clustering_heap(D, linkage) == agglomerative_clustering(D, linkage)


def test_monotone_and_inversion():
    rng = random.Random(5)
    for t in range(300):
        n = rng.randrange(2, 9)
        P = [[rng.randrange(-20, 21) for _ in range(2)] for _ in range(n)]
        D = [[sq(p, q) for q in P] for p in P]
        for linkage in ("single", "complete", "average", "weighted", "ward"):
            hs = [h for _, _, h, _ in agglomerative_clustering(D, linkage)]
            assert hs == sorted(hs), linkage
    P = [[0, 0], [8, 0], [4, 7]]
    D = [[sq(p, q) for q in P] for p in P]
    for linkage in ("centroid", "median"):
        assert [h for _, _, h, _ in agglomerative_clustering(D, linkage)] == [64, 49]
