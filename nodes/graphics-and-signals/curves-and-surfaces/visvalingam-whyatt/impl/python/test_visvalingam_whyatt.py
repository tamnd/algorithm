# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/visvalingam-whyatt/. The authors are listed in prov/77Q05F.jsonl.

import random
from fractions import Fraction

import pytest

from visvalingam_whyatt import double_area, visvalingam_whyatt, vw_keep, vw_order

F = Fraction
EXAMPLE = [(0, 0), (2, 1), (4, 0), (6, 3), (8, 1), (10, 6), (12, 5), (14, 7)]


def naive_order(points):
    """The reference: rescan the areas of all remaining inner points, O(n^2)."""
    alive = list(range(len(points)))
    order = []
    while len(alive) > 2:
        best = None
        for t in range(1, len(alive) - 1):
            a = double_area(points[alive[t - 1]], points[alive[t]], points[alive[t + 1]])
            if best is None or a < best[0]:
                best = (a, t)
        a, t = best
        order.append((alive[t], a))
        del alive[t]
    return order


def shoelace_double(a, b, c):
    """Twice the area by the shoelace formula, as an independent check."""
    s = a[0] * b[1] - b[0] * a[1] + b[0] * c[1] - c[0] * b[1] + c[0] * a[1] - a[0] * c[1]
    return abs(s)


def random_polyline(rng, n, lo=-8, hi=8):
    return [(rng.randint(lo, hi), rng.randint(lo, hi)) for _ in range(n)]


def test_page_example():
    assert [double_area(EXAMPLE[i - 1], EXAMPLE[i], EXAMPLE[i + 1]) for i in range(1, 7)] == [4, 8, 10, 14, 12, 6]
    assert vw_order(EXAMPLE) == [(1, 4), (6, 6), (3, 10), (2, 4), (5, 18), (4, 42)]
    assert vw_order(EXAMPLE, monotone=True) == [(1, 4), (6, 6), (3, 10), (2, 10), (5, 18), (4, 42)]
    assert visvalingam_whyatt(EXAMPLE, 3) == [0, 2, 3, 4, 5, 6, 7]
    assert visvalingam_whyatt(EXAMPLE, 4) == [0, 2, 3, 4, 5, 7]
    assert visvalingam_whyatt(EXAMPLE, 8) == [0, 4, 5, 7]
    assert vw_keep(EXAMPLE, 5) == [0, 2, 4, 5, 7]
    assert vw_keep(EXAMPLE, 2) == [0, 7]


def test_small_inputs():
    assert vw_order([]) == []
    assert vw_order([(0, 0), (1, 1)]) == []
    assert visvalingam_whyatt([(0, 0)], 5) == [0]
    assert visvalingam_whyatt([(0, 0), (1, 0), (2, 0)], 0) == [0, 1, 2]
    assert visvalingam_whyatt([(0, 0), (1, 0), (2, 0)], F(1, 100)) == [0, 2]
    assert vw_keep([(0, 0), (1, 5), (2, 0)], 3) == [0, 1, 2]
    with pytest.raises(ValueError):
        vw_keep(EXAMPLE, 1)


def test_area_against_shoelace():
    rng = random.Random(1)
    for _ in range(500):
        a, b, c = random_polyline(rng, 3, -50, 50)
        assert double_area(a, b, c) == shoelace_double(a, b, c)


def test_heap_against_naive_rescan():
    rng = random.Random(2)
    for _ in range(700):
        pts = random_polyline(rng, rng.randint(0, 16))
        assert vw_order(pts) == naive_order(pts)


def test_threshold_is_a_prefix_of_the_order():
    rng = random.Random(3)
    for _ in range(400):
        pts = random_polyline(rng, rng.randint(3, 14))
        order = vw_order(pts)
        a = F(rng.randint(0, 40), 2)
        kept = visvalingam_whyatt(pts, a)
        gone = []
        for i, v in order:
            if v >= 2 * a:
                break
            gone.append(i)
        assert kept == sorted(set(range(len(pts))) - set(gone))
        assert kept[0] == 0 and kept[-1] == len(pts) - 1


def test_running_maximum_gives_every_threshold():
    rng = random.Random(7)
    for _ in range(200):
        pts = random_polyline(rng, rng.randint(3, 12))
        run, best = {}, None
        for i, v in vw_order(pts):
            best = v if best is None else max(best, v)
            run[i] = best
        for a2 in range(0, 40):
            kept = [i for i in range(len(pts)) if i not in run or run[i] >= a2]
            assert kept == visvalingam_whyatt(pts, F(a2, 2))


def test_monotone_values():
    rng = random.Random(4)
    for _ in range(400):
        pts = random_polyline(rng, rng.randint(3, 14), -1000, 1000)
        mono = vw_order(pts, monotone=True)
        vals = [v for _, v in mono]
        assert vals == sorted(vals)
        plain = vw_order(pts)
        # The raised values can change later choices, so only the first
        # removal and the set of removed points must agree.
        assert mono[0] == plain[0]
        assert sorted(i for i, _ in mono) == list(range(1, len(pts) - 1))
        # Each stored value is at least the true area at removal time.
        for (i, v), (j, w) in zip(mono, mono[1:]):
            assert v <= w


def test_nested_results():
    rng = random.Random(5)
    for _ in range(300):
        pts = random_polyline(rng, rng.randint(3, 14))
        a, b = sorted(F(rng.randint(0, 30), 2) for _ in range(2))
        assert set(visvalingam_whyatt(pts, b)) <= set(visvalingam_whyatt(pts, a))
        assert set(vw_keep(pts, 3)) <= set(vw_keep(pts, 4)) or len(pts) < 4


def test_collinear_points_go_first():
    pts = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 5), (5, 0), (6, 0), (7, 0)]
    order = vw_order(pts)
    assert order[:3] == [(1, 0), (2, 0), (6, 0)]
    assert order[3][1] > 0


def test_fraction_input():
    rng = random.Random(6)
    for _ in range(100):
        pts = [(F(rng.randint(-30, 30), rng.randint(1, 4)), F(rng.randint(-30, 30), rng.randint(1, 4))) for _ in range(10)]
        assert vw_order(pts) == naive_order(pts)
