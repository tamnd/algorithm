# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dalal-triggs-detector/. The authors are listed in prov/7BC4KB.jsonl.

import math
import random

from dalal_triggs_detector import (Model, block_grid, cell_histograms, descriptor_length, detect,
                                   dot, downscale, dual_objective, gradients, hog_descriptor,
                                   iou, l2_hys, primal_objective, scan_level, train_detector,
                                   train_linear_svm, train_with_mining)


def noise(rng, h, w, top=0.3):
    return [[rng.random() * top for _ in range(w)] for _ in range(h)]


def paste(img, x, y, w, h, v=1.0):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            img[yy][xx] = v


def close(a, b, tol=1e-9):
    return all(abs(p - q) <= tol for p, q in zip(a, b)) and len(a) == len(b)


def test_default_descriptor_length_is_3780():
    assert descriptor_length(64, 128) == 7 * 15 * 36 == 3780
    rng = random.Random(1)
    img = noise(rng, 128, 64, 1.0)
    assert len(hog_descriptor(img)) == 3780


def test_orientation_bins():
    # A ramp along y has gradient angle 90 degrees, the centre of bin 4.
    ramp_y = [[float(y) for x in range(16)] for y in range(16)]
    for row in cell_histograms(ramp_y, 8, 9):
        for h in row:
            assert h[4] > 0 and all(h[b] == 0 for b in range(9) if b != 4)
    # A ramp along x has angle 0, half way between the centres of bins 8
    # and 0 (10 and 170 degrees): the vote is split equally, with wrap-around.
    ramp_x = [[float(x) for x in range(16)] for y in range(16)]
    for row in cell_histograms(ramp_x, 8, 9):
        for h in row:
            assert abs(h[0] - h[8]) < 1e-9 and h[0] > 0 and sum(h[1:8]) == 0
    # 45 degrees: t = 45 / 20 - 0.5 = 1.75, so bin 2 gets 3 times bin 1.
    # Only the middle cell is checked: the repeated border pixels have
    # another angle, and they vote only into the outer cells.
    diag = [[float(x + y) for x in range(24)] for y in range(24)]
    h = cell_histograms(diag, 8, 9)[1][1]
    assert abs(h[2] - 3 * h[1]) < 1e-9 and h[1] > 0 and h[0] == 0 and sum(h[3:]) == 0


def reference_histograms(img, cell, bins):
    """Trilinear voting written with tent functions, pixel by cell by bin."""
    h, w = len(img), len(img[0])
    ny, nx = h // cell, w // cell
    gx, gy = gradients(img)
    width = 180.0 / bins
    out = [[[0.0] * bins for _ in range(nx)] for _ in range(ny)]
    for y in range(ny * cell):
        for x in range(nx * cell):
            mag = math.hypot(gx[y][x], gy[y][x])
            if mag == 0:
                continue
            ang = math.degrees(math.atan2(gy[y][x], gx[y][x])) % 180.0
            for cy in range(ny):
                wy = max(0.0, 1 - abs((y + 0.5) - (cy + 0.5) * cell) / cell)
                for cx in range(nx):
                    wx = max(0.0, 1 - abs((x + 0.5) - (cx + 0.5) * cell) / cell)
                    for b in range(bins):
                        d = abs(ang - (b + 0.5) * width)
                        d = min(d, 180.0 - d)
                        wb = max(0.0, 1 - d / width)
                        out[cy][cx][b] += mag * wy * wx * wb
    return out


def test_cell_histograms_match_tent_reference():
    rng = random.Random(2)
    for trial in range(3):
        img = noise(rng, 12, 16, 1.0)
        got = cell_histograms(img, 4, 9)
        ref = reference_histograms(img, 4, 9)
        for r1, r2 in zip(got, ref):
            for h1, h2 in zip(r1, r2):
                assert close(h1, h2, 1e-9)


def test_l2_hys():
    v = l2_hys([3.0, 1.0, 0.0, 0.0], eps=0.0)
    assert close(v, [math.sqrt(0.5), math.sqrt(0.5), 0.0, 0.0], 1e-12)
    rng = random.Random(3)
    for trial in range(50):
        u = [rng.random() for _ in range(36)]
        a = l2_hys(u, eps=1e-9)
        b = l2_hys([7.5 * x for x in u], eps=1e-9)
        assert close(a, b, 1e-9)
        assert abs(math.sqrt(sum(x * x for x in a)) - 1) < 1e-6
    assert l2_hys([0.0] * 36) == [0.0] * 36


def test_invariant_to_affine_intensity_change():
    rng = random.Random(4)
    img = noise(rng, 24, 16, 1.0)
    brighter = [[3.0 * p + 10.0 for p in row] for row in img]
    a, b = hog_descriptor(img, 4), hog_descriptor(brighter, 4)
    assert close(a, b, 1e-5)


