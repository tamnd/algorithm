# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pruefer-decoding/. The authors are listed in prov/BS0MJQ.jsonl.

import itertools
import random

import pytest

from pruefer_decoding import labeled_trees, pruefer_decode


def is_tree(n: int, edges: list[tuple[int, int]]) -> bool:
    if len(edges) != n - 1:
        return False
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for x, y in edges:
        if not (1 <= x <= n and 1 <= y <= n) or x == y:
            return False
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        parent[rx] = ry
    return True


def encode(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Plain O(n^2) Prüfer encoder: remove the smallest leaf n - 2 times."""
    adj: dict[int, set[int]] = {v: set() for v in range(1, n + 1)}
    for x, y in edges:
        adj[x].add(y)
        adj[y].add(x)
    out = []
    for _ in range(n - 2):
        b = min(v for v in adj if len(adj[v]) == 1)
        (u,) = adj[b]
        out.append(u)
        adj[u].discard(b)
        del adj[b]
    return out


def canon(edges: list[tuple[int, int]]) -> frozenset[frozenset[int]]:
    return frozenset(frozenset(e) for e in edges)


def test_example() -> None:
    edges = pruefer_decode([4, 4, 2, 7, 7, 1])
    assert edges == [(3, 4), (5, 4), (4, 2), (2, 7), (6, 7), (7, 1), (1, 8)]


def test_edges() -> None:
    assert pruefer_decode([]) == [(1, 2)]
    assert pruefer_decode([1]) == [(2, 1), (1, 3)]
    assert pruefer_decode([3]) == [(1, 3), (2, 3)]
    assert list(labeled_trees(1)) == [[]]
    assert list(labeled_trees(2)) == [[(1, 2)]]
    with pytest.raises(ValueError):
        pruefer_decode([0])
    with pytest.raises(ValueError):
        pruefer_decode([5, 1])
    with pytest.raises(ValueError):
        list(labeled_trees(0))
    # A star and a path.
    assert canon(pruefer_decode([5, 5, 5])) == canon([(1, 5), (2, 5), (3, 5), (4, 5)])
    assert canon(pruefer_decode([2, 3, 4])) == canon([(1, 2), (2, 3), (3, 4), (4, 5)])


def test_all_codes_small() -> None:
    # Every code decodes to a tree whose code is the input (n <= 7).
    for n in range(2, 8):
        for code in itertools.product(range(1, n + 1), repeat=n - 2):
            edges = pruefer_decode(code)
            assert is_tree(n, edges)
            assert encode(n, edges) == list(code)


def test_bijection_against_brute_force() -> None:
    # The decoded trees are exactly the spanning trees of K_n (n <= 6).
    for n in range(1, 7):
        decoded = [canon(t) for t in labeled_trees(n)]
        assert len(decoded) == (n ** (n - 2) if n >= 2 else 1)
        assert len(set(decoded)) == len(decoded)
        pairs = list(itertools.combinations(range(1, n + 1), 2))
        brute = {canon(list(s)) for s in itertools.combinations(pairs, n - 1) if is_tree(n, list(s))}
        assert set(decoded) == brute


def test_degrees() -> None:
    # A label that occurs c times in the code has degree c + 1.
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(2, 60)
        code = [rng.randint(1, n) for _ in range(n - 2)]
        edges = pruefer_decode(code)
        deg = [0] * (n + 1)
        for x, y in edges:
            deg[x] += 1
            deg[y] += 1
        for v in range(1, n + 1):
            assert deg[v] == code.count(v) + 1


def test_random_round_trip() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(2, 80)
        code = [rng.randint(1, n) for _ in range(n - 2)]
        edges = pruefer_decode(code)
        assert is_tree(n, edges)
        assert encode(n, edges) == code
