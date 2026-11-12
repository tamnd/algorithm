# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ramer-douglas-peucker/. The authors are listed in prov/81WHGP.jsonl.

import random
from fractions import Fraction

import pytest

from ramer_douglas_peucker import (
    ramer_douglas_peucker,
    rdp_indices,
    segment_distance_squared,
)

F = Fraction

EXAMPLE = [(0, 0), (2, 1), (4, 0), (6, 3), (8, 1), (10, 6), (12, 5), (14, 7)]


def naive_rdp(points, epsilon):
    """The reference: the recursive form of the 1972 and 1973 papers."""
    n = len(points)
    if n <= 2:
        return list(range(n))

    def rec(i, j):
        best, k = -1, -1
        for m in range(i + 1, j):
            d = segment_distance_squared(points[m], points[i], points[j])
            if d > best:
                best, k = d, m
        if k < 0 or best <= epsilon * epsilon:
            return [i]
        return rec(i, k) + rec(k, j)

    return rec(0, n - 1) + [n - 1]


def brute_segment_distance_squared(p, a, b):
    """Minimize the squared distance over the parameter by exact algebra."""
    ab = [y - x for x, y in zip(a, b)]
    den = sum(c * c for c in ab)
    if den == 0:
        return sum((x - y) ** 2 for x, y in zip(p, a))
    t = F(sum((x - y) * c for x, y, c in zip(p, a, ab)), den)
    t = min(max(t, F(0)), F(1))
    q = [x + t * c for x, c in zip(a, ab)]
    return sum((x - y) ** 2 for x, y in zip(p, q))


def check_tolerance(points, epsilon, kept):
    """Every removed point lies within epsilon of the output segment over it."""
    assert kept[0] == 0 and kept[-1] == len(points) - 1
    assert kept == sorted(set(kept))
    for a, b in zip(kept, kept[1:]):
        for m in range(a + 1, b):
            d = segment_distance_squared(points[m], points[a], points[b])
            assert d <= F(epsilon) ** 2


def random_polyline(rng, n, d=2, lo=-6, hi=6):
    return [tuple(rng.randint(lo, hi) for _ in range(d)) for _ in range(n)]


def test_page_example():
    assert rdp_indices(EXAMPLE, 2) == [0, 3, 4, 5, 7]
    assert ramer_douglas_peucker(EXAMPLE, 2) == [(0, 0), (6, 3), (8, 1), (10, 6), (14, 7)]
    assert rdp_indices(EXAMPLE, 3) == [0, 7]
    assert rdp_indices(EXAMPLE, 1) == [0, 2, 3, 4, 5, 6, 7]
    assert segment_distance_squared((8, 1), (0, 0), (14, 7)) == F(36, 5)
    assert segment_distance_squared((6, 3), (0, 0), (8, 1)) == F(324, 65)
    assert segment_distance_squared((10, 6), (8, 1), (14, 7)) == F(9, 2)


def test_small_inputs():
    assert rdp_indices([], 1) == []
    assert rdp_indices([(1, 2)], 1) == [0]
    assert rdp_indices([(1, 2), (3, 4)], 0) == [0, 1]
    assert rdp_indices([(0, 0), (1, 0), (2, 0), (3, 0)], 0) == [0, 3]
    with pytest.raises(ValueError):
        rdp_indices([(0, 0), (1, 1), (2, 0)], -1)


def test_segment_not_line():
    # (5, 0) lies on the line through the ends but 5 away from the segment.
    pts = [(0, 0), (5, 0), (-10, 0)]
    assert rdp_indices(pts, 1) == [0, 1, 2]
    assert segment_distance_squared((5, 0), (0, 0), (-10, 0)) == 25


def test_closed_polyline():
    square = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
    kept = rdp_indices(square, 1)
    # The chord of a closed polyline is one point: the far corner splits first.
    assert kept == [0, 1, 2, 3, 4]
    check_tolerance(square, 1, kept)


def test_segment_distance_against_brute():
    rng = random.Random(1)
    for _ in range(500):
        d = rng.randint(1, 3)
        p, a, b = random_polyline(rng, 3, d)
        assert segment_distance_squared(p, a, b) == brute_segment_distance_squared(p, a, b)


def test_random_against_naive_and_tolerance():
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randint(0, 14)
        d = rng.choice([2, 2, 3])
        pts = random_polyline(rng, n, d)
        eps = rng.choice([0, F(1, 2), 1, F(3, 2), 2, 3, 5])
        kept = rdp_indices(pts, eps)
        assert kept == naive_rdp(pts, eps)
        if n:
            check_tolerance(pts, eps, kept)


def test_fraction_coordinates():
    rng = random.Random(3)
    for _ in range(80):
        pts = [(F(rng.randint(-20, 20), rng.randint(1, 5)), F(rng.randint(-20, 20), rng.randint(1, 5))) for _ in range(10)]
        eps = F(rng.randint(0, 8), 3)
        kept = rdp_indices(pts, eps)
        assert kept == naive_rdp(pts, eps)
        check_tolerance(pts, eps, kept)


def test_monotone_in_epsilon_for_two_spans():
    # A larger tolerance never keeps a point of the first split when the
    # smaller one removes all inner points.
    rng = random.Random(11)
    for _ in range(200):
        pts = random_polyline(rng, 9)
        if rdp_indices(pts, 2) == [0, 8]:
            assert rdp_indices(pts, 3) == [0, 8]


def test_quadratic_input():
    # P_k = (k, 1000^k): every split is at j - 1, so all points are kept.
    pts = [(k, 1000 ** k) for k in range(20)]
    assert rdp_indices(pts, 0) == list(range(20))


def test_floats():
    pts = [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 5.0), (4.0, 6.0), (5.0, 7.0)]
    assert rdp_indices(pts, 0.5) == [0, 2, 3, 5]
