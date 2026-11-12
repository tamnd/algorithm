# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strict-consensus/. The authors are listed in prov/RNKXSB.jsonl.

import random

import pytest

from strict_consensus import clusters, strict_consensus


def random_tree(n, rng):
    """Random rooted tree on leaves 0..n-1: merge two or three random parts at a time."""
    parts = list(range(n))
    rng.shuffle(parts)
    while len(parts) > 1:
        m = 2 if len(parts) == 2 or rng.random() < 0.7 else 3
        rng.shuffle(parts)
        group = tuple(parts[:m])
        parts = parts[m:] + [group]
    return parts[0]


def tree_from_clusters(n, cl):
    """Oracle side: the unique rooted tree whose clusters are cl plus the root."""
    cl = set(cl) | {frozenset(range(n))}
    order = sorted(cl, key=len)
    owner = {x: x for x in range(n)}
    built = {}
    for c in order:
        heads = []
        for x in sorted(c):
            h = owner[x]
            if h not in heads:
                heads.append(h)
        node = tuple(built.get(h, h) for h in heads)
        for x in c:
            owner[x] = c
        built[c] = node
    return built[frozenset(range(n))]


def contract_some(tree, n, rng):
    """Same tree with a random subset of its internal edges contracted."""
    cl = {c for c in clusters(tree) if len(c) < n and rng.random() < 0.7}
    return tree_from_clusters(n, cl)


def brute(trees, n):
    common = set(clusters(trees[0]))
    for t in trees[1:]:
        common &= clusters(t)
    return common


A, B, C, D, E, F = range(6)
T1 = (((A, B), C), (D, (E, F)))
T2 = (((A, B), D), (C, (E, F)))
T3 = ((A, (B, C)), (D, (E, F)))


def test_example_from_page():
    out = strict_consensus([T1, T2, T3])
    assert out == (A, B, C, D, (E, F))


def test_one_tree_is_itself():
    assert clusters(strict_consensus([T1])) == clusters(T1)


def test_star_when_nothing_is_shared():
    out = strict_consensus([((0, 1), (2, 3)), ((0, 2), (1, 3))])
    assert out == (0, 1, 2, 3)


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        strict_consensus([((0, 1), 2), ((0, 1), 3)])
    with pytest.raises(ValueError):
        strict_consensus([((0,), 1)])


@pytest.mark.parametrize("seed", range(6))
def test_random_against_cluster_intersection(seed):
    rng = random.Random(seed)
    for _ in range(120):
        n = rng.randint(2, 9)
        k = rng.randint(1, 5)
        if rng.random() < 0.5:
            base = random_tree(n, rng)
            trees = [contract_some(base, n, rng) for _ in range(k)]
            if rng.random() < 0.5:
                trees.append(random_tree(n, rng))
        else:
            trees = [random_tree(n, rng) for _ in range(k)]
        out = strict_consensus(trees)
        assert clusters(out) == brute(trees, n)
        assert sorted(x for x in _leaves(out)) == list(range(n))


def _leaves(t):
    stack = [t]
    while stack:
        x = stack.pop()
        if isinstance(x, tuple):
            stack.extend(x)
        else:
            yield x
