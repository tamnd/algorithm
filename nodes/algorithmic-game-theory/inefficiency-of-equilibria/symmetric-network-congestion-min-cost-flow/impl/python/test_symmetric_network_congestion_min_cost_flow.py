# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symmetric-network-congestion-min-cost-flow/. The authors are listed in prov/KZRBES.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from symmetric_network_congestion_min_cost_flow import (
    _cheapest_path,
    loads,
    min_potential_flow,
    player_costs,
    rosenthal_potential,
    split_into_paths,
    symmetric_congestion_equilibrium,
)


def simple_paths(edges, s, t):
    """All simple s-t paths, as lists of edge indices, by depth-first search."""
    out = []

    def go(u, seen, path):
        if u == t:
            out.append(list(path))
            return
        for e, (a, b, _) in enumerate(edges):
            if a == u and b not in seen:
                path.append(e)
                go(b, seen | {b}, path)
                path.pop()

    go(s, {s}, [])
    return out


def is_pure_nash(edges, profile, strategies):
    costs = player_costs(edges, profile)
    for i in range(len(profile)):
        for q in strategies:
            other = profile[:i] + [q] + profile[i + 1 :]
            if player_costs(edges, other)[i] < costs[i]:
                return False
    return True


def is_simple_st_path(edges, p, s, t):
    w, seen = s, {s}
    for e in p:
        u, v, _ = edges[e]
        if u != w or v in seen:
            return False
        seen.add(v)
        w = v
    return w == t


def braess_example():
    vertices = ["s", "a", "b", "t"]
    edges = [
        ("s", "a", [2, 4, 6]),
        ("a", "t", [5, 5, 5]),
        ("s", "b", [5, 5, 5]),
        ("b", "t", [2, 4, 6]),
        ("a", "b", [0, 0, 0]),
    ]
    return vertices, edges


def test_page_example():
    vertices, edges = braess_example()
    x = min_potential_flow(vertices, edges, "s", "t", 3)
    assert x == [2, 1, 1, 2, 1]
    paths = split_into_paths(edges, x, "s", "t", 3)
    assert sorted(paths) == [[0, 1], [0, 4, 3], [2, 3]]
    assert rosenthal_potential(edges, paths) == 22
    assert sorted(player_costs(edges, paths)) == [8, 9, 9]
    assert sum(player_costs(edges, paths)) == 26
    strategies = simple_paths(edges, "s", "t")
    assert is_pure_nash(edges, paths, strategies)
    best = min(
        sum(player_costs(edges, [strategies[i] for i in prof]))
        for prof in itertools.combinations_with_replacement(range(len(strategies)), 3)
    )
    assert best == 25


def test_without_the_middle_edge():
    vertices, edges = braess_example()
    edges = edges[:4]
    paths = symmetric_congestion_equilibrium(vertices, edges, "s", "t", 3)
    assert sum(player_costs(edges, paths)) == 25
    assert rosenthal_potential(edges, paths) == 23


def random_instance(rng, nv, n, zero_prob):
    vertices = list(range(nv))
    edges = []
    for u in range(nv):
        for v in range(nv):
            if u != v and rng.random() < 0.45:
                if rng.random() < zero_prob:
                    costs = [0] * n
                else:
                    a, b = rng.randint(0, 3), rng.randint(0, 4)
                    bumps = sorted(rng.randint(0, 3) for _ in range(n))
                    q = rng.randint(1, 2)
                    costs = [Fraction(a * j + b + bumps[j - 1], q) for j in range(1, n + 1)]
                edges.append((u, v, costs))
    return vertices, edges


def test_random_against_brute_force():
    rng = random.Random(20040613)
    done = 0
    while done < 120:
        nv = rng.randint(2, 5)
        n = rng.randint(1, 4)
        vertices, edges = random_instance(rng, nv, n, 0.25)
        s, t = 0, nv - 1
        strategies = simple_paths(edges, s, t)
        if not strategies or len(strategies) > 7:
            continue
        done += 1
        paths = symmetric_congestion_equilibrium(vertices, edges, s, t, n)
        assert len(paths) == n
        assert all(is_simple_st_path(edges, p, s, t) for p in paths)
        assert is_pure_nash(edges, paths, strategies)
        phi = rosenthal_potential(edges, paths)
        best = min(
            rosenthal_potential(edges, [strategies[i] for i in prof])
            for prof in itertools.combinations_with_replacement(range(len(strategies)), n)
        )
        assert phi == best


