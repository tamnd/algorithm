# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ward-method/. The authors are listed in prov/G4DBR6.jsonl.

import random
from fractions import Fraction

from ward_method import merge_cost, sum_of_squares, ward_method


def centroid(P, S):
    return [Fraction(sum(P[i][t] for i in S), len(S)) for t in range(len(P[0]))]


def naive(P):
    """Greedy merging by the increase of the sum of squares, recomputed from the points.
    Returns None if two pairs tie for the least increase at some step."""
    clusters = [[i] for i in range(len(P))]
    out = []
    while len(clusters) > 1:
        vals = sorted(
            ((sum_of_squares(P, clusters[x] + clusters[y]) - sum_of_squares(P, clusters[x]) - sum_of_squares(P, clusters[y]), x, y)
             for x in range(len(clusters)) for y in range(x + 1, len(clusters))),
            key=lambda t: t[0],
        )
        if len(vals) > 1 and vals[0][0] == vals[1][0]:
            return None
        h, x, y = vals[0]
        out.append((frozenset(clusters[x] + clusters[y]), h))
        clusters = [c for t, c in enumerate(clusters) if t not in (x, y)] + [clusters[x] + clusters[y]]
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
    P = [[0], [2], [3], [7], [13], [21]]
    got = ward_method(P)
    assert got == [
        (1, 2, Fraction(1, 2), 2),
        (0, 6, Fraction(25, 6), 3),
        (3, 4, 18, 2),
        (5, 8, Fraction(242, 3), 3),
        (7, 9, 216, 6),
    ]
    assert sum(h for _, _, h, _ in got) == sum_of_squares(P, range(6)) == Fraction(958, 3)


def test_edges():
    assert ward_method([]) == []
    assert ward_method([[5, 5]]) == []
    assert ward_method([[0, 0], [3, 4]]) == [(0, 1, Fraction(25, 2), 2)]


def test_increase_identity():
    rng = random.Random(1)
    for _ in range(500):
        d = rng.randrange(1, 4)
        P = [[rng.randrange(-9, 10) for _ in range(d)] for _ in range(rng.randrange(2, 9))]
        idx = list(range(len(P)))
        rng.shuffle(idx)
        cut = rng.randrange(1, len(P))
        A, B = idx[:cut], idx[cut:]
        lhs = sum_of_squares(P, A + B) - sum_of_squares(P, A) - sum_of_squares(P, B)
        assert lhs == merge_cost(len(A), centroid(P, A), len(B), centroid(P, B))


def test_against_naive():
    rng = random.Random(23)
    done = 0
    while done < 300:
        n = rng.randrange(2, 8)
        P = [[rng.randrange(-20, 21) for _ in range(2)] for _ in range(n)]
        want = naive(P)
        if want is None:
            continue
        got = ward_method(P)
        assert as_sets(n, got) == want
        assert sum(h for _, _, h, _ in got) == sum_of_squares(P, range(n))
        done += 1


def test_monotone_heights():
    rng = random.Random(4)
    for _ in range(200):
        P = [[rng.randrange(0, 5) for _ in range(2)] for _ in range(rng.randrange(1, 9))]
        hs = [h for _, _, h, _ in ward_method(P)]
        assert hs == sorted(hs)


def test_not_an_optimal_k_means_partition():
    P = [[0], [1], [2], [3], [5]]
    merges = ward_method(P)
    top = as_sets(5, merges)
    assert top[-2][0] == frozenset({0, 1, 2, 3})
    assert sum_of_squares(P, [0, 1, 2, 3]) + sum_of_squares(P, [4]) == 5
    assert sum_of_squares(P, [0, 1, 2]) + sum_of_squares(P, [3, 4]) == 4
