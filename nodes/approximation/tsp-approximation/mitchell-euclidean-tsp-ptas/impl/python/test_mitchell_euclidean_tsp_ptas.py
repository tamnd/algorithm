# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mitchell-euclidean-tsp-ptas/. The authors are listed in prov/D2DB1X.jsonl.

import itertools
import math
import random

from mitchell_euclidean_tsp_ptas import (
    bounding_box,
    components,
    guillotine_bridges,
    inner_cuts,
    is_m_guillotine,
    length,
    m_span,
    mitchell_tour,
    span_gap,
    tour_segments,
)

SEVEN = [(1, 2), (0, 5), (3, 3), (1, 0), (0, 0), (3, 4), (2, 6)]  # A to G of the page
OPT_SEVEN = [0, 4, 3, 2, 5, 6, 1]  # A E D C F G B, length 15.476


def brute_order(points):
    n = len(points)
    return min(([0, *q] for q in itertools.permutations(range(1, n))), key=lambda o: length(tour_segments(points, o)))


def test_m_span_counts_components() -> None:
    rungs = [((0.0, float(y)), (2.0, float(y))) for y in range(5)]  # five horizontal edges
    window = (0.0, 2.0, 0.0, 4.0)
    assert len(components(rungs, window, 0, 1.0)) == 5
    assert m_span(rungs, window, 0, 1.0, 1) == (0.0, 4.0)
    assert m_span(rungs, window, 0, 1.0, 2) == (1.0, 3.0)
    assert m_span(rungs, window, 0, 1.0, 3) == (2.0, 2.0)  # one point, length 0
    assert m_span(rungs, window, 0, 1.0, 4) is None
    assert span_gap(rungs, window, 0, 1.0, 2) == 2.0
    pole = rungs + [((1.0, 0.0), (1.0, 4.0))]  # an edge on the cut covers the span
    assert components(pole, window, 0, 1.0) == [(0.0, 4.0)] and span_gap(pole, window, 0, 1.0, 1) == 0.0


def test_example() -> None:
    segs = tour_segments(SEVEN, OPT_SEVEN)
    window = bounding_box(segs)
    assert window == (0, 3, 0, 6) and inner_cuts(segs, window) == [(0, 1), (1, 2)]  # only A is inside
    assert abs(span_gap(segs, window, 0, 1, 1) - 5.5) < 1e-9  # x = 1: from D up to the edge G B
    assert abs(span_gap(segs, window, 1, 2, 1) - 4 / 3) < 1e-9  # y = 2: from A to the edge D C
    assert not is_m_guillotine(segs, 1) and is_m_guillotine(segs, 2)
    bridges = guillotine_bridges(segs, 1)
    assert len(bridges) == 1 and abs(length(bridges) - 4 / 3) < 1e-9
    assert is_m_guillotine(segs + bridges, 1)
    order = mitchell_tour(SEVEN, 1)
    assert "".join("ABCDEFG"[i] for i in order) == "ACFGBDE"
    assert abs(length(tour_segments(SEVEN, order)) - 16.0433) < 1e-3
    assert abs(length(tour_segments(SEVEN, mitchell_tour(SEVEN, 2))) - 15.4760) < 1e-3


def test_pinwheel_is_not_one_guillotine() -> None:
    """Four rectangles around a square: no cut through the box is covered by edges."""
    rects = [(0, 0, 2, 1), (2, 0, 3, 2), (1, 2, 3, 3), (0, 1, 1, 3), (1, 1, 2, 2)]
    segs = []
    for x0, y0, x1, y1 in rects:
        corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        segs += [(corners[i], corners[(i + 1) % 4]) for i in range(4)]
    assert not is_m_guillotine(segs, 1)  # the classic subdivision that is not a guillotine subdivision
    assert is_m_guillotine(segs, 2)
    bridges = guillotine_bridges(segs, 1)
    assert bridges == [((1, 0.0), (1, 3))]  # one bridge of length 3 on the cut x = 1
    assert is_m_guillotine(segs + bridges, 1) and length(bridges) <= math.sqrt(2) * length(segs)


def test_conversion_gives_m_guillotine_graphs() -> None:
    rng = random.Random(1999)
    worst = 0.0
    for _ in range(60):
        n = rng.randint(4, 8)
        points = [(rng.random(), rng.random()) for _ in range(n)]
        order = list(range(n))
        rng.shuffle(order)
        segs = tour_segments(points, order)
        for m in (1, 2, 3):
            bridges = guillotine_bridges(segs, m)
            assert is_m_guillotine(segs + bridges, m)
            assert all(p[0] == q[0] or p[1] == q[1] for p, q in bridges)  # each bridge lies on a cut line
            worst = max(worst, length(bridges) / (math.sqrt(2) / m * length(segs)))
    assert worst <= 1.0  # Mitchell's bound sqrt(2) L / m holds on these seeds; measured here, not proved


def test_scheme_against_brute_force() -> None:
    rng = random.Random(2010)
    for n in (4, 5, 6, 7):
        points = [(rng.random(), rng.random()) for _ in range(n)]
        best = brute_order(points)
        opt = length(tour_segments(points, best))
        for m in (1, 2):
            order = mitchell_tour(points, m)
            assert sorted(order) == list(range(n))
            mine = tour_segments(points, order)
            value = length(mine) + length(guillotine_bridges(mine, m))
            assert value <= opt + length(guillotine_bridges(tour_segments(points, best), m)) + 1e-9
            assert opt - 1e-9 <= length(mine) <= (1 + math.sqrt(2) / m) * opt + 1e-9


def test_small_inputs() -> None:
    assert mitchell_tour([(0.0, 0.0)]) == [0]
    assert mitchell_tour([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]) == [0, 1, 2]
    square = tour_segments([(0, 0), (1, 0), (1, 1), (0, 1)], [0, 1, 2, 3])
    assert inner_cuts(square, bounding_box(square)) == [] and is_m_guillotine(square, 1)
