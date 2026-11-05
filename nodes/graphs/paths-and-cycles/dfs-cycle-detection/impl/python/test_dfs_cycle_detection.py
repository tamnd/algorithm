# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dfs-cycle-detection/. The authors are listed in prov/YS8QZ8.jsonl.

import random

from dfs_cycle_detection import dfs_cycle_detection


def is_cycle(n: int, edges: list[tuple[int, int]], c: list[int], directed: bool) -> bool:
    """Check that c lists the ids of the edges of a cycle, in order."""
    if not c or len(set(c)) != len(c) or any(not 0 <= e < len(edges) for e in c):
        return False
    if directed:
        walk = [edges[c[0]][0]]
        for e in c:
            u, v = edges[e]
            if u != walk[-1]:
                return False
            walk.append(v)
    else:
        # Try both directions of the first edge.
        for start in set(edges[c[0]]):
            walk = [start]
            ok = True
            for e in c:
                u, v = edges[e]
                if walk[-1] == u:
                    walk.append(v)
                elif walk[-1] == v:
                    walk.append(u)
                else:
                    ok = False
                    break
            if ok and walk[0] == walk[-1] and len(set(walk[:-1])) == len(c):
                return True
        return False
    return walk[0] == walk[-1] and len(set(walk[:-1])) == len(c)


def has_cycle_brute(n: int, edges: list[tuple[int, int]], directed: bool) -> bool:
    """An edge (u, v) lies on a cycle iff u can be reached from v without that edge."""
    for i, (u, v) in enumerate(edges):
        adj: list[list[int]] = [[] for _ in range(n)]
        for j, (a, b) in enumerate(edges):
            if j == i and not directed:
                continue
            adj[a].append(b)
            if not directed:
                adj[b].append(a)
        seen, todo = {v}, [v]
        while todo:
            x = todo.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    todo.append(y)
        if u in seen:
            return True
    return False


def test_example() -> None:
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 2), (5, 4)]
    assert dfs_cycle_detection(6, edges) == [4, 5, 3]
    edges_u = [(0, 1), (1, 2), (2, 3), (3, 1)]
    assert dfs_cycle_detection(4, edges_u, directed=False) == [1, 2, 3]


def test_acyclic() -> None:
    assert dfs_cycle_detection(0, []) is None
    assert dfs_cycle_detection(3, []) is None  # isolated vertices
    assert dfs_cycle_detection(3, [(0, 1), (1, 2), (0, 2)]) is None
    assert dfs_cycle_detection(4, [(0, 1), (1, 2), (1, 3)], directed=False) is None
    # In a directed graph, u -> v and v -> u is a cycle; one undirected edge is not.
    assert dfs_cycle_detection(2, [(0, 1)], directed=False) is None


def test_self_loops_and_parallel_edges() -> None:
    assert dfs_cycle_detection(1, [(0, 0)]) == [0]
    assert dfs_cycle_detection(1, [(0, 0)], directed=False) == [0]
    assert dfs_cycle_detection(2, [(0, 1), (1, 0)]) == [0, 1]
    assert dfs_cycle_detection(2, [(0, 1), (0, 1)]) is None
    assert dfs_cycle_detection(2, [(0, 1), (0, 1)], directed=False) == [0, 1]
    assert dfs_cycle_detection(2, [(0, 1), (1, 0)], directed=False) == [0, 1]


def test_long_path() -> None:
    n = 200_000
    edges = [(i, i + 1) for i in range(n - 1)]
    assert dfs_cycle_detection(n, edges) is None
    assert dfs_cycle_detection(n, edges, directed=False) is None
    edges.append((n - 1, 0))
    c = dfs_cycle_detection(n, edges)
    assert c is not None and len(c) == n
    c = dfs_cycle_detection(n, edges, directed=False)
    assert c is not None and len(c) == n


def test_random_against_brute_force() -> None:
    rng = random.Random(20261105)
    for case in range(1500):
        n = rng.randint(1, 7)
        m = rng.randint(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        if case % 3 == 0:  # mostly forward edges, so that many graphs are acyclic
            edges = [(min(a, b), max(a, b)) for a, b in edges if a != b]
        for directed in (True, False):
            c = dfs_cycle_detection(n, edges, directed)
            expected = has_cycle_brute(n, edges, directed)
            assert (c is not None) == expected, (n, edges, directed)
            if c is not None:
                assert is_cycle(n, edges, c, directed), (n, edges, directed, c)
