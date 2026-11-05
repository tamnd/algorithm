# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierholzer-algorithm/. The authors are listed in prov/0QG3S6.jsonl.

import random

from hierholzer_algorithm import hierholzer_algorithm


def is_euler_trail(n, edges, directed, res) -> bool:
    walk, trail = res
    m = len(edges)
    if sorted(trail) != list(range(m)) or len(walk) != m + 1:
        return False
    for i, e in enumerate(trail):
        u, v = edges[e]
        a, b = walk[i], walk[i + 1]
        if directed:
            if (u, v) != (a, b):
                return False
        elif (u, v) not in ((a, b), (b, a)):
            return False
    return True


def brute(n, edges, directed):
    """Independent oracle: (some Eulerian trail exists, some Eulerian circuit exists)."""
    m = len(edges)
    if m == 0:
        return True, True
    found_open = found_closed = False
    for s in range(n):
        stack = [(s, s, 0)]  # (start, current vertex, mask of used edges)
        seen = set()
        while stack:
            st, v, mask = stack.pop()
            if mask == (1 << m) - 1:
                found_open = True
                if v == st:
                    found_closed = True
                continue
            if (v, mask) in seen:
                continue
            seen.add((v, mask))
            for e, (a, b) in enumerate(edges):
                if mask >> e & 1:
                    continue
                if a == v:
                    stack.append((st, b, mask | 1 << e))
                elif not directed and b == v:
                    stack.append((st, a, mask | 1 << e))
    return found_open, found_closed


EXAMPLE = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 1)]


def test_example() -> None:
    walk, trail = hierholzer_algorithm(6, EXAMPLE)
    assert walk == [0, 1, 3, 4, 1, 2, 0]
    assert trail == [0, 3, 4, 5, 1, 2]


def test_example_open() -> None:
    edges = EXAMPLE[:2] + EXAMPLE[3:]
    walk, trail = hierholzer_algorithm(6, edges)
    assert walk == [0, 1, 3, 4, 1, 2]
    assert is_euler_trail(6, edges, False, (walk, trail))


def test_small_cases() -> None:
    assert hierholzer_algorithm(0, []) == ([], [])
    assert hierholzer_algorithm(1, []) == ([0], [])
    assert hierholzer_algorithm(3, []) == ([0], [])
    assert hierholzer_algorithm(1, [(0, 0)]) == ([0, 0], [0])
    assert hierholzer_algorithm(1, [(0, 0)], True) == ([0, 0], [0])
    assert hierholzer_algorithm(2, [(0, 1), (0, 1)]) == ([0, 1, 0], [0, 1])
    assert hierholzer_algorithm(2, [(0, 1), (0, 1)], True) is None
    assert hierholzer_algorithm(2, [(0, 1)], True) == ([0, 1], [0])
    assert hierholzer_algorithm(2, [(1, 0)], True) == ([1, 0], [0])
    # isolated vertices are allowed
    assert hierholzer_algorithm(5, [(3, 4)]) == ([3, 4], [0])


def test_no_trail() -> None:
    star = [(0, 1), (0, 2), (0, 3)]
    assert hierholzer_algorithm(4, star) is None
    assert hierholzer_algorithm(4, star, True) is None
    # two triangles in different components: all degrees even, edges not connected
    two = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
    assert hierholzer_algorithm(6, two) is None
    assert hierholzer_algorithm(6, two, True) is None
    # a loop away from the other edges
    assert hierholzer_algorithm(3, [(0, 1), (2, 2)]) is None


def test_long_cycle() -> None:
    n = 100000
    edges = [(i, (i + 1) % n) for i in range(n)]
    walk, trail = hierholzer_algorithm(n, edges, True)
    assert walk == list(range(n)) + [0]
    walk, trail = hierholzer_algorithm(n, edges)
    assert is_euler_trail(n, edges, False, (walk, trail))


def test_random_against_brute_force() -> None:
    rng = random.Random(1873)
    for trial in range(800):
        n = rng.randint(1, 5)
        m = rng.randint(0, 7)
        directed = trial % 2 == 1
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        has_open, has_closed = brute(n, edges, directed)
        got = hierholzer_algorithm(n, edges, directed)
        if not has_open:
            assert got is None
            continue
        assert got is not None and is_euler_trail(n, edges, directed, got)
        if has_closed:
            assert got[0][0] == got[0][-1]
