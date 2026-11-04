# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uniform-cost-search/. The authors are listed in prov/81NJ23.jsonl.

import itertools
import random

import pytest

from uniform_cost_search import uniform_cost_search

EXAMPLE = {
    "S": [("A", 1), ("G", 12)],
    "A": [("B", 4), ("C", 1)],
    "B": [("D", 3)],
    "C": [("D", 1), ("G", 2)],
    "D": [("G", 3)],
    "G": [],
}


def run(graph, start, goals):
    return uniform_cost_search(start, lambda s: graph.get(s, []), lambda s: s in goals)


def path_cost(graph, path):
    total = 0
    for u, v in zip(path, path[1:]):
        total += min(c for w, c in graph[u] if w == v)
    return total


def oracle(graph, start, goals):
    """Least cost to a goal by Bellman-Ford relaxation, or None."""
    nodes = set(graph) | {v for es in graph.values() for v, _ in es} | {start}
    dist = {v: float("inf") for v in nodes}
    dist[start] = 0
    for _ in range(len(nodes)):
        for u, es in graph.items():
            for v, c in es:
                if dist[u] + c < dist[v]:
                    dist[v] = dist[u] + c
    best = min((dist[g] for g in goals if g in dist), default=float("inf"))
    return None if best == float("inf") else best


def test_example() -> None:
    assert run(EXAMPLE, "S", {"G"}) == (["S", "A", "C", "G"], 4)


def test_start_is_goal() -> None:
    assert run(EXAMPLE, "S", {"S"}) == (["S"], 0)


def test_unreachable() -> None:
    assert run(EXAMPLE, "G", {"S"}) is None
    assert run({"X": []}, "X", set()) is None


def test_cycles_and_zero_costs() -> None:
    g = {"a": [("b", 0)], "b": [("a", 0), ("c", 0)], "c": [("a", 0)]}
    assert run(g, "a", {"z"}) is None
    g["c"].append(("z", 5))
    assert run(g, "a", {"z"}) == (["a", "b", "c", "z"], 5)


def test_negative_cost_rejected() -> None:
    with pytest.raises(ValueError):
        run({"a": [("b", -1)]}, "a", {"b"})


def test_implicit_infinite_space() -> None:
    # states are integers; n -> n + 1 costs 1, n -> 2n costs 1; a cheapest way from 1 to 37
    res = uniform_cost_search(1, lambda n: [(n + 1, 1), (2 * n, 1)], lambda n: n == 37)
    assert res is not None
    path, cost = res
    assert cost == 7 and path[0] == 1 and path[-1] == 37 and len(path) == 8


def test_float_costs() -> None:
    g = {"s": [("a", 0.1), ("t", 0.35)], "a": [("b", 0.1)], "b": [("t", 0.1)]}
    path, cost = run(g, "s", {"t"})
    assert path == ["s", "a", "b", "t"]
    assert abs(cost - 0.3) < 1e-12


def test_against_bellman_ford() -> None:
    rng = random.Random(81)
    for _ in range(800):
        n = rng.randrange(1, 9)
        graph = {v: [] for v in range(n)}
        for u, v in itertools.product(range(n), repeat=2):
            if rng.random() < 0.3:
                graph[u].append((v, rng.randrange(0, 6)))
        goals = {v for v in range(n) if rng.random() < 0.25}
        want = oracle(graph, 0, goals)
        got = run(graph, 0, goals)
        if want is None:
            assert got is None
        else:
            path, cost = got
            assert cost == want
            assert path[0] == 0 and path[-1] in goals
            assert path_cost(graph, path) == cost
