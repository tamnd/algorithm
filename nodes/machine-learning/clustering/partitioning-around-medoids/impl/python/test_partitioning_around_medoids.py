# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partitioning-around-medoids/. The authors are listed in prov/52CM06.jsonl.

import random
from itertools import combinations

from partitioning_around_medoids import build, pam, swap_delta, _nearest_two, total_cost

PTS = [(9, 4), (5, 8), (0, 7), (3, 0), (2, 1), (5, 7), (3, 6)]


def manhattan_matrix(pts):
    return [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in pts] for p in pts]


def brute(D, k):
    return min(total_cost(D, c) for c in combinations(range(len(D)), k))


def is_swap_local_optimum(D, medoids):
    base = total_cost(D, medoids)
    for m in medoids:
        for h in range(len(D)):
            if h not in medoids:
                new = [h if x == m else x for x in medoids]
                if total_cost(D, new) < base:
                    return False
    return True


def test_worked_example():
    D = manhattan_matrix(PTS)
    assert build(D, 2) == [6, 3]
    assert total_cost(D, [6, 3]) == 21
    trace = []
    medoids, labels, cost = pam(D, 2, trace)
    assert trace == [(6, 5, -3)]
    assert sorted(medoids) == [3, 5] and cost == 18 == brute(D, 2)
    assert labels == [0, 0, 0, 1, 1, 0, 0]


def test_swap_delta_matches_recomputation():
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(3, 8)
        D = manhattan_matrix([(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(n)])
        k = rng.randint(1, n - 1)
        M = rng.sample(range(n), k)
        info = _nearest_two(D, M)
        for m in M:
            for h in range(n):
                if h not in M:
                    new = [h if x == m else x for x in M]
                    assert swap_delta(D, M, info, m, h) == total_cost(D, new) - total_cost(D, M)


def test_local_optimum_and_brute_force():
    rng = random.Random(4)
    for _ in range(150):
        n = rng.randint(2, 9)
        D = manhattan_matrix([(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(n)])
        k = rng.randint(1, n)
        medoids, labels, cost = pam(D, k)
        assert len(set(medoids)) == k
        assert cost == total_cost(D, medoids)
        assert is_swap_local_optimum(D, medoids)
        opt = brute(D, k)
        # Manhattan distances form a metric: single swap locality gap 5
        assert opt <= cost <= 5 * opt
        assert cost <= total_cost(D, build(D, k))


def test_non_metric_dissimilarity():
    # squared distances break the triangle inequality; PAM still stops at a
    # local optimum of the given dissimilarities
    rng = random.Random(5)
    for _ in range(50):
        n = rng.randint(2, 8)
        xs = [rng.randint(0, 30) for _ in range(n)]
        D = [[(a - b) ** 2 for b in xs] for a in xs]
        k = rng.randint(1, n)
        medoids, _, cost = pam(D, k)
        assert is_swap_local_optimum(D, medoids)
        assert cost >= brute(D, k)
