# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/canopy-clustering/. The authors are listed in prov/3X6R9R.jsonl.

import random

from canopy_clustering import canopies, candidate_pairs, canopy_single_link


def l1(p, q):
    return sum(abs(a - b) for a, b in zip(p, q))


def linf(p, q):
    return max(abs(a - b) for a, b in zip(p, q))


def random_points(rng, n):
    return [(rng.randint(0, 40), rng.randint(0, 40)) for _ in range(n)]


def test_cover_and_threshold_properties():
    rng = random.Random(1)
    for _ in range(100):
        pts = random_points(rng, rng.randint(1, 40))
        t2 = rng.randint(1, 10)
        t1 = t2 + rng.randint(1, 10)
        cl = canopies(pts, l1, t1, t2, random.Random(rng.random()))
        centers = [c for c, _ in cl]
        assert len(set(centers)) == len(centers)
        # every point is in some canopy, and within T2 of a center
        covered = {j for _, m in cl for j in m}
        assert covered == set(range(len(pts)))
        assert all(min(l1(pts[j], pts[c]) for c in centers) < t2 for j in range(len(pts)))
        # a later center was not removed by an earlier one
        for a in range(len(centers)):
            for b in range(a):
                assert l1(pts[centers[a]], pts[centers[b]]) >= t2
        # membership is exactly the T1 ball of the center
        for c, m in cl:
            assert m == [j for j in range(len(pts)) if l1(pts[c], pts[j]) < t1]


def test_close_pairs_share_a_canopy():
    rng = random.Random(2)
    for _ in range(60):
        pts = random_points(rng, 30)
        t2 = rng.randint(2, 8)
        t1 = t2 + rng.randint(1, 10)
        pairs = candidate_pairs(canopies(pts, l1, t1, t2, random.Random(rng.random())))
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                if l1(pts[i], pts[j]) < t1 - t2:
                    assert (i, j) in pairs


def test_second_stage_matches_full_single_link_when_canopies_are_wide():
    rng = random.Random(3)
    for _ in range(30):
        pts = random_points(rng, 25)
        thr = rng.randint(2, 6)
        # cheap distance L_inf <= L1; T1 - T2 > thr makes every pair at L1
        # distance <= thr share a canopy
        groups = canopy_single_link(pts, linf, l1, thr + 6, 5, thr, random.Random(4))
        parent = list(range(len(pts)))

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                if l1(pts[i], pts[j]) <= thr:
                    parent[find(i)] = find(j)
        full = {}
        for i in range(len(pts)):
            full.setdefault(find(i), []).append(i)
        assert groups == sorted(full.values())


def test_example_on_a_line():
    xs = [(0,), (1,), (2,), (3,), (4,), (5,), (9,), (10,), (11,)]
    cl = canopies(xs, l1, 3, 1.5, random.Random(1))
    assert [(xs[c][0], [xs[j][0] for j in m]) for c, m in cl] == [
        (2, [0, 1, 2, 3, 4]), (10, [9, 10, 11]), (0, [0, 1, 2]), (5, [3, 4, 5])]
    assert len(candidate_pairs(cl)) == 15
