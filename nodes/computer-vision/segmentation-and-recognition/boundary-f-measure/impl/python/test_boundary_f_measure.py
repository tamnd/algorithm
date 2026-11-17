# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-f-measure/. The authors are listed in prov/87X9C9.jsonl.

import random
from fractions import Fraction

from boundary_f_measure import (boundary_f, boundary_of, bsds_counts, max_matching, ods_ois, points, scores,
                                threshold)


def line(u, w=6, h=4):
    return [[1 if x == u else 0 for x in range(w)] for _ in range(h)]


def brute_matching_size(bpts, gpts, d):
    def best(i, used):
        if i == len(bpts):
            return 0
        top = best(i + 1, used)
        (u, v) = bpts[i]
        for j, (x, y) in enumerate(gpts):
            if j not in used and (u - x) ** 2 + (v - y) ** 2 <= d * d:
                top = max(top, 1 + best(i + 1, used | {j}))
        return top
    return best(0, frozenset())


def random_map(rng, w, h, rate):
    return [[1 if rng.random() < rate else 0 for _ in range(w)] for _ in range(h)]


def test_double_line_example():
    b = [[1 if x in (1, 3) else 0 for x in range(6)] for _ in range(4)]
    assert boundary_f(b, line(2), 1) == (Fraction(1, 2), 1, Fraction(2, 3))
    assert boundary_f(b, line(2), 0.5) == (0, 0, 0)


def test_two_humans_example():
    assert scores(*bsds_counts(line(2), [line(2), line(4)], 1)) == (1, Fraction(1, 2), Fraction(2, 3))


def test_matching_is_maximum_and_valid():
    rng = random.Random(41)
    for _ in range(60):
        b, g = random_map(rng, 5, 4, 0.3), random_map(rng, 5, 4, 0.3)
        bp, gp = points(b), points(g)
        if len(bp) > 7 or len(gp) > 7:
            continue
        d = rng.choice([0.5, 1, 1.5, 2.3])
        m = max_matching(bp, gp, d)
        assert len(set(m.values())) == len(m)
        for i, j in m.items():
            assert (bp[i][0] - gp[j][0]) ** 2 + (bp[i][1] - gp[j][1]) ** 2 <= d * d
        assert len(m) == brute_matching_size(bp, gp, d)


def test_identity_symmetry_and_shift():
    rng = random.Random(42)
    for _ in range(10):
        b, g = random_map(rng, 8, 8, 0.2), random_map(rng, 8, 8, 0.2)
        if not points(b) or not points(g):
            continue
        assert boundary_f(b, b, 1)[2] == 1
        p, r, f = boundary_f(b, g, 1.5)
        q, s, f2 = boundary_f(g, b, 1.5)
        assert (p, r, f) == (s, q, f2)
    assert boundary_f(line(3), line(2), 1)[2] == 1
    assert boundary_f(line(3), line(2), 0.99)[2] == 0


def test_larger_tolerance_never_lowers_scores():
    rng = random.Random(43)
    b, g = random_map(rng, 10, 10, 0.15), random_map(rng, 10, 10, 0.15)
    last = (0, 0)
    for d in (0, 1, 1.5, 2, 3, 5):
        p, r, _ = boundary_f(b, g, d)
        assert p >= last[0] and r >= last[1]
        last = (p, r)


def test_boundary_of_two_regions():
    labels = [[0, 0, 1, 1] for _ in range(3)]
    assert boundary_of(labels) == [[0, 1, 0, 0] for _ in range(3)]


def test_ods_and_ois_example():
    s1, s2 = [[0.9, 0.6, 0.0, 0.0]], [[0.6, 0.0, 0.0, 0.0]]
    g = [[[1, 0, 0, 0]]]
    assert bsds_counts(threshold(s1, 0.5), g, 0.5) == (1, 2, 1, 1)
    assert ods_ois([s1, s2], [g, g], [0.5, 0.7], 0.5) == (Fraction(4, 5), 0.5, 1)
    f_ods, _, f_ois = ods_ois([s1], [g], [0.5, 0.7], 0.5)
    assert f_ods == f_ois == 1


def test_ois_can_be_below_ods():
    s1, g1 = [[0, 0.9, 0.3, 0.9, 0.6, 0.3]], [[[1, 0, 1, 0, 1, 0]]]
    s2, g2 = [[0.9, 0, 0.6, 0.9, 0.6, 0.3]], [[[1, 0, 0, 1, 0, 1]]]
    assert ods_ois([s1, s2], [g1, g2], [0.3, 0.6, 0.9], 0.5) == (Fraction(5, 8), 0.3, Fraction(8, 13))


def test_empty_maps():
    z = [[0] * 4 for _ in range(4)]
    assert boundary_f(z, line(1, 4, 4), 1) == (0, 0, 0)
    assert boundary_f(line(1, 4, 4), z, 1) == (0, 0, 0)
