# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surf/. The authors are listed in prov/RH1WJP.jsonl.

import math
import random

from surf import box, describe, detect, filter_sizes, hessian_boxes, hessian_det, integral_image, nearest, orientation, surf


def random_image(rng, w, h):
    return [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]


def blobs(seed, n=25):
    rng = random.Random(seed)
    bl = [(rng.uniform(10, 54), rng.uniform(10, 54), rng.uniform(2, 5), rng.uniform(-80, 80)) for _ in range(n)]
    return [[100 + sum(a * math.exp(-((u - x) ** 2 + (v - y) ** 2) / (2 * r * r)) for x, y, r, a in bl)
             for u in range(64)] for v in range(64)]


def direct_masks(img, u, v, size):
    """The box filters from their weights, pixel by pixel, with zero padding."""
    h, w = len(img), len(img[0])
    l0, half = size // 3, (size - 1) // 2
    sxx = syy = sxy = 0
    for dv in range(-half, half + 1):
        for du in range(-half, half + 1):
            x, y = u + du, v + dv
            p = img[y][x] if 0 <= x < w and 0 <= y < h else 0
            if abs(dv) <= l0 - 1:
                sxx += p * (-2 if abs(du) <= (l0 - 1) // 2 else 1)
            if abs(du) <= l0 - 1:
                syy += p * (-2 if abs(dv) <= (l0 - 1) // 2 else 1)
            if 1 <= abs(du) <= l0 and 1 <= abs(dv) <= l0:
                sxy += p * (1 if du * dv > 0 else -1)
    a = float(size * size)
    return sxx / a, syy / a, sxy / a


def test_integral_image_box_sums():
    rng = random.Random(1)
    img = random_image(rng, 13, 9)
    ii = integral_image(img)
    for _ in range(200):
        u0, u1 = sorted(rng.randint(-3, 16) for _ in range(2))
        v0, v1 = sorted(rng.randint(-3, 12) for _ in range(2))
        want = sum(img[v][u] for v in range(max(v0, 0), min(v1, 9)) for u in range(max(u0, 0), min(u1, 13)))
        assert box(ii, u0, v0, u1, v1) == want


def test_box_filters_match_their_masks():
    rng = random.Random(2)
    img = random_image(rng, 40, 40)
    ii = integral_image(img)
    for size in (9, 15, 21, 27):
        for _ in range(6):
            u, v = rng.randint(-2, 41), rng.randint(-2, 41)
            assert hessian_boxes(ii, u, v, size) == direct_masks(img, u, v, size)


def test_filter_sizes_and_the_weight():
    assert filter_sizes(0) == [9, 15, 21, 27]
    assert filter_sizes(1) == [15, 27, 39, 51]
    assert filter_sizes(2) == [27, 51, 75, 99]
    # The weight 0.9 balances the Frobenius norms of the Gaussian and box kernels at sigma 1.2.
    s, r = 1.2, range(-4, 5)
    g = lambda x, y: math.exp(-(x * x + y * y) / (2 * s * s))
    lyy = [(y * y / s ** 4 - 1 / s ** 2) * g(x, y) for y in r for x in r]
    lxy = [(x * y / s ** 4) * g(x, y) for y in r for x in r]
    dyy = [0 if abs(x) > 2 else (-2 if abs(y) <= 1 else 1) for y in r for x in r]
    dxy = [0 if x == 0 or y == 0 or abs(x) > 3 or abs(y) > 3 else (1 if x * y > 0 else -1) for y in r for x in r]
    fro = lambda m: math.sqrt(sum(t * t for t in m))
    assert abs(fro(lxy) * fro(dyy) / (fro(lyy) * fro(dxy)) - 0.912) < 0.005


def test_transpose_keeps_the_determinant():
    rng = random.Random(3)
    img = random_image(rng, 30, 30)
    tr = [[img[u][v] for u in range(30)] for v in range(30)]
    ii, it = integral_image(img), integral_image(tr)
    for size in (9, 15, 21):
        for _ in range(10):
            u, v = rng.randint(0, 29), rng.randint(0, 29)
            assert hessian_det(ii, u, v, size) == hessian_det(it, v, u, size)


def test_bright_disk_is_detected_at_its_center():
    img = [[200 if (u - 32) ** 2 + (v - 30) ** 2 <= 25 else 20 for u in range(64)] for v in range(64)]
    kps = detect(img, threshold=1.0)
    best = min(kps, key=lambda k: (k[0] - 32) ** 2 + (k[1] - 30) ** 2)
    assert abs(best[0] - 32) <= 1 and abs(best[1] - 30) <= 1
    assert best[3] == -1  # a bright blob has a negative Laplacian
    assert 1.5 < best[2] < 4.5


def test_ramp_orientation():
    img = [[3.0 * u + 2.0 * v for u in range(64)] for v in range(64)]
    ii = integral_image(img)
    assert abs(orientation(ii, 32, 32, 2.0) - math.atan2(2.0, 3.0)) < 1e-9
    img = [[-1.0 * u + 4.0 * v for u in range(64)] for v in range(64)]
    ii = integral_image(img)
    assert abs(orientation(ii, 30, 33, 1.6) - math.atan2(4.0, -1.0)) < 1e-9


def test_descriptor_norm_offset_and_gain():
    img = blobs(4)
    ii = integral_image(img)
    d = describe(ii, 32, 32, 2.0, 0.7)
    assert len(d) == 64 and abs(sum(x * x for x in d) - 1.0) < 1e-12
    rng = random.Random(5)
    raw = random_image(rng, 64, 64)
    a = describe(integral_image(raw), 30, 31, 1.5, -1.0)
    b = describe(integral_image([[x + 40 for x in row] for row in raw]), 30, 31, 1.5, -1.0)
    c = describe(integral_image([[3 * x for x in row] for row in raw]), 30, 31, 1.5, -1.0)
    assert a == b
    assert all(abs(x - y) < 1e-12 for x, y in zip(a, c))


def test_rotation_by_90_degrees():
    img = blobs(7)
    rot = [[img[63 - u][v] for u in range(64)] for v in range(64)]
    ii, ir = integral_image(img), integral_image(rot)
    for u, v in [(32, 32), (28, 35), (36, 30), (30, 30)]:
        d1 = describe(ii, u, v, 2.0, orientation(ii, u, v, 2.0))
        # The pixel (u, v) of img is the pixel (63 - v, u) of rot.
        d2 = describe(ir, 63 - v, u, 2.0, orientation(ir, 63 - v, u, 2.0))
        d3 = describe(ii, u + 9, v - 7, 2.0, orientation(ii, u + 9, v - 7, 2.0))
        assert math.dist(d1, d2) < 0.3
        assert math.dist(d1, d2) < math.dist(d1, d3)


def test_shifted_copy_matches_itself():
    img = blobs(8)
    shifted = [[img[v - 3][u - 4] if v >= 3 and u >= 4 else 100 for u in range(64)] for v in range(64)]
    a = surf(img, threshold=5.0, octaves=1)
    b = surf(shifted, threshold=5.0, octaves=1)
    inner = [(k, d) for k, d in a if 20 <= k[0] <= 40 and 20 <= k[1] <= 40]
    assert inner
    for k, d in inner:
        j = nearest(d, [e for _, e in b])
        assert abs(b[j][0][0] - k[0] - 4) < 1e-9 and abs(b[j][0][1] - k[1] - 3) < 1e-9
