# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lin-kernighan-helsgaun/. The authors are listed in prov/44V9MX.jsonl.

import itertools
import math
import random

from lin_kernighan_helsgaun import (
    alpha_lists,
    alpha_values,
    ascent,
    degrees,
    lk_search,
    lkh,
    one_tree,
    tour_cost,
    transformed,
)

SEVEN = [(1, 2), (0, 5), (3, 3), (1, 0), (0, 0), (3, 4), (2, 6)]  # A to G of the page


def euclid(points):
    return [[math.dist(a, b) for b in points] for a in points]


def random_metric(n, rng):
    w = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w[i][j] = w[j][i] = rng.choice([1, 2, 3, 5, 8])
    for k in range(n):
        for i in range(n):
            for j in range(n):
                w[i][j] = min(w[i][j], w[i][k] + w[k][j])
    return w


def brute_opt(cost):
    n = len(cost)
    return min(tour_cost(cost, [0, *q]) for q in itertools.permutations(range(1, n)))


def all_one_trees(n, special=0):
    """Every 1-tree: degree 2 at special, and a spanning tree on the other cities."""
    pairs = list(itertools.combinations(range(n), 2))
    for chosen in itertools.combinations(pairs, n):
        if sum(special in e for e in chosen) != 2:
            continue
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        ok = True
        for u, v in chosen:
            if special in (u, v):
                continue
            ru, rv = find(u), find(v)
            if ru == rv:
                ok = False
                break
            parent[ru] = rv
        if ok:
            yield chosen


def test_one_tree_and_alpha_against_enumeration() -> None:
    rng = random.Random(70)
    for n in (4, 5, 6):
        for _ in range(3):
            d = euclid([(rng.random(), rng.random()) for _ in range(n)])
            trees = [(sum(d[u][v] for u, v in t), t) for t in all_one_trees(n)]
            best = min(length for length, _ in trees)
            assert abs(one_tree(d)[0] - best) < 1e-9
            a = alpha_values(d)
            for i, j in itertools.combinations(range(n), 2):
                forced = min(length for length, t in trees if (i, j) in t)
                assert abs(a[i][j] - (forced - best)) < 1e-9
                assert a[i][j] == a[j][i] and a[i][j] >= -1e-12


def test_lower_bound_never_exceeds_opt() -> None:
    rng = random.Random(1970)
    for n in range(5, 9):
        for trial in range(4):
            cost = random_metric(n, rng) if trial % 2 else euclid([(rng.random(), rng.random()) for _ in range(n)])
            opt = brute_opt(cost)
            pi = [rng.uniform(-0.5, 0.5) for _ in range(n)]
            assert one_tree(transformed(cost, pi))[0] - 2 * sum(pi) <= opt + 1e-9
            w, pi = ascent(cost)
            assert one_tree(cost)[0] - 1e-9 <= w <= opt + 1e-9


def test_example() -> None:
    cost = euclid(SEVEN)
    length, edges = one_tree(cost)  # special city A
    assert abs(length - 14.3138) < 1e-3
    assert degrees(7, edges)[2:4] == [3, 3]  # C and D have degree 3
    a = alpha_values(cost)
    assert abs(a[0][1] - (math.sqrt(10) - math.sqrt(5))) < 1e-9  # alpha(A, B)
    assert abs(a[4][2] - (math.sqrt(18) - math.sqrt(13))) < 1e-9  # alpha(E, C)
    w, pi = ascent(cost)
    assert abs(w - 15.4760) < 1e-3  # equal to OPT: the ascent proves A E D C F G B optimal
    _, edges = one_tree(transformed(cost, pi))
    assert degrees(7, edges) == [2] * 7
    assert abs(brute_opt(cost) - w) < 1e-9


def test_alpha_lists_hold_more_optimal_edges() -> None:
    rng = random.Random(2000)
    hits_alpha = hits_near = 0
    for _ in range(20):
        n = 8
        cost = euclid([(rng.random(), rng.random()) for _ in range(n)])
        best = min(([0, *q] for q in itertools.permutations(range(1, n))), key=lambda t: tour_cost(cost, t))
        alpha = alpha_lists(cost, 3)
        near = [sorted((j for j in range(n) if j != i), key=lambda j: (cost[i][j], j))[:3] for i in range(n)]
        for i in range(n):
            u, v = best[i], best[(i + 1) % n]
            hits_alpha += (v in alpha[u]) + (u in alpha[v])
            hits_near += (v in near[u]) + (u in near[v])
    assert hits_alpha >= hits_near  # measured on these seeds, not a theorem


def test_lkh_is_a_local_optimum() -> None:
    rng = random.Random(2009)
    for n in range(4, 10):
        cost = euclid([(rng.random(), rng.random()) for _ in range(n)])
        start = list(range(n))
        rng.shuffle(start)
        tour, _ = lkh(cost, start)
        assert sorted(tour) == list(range(n))
        assert brute_opt(cost) - 1e-9 <= tour_cost(cost, tour) <= tour_cost(cost, start) + 1e-9
        candidates = alpha_lists(cost, min(5, n - 1))
        for i in range(n):
            ring = tour[i:] + tour[:i]
            for path in (ring[:1] + ring[1:][::-1], ring):
                assert lk_search(cost, path, candidates) is None


def test_small_inputs() -> None:
    assert lkh([[0]], [0]) == ([0], 0)
    cost = euclid([(0, 0), (1, 0), (1, 1)])
    assert lkh(cost, [0, 2, 1]) == ([0, 2, 1], 0)
