# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fleury-algorithm/. The authors are listed in prov/CVA0RG.jsonl.

import random

from fleury_algorithm import fleury_algorithm


def is_trail(n: int, edges: list[tuple[int, int]], walk: list[int], trail: list[int]) -> bool:
    if sorted(trail) != list(range(len(edges))) or len(walk) != len(trail) + 1:
        return False
    for i, e in enumerate(trail):
        if sorted(edges[e]) != sorted((walk[i], walk[i + 1])):
            return False
    return True


def has_trail_brute(n: int, edges: list[tuple[int, int]]) -> bool:
    """Try every order and orientation of the edges, by depth-first search."""
    m = len(edges)
    if m == 0:
        return True
    inc: list[list[int]] = [[] for _ in range(n)]
    for e, (u, v) in enumerate(edges):
        inc[u].append(e)
        if u != v:
            inc[v].append(e)
    for s in range(n):
        stack = [(s, 0, (1 << m) - 1)]
        while stack:
            u, k, free = stack.pop()
            if free == 0:
                return True
            for e in inc[u]:
                if free >> e & 1:
                    a, b = edges[e]
                    stack.append((b if a == u else a, k + 1, free & ~(1 << e)))
    return False


def test_example() -> None:
    # A triangle 0, 1, 2 with a pendant edge to 3 listed first at vertex 0.
    edges = [(0, 3), (0, 1), (1, 2), (2, 0)]
    assert fleury_algorithm(4, edges) == ([0, 1, 2, 0, 3], [1, 2, 3, 0])


def test_house_of_nicholas() -> None:
    # The house of Nicholas: a square 0, 1, 2, 3 with both diagonals and a roof vertex 4.
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3), (2, 4), (3, 4)]
    walk, trail = fleury_algorithm(5, edges)
    assert walk == [0, 1, 2, 3, 0, 2, 4, 3, 1]
    assert trail == [0, 1, 2, 3, 4, 6, 7, 5]


def test_edge_cases() -> None:
    assert fleury_algorithm(0, []) == ([], [])
    assert fleury_algorithm(3, []) == ([0], [])
    assert fleury_algorithm(1, [(0, 0)]) == ([0, 0], [0])  # one self-loop
    assert fleury_algorithm(2, [(0, 1), (0, 1)]) == ([0, 1, 0], [0, 1])  # parallel edges
    # isolated vertex 0 does not matter
    walk, trail = fleury_algorithm(4, [(1, 2), (2, 3), (3, 1)])
    assert walk[0] == walk[-1] and sorted(trail) == [0, 1, 2]
    # two components with edges: no trail
    assert fleury_algorithm(4, [(0, 1), (2, 3)]) is None
    # four odd vertices: the star K_{1,3} has no trail
    assert fleury_algorithm(4, [(0, 1), (0, 2), (0, 3)]) is None
    # a loop on a path
    walk, trail = fleury_algorithm(3, [(0, 1), (1, 1), (1, 2)])
    assert walk == [0, 1, 1, 2]


def test_trap_bridge_is_avoided() -> None:
    # Two triangles joined at vertex 0. From 0, any first edge is fine, but at the far
    # vertex of the first triangle, the walk must not cross back before the triangle ends.
    edges = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]
    walk, trail = fleury_algorithm(5, edges)
    assert is_trail(5, edges, walk, trail) and walk[0] == walk[-1]


def test_random_against_brute_force() -> None:
    rng = random.Random(20261105)
    for case in range(1500):
        n = rng.randint(1, 6)
        m = rng.randint(0, 8)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        res = fleury_algorithm(n, edges)
        expected = has_trail_brute(n, edges)
        assert (res is not None) == expected, (n, edges)
        if res is not None and m > 0:
            walk, trail = res
            assert is_trail(n, edges, walk, trail)
            odd = [v for v in range(n) if sum((a == v) + (b == v) for a, b in edges) % 2]
            if not odd:
                assert walk[0] == walk[-1]
            else:
                assert {walk[0], walk[-1]} == set(odd)
