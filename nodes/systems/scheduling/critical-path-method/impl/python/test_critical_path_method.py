# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/critical-path-method/. The authors are listed in prov/EQ6EWJ.jsonl.

import random

import pytest

from critical_path_method import critical_path_method


def all_paths(n, arcs):
    """Every directed path, as a list of activities, by an explicit stack."""
    succ = [[] for _ in range(n)]
    for i, j in arcs:
        succ[i].append(j)
    paths = []
    for s in range(n):
        stack = [[s]]
        while stack:
            path = stack.pop()
            paths.append(path)
            for k in succ[path[-1]]:
                stack.append(path + [k])
    return paths


def random_dag(rng, n):
    label = list(range(n))
    rng.shuffle(label)
    arcs = [(label[i], label[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.35]
    return arcs


EXAMPLE_P = [2, 4, 3, 5, 2, 6, 1, 3]
EXAMPLE_ARCS = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 7)]


def test_example() -> None:
    r = critical_path_method(EXAMPLE_P, EXAMPLE_ARCS)
    assert r.length == 20
    assert r.es == [0, 2, 2, 6, 5, 11, 7, 17]
    assert r.ls == [0, 2, 3, 6, 14, 11, 16, 17]
    assert r.total_float == [0, 0, 1, 0, 9, 0, 9, 0]
    assert r.free_float == [0, 0, 0, 0, 0, 0, 9, 0]
    assert r.critical_path == [0, 1, 3, 5, 7]


def test_edges() -> None:
    r = critical_path_method([], [])
    assert r.length == 0 and r.critical_path == []
    r = critical_path_method([4], [])
    assert (r.length, r.es, r.ls, r.critical_path) == (4, [0], [0], [0])
    r = critical_path_method([3, 5], [])  # two independent activities
    assert r.length == 5 and r.total_float == [2, 0] and r.critical_path == [1]
    with pytest.raises(ValueError):
        critical_path_method([1, 1, 1], [(0, 1), (1, 2), (2, 0)])


def test_against_all_paths() -> None:
    rng = random.Random(1959)
    for _ in range(300):
        n = rng.randrange(1, 9)
        p = [rng.randrange(0, 8) for _ in range(n)]
        arcs = random_dag(rng, n)
        r = critical_path_method(p, arcs)
        paths = all_paths(n, arcs)
        weight = lambda path: sum(p[k] for k in path)
        assert r.length == max(weight(q) for q in paths)
        for j in range(n):
            assert r.es[j] == max(weight(q) - p[j] for q in paths if q[-1] == j)
            assert r.ls[j] == r.length - max(weight(q) for q in paths if q[0] == j)
            through = max(weight(q) for q in paths if j in q)
            assert (r.total_float[j] == 0) == (through == r.length)
            assert r.total_float[j] == r.length - through
        cp = r.critical_path
        assert cp in paths and weight(cp) == r.length


def test_floats_mean_what_they_say() -> None:
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randrange(1, 10)
        p = [rng.randrange(1, 8) for _ in range(n)]
        arcs = random_dag(rng, n)
        r = critical_path_method(p, arcs)
        for i, j in arcs:  # the earliest schedule is feasible
            assert r.es[j] >= r.ef[i]
            assert r.ls[j] >= r.lf[i]
        for j in range(n):
            assert 0 <= r.free_float[j] <= r.total_float[j]
            # a longer activity j: the project grows by the excess over the total float
            for extra in (r.total_float[j], r.total_float[j] + 1):
                q = list(p)
                q[j] += extra
                assert critical_path_method(q, arcs).length == r.length + max(0, extra - r.total_float[j])
            # using the free float moves no other earliest start
            q = list(p)
            q[j] += r.free_float[j]
            s = critical_path_method(q, arcs)
            assert all(s.es[k] == r.es[k] for k in range(n))
