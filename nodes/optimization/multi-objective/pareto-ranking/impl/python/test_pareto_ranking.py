# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pareto-ranking/. The authors are listed in prov/MN6FJG.jsonl.

import random

from pareto_ranking import (
    dominates,
    fonseca_fleming_rank,
    goldberg_rank,
    pareto_rank_order,
    spea2_raw_fitness,
)

EXAMPLE = [(1, 8), (2, 5), (3, 6), (4, 2), (5, 4), (6, 7), (7, 1), (8, 3)]


def peel_rank(points):
    """Reference: peel the fronts one by one, O(N^2) per front."""
    rank = [0] * len(points)
    rest = list(range(len(points)))
    k = 1
    while rest:
        front = [i for i in rest if not any(dominates(points[j], points[i]) for j in rest)]
        for i in front:
            rank[i] = k
        rest = [i for i in rest if i not in front]
        k += 1
    return rank


def test_example() -> None:
    assert goldberg_rank(EXAMPLE) == [1, 1, 2, 1, 2, 3, 1, 2]
    assert fonseca_fleming_rank(EXAMPLE) == [1, 1, 2, 1, 2, 5, 1, 3]
    assert spea2_raw_fitness(EXAMPLE) == [0, 0, 2, 0, 3, 7, 0, 4]


def test_edges() -> None:
    assert goldberg_rank([]) == []
    assert fonseca_fleming_rank([(1, 1), (1, 1)]) == [1, 1]
    chain = [(k, k) for k in range(4)]
    assert goldberg_rank(chain) == [1, 2, 3, 4]
    assert fonseca_fleming_rank(chain) == [1, 2, 3, 4]
    # strengths 3, 2, 1: raw fitness 0, 3, 3 + 2, 3 + 2 + 1
    assert spea2_raw_fitness(chain) == [0, 3, 5, 6]


def test_exercises() -> None:
    m = 5
    pts = [(0, 10), (1, 11)] + [(2, 11 + i) for i in range(1, m + 1)] + [(5, 5), (6, 6), (7, 7)]
    g, raw = goldberg_rank(pts), spea2_raw_fitness(pts)
    assert (g[1], raw[1]) == (2, m + 1)
    assert (g[-1], raw[-1]) == (3, 3)
    n = 6
    q = [(t, n - 1 - t) for t in range(n - 1)] + [(n, n)]
    assert goldberg_rank(q)[-1] == 2 and fonseca_fleming_rank(q)[-1] == n


def test_template_order() -> None:
    order = pareto_rank_order(EXAMPLE, lambda y: y, rule="fonseca-fleming")
    assert order == [0, 1, 3, 6, 2, 4, 7, 5]
    # a density that prefers the larger first objective breaks the ties of front 1
    order = pareto_rank_order(EXAMPLE, lambda y: y, density=lambda ys, i: ys[i][0])
    assert order[:4] == [6, 3, 1, 0]


def test_against_peeling_and_relations() -> None:
    rng = random.Random(3)
    for _ in range(300):
        p = rng.randint(1, 4)
        pts = [tuple(rng.randint(0, 4) for _ in range(p)) for _ in range(rng.randint(0, 20))]
        g = goldberg_rank(pts)
        ff = fonseca_fleming_rank(pts)
        raw = spea2_raw_fitness(pts)
        assert g == peel_rank(pts)
        for i in range(len(pts)):
            nondominated = not any(dominates(pts[j], pts[i]) for j in range(len(pts)))
            assert (g[i] == 1) == nondominated == (ff[i] == 1) == (raw[i] == 0)
            assert g[i] <= ff[i]
            for j in range(len(pts)):
                if dominates(pts[i], pts[j]):
                    assert g[i] < g[j] and ff[i] < ff[j] and raw[i] < raw[j]
