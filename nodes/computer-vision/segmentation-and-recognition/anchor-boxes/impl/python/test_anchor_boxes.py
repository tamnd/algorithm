# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anchor-boxes/. The authors are listed in prov/JNRSBB.jsonl.

import math
import random
from fractions import Fraction

from anchor_boxes import (
    anchors,
    base_shapes,
    best_iou,
    centered_iou,
    iou,
    kmeans_shapes,
    legacy_base_anchors,
    mean_best_iou,
)


def test_count_area_and_ratio():
    sizes, ratios = (128, 256, 512), (0.5, 1, 2)
    a = anchors(60, 40, 16, sizes, ratios)
    assert len(a) == 60 * 40 * 9
    for k, (w, h) in enumerate(base_shapes(sizes, ratios)):
        assert abs(w * h - sizes[k // 3] ** 2) < 1e-6
        assert abs(h / w - ratios[k % 3]) < 1e-12


def test_centers_follow_stride_and_offset():
    a = anchors(3, 2, 8, (16,), (1,), offset=0.5)
    centers = [((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) for b in a]
    assert centers == [(4.0, 4.0), (12.0, 4.0), (20.0, 4.0), (4.0, 12.0), (12.0, 12.0), (20.0, 12.0)]
    a0 = anchors(2, 1, 8, (16,), (1,), offset=0)
    assert a0[0] == (-8.0, -8.0, 8.0, 8.0)


def test_legacy_table():
    expected = [
        (-84, -40, 99, 55), (-176, -88, 191, 103), (-360, -184, 375, 199),
        (-56, -56, 71, 71), (-120, -120, 135, 135), (-248, -248, 263, 263),
        (-36, -80, 51, 95), (-80, -168, 95, 183), (-168, -344, 183, 359),
    ]
    assert legacy_base_anchors() == expected


def test_centered_same_ratio():
    # Two centered boxes of one ratio and sizes s1 <= s2 have IoU (s1 / s2)^2.
    for s1, s2 in [(32, 64), (100, 128), (7, 7)]:
        assert abs(centered_iou((s1, s1 * 2), (s2, s2 * 2)) - (s1 / s2) ** 2) < 1e-12


def test_centered_same_area_ratio_factor():
    # Same area, ratios that differ by a factor q: IoU 1 / (2 sqrt(q) - 1).
    for q in (2.0, 4.0, 9.0):
        b1 = base_shapes((100,), (1.0,))[0]
        b2 = base_shapes((100,), (q,))[0]
        assert abs(centered_iou(b1, b2) - 1 / (2 * math.sqrt(q) - 1)) < 1e-12
    assert abs(centered_iou((2, 2), (1, 4)) - Fraction(1, 3)) < 1e-12


def test_octave_sizes_cover_half():
    # Square sizes spaced by a factor 2 give every centered square between them IoU >= 1/2.
    sizes = [32, 64, 128, 256]
    for k in range(1000):
        x = 32 * 2 ** (3 * k / 999)
        best = max(centered_iou((x, x), (s, s)) for s in sizes)
        assert best >= 0.5 - 1e-12
    assert abs(max(centered_iou((32 * math.sqrt(2),) * 2, (s, s)) for s in sizes) - 0.5) < 1e-12


def test_half_stride_offset():
    # The worst center for a square box of size 32 lies half a stride from an anchor center in x and y.
    for stride, expected in [(16, Fraction(576, 1472)), (4, Fraction(900, 1148))]:
        grid = [(u * stride - 16, v * stride - 16, u * stride + 16, v * stride + 16)
                for u in range(-3, 4) for v in range(-3, 4)]
        h = stride // 2
        gt = (h - 16, h - 16, h + 16, h + 16)
        assert best_iou(gt, grid) == expected


def test_grid_contains_every_anchor_box():
    rng = random.Random(11)
    a = anchors(5, 4, 16, (32, 64), (0.5, 1, 2))
    for _ in range(20):
        g = a[rng.randrange(len(a))]
        assert abs(best_iou(g, a) - 1.0) < 1e-12


def test_kmeans_recovers_clusters():
    rng = random.Random(5)
    true = [(20.0, 40.0), (60.0, 60.0), (150.0, 75.0)]
    shapes = []
    for w, h in true:
        for _ in range(40):
            shapes.append((w * rng.uniform(0.95, 1.05), h * rng.uniform(0.95, 1.05)))
    best = None
    for seed in range(5):
        centers, _ = kmeans_shapes(shapes, 3, random.Random(seed))
        score = mean_best_iou(shapes, centers)
        if best is None or score > best[0]:
            best = (score, centers)
    score, centers = best
    assert score > 0.9
    for (w, h), (cw, ch) in zip(sorted(true), centers):
        assert abs(cw / w - 1) < 0.03 and abs(ch / h - 1) < 0.03


def test_more_clusters_do_not_hurt():
    rng = random.Random(8)
    shapes = [(rng.uniform(10, 200), rng.uniform(10, 200)) for _ in range(150)]
    s1 = mean_best_iou(shapes, kmeans_shapes(shapes, 1, random.Random(0))[0])
    s5 = mean_best_iou(shapes, kmeans_shapes(shapes, 5, random.Random(0))[0])
    assert s5 > s1


def test_iou_check_values():
    assert iou((0, 0, 2, 2), (1, 1, 3, 3)) == Fraction(1, 7)
    assert iou((0, 0, 10, 10), (5, 0, 15, 10)) == Fraction(1, 3)
