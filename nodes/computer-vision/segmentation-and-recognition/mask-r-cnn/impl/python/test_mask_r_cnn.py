# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mask-r-cnn/. The authors are listed in prov/24WQPY.jsonl.

import math
import random

from mask_r_cnn import bilinear, image_to_feature, mask_loss, paste_mask, roi_align


def tent_interp(g, x, y):
    """Bilinear interpolation written as a sum of tent functions, for points inside the grid."""
    return sum(
        g[j][i] * max(0.0, 1 - abs(x - i)) * max(0.0, 1 - abs(y - j))
        for j in range(len(g))
        for i in range(len(g[0]))
    )


def roi_pool(feat, box, p):
    """Quantized RoI max pooling, for contrast: round the box, split it into integer bins, take the max."""
    x1, y1, x2, y2 = (int(math.floor(c + 0.5)) for c in box)
    rw, rh = max(x2 - x1 + 1, 1), max(y2 - y1 + 1, 1)
    out = [[0.0] * p for _ in range(p)]
    for r in range(p):
        for c in range(p):
            ys = range(y1 + math.floor(r * rh / p), y1 + math.ceil((r + 1) * rh / p))
            xs = range(x1 + math.floor(c * rw / p), x1 + math.ceil((c + 1) * rw / p))
            out[r][c] = max(feat[y][x] for y in ys for x in xs)
    return out


def test_linear_map_example():
    feat = [[x + 4 * y for x in range(4)] for y in range(4)]
    out = roi_align(feat, (0.5, 0.5, 2.5, 2.5), 2, 2)
    assert all(abs(a - b) < 1e-12 for ra, rb in zip(out, [[5, 6], [9, 10]]) for a, b in zip(ra, rb))
    moved = roi_align(feat, (0.6, 0.5, 2.6, 2.5), 2, 2)
    assert abs(moved[0][0] - 5.1) < 1e-12


def test_bilinear_equals_tent_sum_inside_the_grid():
    rng = random.Random(21)
    g = [[rng.uniform(-1, 1) for _ in range(6)] for _ in range(5)]
    for _ in range(200):
        x, y = rng.uniform(0, 5), rng.uniform(0, 4)
        assert abs(bilinear(g, x, y) - tent_interp(g, x, y)) < 1e-12


def test_constant_and_linear_maps():
    rng = random.Random(22)
    const = [[3.5] * 8 for _ in range(7)]
    lin = [[0.3 * x - 1.7 * y + 2.0 for x in range(8)] for y in range(7)]
    for _ in range(30):
        x1, y1 = rng.uniform(0, 3), rng.uniform(0, 3)
        box = (x1, y1, x1 + rng.uniform(0.5, 4), y1 + rng.uniform(0.5, 3))
        for s in (1, 2, 3):
            out = roi_align(const, box, 3, s)
            assert all(abs(v - 3.5) < 1e-12 for row in out for v in row)
            out = roi_align(lin, box, 3, s)
            bw, bh = (box[2] - box[0]) / 3, (box[3] - box[1]) / 3
            for r in range(3):
                for c in range(3):
                    cx, cy = box[0] + (c + 0.5) * bw, box[1] + (r + 0.5) * bh
                    assert abs(out[r][c] - (0.3 * cx - 1.7 * cy + 2.0)) < 1e-12


def test_shift_by_whole_cells():
    rng = random.Random(23)
    feat = [[rng.uniform(0, 1) for _ in range(10)] for _ in range(9)]
    shifted = [[feat[y - 2][x - 3] if y >= 2 and x >= 3 else 0.0 for x in range(10)] for y in range(9)]
    box = (0.3, 0.8, 4.1, 5.2)
    a = roi_align(feat, box, 4, 2)
    b = roi_align(shifted, (box[0] + 3, box[1] + 2, box[2] + 3, box[3] + 2), 4, 2)
    assert all(abs(x - y) < 1e-12 for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_output_is_continuous_in_the_box_but_pooling_jumps():
    rng = random.Random(24)
    feat = [[rng.uniform(0, 1) for _ in range(8)] for _ in range(8)]
    box = (1.45, 1.2, 5.3, 6.1)
    nudged = (1.55, 1.2, 5.3, 6.1)
    a, b = roi_align(feat, box, 2, 2), roi_align(feat, nudged, 2, 2)
    # Each sample moves by at most 0.1 cell, and bilinear interpolation is Lipschitz with constant 2 max |f|.
    assert max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb)) <= 0.2
    pa, pb = roi_pool(feat, box, 2), roi_pool(feat, nudged, 2)
    assert pa != pb  # the rounded box jumps from x1 = 1 to x1 = 2


def test_samples_far_outside_give_zero():
    feat = [[1.0] * 4 for _ in range(4)]
    assert bilinear(feat, -1.5, 1.0) == 0.0 and bilinear(feat, 1.0, 4.5) == 0.0
    assert bilinear(feat, -0.5, 1.0) == 1.0  # between -1 and 0 the value is clamped
    out = roi_align(feat, (-4.0, 0.0, 0.0, 2.0), 2, 1)
    assert out[0][0] == 0.0 and out[0][1] == 1.0


def test_image_to_feature():
    # Pixels 0 .. 3 form cell 0 of a stride 4 map; their area is [-0.5, 3.5] and the cell center is 1.5.
    assert image_to_feature((-0.5, -0.5, 3.5, 7.5), 4) == (-0.5, -0.5, 0.5, 1.5)
    assert image_to_feature((1.5, 1.5, 1.5, 1.5), 4) == (0.0, 0.0, 0.0, 0.0)


def test_paste_example_and_full_masks():
    mask = [[0.9, 0.2], [0.8, 0.1]]
    out = paste_mask(mask, (-0.5, -0.5, 3.5, 3.5), 6, 5)
    assert out == [[1, 1, 0, 0, 0, 0]] * 4 + [[0] * 6]
    full = paste_mask([[1.0] * 28 for _ in range(28)], (1.2, 0.7, 4.9, 3.1), 7, 5)
    inside = {(u, v) for v in range(5) for u in range(7) if 1.2 <= u < 4.9 and 0.7 <= v < 3.1}
    assert {(u, v) for v in range(5) for u in range(7) if full[v][u]} == inside


def test_half_mask_fills_half_the_box():
    m = 28
    left = [[1.0 if j < m // 2 else 0.0 for j in range(m)] for _ in range(m)]
    out = paste_mask(left, (-0.5, -0.5, 15.5, 7.5), 16, 8)
    assert all(out[v] == [1] * 8 + [0] * 8 for v in range(8))


def test_mask_loss_uses_only_the_class_mask():
    rng = random.Random(25)
    m, k = 4, 3
    target = [[rng.randrange(2) for _ in range(m)] for _ in range(m)]
    logits = [[[rng.uniform(-3, 3) for _ in range(m)] for _ in range(m)] for _ in range(k)]
    base = mask_loss(logits, 1, target)
    logits[0] = [[50.0] * m for _ in range(m)]
    logits[2] = [[-50.0] * m for _ in range(m)]
    assert mask_loss(logits, 1, target) == base
    perfect = [[[40.0 if t else -40.0 for t in row] for row in target]]
    assert mask_loss(perfect, 0, target) < 1e-15
    zeros = [[[0.0] * m for _ in range(m)]]
    assert abs(mask_loss(zeros, 0, target) - math.log(2)) < 1e-15
