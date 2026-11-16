# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brisk-features/. The authors are listed in prov/7MW0CV.jsonl.

import math
import random

from brisk_features import (LONG, SHORT, brisk, describe, detect, downsample, fast_score, hamming, is_corner,
                            orientation, pattern, sample)


def blob_image(seed, n=30):
    rng = random.Random(seed)
    bl = [(rng.uniform(5, 59), rng.uniform(5, 59), rng.uniform(2, 5), rng.uniform(-90, 90)) for _ in range(n)]
    return [[int(round(120 + sum(a * math.exp(-((u - x) ** 2 + (v - y) ** 2) / (2 * r * r)) for x, y, r, a in bl)))
             for u in range(64)] for v in range(64)]


def test_pattern_and_pairs():
    pts = pattern()
    assert len(pts) == 60
    assert len(SHORT) == 512 and len(LONG) == 870
    assert len(SHORT) + len(LONG) < 60 * 59 // 2 == 1770
    radii = sorted({round(math.hypot(x, y), 9) for x, y, _ in pts})
    assert radii == [round(0.85 * r, 9) for r in (0.0, 2.9, 4.9, 7.4, 10.8)]
    for i, j in SHORT:
        assert math.dist(pts[i][:2], pts[j][:2]) < 5.85
    for i, j in LONG:
        assert math.dist(pts[i][:2], pts[j][:2]) > 8.2


def test_fast_score_is_the_largest_threshold():
    rng = random.Random(1)
    img = [[rng.choice((0, 40, 80, 120, 160, 200)) + rng.randint(0, 9) for _ in range(16)] for _ in range(16)]
    for v in range(3, 13):
        for u in range(3, 13):
            s = fast_score(img, u, v)
            for t in range(0, 220, 7):
                assert is_corner(img, u, v, t) == (t < s)
            if s > 0:
                assert is_corner(img, u, v, s - 0.5) and not is_corner(img, u, v, s)


def test_sampling_and_downsampling():
    flat = [[77] * 20 for _ in range(20)]
    assert abs(sample(flat, 9.3, 10.7, 1.4) - 77) < 1e-12
    rng = random.Random(2)
    img = [[rng.randint(0, 255) for _ in range(12)] for _ in range(12)]
    half = downsample(img, 2.0)
    for v in range(6):
        for u in range(6):
            want = (img[2 * v][2 * u] + img[2 * v][2 * u + 1] + img[2 * v + 1][2 * u] + img[2 * v + 1][2 * u + 1]) / 4
            assert abs(half[v][u] - want) < 1e-12
    third = downsample(img, 1.5)
    assert len(third) == 8
    assert abs(sum(map(sum, third)) * 2.25 - sum(map(sum, img))) < 1e-6


def test_ramp_orientation():
    ramp = [[3 * u + 2 * v for u in range(64)] for v in range(64)]
    assert abs(orientation(ramp, 32, 32, 1.0) - math.atan2(2, 3)) < math.radians(1)
    ramp = [[-u + 4 * v for u in range(64)] for v in range(64)]
    assert abs(orientation(ramp, 31.5, 30.0, 1.5) - math.atan2(4, -1)) < math.radians(1)


def test_gain_offset_and_length():
    img = blob_image(3)
    a = describe(img, 32, 31, 1.3, 0.4)
    assert a < 1 << 512
    assert describe([[2 * x for x in row] for row in img], 32, 31, 1.3, 0.4) == a
    assert hamming(describe([[x + 50 for x in row] for row in img], 32, 31, 1.3, 0.4), a) <= 3
    assert orientation([[2 * x for x in row] for row in img], 32, 31, 1.3) == orientation(img, 32, 31, 1.3)


def test_rotation_by_90_degrees():
    img = blob_image(7)
    rot = [[img[63 - u][v] for u in range(64)] for v in range(64)]
    for u, v, t in [(32, 32, 1.2), (30, 28, 1.5), (35, 33, 1.0)]:
        a1 = orientation(img, u, v, t)
        a2 = orientation(rot, 63 - v, u, t)
        diff = (a2 - a1 - math.pi / 2 + math.pi) % (2 * math.pi) - math.pi
        assert abs(diff) < math.radians(5)
        d1, d2 = describe(img, u, v, t, a1), describe(rot, 63 - v, u, t, a2)
        d3 = describe(img, u + 5, v - 4, t, orientation(img, u + 5, v - 4, t))
        assert hamming(d1, d2) < 40 < hamming(d1, d3)


def test_square_corners_are_found():
    img = [[200 if 20 <= u < 44 and 20 <= v < 44 else 30 for u in range(64)] for v in range(64)]
    kps = detect(img, threshold=20)
    for cu, cv in [(20, 20), (43, 20), (20, 43), (43, 43)]:
        assert any(abs(x - cu) <= 3 and abs(y - cv) <= 3 for x, y, _, _ in kps)
    for x, y, t, s in kps:
        assert s > 20 and 1.0 / 1.5 <= t <= 4.0
    out = brisk(img, threshold=20)
    assert len(out) == 4
    for (x, y, t, alpha), d in out:
        # The orientation points into the bright square.
        cx, cy = 31.5 - x, 31.5 - y
        diff = (alpha - math.atan2(cy, cx) + math.pi) % (2 * math.pi) - math.pi
        assert abs(diff) < math.radians(20)


def test_hamming():
    rng = random.Random(9)
    for _ in range(50):
        a, b = rng.getrandbits(512), rng.getrandbits(512)
        assert hamming(a, b) == sum(((a >> i) & 1) != ((b >> i) & 1) for i in range(512))
