# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-linkage-clustering/. The authors are listed in prov/NRPC50.jsonl.

import itertools
import random

from single_linkage_clustering import cut_into_k, single_linkage_clustering, spacing


def naive(D):
    """Greedy agglomeration with the minimum over member pairs, recomputed each step."""
    clusters = [frozenset([i]) for i in range(len(D))]
    out = []
    while len(clusters) > 1:
        h, x, y = min(
            (min(D[i][j] for i in clusters[x] for j in clusters[y]), x, y)
            for x in range(len(clusters))
            for y in range(x + 1, len(clusters))
        )
        out.append((clusters[x] | clusters[y], h))
        clusters = [c for t, c in enumerate(clusters) if t not in (x, y)] + [clusters[x] | clusters[y]]
    return out


def sets_of(n, merges):
    sets = [frozenset([i]) for i in range(n)]
    out = []
    for a, b, h, size in merges:
        assert len(sets[a] | sets[b]) == size and not sets[a] & sets[b]
        sets.append(sets[a] | sets[b])
        out.append((sets[-1], h))
    return out


def partition_at(n, D, h):
    """Components of the graph with the edges of weight at most h."""
    comp = list(range(n))
    for _ in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][j] <= h and comp[j] < comp[i]:
                    comp[i] = comp[j]
    return sorted(sorted(i for i in range(n) if comp[i] == c) for c in set(comp))


def random_matrix(rng, n, top):
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            D[i][j] = D[j][i] = rng.randrange(1, top)
    return D


def all_partitions(items, k):
    if k == 0:
        if not items:
            yield []
        return
    if not items:
        return
    first, rest = items[0], items[1:]
    for p in all_partitions(rest, k - 1):
        yield [[first]] + p
    for p in all_partitions(rest, k):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]


def test_worked_example():
    xs = [0, 2, 3, 7, 13, 21]
    D = [[abs(a - b) for b in xs] for a in xs]
    assert single_linkage_clustering(D) == [(1, 2, 1, 2), (0, 6, 2, 3), (3, 7, 4, 4), (4, 8, 6, 5), (5, 9, 8, 6)]
    m = single_linkage_clustering(D)
    assert cut_into_k(6, m, 3) == [0, 0, 0, 0, 1, 2]
    assert spacing(D, cut_into_k(6, m, 3)) == 6


def test_edges():
    assert single_linkage_clustering([]) == []
    assert single_linkage_clustering([[0]]) == []
    assert single_linkage_clustering([[0, 3], [3, 0]]) == [(0, 1, 3, 2)]
    D = [[0, 2, 2], [2, 0, 2], [2, 2, 0]]
    assert [h for _, _, h, _ in single_linkage_clustering(D)] == [2, 2]


def test_distinct_distances_against_naive():
    rng = random.Random(21)
    for _ in range(500):
        n = rng.randrange(1, 9)
        vals = rng.sample(range(1, 200), n * (n - 1) // 2)
        D = [[0] * n for _ in range(n)]
        it = iter(vals)
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = next(it)
        assert sorted(sets_of(n, single_linkage_clustering(D)), key=lambda t: t[1]) == naive(D)


def test_ties_give_the_threshold_partitions():
    rng = random.Random(4)
    for _ in range(500):
        n = rng.randrange(1, 8)
        D = random_matrix(rng, n, 5)
        merges = single_linkage_clustering(D)
        hs = [h for _, _, h, _ in merges]
        assert hs == sorted(hs)
        assert hs == [h for _, h in naive(D)]
        for h in set(hs):
            k = n - sum(1 for x in hs if x <= h)
            got = cut_into_k(n, merges, k)
            parts = sorted(sorted(i for i in range(n) if got[i] == c) for c in set(got))
            assert parts == partition_at(n, D, h)


def test_cut_has_maximum_spacing():
    rng = random.Random(8)
    for _ in range(150):
        n = rng.randrange(2, 8)
        D = random_matrix(rng, n, 9)
        merges = single_linkage_clustering(D)
        for k in range(2, n + 1):
            best = max(
                spacing(D, [next(c for c, part in enumerate(p) if i in part) for i in range(n)])
                for p in all_partitions(list(range(n)), k)
            )
            assert spacing(D, cut_into_k(n, merges, k)) == best


def test_mst_weight_is_minimum():
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randrange(2, 6)
        D = random_matrix(rng, n, 9)
        total = sum(h for _, _, h, _ in single_linkage_clustering(D))
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        best = None
        for es in itertools.combinations(pairs, n - 1):
            comp = list(range(n))
            ok = True
            for i, j in es:
                a, b = comp[i], comp[j]
                if a == b:
                    ok = False
                    break
                comp = [a if c == b else c for c in comp]
            if ok:
                w = sum(D[i][j] for i, j in es)
                best = w if best is None else min(best, w)
        assert total == best
