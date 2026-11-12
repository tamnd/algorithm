# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dali/. The authors are listed in prov/YVJ262.jsonl.

import itertools
import math
import random

from dali import candidate_fragments, dali, distance_matrix, elastic_score, phi


def helix(n):
    """An ideal alpha-helix C-alpha trace: radius 2.3 A, 100 degrees and 1.5 A per residue."""
    return [(2.3 * math.cos(math.radians(100 * i)), 2.3 * math.sin(math.radians(100 * i)), 1.5 * i) for i in range(n)]


def direct_score(m, a, b, theta=0.2, alpha=20.0):
    """The elastic score written out again, as a double sum over all ordered pairs."""
    s = 0.0
    for (i, j) in m:
        for (i2, j2) in m:
            if (i, j) == (i2, j2):
                s += theta
                continue
            da, db = math.dist(a[i], a[i2]), math.dist(b[j], b[j2])
            dstar = (da + db) / 2
            s += (theta - abs(da - db) / dstar) * math.exp(-(dstar / alpha) ** 2) if dstar > 0 else theta
    return s


def brute_force(a, b):
    """The best elastic score over all sequential alignments."""
    dA, dB = distance_matrix(a), distance_matrix(b)
    best = 0.0
    for k in range(1, min(len(a), len(b)) + 1):
        for si in itertools.combinations(range(len(a)), k):
            for sj in itertools.combinations(range(len(b)), k):
                best = max(best, elastic_score(list(zip(si, sj)), dA, dB))
    return best


def is_sequential(m):
    return all(m[k][0] < m[k + 1][0] and m[k][1] < m[k + 1][1] for k in range(len(m) - 1))


def test_phi_values_of_the_page() -> None:
    assert abs(phi(5, 5) - 0.1879) < 1e-4
    assert abs(phi(5, 6) - 0.0169) < 1e-4
    assert abs(phi(5, 7) + 0.1219) < 1e-4
    assert abs(phi(20, 20) - 0.0736) < 1e-4
    assert abs(phi(20, 22) - 0.0348) < 1e-4


def test_example_of_the_page() -> None:
    a = helix(12)
    b = a[:6] + [(6.0, 6.0, 8.0), (6.5, 4.0, 9.0)] + a[6:]
    planted = [(i, i if i < 6 else i + 2) for i in range(12)]
    s, m = dali(a, b, w=4)
    assert m == planted
    assert abs(s - 24.8241) < 1e-4
    assert len(candidate_fragments(distance_matrix(a), distance_matrix(b), 4)) == 72


def test_edges() -> None:
    a = helix(16)
    s, m = dali(a, a, w=6)
    assert m == [(i, i) for i in range(16)]
    assert abs(s - direct_score(m, a, a)) < 1e-9
    s, m = dali([(0.0, 0.0, 0.0)], [(1.0, 1.0, 1.0)])
    assert m == [(0, 0)] and abs(s - 0.2) < 1e-12
    s, m = dali([], [(1.0, 1.0, 1.0)])
    assert m == [] and s == 0.0


def test_score_against_direct_sum() -> None:
    rng = random.Random(6)
    for _ in range(500):
        n, k = rng.randint(1, 12), rng.randint(0, 6)
        a = [tuple(rng.uniform(-15, 15) for _ in range(3)) for _ in range(n)]
        b = [tuple(rng.uniform(-15, 15) for _ in range(3)) for _ in range(n)]
        k = min(k, n)
        m = list(zip(sorted(rng.sample(range(n), k)), sorted(rng.sample(range(n), k))))
        assert abs(elastic_score(m, distance_matrix(a), distance_matrix(b)) - direct_score(m, a, b)) < 1e-9


def test_search_against_brute_force() -> None:
    rng = random.Random(1)
    hits = 0
    trials = 500
    for t in range(trials):
        n, m = rng.randint(2, 5), rng.randint(2, 5)
        if t % 2 == 0:  # random points
            a = [tuple(rng.uniform(-8, 8) for _ in range(3)) for _ in range(n)]
            b = [tuple(rng.uniform(-8, 8) for _ in range(3)) for _ in range(m)]
        else:  # b is a noisy copy of part of a chain
            a = [tuple(rng.uniform(-8, 8) for _ in range(3)) for _ in range(n)]
            b = [tuple(c + rng.gauss(0, 0.7) for c in p) for p in a[:m]] + \
                [tuple(rng.uniform(-8, 8) for _ in range(3)) for _ in range(max(0, m - n))]
        s, mm = dali(a, b, w=1, seeds=3, steps=150, seed=t)
        assert is_sequential(mm)
        assert len({i for i, _ in mm}) == len(mm) == len({j for _, j in mm})
        assert abs(s - direct_score(mm, a, b)) < 1e-9
        best = brute_force(a, b)
        assert s <= best + 1e-9  # a heuristic never beats the optimum
        hits += abs(s - best) < 1e-9
    assert hits >= 0.85 * trials
