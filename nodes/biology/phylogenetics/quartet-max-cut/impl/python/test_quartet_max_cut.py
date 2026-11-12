# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quartet-max-cut/. The authors are listed in prov/GXXKFF.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from quartet_max_cut import displayed, max_ratio_cut, quartet_max_cut, splits


def all_binary_split_sets(n):
    """Every unrooted binary tree on 0..n-1 (n >= 4), as its set of nontrivial splits."""
    trees = [[(0, n), (1, n), (2, n)]]
    nxt = n + 1
    for x in range(3, n):
        new = []
        for edges in trees:
            for k in range(len(edges)):
                u, v = edges[k]
                p = nxt
                new.append(edges[:k] + edges[k + 1:] + [(u, p), (p, v), (x, p)])
            nxt += 1
        trees = new
    return [splits(e, range(n)) for e in trees]


TREES = {n: all_binary_split_sets(n) for n in range(4, 7)}


def random_quartets(n, m, rng):
    out = []
    for _ in range(m):
        a, b, c, d = rng.sample(range(n), 4)
        out.append(((a, b), (c, d)))
    return out


def check_tree(edges, taxa):
    nodes = {u for e in edges for u in e}
    deg = {}
    for u, v in edges:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    leaves = {x for x, k in deg.items() if k == 1}
    assert leaves == set(taxa)
    assert all(k >= 3 for x, k in deg.items() if x not in leaves)
    assert len(edges) == len(nodes) - 1
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    seen = {next(iter(nodes))}
    stack = list(seen)
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    assert seen == nodes


def tree_quartets(edges, n):
    sp = splits(edges, range(n))
    out = []
    for s in combinations(range(n), 4):
        a, b, c, d = s
        for q in (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))):
            if displayed(sp, range(n), q):
                out.append(q)
    return out


def random_binary_tree(n, rng):
    edges = [(0, n), (1, n), (2, n)]
    nxt = n + 1
    for x in range(3, n):
        k = rng.randrange(len(edges))
        u, v = edges.pop(k)
        edges += [(u, nxt), (nxt, v), (x, nxt)]
        nxt += 1
    return edges


A, B, C, D, E, F = range(6)
PAGE_Q = [((A, B), (C, D)), ((A, B), (C, E)), ((A, B), (D, E)), ((C, D), (E, F)), ((A, C), (D, F)), ((B, F), (C, D))]


def test_example_from_page():
    edges, sat = quartet_max_cut(range(6), PAGE_Q)
    check_tree(edges, range(6))
    sp = splits(edges, range(6))
    assert sp == {frozenset([C, D]), frozenset([C, D, E, F])}
    assert sat == 5
    assert max_ratio_cut(list(range(6)), PAGE_Q) == {A: 1, B: 1, C: 0, D: 0, E: 0, F: 0}
    best = max(sum(displayed(t, range(6), q) for q in PAGE_Q) for t in TREES[6])
    assert best == 5


def test_small_sets_are_stars():
    edges, sat = quartet_max_cut([4, 7, 9], [])
    check_tree(edges, [4, 7, 9])
    assert sat == 0
    edges, _ = quartet_max_cut([0, 1, 2, 3, 4], [])
    check_tree(edges, range(5))
    assert splits(edges, range(5)) == set()


def test_rejects_bad_quartet():
    with pytest.raises(ValueError):
        quartet_max_cut(range(4), [((0, 1), (1, 2))])
    with pytest.raises(ValueError):
        quartet_max_cut(range(4), [((0, 1), (2, 5))])


@pytest.mark.parametrize("seed", range(4))
def test_dinkelbach_finds_the_best_ratio(seed):
    rng = random.Random(seed)
    for _ in range(40):
        n = rng.randint(4, 8)
        q = random_quartets(n, rng.randint(1, 10), rng)
        side = max_ratio_cut(list(range(n)), q)
        def ratio(sd):
            g = b = 0
            for (a, b_), (c, d) in q:
                b += (sd[a] != sd[b_]) + (sd[c] != sd[d])
                g += (sd[a] != sd[c]) + (sd[a] != sd[d]) + (sd[b_] != sd[c]) + (sd[b_] != sd[d])
            return g, b
        g, b = ratio(side)
        for mask in range(1 << n):
            k = bin(mask).count("1")
            if k < 2 or n - k < 2:
                continue
            sd = {x: (mask >> x) & 1 for x in range(n)}
            g2, b2 = ratio(sd)
            if b == 0:
                continue
            if b2 == 0:
                assert g2 == 0
            else:
                assert Fraction(g2, b2) <= Fraction(g, b)


@pytest.mark.parametrize("seed", range(5))
def test_random_against_brute_force_optimum(seed):
    rng = random.Random(10 + seed)
    for _ in range(100):
        n = rng.randint(4, 6)
        q = random_quartets(n, rng.randint(0, 12), rng)
        edges, sat = quartet_max_cut(range(n), q, rng=random.Random(seed))
        check_tree(edges, range(n))
        sp = splits(edges, range(n))
        assert sat == sum(displayed(sp, range(n), x) for x in q)
        best = max(sum(displayed(t, range(n), x) for x in q) for t in TREES[n])
        assert sat <= best


@pytest.mark.parametrize("seed", range(3))
def test_local_search_path_gives_a_valid_tree(seed):
    rng = random.Random(30 + seed)
    for _ in range(20):
        n = rng.randint(6, 12)
        q = random_quartets(n, rng.randint(5, 30), rng)
        edges, sat = quartet_max_cut(range(n), q, exact_limit=4, rng=random.Random(seed))
        check_tree(edges, range(n))
        sp = splits(edges, range(n))
        assert sat == sum(displayed(sp, range(n), x) for x in q)


@pytest.mark.parametrize("seed", range(3))
def test_consistent_complete_input_is_recovered(seed):
    rng = random.Random(60 + seed)
    for _ in range(10):
        n = rng.randint(4, 8)
        tree = random_binary_tree(n, rng)
        q = tree_quartets(tree, n)
        edges, sat = quartet_max_cut(range(n), q)
        assert sat == len(q)
        assert splits(edges, range(n)) == splits(tree, range(n))
