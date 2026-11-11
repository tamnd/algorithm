# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/supersingular-isogeny-problem/. The authors are listed in prov/QQP1FK.jsonl.

import random

import pytest

from supersingular_isogeny_problem import (
    Curve,
    Fp2,
    bfs_path,
    isogeny_from_path,
    mitm_path,
    phi2,
    two_isogeny_graph,
)


@pytest.fixture(scope="module")
def small():
    return two_isogeny_graph(431, seed=1)


@pytest.fixture(scope="module")
def large():
    return two_isogeny_graph(10007, seed=1)


def check_path(adj, path, s, t):
    assert path[0] == s and path[-1] == t
    for u, v in zip(path, path[1:]):
        assert v in adj[u]
        assert phi2(u, v).is_zero()


def test_graph_sizes(small, large):
    # p = 11 mod 12 for both primes: floor(p / 12) + 2 vertices.
    assert len(small[0]) == 431 // 12 + 2 == 37
    assert len(large[0]) == 10007 // 12 + 2 == 835


def test_paths_are_shortest(small):
    adj, _ = small
    js = sorted(adj, key=lambda z: z.key())
    for s in js[:6]:
        for t in js:
            p1, _ = bfs_path(adj, s, t)
            p2, _ = mitm_path(adj, s, t)
            check_path(adj, p1, s, t)
            check_path(adj, p2, s, t)
            assert len(p1) == len(p2)


def test_meet_in_the_middle_touches_fewer_vertices(large):
    adj, _ = large
    js = sorted(adj, key=lambda z: z.key())
    rng = random.Random(7)
    one_side = two_sides = 0
    for _ in range(40):
        s, t = rng.choice(js), rng.choice(js)
        p1, n1 = bfs_path(adj, s, t)
        p2, n2 = mitm_path(adj, s, t)
        check_path(adj, p2, s, t)
        assert len(p1) == len(p2)
        one_side += n1
        two_sides += n2
    # The two balls of radius d/2 are much smaller than one ball of radius d.
    assert 3 * two_sides < one_side


def test_path_gives_an_isogeny(small):
    adj, curves = small
    rng = random.Random(3)
    E0 = Curve(Fp2(1, 0, 431), Fp2(0, 0, 431))
    js = sorted(adj, key=lambda z: z.key())
    for t in js[::5]:
        path, _ = mitm_path(adj, E0.j(), t)
        E, maps = isogeny_from_path(E0, path, rng)
        assert E.j() == t
        # Push a point through the chain: it stays on the curves.
        P = E0.random_point(rng)
        for phi in maps:
            P = phi(P)
            if P is None:
                break
        if P is not None:
            assert P[1] * P[1] == E.rhs(P[0])
