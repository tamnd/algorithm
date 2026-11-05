# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-cover-by-bipartite-matching/. The authors are listed in prov/775KP1.jsonl.

import random

import pytest

from path_cover_by_bipartite_matching import path_cover_by_bipartite_matching


def is_cover(n, arcs, paths) -> bool:
    arcset = set(arcs)
    seen = [v for p in paths for v in p]
    if sorted(seen) != list(range(n)):
        return False
    return all((p[i], p[i + 1]) in arcset for p in paths for i in range(len(p) - 1))


def brute_min_cover(n, arcs) -> int:
    """Independent oracle: n minus the largest arc set with in- and out-degree at most 1."""
    pairs = sorted(set(arcs))
    best = 0
    for mask in range(1 << len(pairs)):
        outs, ins, size, ok = set(), set(), 0, True
        for i, (u, v) in enumerate(pairs):
            if mask >> i & 1:
                if u in outs or v in ins:
                    ok = False
                    break
                outs.add(u)
                ins.add(v)
                size += 1
        if ok:
            best = max(best, size)
    return n - best


EXAMPLE = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (2, 5), (5, 6), (1, 5)]


def test_example() -> None:
    paths = path_cover_by_bipartite_matching(7, EXAMPLE)
    assert paths == [[0, 1, 5, 6], [2, 3, 4]]


def test_edge_cases() -> None:
    assert path_cover_by_bipartite_matching(0, []) == []
    assert path_cover_by_bipartite_matching(3, []) == [[0], [1], [2]]
    assert path_cover_by_bipartite_matching(3, [(0, 1), (1, 2)]) == [[0, 1, 2]]
    # a star: one path through the centre and the rest alone
    assert len(path_cover_by_bipartite_matching(4, [(0, 1), (0, 2), (0, 3)])) == 3
    # parallel arcs and an isolated vertex
    assert path_cover_by_bipartite_matching(3, [(0, 1), (0, 1)]) == [[0, 1], [2]]
    # a greedy choice 0->2 would need 3 paths; augmenting fixes it
    paths = path_cover_by_bipartite_matching(4, [(0, 2), (0, 3), (1, 2)])
    assert len(paths) == 2 and is_cover(4, [(0, 2), (0, 3), (1, 2)], paths)


def test_rejects_cycles() -> None:
    with pytest.raises(ValueError):
        path_cover_by_bipartite_matching(2, [(0, 1), (1, 0)])
    with pytest.raises(ValueError):
        path_cover_by_bipartite_matching(1, [(0, 0)])


def test_random_against_brute_force() -> None:
    rng = random.Random(775)
    for _ in range(800):
        n = rng.randint(1, 7)
        order = list(range(n))
        rng.shuffle(order)
        arcs = []
        for _ in range(rng.randint(0, 11)):
            i, j = sorted(rng.sample(range(n), 2)) if n >= 2 else (0, 0)
            if i != j:
                arcs.append((order[i], order[j]))
        paths = path_cover_by_bipartite_matching(n, arcs)
        assert is_cover(n, arcs, paths)
        assert len(paths) == brute_min_cover(n, arcs)
