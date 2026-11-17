# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pictorial-structures/. The authors are listed in prov/ZNK7K3.jsonl.

import random

from pictorial_structures import (dt1d, dt1d_brute, dt2d, dt2d_quadratic, energy, match,
                                  match_brute)


def random_costs(rng, parts, W, H, top=9):
    return [[[rng.randint(0, top) for _ in range(W)] for _ in range(H)] for _ in range(parts)]


def random_tree(rng, parts):
    parent = [None] + [rng.randrange(i) for i in range(1, parts)]
    edges = [None] + [(rng.randint(-2, 2), rng.randint(-2, 2), rng.randint(1, 3), rng.randint(1, 3))
                      for _ in range(1, parts)]
    return parent, edges


def test_page_examples():
    assert dt1d([3, 0, 5, 1, 4]) == ([1, 0, 1, 1, 2], [1, 1, 1, 3, 3])
    assert dt1d([3, 0, 5, 1, 4], 1, 2)[0] == [1, 1, 2, 5, 8]
    costs = [[[2, 1, 3, 0, 2, 4]], [[1, 3, 0, 2, 4, 1]], [[3, 2, 2, 0, 1, 0]]]
    parent, edges = [None, 0, 0], [None, (1, 0, 1, 1), (-1, 0, 1, 1)]
    assert dt1d(costs[1][0], 1, 1)[0] == [1, 0, 1, 2, 1, 2]
    assert dt1d(costs[2][0], 1, -1)[0] == [4, 3, 2, 1, 0, 1]
    assert match(costs, parent, edges) == (3, [(3, 0), (5, 0), (3, 0)])


def test_dt1d_matches_brute_force():
    rng = random.Random(31)
    for trial in range(400):
        n = rng.randint(1, 12)
        f = [rng.randint(-5, 20) for _ in range(n)]
        w, u = rng.randint(1, 4), rng.randint(-4, 4)
        D, arg = dt1d(f, w, u)
        Db, _ = dt1d_brute(f, w, u)
        assert D == Db
        assert all(f[arg[p]] + w * (arg[p] - p - u) ** 2 == D[p] for p in range(n))


def test_dt2d_matches_quadratic():
    rng = random.Random(32)
    for trial in range(60):
        W, H = rng.randint(1, 6), rng.randint(1, 5)
        f = [[rng.randint(0, 15) for _ in range(W)] for _ in range(H)]
        wx, wy, ux, uy = rng.randint(1, 3), rng.randint(1, 3), rng.randint(-2, 2), rng.randint(-2, 2)
        D, A = dt2d(f, wx, wy, ux, uy)
        Dq, _ = dt2d_quadratic(f, wx, wy, ux, uy)
        assert D == Dq
        for y in range(H):
            for x in range(W):
                xx, yy = A[y][x]
                assert f[yy][xx] + wx * (xx - x - ux) ** 2 + wy * (yy - y - uy) ** 2 == D[y][x]


def test_match_equals_brute_force():
    rng = random.Random(33)
    for trial in range(60):
        parts = rng.randint(1, 4)
        W, H = (4, 3) if parts <= 3 else (3, 3)
        costs = random_costs(rng, parts, W, H)
        parent, edges = random_tree(rng, parts)
        e, config = match(costs, parent, edges)
        eb, _ = match_brute(costs, parent, edges)
        assert e == eb
        assert energy(costs, parent, edges, config) == e


def test_distance_transform_and_quadratic_dp_agree_on_larger_grids():
    rng = random.Random(34)
    for trial in range(6):
        parts = 5
        costs = random_costs(rng, parts, 6, 5, top=30)
        parent, edges = random_tree(rng, parts)
        e1, c1 = match(costs, parent, edges)
        e2, c2 = match(costs, parent, edges, transform=dt2d_quadratic)
        assert e1 == e2
        assert energy(costs, parent, edges, c1) == e1 == energy(costs, parent, edges, c2)


def test_envelope_is_linear():
    # Every q is pushed once and popped at most once, and the query pointer
    # only moves forward, so the work is O(n) even for adversarial input.
    rng = random.Random(35)
    f = [rng.randint(0, 10 ** 6) for _ in range(5000)]
    D, arg = dt1d(f, 3, 7)
    assert len(D) == 5000
    assert all(arg[p] <= arg[p + 1] for p in range(4999))  # minimizers are monotone
