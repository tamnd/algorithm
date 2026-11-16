# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/j-linkage/. The authors are listed in prov/ZDYX7K.jsonl.

import math
import random

from j_linkage import (cluster, fit_line_tls, j_linkage, jaccard_distance, line_through, locality_sample,
                       make_hypotheses, point_line_distance, preference_sets)

POINTS = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (1, 3)]
PAIRS = [(0, 1), (1, 7), (4, 5), (2, 4), (3, 6), (2, 3), (5, 6), (0, 7)]
HYPS = [line_through([POINTS[a], POINTS[b]]) for a, b in PAIRS]


def mask(hyp_numbers):
    return sum(1 << (h - 1) for h in hyp_numbers)


def planted(rng):
    pts = []
    for _ in range(30):
        x = rng.uniform(0, 10)
        pts.append((x, 0.5 * x + 1 + rng.gauss(0, 0.03)))
    for _ in range(30):
        x = rng.uniform(0, 10)
        pts.append((x, -x + 8 + rng.gauss(0, 0.03)))
    for _ in range(15):
        pts.append((rng.uniform(0, 10), rng.uniform(-3, 10)))
    return pts


def same_line(g, h, ang_tol=math.radians(2.0), off_tol=0.1):
    if g[0] * h[0] + g[1] * h[1] < 0:
        h = (-h[0], -h[1], -h[2])
    ang = math.atan2(abs(g[0] * h[1] - g[1] * h[0]), g[0] * h[0] + g[1] * h[1])
    return ang < ang_tol and abs(g[2] - h[2]) < off_tol


def test_jaccard_distance():
    assert jaccard_distance(0b0111, 0b0111) == 0.0
    assert jaccard_distance(0b0011, 0b1100) == 1.0
    assert jaccard_distance(0, 0) == 1.0
    assert abs(jaccard_distance(0b0111, 0b0110) - 1 / 3) < 1e-12
    assert abs(jaccard_distance(0b0111, 0b1110) - 0.5) < 1e-12


def test_example_preferences_and_merges():
    prefs = preference_sets(POINTS, HYPS, 0.1)
    assert prefs == [mask(s) for s in ([1, 6, 8], [1, 2, 6], [1, 4, 6], [1, 5, 6], [3, 4, 7], [3, 7], [3, 5, 7],
                                       [2, 8])]
    merges = []
    result = cluster(prefs, on_merge=lambda a, b, d: merges.append((list(a), list(b), round(d, 4))))
    assert merges == [([4], [5], 0.3333), ([4, 5], [6], 0.3333), ([0], [1], 0.5), ([0, 1], [2], 0.3333),
                      ([0, 1, 2], [3], 0.3333)]
    assert result == [([0, 1, 2, 3], mask([1, 6])), ([4, 5, 6], mask([3, 7])), ([7], mask([2, 8]))]
    models, _ = j_linkage(POINTS, 0.1, hypotheses=HYPS, m_min=3)
    assert [m for _, m in models] == [[0, 1, 2, 3], [4, 5, 6]]
    assert same_line(models[0][0], (0.0, 1.0, 0.0)) and same_line(models[1][0], (1.0, 0.0, -4.0))


def test_cluster_invariants():
    rng = random.Random(4)
    data = planted(rng)
    hyps = make_hypotheses(data, 150, 2.0, rng)
    prefs = preference_sets(data, hyps, 0.1)
    result = cluster(prefs)
    members = sorted(i for m, _ in result for i in m)
    assert members == list(range(len(data)))
    for m, ps in result:
        inter = prefs[m[0]]
        for i in m:
            inter &= prefs[i]
        assert ps == inter
        if len(m) > 1:
            assert ps != 0
    for a in range(len(result)):
        for b in range(a + 1, len(result)):
            assert result[a][1] & result[b][1] == 0


def test_locality_sampler():
    rng = random.Random(0)
    data = [(float(i), 0.0) for i in range(20)]
    near = 0
    for _ in range(300):
        idx = locality_sample(data, 3, 1.5, rng)
        assert len(set(idx)) == 3
        near += abs(idx[1] - idx[0]) <= 3
    assert near > 270
    assert len(make_hypotheses(data, 25, 1.0, random.Random(1))) == 25
    assert make_hypotheses(data[:1], 5, 1.0, random.Random(1)) == []


def test_planted_two_lines():
    truth = [line_through([(0, 1), (2, 2)]), line_through([(0, 8), (8, 0)])]
    for seed in range(3):
        data = planted(random.Random(seed))
        models, _ = j_linkage(data, 0.1, M=300, sigma=2.0, m_min=8, rng=random.Random(seed))
        assert len(models) == 2
        for t in truth:
            assert any(same_line(m, t) and len(mem) >= 28 for m, mem in models)


def test_tls_fit():
    pts = [(x, 2 * x + 1) for x in range(5)]
    assert same_line(fit_line_tls(pts), line_through([(0, 1), (1, 3)]), off_tol=1e-9)
    assert fit_line_tls([(1, 1)]) is None and fit_line_tls([(1, 1), (1, 1)]) is None
    assert point_line_distance((0.0, 1.0, -2.0), (5, 3)) == 1.0
