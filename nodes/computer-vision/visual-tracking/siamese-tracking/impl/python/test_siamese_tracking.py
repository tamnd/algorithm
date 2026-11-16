# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/siamese-tracking/. The authors are listed in prov/RDHCZ9.jsonl.

import math
import random

from siamese_tracking import (
    SiameseTracker,
    bias_step,
    context_side,
    features,
    label_map,
    logistic_grad,
    logistic_loss,
    map_loss,
    score,
    upsample,
    xcorr,
)


def random_image(seed, h, w):
    rng = random.Random(seed)
    return [[rng.uniform(0, 255) for _ in range(w)] for _ in range(h)]


def test_score_map_equals_every_sub_window():
    z = random_image(1, 6, 6)
    x = random_image(2, 11, 13)
    v = score(z, x, bias=0.5)
    assert (len(v), len(v[0])) == (6, 8)
    for i in range(6):
        for j in range(8):
            sub = [row[j:j + 6] for row in x[i:i + 6]]
            one = score(z, sub, bias=0.5)
            assert len(one) == 1 and len(one[0]) == 1
            assert abs(one[0][0] - v[i][j]) < 1e-6 * max(1.0, abs(v[i][j]))


def test_shift_of_the_search_image_shifts_the_score_map():
    z = random_image(3, 5, 5)
    big = random_image(4, 16, 16)
    x = [row[0:12] for row in big[0:12]]
    shifted = [row[3:15] for row in big[2:14]]  # x moved by (-3, -2)
    v, w = score(z, x), score(z, shifted)
    for i in range(len(w) - 2):
        for j in range(len(w[0]) - 3):
            assert abs(w[i][j] - v[i + 2][j + 3]) < 1e-6 * max(1.0, abs(w[i][j]))


def test_features_are_nonnegative_and_valid_size():
    img = random_image(5, 7, 9)
    f = features(img)
    assert len(f) == 4 and len(f[0]) == 5 and len(f[0][0]) == 7
    assert min(t for ch in f for row in ch for t in row) >= 0.0


def test_self_match_peaks_at_the_true_offset():
    big = random_image(6, 20, 20)
    z = [row[7:14] for row in big[5:12]]
    v = xcorr(features(z), features(big))
    best = max((t, i, j) for i, row in enumerate(v) for j, t in enumerate(row))
    assert best[1:] == (5, 7)


def test_logistic_loss_and_gradient():
    assert abs(logistic_loss(1, 0.0) - math.log(2)) < 1e-15
    assert abs(logistic_loss(1, 2.0) - logistic_loss(-1, -2.0)) < 1e-15
    assert abs(logistic_loss(1, 800.0)) < 1e-300 + 1e-12
    assert abs(logistic_loss(-1, 800.0) - 800.0) < 1e-9
    for y in (1, -1):
        for v in (-3.0, -0.2, 0.0, 0.7, 4.0):
            h = 1e-6
            num = (logistic_loss(y, v + h) - logistic_loss(y, v - h)) / (2 * h)
            assert abs(num - logistic_grad(y, v)) < 1e-6


def test_label_map_and_balanced_loss():
    y = label_map(17, 16, 8)  # positive within 2 cells of the center
    assert sum(t > 0 for row in y for t in row) == 13
    assert y[8][8] == 1 and y[8][10] == 1 and y[9][10] == -1
    zero = [[0.0] * 17 for _ in range(17)]
    assert abs(map_loss(y, zero) - math.log(2)) < 1e-12
    good = [[3.0 * t for t in row] for row in y]
    assert map_loss(y, good) < map_loss(y, zero) < map_loss(y, [[-t for t in row] for row in good])
    rng = random.Random(9)
    v = [[rng.uniform(-2, 2) for _ in range(17)] for _ in range(17)]
    b, grad = bias_step(y, v, 0.0, 0.5)
    h = 1e-6
    num = (map_loss(y, [[t + h for t in row] for row in v]) - map_loss(y, [[t - h for t in row] for row in v])) / (2 * h)
    assert abs(num - grad) < 1e-6
    assert map_loss(y, [[t + b for t in row] for row in v]) < map_loss(y, v)


