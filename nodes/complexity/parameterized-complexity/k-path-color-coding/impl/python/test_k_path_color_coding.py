# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-path-color-coding/. The authors are listed in prov/BTJ3GM.jsonl.

import itertools
import math
import random

import pytest

from k_path_color_coding import (
    adjacency,
    colorful_path,
    count_colorful_paths,
    k_path,
    table_size,
    trials,
)

# The page example: the path a-b-c-d-e-f with the chord b-e. The page uses the
# colors 1 to 4; the code uses 0 to 3.
V = "abcdef"
E = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("b", "e"), ("e", "f")]


def all_paths(adj: dict, k: int) -> list[tuple]:
    """Return every vertex sequence that is a simple path with k vertices, by brute force."""
    out = []

    def extend(p: list) -> None:
        if len(p) == k:
            out.append(tuple(p))
            return
        for w in adj[p[-1]]:
            if w not in p:
                extend(p + [w])

    for v in adj:
        extend([v])
    return out


def is_path(adj: dict, p: list, k: int) -> bool:
    return len(p) == k and len(set(p)) == k and all(b in adj[a] for a, b in zip(p, p[1:]))


def random_graph(rng: random.Random, n: int, p: float) -> dict:
    edges = [(u, v) for u, v in itertools.combinations(range(n), 2) if rng.random() < p]
    return adjacency(range(n), edges)


def test_page_example() -> None:
    adj = adjacency(V, E)
    paths = all_paths(adj, 4)
    assert len(paths) == 18  # 9 paths, each in two directions
    c = dict(zip(V, [0, 1, 0, 1, 2, 3]))
    assert colorful_path(adj, c, 4) == ["a", "b", "e", "f"]
    assert count_colorful_paths(adj, c, 4) == 6  # a-b-e-f, c-b-e-f, c-d-e-f
    assert table_size(adj, c, 4) == 6 + 9 + 6 + 3
    bad = dict(zip(V, [0, 0, 1, 2, 1, 3]))
    assert colorful_path(adj, bad, 4) is None
    assert count_colorful_paths(adj, bad, 4) == 0
    # Exactly 1392 of the 4^6 = 4096 colorings find a 4-path.
    good = sum(colorful_path(adj, dict(zip(V, cols)), 4) is not None for cols in itertools.product(range(4), repeat=6))
    assert good == 1392


def test_edge_cases() -> None:
    adj = adjacency([1, 2, 3], [(1, 2)])
    assert colorful_path(adj, {1: 0, 2: 0, 3: 0}, 1) == [1]
    assert count_colorful_paths(adj, {1: 0, 2: 0, 3: 0}, 1) == 3
    assert colorful_path(adj, {1: 0, 2: 1, 3: 0}, 2) in ([1, 2], [2, 1])
    assert colorful_path(adj, {1: 0, 2: 0, 3: 1}, 2) is None
    assert colorful_path(adj, {1: 0, 2: 1, 3: 2}, 3) is None
    assert k_path(adj, 3, random.Random(0), error=0.01) is None
    assert k_path({}, 1, random.Random(0), error=0.5) is None
    with pytest.raises(ValueError):
        colorful_path(adj, {1: 0, 2: 0, 3: 0}, 0)
    with pytest.raises(ValueError):
        colorful_path(adj, {1: 0, 2: 2, 3: 0}, 2)
    with pytest.raises(ValueError):
        adjacency([1], [(1, 1)])
    with pytest.raises(ValueError):
        trials(3, 1.0)


def test_against_brute_force() -> None:
    rng = random.Random(2024)
    for _ in range(120):
        n = rng.randrange(1, 8)
        adj = random_graph(rng, n, rng.choice([0.25, 0.4, 0.6]))
        for k in range(1, n + 1):
            c = {v: rng.randrange(k) for v in adj}
            paths = all_paths(adj, k)
            colorful = [p for p in paths if len({c[v] for v in p}) == k]
            assert count_colorful_paths(adj, c, k) == len(colorful)
            p = colorful_path(adj, c, k)
            if colorful:
                assert p is not None and is_path(adj, p, k) and len({c[v] for v in p}) == k
            else:
                assert p is None


def test_directed() -> None:
    # A directed 4-cycle 0 -> 1 -> 2 -> 3 -> 0 and the arc 0 -> 2.
    adj = {0: [1, 2], 1: [2], 2: [3], 3: [0]}
    c = {0: 0, 1: 1, 2: 2, 3: 3}
    assert colorful_path(adj, c, 4) == [0, 1, 2, 3]
    assert count_colorful_paths(adj, c, 4) == 4
    assert len(all_paths(adj, 3)) == 6
    c3 = {0: 0, 1: 1, 2: 2, 3: 0}
    assert count_colorful_paths(adj, c3, 3) == 2  # 0 -> 1 -> 2 and 1 -> 2 -> 3


def test_success_probability_is_k_factorial_over_k_to_the_k() -> None:
    # On a path with k vertices, exactly the k! injective colorings succeed.
    for k in (3, 4, 5):
        adj = adjacency(range(k), [(i, i + 1) for i in range(k - 1)])
        good = sum(
            colorful_path(adj, dict(enumerate(cols)), k) is not None for cols in itertools.product(range(k), repeat=k)
        )
        assert good == math.factorial(k)
        assert math.factorial(k) / k**k > math.exp(-k)


def test_k_path_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randrange(1, 7)
        adj = random_graph(rng, n, rng.choice([0.3, 0.5]))
        for k in range(1, min(n, 5) + 1):
            exists = bool(all_paths(adj, k))
            p = k_path(adj, k, rng, error=1e-3)
            if p is None:
                assert not exists  # with this seed no existing path is missed
            else:
                assert is_path(adj, p, k)


def test_trials() -> None:
    assert trials(1, 0.5) == 1
    assert trials(4, 0.01) == 50
    assert trials(10, 1e-6) == 38072
    for k in range(1, 12):
        p = math.factorial(k) / k**k
        t = trials(k, 0.01)
        assert (1 - p) ** t <= 0.01
