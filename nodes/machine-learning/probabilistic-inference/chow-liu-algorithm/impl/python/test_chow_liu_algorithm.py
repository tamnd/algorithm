# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chow-liu-algorithm/. The authors are listed in prov/Q3KGA9.jsonl.

import itertools
import math
import random

from chow_liu_algorithm import chow_liu, likelihood, mutual_information


def prufer_trees(n):
    """All labelled trees on n >= 2 nodes as parent arrays rooted at 0."""
    for seq in itertools.product(range(n), repeat=n - 2):
        degree = [1] * n
        for a in seq:
            degree[a] += 1
        adj = [[] for _ in range(n)]
        for a in seq:
            leaf = min(v for v in range(n) if degree[v] == 1)
            adj[leaf].append(a)
            adj[a].append(leaf)
            degree[leaf] -= 1
            degree[a] -= 1
        u, w = [v for v in range(n) if degree[v] == 1]
        adj[u].append(w)
        adj[w].append(u)
        parent = [None] * n
        seen, stack = {0}, [0]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    parent[y] = x
                    stack.append(y)
        yield parent


def edges(parent):
    return {frozenset((v, p)) for v, p in enumerate(parent) if p is not None}


def random_data(n, s, rng, k=2):
    # a random tree-shaped source with noisy copies, so that the data has structure
    order = list(range(n))
    rng.shuffle(order)
    par = {order[i]: order[rng.randrange(i)] for i in range(1, n)}
    flip = {v: rng.uniform(0.05, 0.45) for v in par}
    data = []
    for _ in range(s):
        x = [0] * n
        x[order[0]] = rng.randrange(k)
        for v in order[1:]:
            x[v] = x[par[v]] if rng.random() > flip[v] else rng.randrange(k)
        data.append(tuple(x))
    return data


def test_cayley_count():
    for n in range(2, 6):
        trees = list(prufer_trees(n))
        assert len(trees) == n ** (n - 2)
        assert len({frozenset(edges(p)) for p in trees}) == n ** (n - 2)


def test_maximum_likelihood_against_all_spanning_trees():
    rng = random.Random(1968)
    for _ in range(60):
        n = rng.randint(2, 5)
        data = random_data(n, rng.randint(8, 30), rng, k=rng.choice((2, 3)))
        parent, _ = chow_liu(data, n)
        best = max(likelihood(data, p) for p in prufer_trees(n))
        assert likelihood(data, parent) == best


def test_root_does_not_change_the_likelihood():
    rng = random.Random(5)
    data = random_data(5, 25, rng)
    values = {likelihood(data, chow_liu(data, 5, root=r)[0]) for r in range(5)}
    assert len(values) == 1


def test_log_likelihood_decomposition():
    # log L(T) = s * sum of edge MI - s * sum of entropies
    rng = random.Random(9)
    data = random_data(4, 40, rng, k=3)
    s = len(data)
    ent = 0.0
    for v in range(4):
        cnt = {}
        for x in data:
            cnt[x[v]] = cnt.get(x[v], 0) + 1
        ent += -sum(c / s * math.log(c / s) for c in cnt.values())
    for p in prufer_trees(4):
        mi = sum(mutual_information(data, *sorted(e)) for e in edges(p))
        assert abs(math.log(likelihood(data, p)) - (s * mi - s * ent)) < 1e-9


def test_tables_are_empirical_conditionals():
    data = [(0, 0, 1), (0, 0, 0), (1, 1, 1), (1, 1, 1), (1, 0, 1), (0, 0, 0)]
    parent, cpt = chow_liu(data, 3)
    for v, p in enumerate(parent):
        for b in {None if p is None else x[p] for x in data}:
            assert sum(q for (a, bb), q in cpt[v].items() if bb == b) == 1


def test_recovers_the_source_tree_from_many_samples():
    rng = random.Random(2024)
    n = 6
    par = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2}
    data = []
    for _ in range(4000):
        x = [rng.randrange(2)] + [0] * 5
        for v in range(1, n):
            x[v] = x[par[v]] if rng.random() < 0.8 else 1 - x[par[v]]
        data.append(tuple(x))
    parent, _ = chow_liu(data, n)
    assert edges(parent) == {frozenset(e) for e in par.items()}
