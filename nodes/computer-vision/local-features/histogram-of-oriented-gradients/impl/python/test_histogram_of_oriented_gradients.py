# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram-of-oriented-gradients/. The authors are listed in prov/DA8C98.jsonl.

import math
import random

from histogram_of_oriented_gradients import cell_histograms, gradients, hog, hog_length, l2_hys, orientation_votes


def random_image(rng, w, h):
    return [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]


def close(a, b, tol=1e-9):
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


def test_lengths():
    assert hog_length(64, 128) == 3780
    assert hog_length(64, 64) == 1764
    rng = random.Random(1)
    img = random_image(rng, 64, 64)
    assert len(hog(img)) == 1764
    img2 = random_image(rng, 32, 48)
    assert len(hog(img2)) == hog_length(32, 48) == 3 * 5 * 36


def test_orientation_votes():
    # Bin centers 10, 30, ..., 170 degrees.
    (b0, w0), (b1, w1) = orientation_votes(10.0, 9)
    assert (b0, b1) == (0, 1) and w0 == 1.0 and w1 == 0.0
    (b0, w0), (b1, w1) = orientation_votes(25.0, 9)
    assert (b0, b1) == (0, 1) and abs(w0 - 0.25) < 1e-12 and abs(w1 - 0.75) < 1e-12
    (b0, w0), (b1, w1) = orientation_votes(0.0, 9)
    assert (b0, b1) == (8, 0) and abs(w0 - 0.5) < 1e-12 and abs(w1 - 0.5) < 1e-12
    (b0, w0), (b1, w1) = orientation_votes(175.0, 9)
    assert (b0, b1) == (8, 0) and abs(w0 - 0.75) < 1e-12


def test_cells_match_direct_computation_without_spatial_voting():
    rng = random.Random(2)
    img = random_image(rng, 24, 16)
    hist = cell_histograms(img, 8, 9, spatial=False)
    for cy in range(2):
        for cx in range(3):
            want = [0.0] * 9
            for v in range(cy * 8, cy * 8 + 8):
                for u in range(cx * 8, cx * 8 + 8):
                    gu = img[v][min(u + 1, 23)] - img[v][max(u - 1, 0)]
                    gv = img[min(v + 1, 15)][u] - img[max(v - 1, 0)][u]
                    m = math.sqrt(gu * gu + gv * gv)
                    a = math.degrees(math.atan2(gv, gu))
                    if a < 0:
                        a += 180.0
                    if a >= 180.0:
                        a -= 180.0
                    # Distance to each bin center on the circle of 180 degrees.
                    for b in range(9):
                        c = 20.0 * b + 10.0
                        d = abs(a - c)
                        d = min(d, 180.0 - d)
                        if d < 20.0:
                            want[b] += m * (1.0 - d / 20.0)
            assert close(hist[cy][cx], want, 1e-9)


def test_spatial_votes_keep_the_total_inside():
    rng = random.Random(3)
    img = random_image(rng, 32, 32)
    mag, _ = gradients(img)
    hist = cell_histograms(img, 8, 9, spatial=True)
    # Pixels whose four cell centers all exist give all their weight to the cells.
    inner = sum(mag[v][u] for v in range(4, 28) for u in range(4, 28))
    total = sum(sum(sum(c) for c in row) for row in hist)
    edge = sum(mag[v][u] for v in range(32) for u in range(32)) - inner
    assert inner - 1e-6 <= total <= inner + edge + 1e-6


def test_step_edge_votes_split_between_bins_zero_and_eight():
    img = [[0] * 8 + [100] * 8 for _ in range(16)]
    hist = cell_histograms(img, 8, 9, spatial=False)
    for row in hist:
        for c in row:
            assert c[0] == c[8]
            assert all(c[b] == 0.0 for b in range(1, 8))
    assert hist[0][0][0] == 8 * 100 * 0.5


def test_offset_and_negation_give_the_same_descriptor():
    rng = random.Random(4)
    img = random_image(rng, 32, 32)
    base = hog(img)
    assert hog([[x + 40 for x in row] for row in img]) == base
    assert close(hog([[255 - x for x in row] for row in img]), base)


def test_gain_changes_little():
    rng = random.Random(5)
    img = random_image(rng, 32, 32)
    a = hog(img)
    b = hog([[3 * x for x in row] for row in img])
    assert close(a, b, 1e-6)


def test_mirror_reverses_cells_and_bins():
    rng = random.Random(6)
    img = random_image(rng, 32, 24)
    mir = [row[::-1] for row in img]
    h1 = cell_histograms(img, 8, 9)
    h2 = cell_histograms(mir, 8, 9)
    for cy in range(3):
        for cx in range(4):
            assert close(h2[cy][3 - cx], [h1[cy][cx][8 - b] for b in range(9)], 1e-9)


def test_l2_hys_clips_and_normalizes():
    v = [10.0, 0.0, 0.0, 0.0]
    out = l2_hys(v, eps=0.0)
    assert out == [1.0, 0.0, 0.0, 0.0]
    w = [5.0, 1.0, 1.0, 1.0]
    out = l2_hys(w, eps=0.0)
    assert abs(sum(x * x for x in out) - 1.0) < 1e-12
    first = l2_hys([5.0, 1.0, 1.0, 1.0], eps=0.0)
    assert first[0] > first[1]
    # The first value is clipped at 0.2 and the others are not, then all are scaled alike.
    z = l2_hys([3.0] + [1.0] * 35, eps=0.0)
    assert abs(sum(x * x for x in z) - 1.0) < 1e-12
    assert abs(z[0] / z[1] - 0.2 / (1.0 / math.sqrt(44.0))) < 1e-9