def test_downscale():
    rng = random.Random(5)
    img = noise(rng, 8, 8, 1.0)
    assert downscale(img, 1.0) == img
    half = downscale(img, 2.0)
    for y in range(4):
        for x in range(4):
            m = (img[2 * y][2 * x] + img[2 * y][2 * x + 1] + img[2 * y + 1][2 * x] + img[2 * y + 1][2 * x + 1]) / 4
            assert abs(half[y][x] - m) < 1e-12


def test_svm_duality_gap():
    rng = random.Random(6)
    X = [[rng.gauss(1 if i < 15 else -1, 1.0) for _ in range(4)] for i in range(30)]
    y = [1] * 15 + [-1] * 15
    for C in (0.01, 1.0, 10.0):
        w, b, alpha = train_linear_svm(X, y, C, tol=1e-9, max_epochs=20000)
        p, d = primal_objective(w, b, X, y, C), dual_objective(alpha, X, y)
        assert d <= p + 1e-12
        assert p - d < 1e-6 * max(1.0, p)
        assert all(0 <= a <= C for a in alpha)


def test_mining_gives_the_same_svm_as_all_negatives():
    # The cache argument of Felzenszwalb et al.: once no negative outside the
    # cache violates the margin, the SVM on the cache is the SVM on the pool.
    rng = random.Random(7)
    pos = [[rng.gauss(1.0, 1.0) for _ in range(5)] for _ in range(15)]
    pool = [[rng.gauss(-1.0, 1.0) for _ in range(5)] for _ in range(120)]
    C = 0.5
    w1, b1, cache = train_with_mining(pos, pool, range(10), C, tol=1e-9)
    w2, b2, _ = train_linear_svm(pos + pool, [1] * 15 + [-1] * 120, C, tol=1e-9)
    assert len(cache) < len(pool)
    assert close(w1 + [b1], w2 + [b2], 1e-4)
    p1 = primal_objective(w1, b1, pos + pool, [1] * 15 + [-1] * 120, C)
    p2 = primal_objective(w2, b2, pos + pool, [1] * 15 + [-1] * 120, C)
    assert abs(p1 - p2) < 1e-6 * p2


def test_score_map_moves_with_a_whole_cell_shift():
    rng = random.Random(8)
    big = noise(rng, 32, 40, 1.0)
    cell = 4
    a = [row[0:36] for row in big]
    b = [row[cell:40] for row in big]
    w = [rng.uniform(-1, 1) for _ in range(descriptor_length(12, 24, cell))]
    model = Model(w, 0.25, 3, 6, cell)
    sa, sb = scan_level(a, model), scan_level(b, model)
    # Windows that keep one cell away from the left and right borders of
    # both crops see the same pixels and the same gradients.
    nx = 36 // cell
    for (by, bx), v in sb.items():
        if bx >= 1 and bx + 3 <= nx - 2:
            assert abs(v - sa[(by, bx + 1)]) < 1e-9


def make_data(rng):
    def pos_window():
        im = noise(rng, 24, 12)
        paste(im, 4 + rng.randint(-1, 1), 4 + rng.randint(-1, 1), 4, 16)
        return im

    def neg_image():
        im = noise(rng, 40, 40)
        for _ in range(2):
            paste(im, rng.randint(0, 24), rng.randint(0, 34), rng.randint(8, 16), 4)
        paste(im, rng.randint(0, 26), rng.randint(0, 6), 12, 32)  # a wide bar
        return im

    return [pos_window() for _ in range(20)], [neg_image() for _ in range(4)]


def test_detects_a_synthetic_object_at_two_scales():
    rng = random.Random(1)
    pos, neg = make_data(rng)
    model = train_detector(pos, neg, cell=4, C=1.0, n_random=40, rounds=1, seed=3)
    for trial in range(2):
        img = noise(rng, 48, 48)
        x, y = 4 * rng.randint(0, 6), 4 * rng.randint(0, 5)
        paste(img, x + 4, y + 4, 4, 16)
        found = detect(img, model)
        assert found and iou(found[0][0], (x, y, x + 12, y + 24)) > 0.5
        # Twice as large: found on the pyramid level of scale 2.
        img = noise(rng, 64, 64)
        paste(img, 16, 16, 8, 32)
        found = detect(img, model, step=2.0)
        assert found and iou(found[0][0], (8, 8, 32, 56)) > 0.5
    # Kept detections do not overlap above the NMS threshold.
    for i in range(len(found)):
        for j in range(i + 1, len(found)):
            assert iou(found[i][0], found[j][0]) <= 0.5


def test_window_scores_are_dot_products():
    rng = random.Random(9)
    img = noise(rng, 24, 12, 1.0)
    w = [rng.uniform(-1, 1) for _ in range(descriptor_length(12, 24, 4))]
    model = Model(w, -0.5, 3, 6, 4)
    s = scan_level(img, model)
    assert list(s) == [(0, 0)]
    assert abs(s[(0, 0)] - (dot(w, hog_descriptor(img, 4)) - 0.5)) < 1e-12
    assert block_grid(cell_histograms(img, 4))[0][0] == l2_hys(
        sum((cell_histograms(img, 4)[i][j] for i in (0, 1) for j in (0, 1)), []))