def test_bicubic_upsampling_keeps_nodes_and_quadratics():
    m = [[2 * i + 3 * j + 0.5 * i * i for j in range(7)] for i in range(7)]
    u = upsample(m, 4)
    assert len(u) == 25
    assert max(abs(u[4 * a][4 * b] - m[a][b]) for a in range(7) for b in range(7)) < 1e-12
    inner = range(4, 21)  # away from the clamped border
    assert max(abs(u[a][b] - (a / 2 + 3 * b / 4 + 0.5 * (a / 4) ** 2)) for a in inner for b in inner) < 1e-9
    peak = [[0.0, 0.0, 0.0], [0.0, 1.0, 0.8], [0.0, 0.0, 0.0]]
    big = upsample(peak, 8)
    best = max((t, i, j) for i, row in enumerate(big) for j, t in enumerate(row))
    assert best[1] == 8 and 8 < best[2] < 16  # the peak moves between the nodes


def test_context_side():
    assert context_side(10, 10) == 20.0
    assert abs(context_side(8, 4) - math.sqrt(14 * 10)) < 1e-12


def blobs(seed, k, lo, hi, amp):
    rng = random.Random(seed)
    return [(rng.uniform(lo, hi), rng.uniform(lo, hi), rng.uniform(2, 4), rng.uniform(-amp, amp))
            for _ in range(k)]


def test_tracks_a_moving_target():
    n, side = 48, 10
    rng = random.Random(7)
    pix = [[rng.choice([40, 110, 180, 250]) for _ in range(side)] for _ in range(side)]
    back = blobs(8, 15, 0, n, 25)
    base = [[120 + sum(a * math.exp(-((u - x) ** 2 + (v - y) ** 2) / (2 * s * s)) for x, y, s, a in back)
             for u in range(n)] for v in range(n)]

    def frame(px, py):
        img = [row[:] for row in base]
        for v in range(n):
            for u in range(n):
                a, b = u - px, v - py  # target pixel coordinates, bilinear
                if -1 < a < side and -1 < b < side:
                    i0, j0 = math.floor(b), math.floor(a)
                    fa, fb = a - j0, b - i0
                    tot = 0.0
                    for di, wi in ((0, 1 - fb), (1, fb)):
                        for dj, wj in ((0, 1 - fa), (1, fa)):
                            ii, jj = i0 + di, j0 + dj
                            t = pix[ii][jj] if 0 <= ii < side and 0 <= jj < side else img[v][u]
                            tot += wi * wj * t
                    img[v][u] = tot
        return img

    path = [(10 + 2.3 * t, 12 + 1.6 * t) for t in range(8)]
    tracker = SiameseTracker(frame(*path[0]), (10, 12, 20, 22))
    for px, py in path[1:]:
        box = tracker.update(frame(px, py))
        cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
        assert math.hypot(cx - (px + side / 2), cy - (py + side / 2)) < 0.6
        assert 9.0 < box[2] - box[0] < 11.0


def test_scale_search_follows_a_shrinking_target():
    n, side = 48, 10
    rng = random.Random(7)
    pix = [[rng.choice([40, 110, 180, 250]) for _ in range(side)] for _ in range(side)]

    def frame(cx, cy, size):  # nearest-pixel rendering of the target, scaled about its center
        img = [[120.0] * n for _ in range(n)]
        for v in range(n):
            for u in range(n):
                a = (u - cx) / size * side + side / 2 - 0.5
                b = (v - cy) / size * side + side / 2 - 0.5
                if -0.5 <= a < side - 0.5 and -0.5 <= b < side - 0.5:
                    img[v][u] = pix[min(side - 1, int(b + 0.5))][min(side - 1, int(a + 0.5))]
        return img

    tracker = SiameseTracker(frame(20, 20, 10), (15, 15, 25, 25), scales=(1 / 1.05, 1.0, 1.05))
    widths = [10.0]
    for t in range(1, 8):
        cx, cy = 20 + 0.7 * t, 20 + 0.5 * t
        box = tracker.update(frame(cx, cy, 10 * 0.96 ** t))
        widths.append(box[2] - box[0])
        assert math.hypot((box[0] + box[2]) / 2 - (cx + 0.5), (box[1] + box[3]) / 2 - (cy + 0.5)) < 1.0
    assert all(b <= a + 1e-12 for a, b in zip(widths, widths[1:]))
    assert widths[-1] < 9.5
