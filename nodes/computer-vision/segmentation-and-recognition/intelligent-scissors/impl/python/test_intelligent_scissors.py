# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/intelligent-scissors/. The authors are listed in prov/EF89RD.jsonl.

import random

from intelligent_scissors import (
    bellman_ford,
    laplacian,
    live_wire,
    live_wire_buckets,
    local_costs,
    path_cost,
    path_to,
    quantize,
    zero_crossing_cost,
)

STAIR = [
    [10, 10, 10, 90, 90],
    [10, 10, 10, 90, 90],
    [10, 10, 90, 90, 90],
    [10, 10, 90, 90, 90],
    [10, 10, 90, 90, 90],
]


def random_image(rng, w, h):
    return [[rng.randrange(256) for _ in range(w)] for _ in range(h)]


def test_staircase_example():
    adj = local_costs(STAIR)
    costs = dict(adj[2])
    assert abs(costs[7] - 0.0233) < 1e-4
    assert abs(costs[7] - 0.14 / 6) < 1e-12
    assert abs(costs[3] - 0.1824) < 1e-4
    assert abs(costs[1] - 0.8274) < 1e-4
    g, back = live_wire(adj, 2)
    assert path_to(back, 2, 22) == [2, 7, 12, 17, 22]
    assert abs(g[22] - 0.2714) < 1e-4
    fz = zero_crossing_cost(laplacian(STAIR))
    assert [row[2] for row in fz] == [0.0] * 5


def test_costs_in_unit_interval():
    rng = random.Random(1)
    for _ in range(5):
        adj = local_costs(random_image(rng, 7, 6))
        for row in adj:
            for _, c in row:
                assert -1e-12 <= c <= 1.0 + 1e-12


def test_matches_bellman_ford():
    rng = random.Random(2)
    for _ in range(6):
        w, h = 7, 6
        adj = local_costs(random_image(rng, w, h))
        seed = rng.randrange(w * h)
        g, back = live_wire(adj, seed)
        ref = bellman_ford(adj, seed)
        for t in range(w * h):
            assert abs(g[t] - ref[t]) < 1e-9
            path = path_to(back, seed, t)
            assert path[0] == seed and path[-1] == t
            assert abs(path_cost(adj, path) - g[t]) < 1e-9


def test_bucket_queue_matches_dijkstra():
    rng = random.Random(3)
    for _ in range(5):
        w, h = 8, 6
        adj = quantize(local_costs(random_image(rng, w, h)), 255)
        seed = rng.randrange(w * h)
        gb, back = live_wire_buckets(adj, seed, 255)
        gd, _ = live_wire([[(q, float(c)) for q, c in row] for row in adj], seed)
        assert gb == [int(x) for x in gd]
        for t in range(w * h):
            assert path_cost(adj, path_to(back, seed, t)) == gb[t]


def test_affine_intensity_invariance():
    rng = random.Random(4)
    img = random_image(rng, 6, 5)
    base = local_costs(img)
    for a, b in ((2.0, 7.0), (-1.0, 255.0), (0.5, -3.0)):
        other = local_costs([[a * x + b for x in row] for row in img])
        for r1, r2 in zip(base, other):
            for (q1, c1), (q2, c2) in zip(r1, r2):
                assert q1 == q2 and abs(c1 - c2) < 1e-9


def test_path_follows_straight_edge():
    img = [[0 if u < 3 else 100 for u in range(7)] for _ in range(7)]
    adj = local_costs(img)
    g, back = live_wire(adj, 3)
    path = path_to(back, 3, 6 * 7 + 3)
    assert all(p % 7 in (2, 3) for p in path)
    assert len(path) == 7
