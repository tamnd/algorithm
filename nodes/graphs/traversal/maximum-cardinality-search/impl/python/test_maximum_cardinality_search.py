# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-cardinality-search/. The authors are listed in prov/M2KXJV.jsonl.

import itertools
import random

from maximum_cardinality_search import maximum_cardinality_search


def make(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for lst in adj:
        lst.sort()
    return adj


def is_mcs(adj: list[list[int]], order: list[int]) -> bool:
    """Check the definition: each chosen vertex has the most visited neighbours."""
    n = len(adj)
    if sorted(order) != list(range(n)) or (n and order[0] != 0):
        return False
    pos = {v: i for i, v in enumerate(order)}

    def count(x: int, i: int) -> int:
        return sum(1 for u in adj[x] if pos[u] < i)

    return all(count(v, i) >= count(x, i) for i, v in enumerate(order) for x in order[i + 1 :])


def reverse_is_peo(adj: list[list[int]], order: list[int]) -> bool:
    pos = {v: i for i, v in enumerate(order)}
    nbr = [set(lst) for lst in adj]
    for v in order:
        earlier = [u for u in adj[v] if pos[u] < pos[v]]
        if any(y not in nbr[x] for x, y in itertools.combinations(earlier, 2)):
            return False
    return True


def is_chordal(adj: list[list[int]]) -> bool:
    """Independent oracle: repeatedly delete a simplicial vertex."""
    alive = set(range(len(adj)))
    nbr = [set(lst) for lst in adj]
    while alive:
        for v in alive:
            nv = nbr[v] & alive
            if all(y in nbr[x] for x, y in itertools.combinations(nv, 2)):
                alive.remove(v)
                break
        else:
            return False
    return True


EXAMPLE = [(0, 3), (1, 2), (1, 3), (1, 6), (2, 6), (3, 4), (3, 6), (4, 5), (4, 6), (5, 6)]


def test_example() -> None:
    adj = make(7, EXAMPLE)
    order = maximum_cardinality_search(adj)
    assert order == [0, 3, 1, 6, 2, 4, 5]
    assert reverse_is_peo(adj, order)


def test_four_cycle() -> None:
    adj = make(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    order = maximum_cardinality_search(adj)
    assert order == [0, 1, 3, 2]
    assert not reverse_is_peo(adj, order)


def test_small_cases() -> None:
    assert maximum_cardinality_search([]) == []
    assert maximum_cardinality_search([[]]) == [0]
    assert maximum_cardinality_search([[], [], []]) == [0, 1, 2]
    assert maximum_cardinality_search(make(3, [(1, 2)])) == [0, 1, 2]
    assert maximum_cardinality_search(make(3, [(0, 2)])) == [0, 2, 1]


def test_long_path() -> None:
    n = 100000
    adj = make(n, [(i, i + 1) for i in range(n - 1)])
    order = maximum_cardinality_search(adj)
    assert order == list(range(n))
    assert reverse_is_peo(adj, order)


def random_chordal(rng: random.Random, n: int) -> list[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for v in range(1, n):
        if rng.random() < 0.15:
            continue
        clique = [rng.randrange(v)]
        for w in range(v):
            if w not in clique and rng.random() < 0.5:
                if all((min(w, x), max(w, x)) in edges for x in clique):
                    clique.append(w)
        edges.update((x, v) for x in clique)
    perm = list(range(n))
    rng.shuffle(perm)
    return [(perm[a], perm[b]) for a, b in edges]


def test_random_against_definition_and_chordality() -> None:
    rng = random.Random(1984)
    for trial in range(600):
        n = rng.randint(1, 9)
        if trial % 2 == 0:
            edges = random_chordal(rng, n)
        else:
            pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
            edges = [p for p in pairs if rng.random() < 0.4]
        adj = make(n, edges)
        for lst in adj:
            rng.shuffle(lst)
        order = maximum_cardinality_search(adj)
        assert is_mcs(adj, order)
        assert reverse_is_peo(adj, order) == is_chordal(adj)