def braess_like_instance(rng, nv, n):
    """Steep edges s-a and b-t, flat edges a-t and s-b, a cheap edge a-b, and a few random edges."""

    def steep():
        a, z = rng.randint(1, 4), rng.randint(0, 1)
        return [a * j + z * j * j for j in range(1, n + 1)]

    def flat(lo, hi):
        return [rng.randint(lo, hi)] * n

    t = nv - 1
    edges = [(0, 1, steep()), (1, t, flat(2, 9)), (0, 2, flat(2, 9)), (2, t, steep()), (1, 2, flat(0, 1))]
    for u in range(nv):
        for v in range(nv):
            if u != v and rng.random() < 0.12:
                edges.append((u, v, steep() if rng.random() < 0.5 else flat(0, 9)))
    rng.shuffle(edges)
    return list(range(nv)), edges


def test_braess_like_instances_use_backward_arcs():
    rng = random.Random(2004)
    done = backward = 0
    while done < 120:
        nv, n = rng.randint(4, 5), rng.randint(2, 4)
        vertices, edges = braess_like_instance(rng, nv, n)
        s, t = 0, nv - 1
        strategies = simple_paths(edges, s, t)
        if len(strategies) > 9:
            continue
        done += 1
        x = [0] * len(edges)
        used = False
        for _ in range(n):
            path = _cheapest_path(vertices, edges, x, s, t, n)
            used = used or any(d == -1 for _, d in path)
            for e, d in path:
                x[e] += d
        backward += used
        assert x == min_potential_flow(vertices, edges, s, t, n)
        paths = split_into_paths(edges, x, s, t, n)
        assert all(is_simple_st_path(edges, p, s, t) for p in paths)
        assert is_pure_nash(edges, paths, strategies)
        best = min(
            rosenthal_potential(edges, [strategies[i] for i in prof])
            for prof in itertools.combinations_with_replacement(range(len(strategies)), n)
        )
        assert rosenthal_potential(edges, paths) == best
    assert backward >= 10


def test_flow_is_conserved():
    rng = random.Random(7)
    for _ in range(60):
        vertices, edges = random_instance(rng, 5, 3, 0.5)
        if not simple_paths(edges, 0, 4):
            continue
        x = min_potential_flow(vertices, edges, 0, 4, 3)
        for w in vertices:
            net = sum(x[e] for e, (u, _, _) in enumerate(edges) if u == w) - sum(
                x[e] for e, (_, v, _) in enumerate(edges) if v == w
            )
            assert net == (3 if w == 0 else -3 if w == 4 else 0)
        paths = split_into_paths(edges, x, 0, 4, 3)
        assert all(a <= b for a, b in zip(loads(edges, paths), x))


def test_zero_cost_cycle_is_removed():
    vertices = ["s", "a", "b", "t"]
    edges = [("s", "a", [1, 1]), ("a", "b", [0, 0]), ("b", "a", [0, 0]), ("a", "t", [1, 1])]
    x = [2, 1, 1, 2]
    paths = split_into_paths(edges, x, "s", "t", 2)
    assert paths == [[0, 3], [0, 3]]


def test_errors():
    vertices = ["s", "t"]
    with pytest.raises(ValueError):
        symmetric_congestion_equilibrium(vertices, [("s", "t", [3, 2])], "s", "t", 2)
    with pytest.raises(ValueError):
        symmetric_congestion_equilibrium(vertices, [("s", "t", [-1, 2])], "s", "t", 2)
    with pytest.raises(ValueError):
        symmetric_congestion_equilibrium(vertices, [("t", "s", [1, 2])], "s", "t", 2)
    with pytest.raises(ValueError):
        symmetric_congestion_equilibrium(vertices, [("s", "t", [1])], "s", "t", 2)
