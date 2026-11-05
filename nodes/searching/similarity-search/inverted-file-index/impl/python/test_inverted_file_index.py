# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverted-file-index/. The authors are listed in prov/B1PB10.jsonl.

import random

from inverted_file_index import IVFIndex, lloyd, nearest_centroid, sq_dist

PTS = [(0, 1), (2, 2), (1, 0), (3, 2), (5, 5), (7, 4), (6, 6)]


def brute(points, q, k):
    return sorted((sq_dist(q, p), i) for i, p in enumerate(points))[:k]


def test_example() -> None:
    idx = IVFIndex(PTS, 2, centroids=[(1, 1), (6, 5)])
    assert idx.lists == [[0, 1, 2, 3], [4, 5, 6]]
    assert idx.search((4, 3), 1, 1) == [(5, 4)]
    assert idx.search((4, 3), 1, 2) == [(2, 3)]
    assert idx.search_exact((4, 3), 1) == [(2, 3)]


def test_lloyd_assigns_to_nearest() -> None:
    rng = random.Random(1)
    pts = [(rng.random(), rng.random()) for _ in range(100)]
    idx = IVFIndex(pts, 5, rng=rng)
    for j, lst in enumerate(idx.lists):
        for i in lst:
            assert nearest_centroid(idx.cent, pts[i]) == j
    assert sorted(i for lst in idx.lists for i in lst) == list(range(100))


def test_random_against_brute_force() -> None:
    rng = random.Random(99)
    for _ in range(500):
        d = rng.randint(1, 4)
        n = rng.randint(1, 40)
        pts = [tuple(float(rng.randint(-5, 5)) for _ in range(d)) for _ in range(n)]
        m = rng.randint(1, 6)
        idx = IVFIndex(pts, m, iters=rng.randint(0, 4), rng=rng)
        q = tuple(rng.uniform(-6, 6) for _ in range(d))
        k = rng.randint(1, 5)
        want = brute(pts, q, k)
        assert idx.search(q, k, len(idx.cent)) == want
        assert [a for a, _ in idx.search_exact(q, k)] == [a for a, _ in want]
        prev = None
        for nprobe in range(1, len(idx.cent) + 1):
            got = idx.search(q, k, nprobe)
            assert all(sq_dist(q, pts[i]) == a for a, i in got)
            if prev is not None and len(prev) == len(got) == k:
                assert got[-1][0] <= prev[-1][0]
            prev = got


def test_insert() -> None:
    rng = random.Random(3)
    pts = [(rng.random(), rng.random()) for _ in range(50)]
    idx = IVFIndex(pts[:30], 4, rng=rng)
    for p in pts[30:]:
        idx.insert(p)
    q = (0.5, 0.5)
    assert idx.search(q, 3, 4) == brute(pts, q, 3)
