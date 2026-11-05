# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reverse-delete/. The authors are listed in prov/WC91FF.jsonl.

import itertools
import random

from reverse_delete import reverse_delete

# a=0, b=1, c=2, d=3, e=4, f=5
EXAMPLE = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (2, 4, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]


def components(n, edges, chosen):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for i in chosen:
        u, v, _ = edges[i]
        parent[find(u)] = find(v)
    return len({find(x) for x in range(n)})


def is_forest(n, edges, chosen):
    return components(n, edges, chosen) == n - len(chosen)


def brute_force(n, edges):
    """Least weight of a spanning forest, by trying every edge set of the right size."""
    k = n - components(n, edges, range(len(edges)))
    best = None
    for s in itertools.combinations(range(len(edges)), k):
        if is_forest(n, edges, s):
            w = sum(edges[i][2] for i in s)
            best = w if best is None or w < best else best
    return best


def weight(edges, chosen):
    return sum(edges[i][2] for i in chosen)


def test_example():
    f = reverse_delete(6, EXAMPLE)
    assert f == [1, 2, 3, 5, 8]  # ac, bc, bd, ce, ef
    assert weight(EXAMPLE, f) == 13


def test_edge_cases():
    assert reverse_delete(0, []) == []
    assert reverse_delete(1, []) == []
    assert reverse_delete(1, [(0, 0, -7)]) == []  # a self-loop is always deleted
    assert reverse_delete(2, [(0, 1, 5), (0, 1, 2)]) == [1]  # parallel edges: keep the lighter
    assert reverse_delete(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)]) == [0, 1]  # all weights tie
    assert reverse_delete(3, [(0, 1, -2), (1, 2, -5), (0, 2, 0)]) == [0, 1]  # negative weights


def test_disconnected():
    edges = [(0, 1, 3), (2, 3, 1), (3, 4, 2), (2, 4, 9)]
    f = reverse_delete(6, edges)
    assert f == [0, 1, 2]
    assert components(6, edges, f) == 3


def test_bridge_is_kept():
    # The heaviest edge is a bridge; deleting it by weight alone would split the graph.
    edges = [(0, 1, 1), (1, 2, 1), (0, 2, 1), (2, 3, 100)]
    assert reverse_delete(4, edges) == [0, 1, 3]


def test_increasing_order_is_wrong_order():
    # Scanning from the lightest edge would delete the edge of weight 1 first.
    edges = [(0, 1, 1), (1, 2, 5), (0, 2, 5)]
    f = reverse_delete(3, edges)
    assert 0 in f and weight(edges, f) == 6


def test_large_integers():
    big = 2**62
    edges = [(0, 1, big), (1, 2, big + 1), (0, 2, big - 1)]
    assert reverse_delete(3, edges) == [0, 2]


def test_against_brute_force():
    rng = random.Random(1956)
    for _ in range(600):
        n = rng.randrange(1, 7)
        m = rng.randrange(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randrange(-2, 4)) for _ in range(m)]
        f = reverse_delete(n, edges)
        assert is_forest(n, edges, f)
        assert components(n, edges, f) == components(n, edges, range(m))
        assert weight(edges, f) == brute_force(n, edges)
