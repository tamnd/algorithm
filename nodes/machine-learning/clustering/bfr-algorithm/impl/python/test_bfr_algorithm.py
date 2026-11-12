# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bfr-algorithm/. The authors are listed in prov/G9NW7V.jsonl.

import random
from fractions import Fraction

from bfr_algorithm import BFR, Summary, bfr, mahalanobis_sq


def blobs(rng, centers, per, spread):
    pts, truth = [], []
    for c, (cx, cy) in enumerate(centers):
        for _ in range(per):
            pts.append([Fraction(round(rng.gauss(cx, spread) * 100), 100),
                        Fraction(round(rng.gauss(cy, spread) * 100), 100)])
            truth.append(c)
    order = list(range(len(pts)))
    rng.shuffle(order)
    return [pts[i] for i in order], [truth[i] for i in order]


def direct(points):
    d = len(points[0])
    n = len(points)
    return n, [sum(p[i] for p in points) for i in range(d)], [sum(p[i] ** 2 for p in points) for i in range(d)]


def test_summary_statistics_are_exact():
    rng = random.Random(1)
    pts = [[Fraction(rng.randint(-50, 50), rng.randint(1, 9)) for _ in range(3)] for _ in range(20)]
    a = Summary(3)
    for p in pts[:12]:
        a.add(p)
    b = Summary(3)
    for p in pts[12:]:
        b.add(p)
    m = a.merge(b)
    n, s, sq = direct(pts)
    assert (m.n, m.s, m.sq) == (n, s, sq)
    mean = [v / n for v in s]
    assert m.centroid() == mean
    assert m.variance() == [sum((p[i] - mean[i]) ** 2 for p in pts) / n for i in range(3)]


def test_mahalanobis_with_diagonal_variance():
    s = Summary(2)
    for p in ([0, 0], [2, 0], [0, 4], [2, 4]):
        s.add([Fraction(v) for v in p])
    # centroid (1, 2), variances (1, 4)
    assert mahalanobis_sq([Fraction(3), Fraction(2)], s, Fraction(1, 10**9)) == 4
    assert mahalanobis_sq([Fraction(1), Fraction(6)], s, Fraction(1, 10**9)) == 4


def test_each_point_counted_once_and_summaries_match_members():
    rng = random.Random(2)
    pts, _ = blobs(rng, [(0, 0), (10, 0), (0, 10)], 40, 1)
    pts.extend([[Fraction(30), Fraction(30)], [Fraction(-20), Fraction(25)]])  # outliers
    chunks = [pts[i:i + 20] for i in range(0, len(pts), 20)]
    algo = BFR(3, random.Random(3), alpha=3, cs_var=Fraction(1), var_floor=Fraction(1, 100), track=True)
    algo.first_chunk(chunks[0])
    for ch in chunks[1:]:
        algo.next_chunk(ch)
        assert algo.total() == algo.seen
        ids = [i for s in algo.ds + algo.cs + algo.rs for i in s.ids]
        assert sorted(ids) == list(range(algo.seen))
        for s in algo.ds + algo.cs + algo.rs:
            assert (s.n, s.s, s.sq) == direct([pts[i] for i in s.ids])
        assert all(s.n > 1 for s in algo.cs) and all(s.n == 1 for s in algo.rs)
        assert all(max(s.variance()) <= 1 for s in algo.cs)
    final = algo.finish()
    assert len(final) == 3 and sum(s.n for s in final) == len(pts)
    assert sorted(i for s in final for i in s.ids) == list(range(len(pts)))


def test_separated_axis_aligned_clusters_are_recovered():
    rng = random.Random(4)
    centers = [(0, 0), (20, 0), (0, 20), (20, 20)]
    for trial in range(3):
        pts, truth = blobs(rng, centers, 50, 1.5)
        chunks = [pts[i:i + 50] for i in range(0, len(pts), 50)]
        final = bfr(chunks, 4, random.Random(10 + trial), alpha=3, cs_var=Fraction(4),
                    var_floor=Fraction(1, 100), track=True)
        groups = sorted(sorted({truth[i] for i in s.ids}) for s in final)
        assert groups == [[0], [1], [2], [3]]
        assert sorted(s.n for s in final) == [50, 50, 50, 50]
