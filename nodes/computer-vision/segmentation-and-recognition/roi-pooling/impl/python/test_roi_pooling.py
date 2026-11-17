# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roi-pooling/. The authors are listed in prov/BAJKQQ.jsonl.

import math
import random

from roi_pooling import (
    bins,
    roi_box_cells,
    roi_pool,
    roi_pool_backward,
    roi_pool_many,
    round_half_away,
)

FEAT = [[[(3 * r + 5 * c) % 11 for c in range(8)] for r in range(6)]]
BOX = (5, 3, 26, 17)


def test_page_example():
    assert roi_box_cells(BOX, 0.25) == ((1, 1, 7, 4), (4, 7))
    assert bins(BOX, 0.25, 2, 2, 6, 8) == {
        (0, 0): (1, 3, 1, 5), (0, 1): (1, 3, 4, 8),
        (1, 0): (3, 5, 1, 5), (1, 1): (3, 5, 4, 8),
    }
    y, s = roi_pool(FEAT, BOX, 0.25, 2, 2)
    assert y == [[[10, 9], [10, 10]]]
    assert s == [[[(2, 3), (2, 5)], [(4, 4), (4, 4)]]]
    g = roi_pool_backward([[[1.0, 1.0], [1.0, 1.0]]], s, 6, 8)
    assert g[0][4][4] == 2.0 and g[0][2][3] == 1.0 and g[0][2][5] == 1.0
    assert sum(sum(row) for row in g[0]) == 4.0


def test_rounding():
    assert [round_half_away(v) for v in (0.5, 1.5, 2.5, -0.5, -1.5, 0.49)] == [1, 2, 3, -1, -2, 0]


def brute_bins(h, w, out_h, out_w):
    rows = [(math.floor(p * h / out_h), math.ceil((p + 1) * h / out_h)) for p in range(out_h)]
    cols = [(math.floor(q * w / out_w), math.ceil((q + 1) * w / out_w)) for q in range(out_w)]
    return rows, cols


def test_bins_cover_the_box():
    rng = random.Random(1)
    for _ in range(300):
        h, w = rng.randint(1, 30), rng.randint(1, 30)
        out_h, out_w = rng.randint(1, 8), rng.randint(1, 8)
        rows, cols = brute_bins(h, w, out_h, out_w)
        box = (0, 0, w - 1, h - 1)
        got = bins(box, 1, out_h, out_w, 100, 100)
        for p in range(out_h):
            for q in range(out_w):
                assert got[(p, q)] == (rows[p][0], rows[p][1], cols[q][0], cols[q][1])
        # Every row of the box is in some bin, bins are in order, and next bins share at most one row.
        assert rows[0][0] == 0 and rows[-1][1] == h
        for p in range(out_h - 1):
            assert rows[p][0] <= rows[p + 1][0] and rows[p + 1][0] <= rows[p][1] <= rows[p + 1][0] + 1
        for p in range(out_h):
            assert rows[p][1] - rows[p][0] >= 1


def test_against_brute_force_max():
    rng = random.Random(2)
    for _ in range(100):
        fh, fw = rng.randint(3, 12), rng.randint(3, 12)
        feat = [[[rng.randint(-20, 20) for _ in range(fw)] for _ in range(fh)] for _ in range(2)]
        scale = rng.choice([1.0, 0.5, 0.25, 1 / 16])
        x1, y1 = rng.uniform(-3, fw / scale), rng.uniform(-3, fh / scale)
        box = (x1, y1, x1 + rng.uniform(0, fw / scale), y1 + rng.uniform(0, fh / scale))
        out_h, out_w = rng.randint(1, 4), rng.randint(1, 4)
        y, s = roi_pool(feat, box, scale, out_h, out_w)
        grid = bins(box, scale, out_h, out_w, fh, fw)
        for c in range(2):
            for (p, q), (rs, re, cs, ce) in grid.items():
                cells = [(feat[c][r][k], r, k) for r in range(rs, re) for k in range(cs, ce)]
                if not cells:
                    assert y[c][p][q] == 0.0 and s[c][p][q] is None
                else:
                    best = max(v for v, _, _ in cells)
                    first = next((r, k) for v, r, k in cells if v == best)
                    assert y[c][p][q] == best and s[c][p][q] == first


def test_backward_matches_finite_differences():
    rng = random.Random(3)
    fh, fw = 9, 11
    for _ in range(10):
        vals = rng.sample(range(10000), fh * fw)
        feat = [[[vals[r * fw + c] / 100.0 for c in range(fw)] for r in range(fh)]]
        box = (rng.uniform(0, 16), rng.uniform(0, 16), rng.uniform(20, 40), rng.uniform(20, 32))
        dy = [[[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]]
        _, s = roi_pool(feat, box, 0.25, 3, 3)
        g = roi_pool_backward(dy, s, fh, fw)

        def loss(f):
            y, _ = roi_pool(f, box, 0.25, 3, 3)
            return sum(y[0][p][q] * dy[0][p][q] for p in range(3) for q in range(3))

        eps = 1e-4
        for r in range(fh):
            for c in range(fw):
                plus = [[row[:] for row in feat[0]]]
                minus = [[row[:] for row in feat[0]]]
                plus[0][r][c] += eps
                minus[0][r][c] -= eps
                num = (loss(plus) - loss(minus)) / (2 * eps)
                assert abs(num - g[0][r][c]) < 1e-6


def test_shift_by_whole_cells():
    # Moving the box by whole cells and the content with it gives the same output.
    rng = random.Random(4)
    base = [[rng.randint(0, 99) for _ in range(20)] for _ in range(20)]
    box = (13, 9, 50, 45)
    y0, _ = roi_pool([base], box, 0.25, 7, 7)
    shifted = [[base[(r - 2) % 20][(c - 3) % 20] for c in range(20)] for r in range(20)]
    y1, _ = roi_pool([shifted], (box[0] + 12, box[1] + 8, box[2] + 12, box[3] + 8), 0.25, 7, 7)
    assert y0 == y1


def test_quantization_hides_small_shifts():
    # A shift of less than half a cell (2 pixels at scale 1/4) can leave the output unchanged.
    moved = (BOX[0], BOX[1] - 1, BOX[2], BOX[3] - 1)
    assert roi_box_cells(moved, 0.25) == roi_box_cells(BOX, 0.25)
    y0 = roi_pool_many(FEAT, [BOX, moved], 0.25, 2, 2)
    assert y0[0] == y0[1]


def test_empty_bins_and_outside_box():
    y, s = roi_pool(FEAT, (100, 100, 120, 120), 0.25, 2, 2)
    assert y == [[[0.0, 0.0], [0.0, 0.0]]] and s == [[[None, None], [None, None]]]
    # A box of one cell with a 2 x 2 output: every bin is that cell.
    y, _ = roi_pool(FEAT, (8, 8, 8, 8), 0.25, 2, 2)
    assert y == [[[FEAT[0][2][2]] * 2] * 2]
