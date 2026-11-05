# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asymmetric-lsh/. The authors are listed in prov/NNNB37.jsonl.

import math
import random

from asymmetric_lsh import (SimpleALSH, collision_probability, dot, l2_alsh_transforms,
                            norm, parameters, transform_data, transform_query)

X = [(2, 0), (1, 1), (0, 3), (-1, -1)]


def test_example() -> None:
    q = (1, 1)
    m = max(norm(x) for x in X)
    assert m == 3
    sims = [dot(transform_data(x, m), transform_query(q)) for x in X]
    assert [round(s, 4) for s in sims] == [0.4714, 0.4714, 0.7071, -0.4714]
    assert round(collision_probability(sims[2]), 4) == 0.75
    assert round(collision_probability(sims[0]), 4) == 0.6563
    assert parameters(10 ** 6, 0.9, 0.5) == (32, 165, parameters(10 ** 6, 0.9, 0.5)[2])
    assert abs(parameters(10 ** 6, 0.9, 0.5)[2] - 0.3579) < 1e-4
    # One table with zero hyperplanes puts everything in one bucket: exact MIPS.
    assert SimpleALSH(X, k=0, L=1).query(q) == 2
    assert SimpleALSH([], k=2, L=2).query(q) is None


def test_transforms_random() -> None:
    rng = random.Random(37)
    for _ in range(500):
        d = rng.randint(1, 6)
        pts = [[rng.uniform(-5, 5) for _ in range(d)] for _ in range(rng.randint(1, 8))]
        q = [rng.uniform(-5, 5) for _ in range(d)]
        if norm(q) < 1e-6:
            continue
        m = max(norm(x) for x in pts)
        for x in pts:
            px, qq = transform_data(x, m), transform_query(q)
            assert abs(norm(px) - 1) < 1e-9 and abs(norm(qq) - 1) < 1e-9
            assert abs(dot(px, qq) - dot(q, x) / (m * norm(q))) < 1e-9
        # L2-ALSH identity: |Q - P|^2 = 1 + m/4 - 2 q.x + |x|^(2^(m+1)).
        u = rng.uniform(0.3, 0.95)
        x = [v * u / m for v in pts[0]]
        qn = [v / norm(q) for v in q]
        mm = rng.randint(1, 4)
        P, Q = l2_alsh_transforms(x, qn, mm)
        lhs = sum((a - b) ** 2 for a, b in zip(P, Q))
        rhs = 1 + mm / 4 - 2 * dot(qn, x) + dot(x, x) ** (2 ** mm)
        assert abs(lhs - rhs) < 1e-9


def test_query_against_oracle() -> None:
    rng = random.Random(3)
    for _ in range(500):
        d = rng.randint(1, 4)
        pts = [[rng.uniform(-3, 3) for _ in range(d)] for _ in range(rng.randint(1, 10))]
        idx = SimpleALSH(pts, k=rng.randint(0, 4), L=rng.randint(1, 4), rng=rng)
        q = [rng.uniform(-3, 3) for _ in range(d)]
        if norm(q) < 1e-6:
            continue
        cand = idx.candidates(q)
        got = idx.query(q)
        if not cand:
            assert got is None
            continue
        best = max(dot(q, pts[i]) for i in cand)
        assert got in cand and dot(q, pts[got]) == best
        # Candidates are exactly the points sharing a bucket in some table.
        qq = transform_query(q)
        m = max(norm(p) for p in pts)
        want = {i for i, p in enumerate(pts)
                if any(idx.key(j, transform_data(p, m)) == idx.key(j, qq) for j in range(idx.L))}
        assert cand == want


def test_collision_rate() -> None:
    rng = random.Random(11)
    u = transform_data([1.0, 2.0], 3.0)
    v = transform_query([2.0, 1.0])
    s = dot(u, v)
    trials = 4000
    hits = 0
    for _ in range(trials):
        a = [rng.gauss(0, 1) for _ in range(3)]
        hits += (dot(a, u) >= 0) == (dot(a, v) >= 0)
    assert abs(hits / trials - collision_probability(s)) < 0.03


def test_success_probability() -> None:
    rng = random.Random(5)
    n, ok, runs = 60, 0, 60
    for _ in range(runs):
        pts = [[rng.gauss(0, 1) for _ in range(4)] for _ in range(n)]
        q = [rng.gauss(0, 1) for _ in range(4)]
        best = max(range(n), key=lambda i: dot(q, pts[i]))
        idx = SimpleALSH(pts, k=3, L=12, rng=rng)
        ok += idx.query(q) == best
    assert ok >= runs * 0.8
