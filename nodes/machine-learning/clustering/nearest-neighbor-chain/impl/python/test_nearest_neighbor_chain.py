# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-chain/. The authors are listed in prov/5P8XRG.jsonl.

import random
from fractions import Fraction

import pytest

from nearest_neighbor_chain import REDUCIBLE, nearest_neighbor_chain


def sq(u, v):
    return sum((a - b) ** 2 for a, b in zip(u, v))


def sse(pts):
    c = [Fraction(sum(x), len(pts)) for x in zip(*pts)]
    return sum(sq(p, c) for p in pts)


def linkage_value(name, P, D, wa, wb):
    A, B = list(wa), list(wb)
    if name == "single":
        return min(D[i][j] for i in A for j in B)
    if name == "complete":
        return max(D[i][j] for i in A for j in B)
    if name == "average":
        return Fraction(sum(D[i][j] for i in A for j in B), len(A) * len(B))
    if name == "weighted":
        return sum(wa[i] * wb[j] * D[i][j] for i in A for j in B)
    return 2 * (sse([P[i] for i in A + B]) - sse([P[i] for i in A]) - sse([P[i] for i in B]))


def greedy(P, D, name):
    """The naive greedy method with each linkage recomputed from the points.
    Returns None if two pairs tie for the least value at some step."""
    clusters = [{i: Fraction(1)} for i in range(len(P))]
    out = []
    while len(clusters) > 1:
        vals = sorted(
            ((linkage_value(name, P, D, clusters[x], clusters[y]), x, y)
             for x in range(len(clusters)) for y in range(x + 1, len(clusters))),
            key=lambda t: t[0],
        )
        if len(vals) > 1 and vals[0][0] == vals[1][0]:
            return None
        h, x, y = vals[0]
        new = {i: w / 2 for i, w in clusters[x].items()}
        new.update({j: w / 2 for j, w in clusters[y].items()})
        out.append((frozenset(new), h))
        clusters = [c for t, c in enumerate(clusters) if t not in (x, y)] + [new]
    return out


def as_sets(n, merges):
    sets = [frozenset([i]) for i in range(n)]
    out = []
    for a, b, h, size in merges:
        assert not sets[a] & sets[b] and len(sets[a] | sets[b]) == size
        sets.append(sets[a] | sets[b])
        out.append((sets[-1], h))
    return out


def test_worked_example():
    xs = [0, 2, 3, 7, 13, 21]
    D = [[abs(a - b) for b in xs] for a in xs]
    assert nearest_neighbor_chain(D, "complete") == [(1, 2, 1, 2), (0, 6, 3, 3), (3, 4, 6, 2), (7, 8, 13, 5), (5, 9, 21, 6)]
    got = nearest_neighbor_chain(D, "average")
    assert [h for _, _, h, _ in got] == [1, Fraction(5, 2), Fraction(16, 3), 8, 14]


def test_edges():
    for name in REDUCIBLE:
        assert nearest_neighbor_chain([], name) == []
        assert nearest_neighbor_chain([[0]], name) == []
        assert nearest_neighbor_chain([[0, 4], [4, 0]], name) == [(0, 1, 4, 2)]
    for name in ("centroid", "median"):
        with pytest.raises(ValueError):
            nearest_neighbor_chain([[0]], name)


def test_same_hierarchy_as_greedy():
    rng = random.Random(17)
    done = 0
    while done < 500:
        n = rng.randrange(2, 9)
        P = [[rng.randrange(-30, 31) for _ in range(2)] for _ in range(n)]
        D = [[sq(p, q) for q in P] for p in P]
        name = REDUCIBLE[done % len(REDUCIBLE)]
        want = greedy(P, D, name)
        if want is None:
            continue
        assert as_sets(n, nearest_neighbor_chain(D, name)) == want, name
        done += 1


def test_ties_still_give_a_monotone_hierarchy():
    rng = random.Random(9)
    for t in range(400):
        n = rng.randrange(1, 9)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randrange(1, 4)
        name = REDUCIBLE[t % 4]
        merges = nearest_neighbor_chain(D, name)
        hs = [h for _, _, h, _ in merges]
        assert len(merges) == max(n - 1, 0) and hs == sorted(hs)
        if merges:
            assert as_sets(n, merges)[-1][0] == frozenset(range(n))
