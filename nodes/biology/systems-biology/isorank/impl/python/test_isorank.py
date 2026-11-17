# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isorank/. The authors are listed in prov/35D89N.jsonl.

import itertools
import random
from fractions import Fraction

from isorank import (
    exact_scores,
    greedy_matching,
    isorank,
    isorank_scores,
    isorank_step,
    normalize,
    personalized_pagerank,
    product_graph,
)


def random_graph(rng, n, p, allow_isolated=False):
    """Edges in the order of the pairs (u, v), u < v, each kept when rng.random() < p.

    Unless allow_isolated, a node left with no edge is joined to rng.randrange over the other nodes.
    """
    adj = [[] for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].append(v)
                adj[v].append(u)
    if not allow_isolated:
        for u in range(n):
            if not adj[u]:
                v = rng.choice([w for w in range(n) if w != u])
                adj[u].append(v)
                adj[v].append(u)
    return adj


def l1(a, b):
    return sum(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def brute_force_max_matching_weight(r):
    n, m = len(r), len(r[0])
    best = 0.0
    if n <= m:
        for k in range(n + 1):
            for rows in itertools.combinations(range(n), k):
                for cols in itertools.permutations(range(m), k):
                    best = max(best, sum(r[i][j] for i, j in zip(rows, cols)))
    return best


PATH = [[1], [0, 2], [1]]  # a - b - c
STAR = [[1, 2, 3], [0], [0], [0]]  # x in the center, leaves y, z, w


def test_worked_example_path_and_star():
    e = [[1] * 4 for _ in range(3)]
    ex = exact_scores(PATH, STAR, e, Fraction(3, 5))
    assert ex[1][0] == Fraction(23, 96)
    assert all(ex[1][j] == Fraction(7, 96) for j in (1, 2, 3))
    assert ex[0][0] == ex[2][0] == Fraction(19, 192)
    assert all(ex[i][j] == Fraction(11, 192) for i in (0, 2) for j in (1, 2, 3))
    assert sum(sum(row) for row in ex) == 1
    match, r = isorank(PATH, STAR, e, 0.6)
    assert match == [(1, 0), (0, 1), (2, 2)]
    assert l1(r, [[float(v) for v in row] for row in ex]) < 1e-10


def test_second_example_with_sequence_scores():
    # a triangle 0, 1, 2 with a tail 2 - 3, against a triangle 0, 1, 2
    g1 = [[1, 2], [0, 2], [0, 1, 3], [2]]
    g2 = [[1, 2], [0, 2], [0, 1]]
    e = [[3, 1, 0], [1, 3, 0], [0, 0, 2], [0, 0, 1]]
    ex = exact_scores(g1, g2, e, Fraction(1, 2))
    r, steps = isorank_scores(g1, g2, e, 0.5)
    assert l1(r, [[float(v) for v in row] for row in ex]) < 1e-10
    assert steps < 60
    match, _ = isorank(g1, g2, e, 0.5)
    assert sorted(match) == [(0, 0), (1, 1), (2, 2)]


def test_iteration_matches_exact_solve_on_random_graphs():
    rng = random.Random(1)
    for _ in range(25):
        n, m = rng.randint(2, 5), rng.randint(2, 5)
        g1 = random_graph(rng, n, 0.5, allow_isolated=True)
        g2 = random_graph(rng, m, 0.5, allow_isolated=True)
        e = [[rng.randint(0, 3) for _ in range(m)] for _ in range(n)]
        if sum(map(sum, e)) == 0:
            e[0][0] = 1
        ex = exact_scores(g1, g2, e, Fraction(3, 5))
        r, _ = isorank_scores(g1, g2, e, 0.6)
        assert l1(r, [[float(v) for v in row] for row in ex]) < 1e-9


def test_scores_are_personalized_pagerank_of_the_product_graph():
    rng = random.Random(2)
    for _ in range(20):
        n, m = rng.randint(2, 6), rng.randint(2, 6)
        g1, g2 = random_graph(rng, n, 0.4), random_graph(rng, m, 0.4)
        e = normalize([[rng.random() for _ in range(m)] for _ in range(n)])
        r, _ = isorank_scores(g1, g2, e, 0.7)
        ppr = personalized_pagerank(product_graph(g1, g2), [v for row in e for v in row], 0.7, 200)
        assert max(abs(r[i][j] - ppr[i * m + j]) for i in range(n) for j in range(m)) < 1e-12
        # no isolated node, so the walk keeps all mass
        assert abs(sum(map(sum, r)) - 1.0) < 1e-12


def test_alpha_zero_gives_the_sequence_scores():
    rng = random.Random(3)
    g1, g2 = random_graph(rng, 4, 0.5), random_graph(rng, 5, 0.5)
    e = [[rng.random() for _ in range(5)] for _ in range(4)]
    r, steps = isorank_scores(g1, g2, e, 0.0)
    assert steps == 1
    assert l1(r, normalize(e)) < 1e-15


def test_each_step_contracts_by_alpha():
    rng = random.Random(4)
    for _ in range(20):
        n, m = rng.randint(2, 6), rng.randint(2, 6)
        g1 = random_graph(rng, n, 0.5, allow_isolated=True)
        g2 = random_graph(rng, m, 0.5, allow_isolated=True)
        e = normalize([[rng.random() for _ in range(m)] for _ in range(n)])
        a = [[rng.random() for _ in range(m)] for _ in range(n)]
        b = [[rng.random() for _ in range(m)] for _ in range(n)]
        alpha = rng.choice([0.3, 0.6, 0.9])
        da = l1(isorank_step(g1, g2, a, e, alpha), isorank_step(g1, g2, b, e, alpha))
        assert da <= alpha * l1(a, b) + 1e-12


def test_greedy_matching_is_at_least_half_the_maximum():
    rng = random.Random(5)
    for _ in range(150):
        n = rng.randint(1, 4)
        m = rng.randint(n, 5)
        r = [[rng.choice([rng.random(), 0.5, 1.0]) for _ in range(m)] for _ in range(n)]
        match = greedy_matching(r)
        assert len({i for i, _ in match}) == len(match) == len({j for _, j in match})
        got = sum(r[i][j] for i, j in match)
        best = brute_force_max_matching_weight(r)
        assert got <= best + 1e-12
        assert 2 * got >= best - 1e-12


def test_greedy_can_be_half_of_the_maximum():
    r = [[1.0, 1.0], [1.0, 0.0]]
    r[0][0] = 1.0 + 1e-9
    match = greedy_matching(r)
    # the greedy pair (0, 0) blocks both pairs of weight 1, and (1, 1) adds 0
    assert match == [(0, 0), (1, 1)]
    assert sum(r[i][j] for i, j in match) == 1.0 + 1e-9
    assert brute_force_max_matching_weight(r) == 2.0
