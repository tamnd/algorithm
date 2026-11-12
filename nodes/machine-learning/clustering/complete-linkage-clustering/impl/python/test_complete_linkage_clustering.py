# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/complete-linkage-clustering/. The authors are listed in prov/6884Z8.jsonl.

import random

from complete_linkage_clustering import complete_linkage_clustering, cut_into_k


def line(xs):
    return [[abs(a - b) for b in xs] for a in xs]


def naive(D):
    """Greedy agglomeration with the largest member distance recomputed each step."""
    clusters = [frozenset([i]) for i in range(len(D))]
    out = []
    while len(clusters) > 1:
        h, x, y = min(
            (max(D[i][j] for i in clusters[x] for j in clusters[y]), x, y)
            for x in range(len(clusters))
            for y in range(x + 1, len(clusters))
        )
        out.append((clusters[x] | clusters[y], h))
        clusters = [c for t, c in enumerate(clusters) if t not in (x, y)] + [clusters[x] | clusters[y]]
    return out


def as_sets(n, merges):
    sets = [frozenset([i]) for i in range(n)]
    out = []
    for a, b, h, size in merges:
        assert not sets[a] & sets[b] and len(sets[a] | sets[b]) == size
        sets.append(sets[a] | sets[b])
        out.append((sets[-1], h))
    return out


def diameter(D, labels, c):
    pts = [i for i in range(len(D)) if labels[i] == c]
    return max((D[i][j] for i in pts for j in pts), default=0)


def test_worked_example():
    D = line([0, 2, 3, 7, 13, 21])
    assert complete_linkage_clustering(D) == [(1, 2, 1, 2), (0, 6, 3, 3), (3, 4, 6, 2), (7, 8, 13, 5), (5, 9, 21, 6)]


def test_edges():
    assert complete_linkage_clustering([]) == []
    assert complete_linkage_clustering([[0]]) == []
    assert complete_linkage_clustering([[0, 2], [2, 0]]) == [(0, 1, 2, 2)]


def test_distinct_distances_against_naive():
    rng = random.Random(31)
    for _ in range(500):
        n = rng.randrange(1, 9)
        vals = rng.sample(range(1, 300), n * (n - 1) // 2)
        D = [[0] * n for _ in range(n)]
        it = iter(vals)
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = next(it)
        assert as_sets(n, complete_linkage_clustering(D)) == naive(D)


def test_height_bounds_member_distances():
    rng = random.Random(6)
    for _ in range(300):
        n = rng.randrange(2, 9)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randrange(1, 7)
        merges = complete_linkage_clustering(D)
        hs = [h for _, _, h, _ in merges]
        assert hs == sorted(hs)
        for s, h in as_sets(n, merges):
            assert h == max(D[i][j] for i in s for j in s)


def test_not_an_optimal_k_diameter_clustering():
    D = line([0, 1, 6, 9, 13])
    labels = cut_into_k(5, complete_linkage_clustering(D), 2)
    assert labels == [0, 0, 1, 1, 1]
    assert max(diameter(D, labels, c) for c in (0, 1)) == 7
    better = [0, 0, 0, 1, 1]
    assert max(diameter(D, better, c) for c in (0, 1)) == 6
