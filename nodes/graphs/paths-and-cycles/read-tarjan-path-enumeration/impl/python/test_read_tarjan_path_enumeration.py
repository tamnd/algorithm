# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/read-tarjan-path-enumeration/. The authors are listed in prov/89EF45.jsonl.

import itertools
import random

from read_tarjan_path_enumeration import read_tarjan_path_enumeration


def brute_paths(n, edges, s, t, directed=True):
    """Independent oracle: try every sequence of distinct vertices from s to t."""
    arcs = set()
    for u, v in edges:
        if u != v:
            arcs.add((u, v))
            if not directed:
                arcs.add((v, u))
    if s == t:
        return [[s]]
    found = []
    middle = [v for v in range(n) if v not in (s, t)]
    for k in range(len(middle) + 1):
        for mid in itertools.permutations(middle, k):
            seq = [s, *mid, t]
            if all((seq[i], seq[i + 1]) in arcs for i in range(len(seq) - 1)):
                found.append(seq)
    return found


EXAMPLE = [(0, 1), (0, 2), (1, 2), (2, 1), (1, 3), (2, 3), (3, 4), (2, 4), (4, 5)]


def test_example() -> None:
    got = read_tarjan_path_enumeration(6, EXAMPLE, 0, 4)
    assert sorted(got) == sorted(brute_paths(6, EXAMPLE, 0, 4))
    assert len(got) == 6
    assert got[0] == [0, 2, 4]


def test_edge_cases() -> None:
    assert read_tarjan_path_enumeration(1, [], 0, 0) == [[0]]
    assert read_tarjan_path_enumeration(3, [(0, 1)], 0, 2) == []
    assert read_tarjan_path_enumeration(2, [(1, 0)], 0, 1) == []
    assert read_tarjan_path_enumeration(2, [(1, 0)], 0, 1, directed=False) == [[0, 1]]
    # loops and parallel edges do not add paths
    assert read_tarjan_path_enumeration(2, [(0, 1), (0, 1), (0, 0), (1, 1)], 0, 1) == [[0, 1]]
    # complete digraph on 4 vertices: 1 + 2 + 2 = 5 paths from 0 to 3
    k4 = [(u, v) for u in range(4) for v in range(4) if u != v]
    assert len(read_tarjan_path_enumeration(4, k4, 0, 3)) == 5


def test_random_against_brute_force() -> None:
    rng = random.Random(1975)
    for _ in range(800):
        n = rng.randint(1, 7)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 14))]
        s, t = rng.randrange(n), rng.randrange(n)
        directed = rng.random() < 0.6
        got = read_tarjan_path_enumeration(n, edges, s, t, directed)
        want = brute_paths(n, edges, s, t, directed)
        assert len(got) == len(want)
        assert sorted(got) == sorted(want)
