# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/micali-vazirani-algorithm/. The authors are listed in prov/ZG9QWA.jsonl.

import random
from functools import lru_cache

import micali_vazirani_algorithm as mv
from micali_vazirani_algorithm import micali_vazirani_algorithm


def brute_force(n, edges):
    """Oracle: the size of a maximum matching, by recursion on the lowest free vertex."""
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    @lru_cache(maxsize=None)
    def best(used):
        v = 0
        while v < n and used >> v & 1:
            v += 1
        if v == n:
            return 0
        result = best(used | 1 << v)
        for u in adj[v]:
            if not used >> u & 1:
                result = max(result, 1 + best(used | 1 << v | 1 << u))
        return result

    return best(0)


def check(n, edges):
    """Return the size of the matching after checking that it is a matching of the graph."""
    mate = micali_vazirani_algorithm(n, edges)
    es = {(min(a, b), max(a, b)) for a, b in edges}
    assert len(mate) == n
    for v in range(n):
        if mate[v] != -1:
            assert mate[mate[v]] == v
            assert (min(v, mate[v]), max(v, mate[v])) in es
    return sum(x != -1 for x in mate) // 2


def run_phase(n, edges, mate):
    """Run one phase from a given matching and return the paths it augments along."""
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    phase = mv._Phase(n, adj, mate)
    paths = []
    original = phase.augment

    def record(path):
        paths.append(list(path))
        original(path)

    phase.augment = record
    phase.run()
    return phase, paths


def test_empty_graph():
    assert micali_vazirani_algorithm(0, []) == []
    assert micali_vazirani_algorithm(3, []) == [-1, -1, -1]


def test_single_edge_and_path():
    assert micali_vazirani_algorithm(2, [(0, 1)]) == [1, 0]
    assert check(4, [(0, 1), (1, 2), (2, 3)]) == 2


def test_odd_cycles():
    assert check(3, [(0, 1), (1, 2), (2, 0)]) == 1
    assert check(5, [(i, (i + 1) % 5) for i in range(5)]) == 2
    assert check(7, [(i, (i + 1) % 7) for i in range(7)]) == 3


def test_no_perfect_matching():
    # A centre joined to one vertex of each of three triangles: 10 vertices, at most 4 edges.
    edges = []
    for k in range(3):
        a, b, c = 1 + 3 * k, 2 + 3 * k, 3 + 3 * k
        edges += [(a, b), (b, c), (c, a), (0, a)]
    assert check(10, edges) == 4
    # A star has only one edge in any matching.
    assert check(6, [(0, k) for k in range(1, 6)]) == 1


def test_petersen_graph_has_a_perfect_matching():
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    assert check(10, outer + spokes + inner) == 5


def test_worked_example_one_phase():
    # Triangle 0-1-2 with 1=2 matched, then 2-3=4-5; free vertices 0 and 5.
    edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 5)]
    mate = [-1, 2, 1, 4, 3, -1]
    phase, paths = run_phase(6, edges, mate)
    assert phase.petals[0][0] == 0  # the petal {1, 2} has bud 0
    assert phase.lev[1] == [2, 1] and phase.lev[2] == [2, 1]
    assert paths == [[5, 4, 3, 2, 1, 0]]
    assert mate == [1, 0, 3, 2, 5, 4]


def test_blossom_split_by_path():
    # The 5-cycle 2-3-5-6-4 with matched edges 3=5 and 4=6, entered from 0-1=2 and left to 7.
    edges = [(0, 1), (1, 2), (2, 3), (2, 4), (3, 5), (5, 6), (4, 6), (3, 7)]
    mate = [-1, 2, 1, 5, 6, 3, 4, -1]
    _, paths = run_phase(8, edges, mate)
    assert len(paths) == 1 and len(paths[0]) == 8
    assert sorted((paths[0][0], paths[0][-1])) == [0, 7]
    assert check(8, edges) == 4


def test_bipartite_graph():
    edges = [(0, 3), (0, 4), (1, 3), (2, 4), (2, 5)]
    assert check(6, edges) == 3


def test_bad_input():
    for n, edges in ((2, [(0, 0)]), (2, [(0, 2)]), (-1, [])):
        try:
            micali_vazirani_algorithm(n, edges)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    assert micali_vazirani_algorithm(2, [(0, 1), (1, 0), (0, 1)]) == [1, 0]


def test_random_against_brute_force():
    rng = random.Random(20260511)
    for _ in range(600):
        n = rng.randint(0, 12)
        p = rng.random()
        edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < p]
        assert check(n, edges) == brute_force(n, edges)


def test_phases_use_shortest_paths_of_growing_length():
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(2, 14)
        d = rng.uniform(1.5, 4)
        edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < d / n]
        mate = [-1] * n
        lengths = []
        while True:
            _, paths = run_phase(n, edges, mate)
            if not paths:
                break
            assert len({len(p) for p in paths}) == 1
            lengths.append(len(paths[0]))
        assert lengths == sorted(set(lengths))
        assert sum(x != -1 for x in mate) // 2 == brute_force(n, edges)
