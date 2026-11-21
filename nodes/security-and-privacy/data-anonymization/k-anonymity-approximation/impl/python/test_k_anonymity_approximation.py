# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-anonymity-approximation/. The authors are listed in prov/3CXF3J.jsonl.
import random
from collections import Counter

from k_anonymity_approximation import anonymize, build_forest, hamming

ROWS = [
    (0, 0, 0, 0),
    (0, 0, 0, 1),
    (0, 0, 1, 1),
    (1, 1, 1, 1),
    (1, 1, 1, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 1),
]


def block_cost(rows, block):
    d = len(rows[0])
    return len(block) * sum(1 for j in range(d) if len({rows[i][j] for i in block}) > 1)


def partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        yield [[first]] + part


def optimum(rows, k):
    return min(
        sum(block_cost(rows, b) for b in part)
        for part in partitions(list(range(len(rows))))
        if all(len(b) >= k for b in part)
    )


def forest_weight(rows, edges):
    return sum(hamming(rows[u], rows[x]) for u, x in edges)


def check(rows, k):
    clusters, table, cost = anonymize(rows, k)
    n = len(rows)
    assert sorted(i for c in clusters for i in c) == list(range(n))
    assert all(k <= len(c) <= 3 * k - 3 for c in clusters)
    assert cost == sum(block_cost(rows, c) for c in clusters)
    assert cost == sum(1 for r in table for x in r if x is None)
    counts = Counter(table)
    assert all(counts[r] >= k for r in table)
    for i in range(n):
        assert all(table[i][j] is None or table[i][j] == rows[i][j] for j in range(len(rows[i])))
    return clusters, cost


def test_page_example() -> None:
    edges = build_forest(ROWS, 3)
    assert edges == [(0, 1), (1, 2), (3, 4), (4, 5), (6, 1)]
    assert forest_weight(ROWS, edges) == 5
    clusters, cost = check(ROWS, 3)
    assert clusters == [[0, 1, 2, 6], [3, 4, 5]]
    assert cost == 4 * 3 + 3 * 2
    assert optimum(ROWS, 3) == 18


def test_split_of_a_large_tree() -> None:
    rows = [(i,) for i in range(8)]
    clusters, cost = check(rows, 2)
    assert all(len(c) <= 3 for c in clusters)
    assert cost <= 3 * optimum(rows, 2)


def test_edge_cases() -> None:
    assert anonymize([(1, 2), (1, 2)], 2) == ([[0, 1]], [(1, 2), (1, 2)], 0)
    assert anonymize([(1, 2), (3, 4)], 2) == ([[0, 1]], [(None, None), (None, None)], 4)
    same = [(5, 5, 5)] * 9
    clusters, cost = check(same, 2)
    assert cost == 0


def test_random_against_brute_force() -> None:
    rng = random.Random(2005)
    for _ in range(500):
        k = rng.randint(2, 3)
        n = rng.randint(k, 7)
        d = rng.randint(1, 4)
        sigma = rng.randint(2, 3)
        rows = [tuple(rng.randrange(sigma) for _ in range(d)) for _ in range(n)]
        _, cost = check(rows, k)
        opt = optimum(rows, k)
        assert forest_weight(rows, build_forest(rows, k)) <= opt
        assert cost <= (3 * k - 3) * opt


def test_random_larger_tables() -> None:
    rng = random.Random(77)
    for _ in range(200):
        k = rng.randint(2, 5)
        n = rng.randint(k, 30)
        d = rng.randint(1, 4)
        rows = [tuple(rng.randrange(3) for _ in range(d)) for _ in range(n)]
        check(rows, k)
