# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/four-point-method/. The authors are listed in prov/63RW19.jsonl.

import random
from fractions import Fraction

import pytest

from four_point_method import four_point_method


def random_tree(n, rng, max_len=10):
    """Random unrooted binary tree on leaves 0..n-1 with positive integer edge lengths."""
    if n == 2:
        return [(0, 1, rng.randint(1, max_len))]
    c = n
    edges = [(0, c, rng.randint(1, max_len)), (1, c, rng.randint(1, max_len)), (2, c, rng.randint(1, max_len))]
    nxt = n + 1
    for x in range(3, n):
        k = rng.randrange(len(edges))
        u, v, _ = edges[k]
        p = nxt
        nxt += 1
        edges[k] = (u, p, rng.randint(1, max_len))
        edges.append((p, v, rng.randint(1, max_len)))
        edges.append((x, p, rng.randint(1, max_len)))
    return edges


def leaf_metric(n, edges):
    """Oracle: path lengths between leaves by a search from each leaf."""
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, Fraction(w)))
        adj.setdefault(v, []).append((u, Fraction(w)))
    out = []
    for s in range(n):
        dist, stack = {s: Fraction(0)}, [s]
        while stack:
            x = stack.pop()
            for y, w in adj[x]:
                if y not in dist:
                    dist[y] = dist[x] + w
                    stack.append(y)
        out.append([dist[t] for t in range(n)])
    return out


def splits(n, edges):
    adj = {}
    for u, v, _ in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    out = set()
    for u, v, _ in edges:
        seen, stack, side = {u, v}, [v], set()
        while stack:
            x = stack.pop()
            if x < n:
                side.add(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        if 0 in side:
            side = set(range(n)) - side
        if 2 <= len(side) <= n - 2:
            out.add(frozenset(side))
    return out


EXAMPLE = [
    [0, 9, 8, 11, 8],
    [9, 0, 13, 16, 13],
    [8, 13, 0, 9, 10],
    [11, 16, 9, 0, 13],
    [8, 13, 10, 13, 0],
]


def test_example_from_page():
    edges = four_point_method(EXAMPLE)
    assert leaf_metric(5, edges) == EXAMPLE
    assert splits(5, edges) == {frozenset({2, 3}), frozenset({2, 3, 4})}
    assert sorted(w for _, _, w in edges) == [1, 2, 2, 3, 5, 6, 7]


def test_small_cases():
    assert four_point_method([[0, 4], [4, 0]]) == [(0, 1, 4)]
    edges = four_point_method([[0, 3, 4], [3, 0, 5], [4, 5, 0]])
    assert sorted(w for _, _, w in edges) == [1, 2, 3]
    with pytest.raises(ValueError):
        four_point_method([[0]])


def test_random_tree_metrics():
    rng = random.Random(83)
    for _ in range(500):
        n = rng.randint(2, 14)
        true = random_tree(n, rng)
        D = leaf_metric(n, true)
        edges = four_point_method(D)
        assert len(edges) == (1 if n == 2 else 2 * n - 3)
        assert all(w > 0 for _, _, w in edges)
        assert leaf_metric(n, edges) == D
        assert splits(n, edges) == splits(n, true)


def test_fractional_lengths_and_caterpillars():
    rng = random.Random(89)
    for _ in range(100):
        n = rng.randint(4, 12)
        # a caterpillar: the walk must travel the whole spine
        spine = list(range(n, 2 * n - 2))
        edges = [(0, spine[0], Fraction(rng.randint(1, 9), 7)), (1, spine[0], Fraction(rng.randint(1, 9), 7))]
        for k in range(len(spine) - 1):
            edges.append((spine[k], spine[k + 1], Fraction(rng.randint(1, 9), 7)))
            edges.append((k + 2, spine[k + 1], Fraction(rng.randint(1, 9), 7)))
        edges.append((n - 1, spine[-1], Fraction(rng.randint(1, 9), 7)))
        perm = list(range(n))
        rng.shuffle(perm)
        edges = [(perm[u] if u < n else u, perm[v] if v < n else v, w) for u, v, w in edges]
        D = leaf_metric(n, edges)
        out = four_point_method(D)
        assert leaf_metric(n, out) == D
        assert splits(n, out) == splits(n, edges)


def test_other_input_still_gives_a_tree():
    rng = random.Random(97)
    for _ in range(200):
        n = rng.randint(3, 9)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randint(1, 20)
        edges = four_point_method(D)
        assert len(edges) == 2 * n - 3
        deg = {}
        for u, v, _ in edges:
            deg[u] = deg.get(u, 0) + 1
            deg[v] = deg.get(v, 0) + 1
        assert all(k == (1 if x < n else 3) for x, k in deg.items())
