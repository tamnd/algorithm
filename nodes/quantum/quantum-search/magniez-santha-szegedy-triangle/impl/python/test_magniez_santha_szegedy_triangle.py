# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/magniez-santha-szegedy-triangle/. The authors are listed in prov/A5A7MR.jsonl.
import math
import random
from fractions import Fraction
from itertools import combinations

from magniez_santha_szegedy_triangle import (
    MSS_TERMS,
    PLAIN_TERMS,
    Data,
    best_exponent,
    check,
    check_cost,
    graph_collision,
    graph_collision_cost,
    johnson_search,
    mss_r,
    mss_triangle,
    random_graph,
    setup_cost,
    step_cost,
    total_cost,
    triangles,
)


def all_graphs(n):
    pairs = list(combinations(range(n), 2))
    for bits in range(1 << len(pairs)):
        adj = [[0] * n for _ in range(n)]
        for i, (u, v) in enumerate(pairs):
            if bits >> i & 1:
                adj[u][v] = adj[v][u] = 1
        yield adj


def marked_mass(adj, dist):
    n = len(adj)
    return sum(p for m, p in dist.items() if check(adj, {i for i in range(n) if m >> i & 1}))


def test_exponents():
    assert best_exponent(MSS_TERMS) == (Fraction(3, 5), Fraction(13, 10))
    assert best_exponent(PLAIN_TERMS)[1] == Fraction(3, 2)  # no gain over Grover without graph collision
    # graph collision on r vertices, walk on q = r^b subsets: q + (r/q) sqrt(q)
    assert best_exponent([(Fraction(0), Fraction(1)), (Fraction(1), Fraction(-1, 2))]) == (Fraction(2, 3), Fraction(2, 3))


def test_cost_scaling():
    for n in (10**4, 10**6, 10**8):
        rs = [int(n**0.6 * k / 100) for k in range(20, 500)]
        r = min(rs, key=lambda r: total_cost(n, r))
        assert 0.3 < r / n**0.6 < 0.6
        assert 1.95 < total_cost(n, r) / n**1.3 < 2.1
        assert total_cost(n, r, c=math.sqrt(n) * r) > n**1.5  # the plain check
    for r in (10**3, 10**5):
        best = min(graph_collision_cost(r, q) for q in range(1, r))
        assert abs(best / r ** (2 / 3) - 3 / 2 ** (2 / 3)) < 1e-2
    for n in (6, 10, 1000, 10**6):
        assert 0 <= mss_r(n) - n**0.6 < 1 or mss_r(n) == 2


def test_check_against_brute_force():
    for adj in all_graphs(5):
        tri = set(triangles(adj))
        for r in (2, 3):
            for a in combinations(range(5), r):
                a = set(a)
                got = check(adj, a)
                want = any(len(a & set(t)) >= 2 for t in tri)
                assert (got is not None) == want
                if got:
                    assert tuple(sorted(got)) in tri and got[0] in a and got[1] in a
                for v in range(5):
                    pair = graph_collision(adj, a, lambda u: adj[u][v])
                    brute = [(u, w) for u, w in combinations(sorted(a), 2) if adj[u][w] and adj[u][v] and adj[w][v]]
                    assert (pair is not None) == bool(brute)


def test_data_structure_counts():
    rng = random.Random(7)
    for n, r in ((8, 3), (10, 4)):
        adj = random_graph(n, 0.5, rng)
        a = set(rng.sample(range(n), r))
        d = Data(adj, a)
        assert d.queries == setup_cost(r)
        for _ in range(20):
            x = rng.choice([v for v in range(n) if v not in d.a])
            d.add(x)
            d.remove(rng.choice(sorted(d.a)))
        assert d.queries == setup_cost(r) + 20 * step_cost(r)
        assert d.edges == {(u, w): adj[u][w] for u, w in combinations(sorted(d.a), 2)}


def test_johnson_walk_spectrum():
    # the set register moves like the classical walk that swaps one element; f(A) = [0 in A] - r/n
    # is an eigenvector with the second eigenvalue 1 - n/(r(n - r)), so the gap is about 1/r
    for n, r in ((7, 3), (8, 3), (9, 4)):
        sets = [frozenset(c) for c in combinations(range(n), r)]
        f = {a: (0 in a) - r / n for a in sets}
        lam = 1 - n / (r * (n - r))
        for a in sets:
            pf = sum(f[(a - {u}) | {w}] for u in a for w in range(n) if w not in a) / (r * (n - r))
            assert abs(pf - lam * f[a]) < 1e-12


def test_one_triangle_is_amplified():
    for n, t1, low in ((8, 4, 0.82), (9, 5, 0.95), (10, 5, 0.9)):
        adj = [[0] * n for _ in range(n)]
        for u, v in ((0, 1), (1, 2), (0, 2)):
            adj[u][v] = adj[v][u] = 1
        start = marked_mass(adj, johnson_search(n, 3, lambda a: check(adj, a) is not None, 0, 2))
        assert abs(start - Fraction(3 * (n - 3) + 1, math.comb(n, 3))) < 1e-12
        dist = johnson_search(n, 3, lambda a: check(adj, a) is not None, t1, 2)
        assert abs(sum(dist.values()) - 1) < 1e-9  # the walk is unitary
        assert marked_mass(adj, dist) > low > 2.5 * start


def test_against_brute_force():
    rng = random.Random(2026)
    found = trials = 0
    for _ in range(40):
        n = rng.choice((6, 7, 8))
        adj = random_graph(n, rng.choice((0.15, 0.25, 0.35)), rng)
        truth = triangles(adj)  # brute force over all triples
        tri = None
        for _ in range(5):  # at most five runs, each with a random number of rounds
            t1 = rng.randrange(1, 5)
            tri, queries = mss_triangle(adj, t1, 2, 3, rng)
            assert queries == setup_cost(3) + t1 * 2 * step_cost(3) + (t1 + 1) * check_cost(n, 3)
            if tri:
                break
        if not truth:
            assert tri is None  # one-sided: never a false triangle
        else:
            trials += 1
            assert tri is None or tuple(sorted(tri)) in truth
            found += tri is not None
    assert trials >= 15 and found >= 0.8 * trials
