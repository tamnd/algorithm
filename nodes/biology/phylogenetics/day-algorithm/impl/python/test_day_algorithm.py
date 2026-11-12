# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/day-algorithm/. The authors are listed in prov/WDM8Q2.jsonl.

import random

import pytest

from day_algorithm import cluster_table, clusters_direct, rf_direct, rf_rooted, rf_unrooted, root_at_leaf


def edges(tree):
    return [(u, v) for u in tree for v in tree[u] if repr(u) < repr(v)]


def random_unrooted(rng, taxa, contract=0.0):
    """A random unrooted binary tree by stepwise addition; then contract internal edges at random."""
    a, b, c = taxa[:3]
    t = {0: [a, b, c], a: [0], b: [0], c: [0]}
    for k, x in enumerate(taxa[3:], start=1):
        u, v = rng.choice(edges(t))
        t[u][t[u].index(v)] = k
        t[v][t[v].index(u)] = k
        t[k] = [u, v, x]
        t[x] = [k]
    for u, v in edges(t):
        if isinstance(u, int) and isinstance(v, int) and u in t and v in t and v in t[u] and rng.random() < contract:
            for w in t[v]:
                if w != u:
                    t[w][t[w].index(v)] = u
                    t[u].append(w)
            t[u].remove(v)
            del t[v]
    for v in t:
        rng.shuffle(t[v])  # the order of neighbours must not matter
    return t


def random_rooted(rng, taxa, max_degree=2):
    """A random rooted tree: join 2 to max_degree random subtrees until one is left."""
    pool = list(taxa)
    children = {}
    k = 0
    while len(pool) > 1:
        d = min(len(pool), rng.randint(2, max_degree))
        rng.shuffle(pool)
        kids, pool = pool[:d], pool[d:]
        children[("v", k)] = kids
        pool.append(("v", k))
        k += 1
    return pool[0], children


def move_one_leaf(rng, t):
    """A small change: prune one leaf and regraft it on a random edge."""
    t = {v: list(nb) for v, nb in t.items()}
    leaf = rng.choice([v for v, nb in t.items() if len(nb) == 1])
    (p,) = t[leaf]
    if len(t[p]) == 3:  # suppress p
        x, y = [w for w in t[p] if w != leaf]
        t[x][t[x].index(p)] = y
        t[y][t[y].index(p)] = x
        del t[p]
        del t[leaf]
        u, v = rng.choice(edges(t))
        t[u][t[u].index(v)] = p
        t[v][t[v].index(u)] = p
        t[p] = [u, v, leaf]
        t[leaf] = [p]
    return t


def names(n):
    return [f"t{i}" for i in range(n)]


def test_example_of_the_page():
    t1 = ("r", {"r": ["x", "y"], "x": ["a", "b"], "y": ["c", "z"], "z": ["d", "e"]})
    t2 = ("r", {"r": ["x", "y"], "x": ["a", "c"], "y": ["b", "z"], "z": ["d", "e"]})
    num, X, c1 = cluster_table(t1)
    assert num == {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
    assert X == [(0, 4), (0, 1), (2, 4), (3, 4), None]
    assert c1 == 4
    assert rf_rooted(t1, t2) == 4 == len(clusters_direct(t1) ^ clusters_direct(t2))


def test_unrooted_against_direct_split_comparison():
    rng = random.Random(1985)
    for _ in range(200):
        n = rng.randint(3, 30)
        taxa = names(n)
        c1, c2 = rng.choice([0.0, 0.0, 0.3, 0.7]), rng.choice([0.0, 0.3])
        t1 = random_unrooted(rng, taxa, c1)
        t2 = random_unrooted(rng, rng.sample(taxa, n), c2) if rng.random() < 0.5 else move_one_leaf(rng, t1)
        d = rf_unrooted(t1, t2)
        assert d == rf_direct(t1, t2)
        assert d == rf_unrooted(t2, t1)
        if c1 == 0 and c2 == 0:
            assert d % 2 == 0 and d <= 2 * (n - 3)


def test_rooted_against_direct_cluster_comparison():
    rng = random.Random(81)
    for _ in range(200):
        n = rng.randint(2, 30)
        t1 = random_rooted(rng, names(n), rng.choice([2, 3, 5]))
        t2 = random_rooted(rng, names(n), rng.choice([2, 3, 5]))
        assert rf_rooted(t1, t2) == len(clusters_direct(t1) ^ clusters_direct(t2))
        assert rf_rooted(t1, t1) == 0


def test_identical_and_reordered_trees_have_distance_zero():
    rng = random.Random(5)
    for _ in range(50):
        t = random_unrooted(rng, names(rng.randint(3, 30)), 0.3)
        t2 = {v: rng.sample(nb, len(nb)) for v, nb in t.items()}
        assert rf_unrooted(t, t2) == 0


def test_maximum_distance_of_two_caterpillars():
    # The caterpillars (1,2,...,n) and (1,3,5,...,2,4,6,...) share no nontrivial split for n = 8.
    def caterpillar(order):
        t = {}
        prev = order[0]
        for i, x in enumerate(order[1:-1]):
            t.setdefault(prev, []).append(i)
            t[i] = [prev, x]
            t[x] = [i]
            prev = i
        t[prev].append(order[-1])
        t[order[-1]] = [prev]
        return t

    a = caterpillar([f"t{i}" for i in [0, 1, 2, 3, 4, 5, 6, 7]])
    b = caterpillar([f"t{i}" for i in [0, 2, 4, 6, 1, 3, 5, 7]])
    assert rf_unrooted(a, b) == rf_direct(a, b) == 2 * (8 - 3)


def test_deep_caterpillar_is_linear_and_iterative():
    n = 30000
    order = [f"t{i}" for i in range(n)]
    ch = {}
    for i in range(n - 2, -1, -1):
        ch[("v", i)] = [order[i], ("v", i + 1) if i < n - 2 else order[n - 1]]
    t = (("v", 0), ch)
    assert rf_rooted(t, t) == 0


def test_different_leaf_sets_raise():
    t1 = ("r", {"r": ["a", "b", "c"]})
    t2 = ("r", {"r": ["a", "b", "d"]})
    with pytest.raises(ValueError):
        rf_rooted(t1, t2)


def test_root_at_leaf():
    t = {0: ["a", "b", 1], 1: [0, "c", "d"], "a": [0], "b": [0], "c": [1], "d": [1]}
    root, ch = root_at_leaf(t, "a")
    assert root == 0 and sorted(map(str, ch[0])) == ["1", "b"]
