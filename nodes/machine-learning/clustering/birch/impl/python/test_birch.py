# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/birch/. The authors are listed in prov/3BD165.jsonl.

import random
from fractions import Fraction

from birch import CF, birch, phase1, phase3, phase4, sqdist, total, ward_increase


def rand_points(rng, n, d=2, lo=-30, hi=30):
    return [[Fraction(rng.randint(lo, hi), rng.randint(1, 3)) for _ in range(d)] for _ in range(n)]


def sse(points, labels, centroids):
    return sum(sqdist(x, centroids[l]) for x, l in zip(points, labels))


def test_ward_increase_from_cfs_is_exact():
    rng = random.Random(1)
    for _ in range(100):
        a_pts = rand_points(rng, rng.randint(1, 5))
        b_pts = rand_points(rng, rng.randint(1, 5))
        a = total([CF.of_point(x) for x in a_pts])
        b = total([CF.of_point(x) for x in b_pts])

        def direct(pts):
            c = [sum(p[i] for p in pts) / len(pts) for i in range(2)]
            return sum(sqdist(p, c) for p in pts)

        assert a.sse() == direct(a_pts)
        assert ward_increase(a, b) == direct(a_pts + b_pts) - direct(a_pts) - direct(b_pts)


def test_phase1_respects_memory_and_keeps_the_total():
    rng = random.Random(2)
    for _ in range(4):
        pts = rand_points(rng, 80)
        M = rng.randint(6, 20)
        tree, rebuilds = phase1(pts, 3, 3, M)
        entries = tree.leaf_entries()
        assert len(entries) <= M
        assert total(entries) == total([CF.of_point(x) for x in pts])
        assert all(e.radius_sq() <= tree.t2 for e in entries)
        assert rebuilds >= 1


def test_phase3_and_phase4():
    rng = random.Random(3)
    for _ in range(4):
        pts = rand_points(rng, 60)
        tree, _ = phase1(pts, 4, 4, 15)
        entries = tree.leaf_entries()
        k = 3
        clusters = phase3(entries, k)
        assert len(clusters) == k
        assert sorted(i for _, ids in clusters for i in ids) == list(range(len(entries)))
        for cf, ids in clusters:
            assert cf == total([entries[i] for i in ids])
        # the phase 3 partition of the points has SSE = sum of the cluster SSEs;
        # one redistribution pass cannot be worse
        phase3_sse = sum(cf.sse() for cf, _ in clusters)
        old = [cf.centroid() for cf, _ in clusters]
        labels, cents = phase4(pts, old)
        assert sse(pts, labels, cents) <= phase3_sse
        for x, l in zip(pts, labels):
            assert sqdist(x, old[l]) == min(sqdist(x, c) for c in old)


def test_separated_blobs_are_found():
    rng = random.Random(4)
    centers = [(0, 0), (40, 0), (0, 40)]
    pts, truth = [], []
    for t, (cx, cy) in enumerate(centers):
        for _ in range(60):
            pts.append([Fraction(cx + rng.randint(-5, 5)), Fraction(cy + rng.randint(-5, 5))])
            truth.append(t)
    order = list(range(len(pts)))
    rng.shuffle(order)
    pts = [pts[i] for i in order]
    truth = [truth[i] for i in order]
    labels, cents = birch(pts, 3, B=3, L=3, max_entries=12)
    groups = {}
    for l, t in zip(labels, truth):
        groups.setdefault(l, set()).add(t)
    assert sorted(len(g) for g in groups.values()) == [1, 1, 1]
    assert len(groups) == 3
