# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orb-features/. The authors are listed in prov/X00NNP.jsonl.

import math
import random

from orb_features import (CIRCLE, angle_bin, centroid_angle, correlation, describe, detect, hamming,
                          integral_image, is_fast_corner, learn_tests, orb, random_pattern, steered_patterns,
                          bit_table, window_sum)


def blob_image(seed, w=64, h=64, n=30):
    rng = random.Random(seed)
    bl = [(rng.uniform(5, w - 5), rng.uniform(5, h - 5), rng.uniform(2, 5), rng.uniform(-90, 90)) for _ in range(n)]
    return [[int(round(120 + sum(a * math.exp(-((u - x) ** 2 + (v - y) ** 2) / (2 * r * r)) for x, y, r, a in bl)))
             for u in range(w)] for v in range(h)]


def rot90(img):
    """rot[v][u] = img[63 - u][v]: the pixel (u, v) of img goes to (63 - v, u), an angle grows by pi / 2."""
    n = len(img)
    return [[img[n - 1 - u][v] for u in range(n)] for v in range(n)]


def test_fast_matches_the_definition():
    rng = random.Random(1)
    img = [[rng.choice((0, 50, 100, 150, 200)) for _ in range(20)] for _ in range(20)]
    for v in range(3, 17):
        for u in range(3, 17):
            p = img[v][u]
            s = "".join("b" if img[v + dv][u + du] > p + 30 else ("d" if img[v + dv][u + du] < p - 30 else "s")
                        for du, dv in CIRCLE)
            want = "b" * 9 in s + s or "d" * 9 in s + s
            assert is_fast_corner(img, u, v, 30) == want
    assert len(set(CIRCLE)) == 16 and all(round(math.hypot(x, y)) == 3 for x, y in CIRCLE)


def test_centroid_angle():
    ramp_u = [[100 + 3 * u for u in range(40)] for _ in range(40)]
    ramp_v = [[100 + 3 * v for _ in range(40)] for v in range(40)]
    assert centroid_angle(ramp_u, 20, 20) == 0.0
    assert abs(centroid_angle(ramp_v, 20, 20) - math.pi / 2) < 1e-15
    img = blob_image(2)
    rot = rot90(img)
    for u, v in [(30, 31), (25, 40), (40, 22)]:
        a, b = centroid_angle(img, u, v), centroid_angle(rot, 63 - v, u)
        d = (b - a - math.pi / 2 + math.pi) % (2 * math.pi) - math.pi
        assert abs(d) < 1e-12


def test_steered_patterns():
    pattern = random_pattern(256, seed=3)
    assert all(x * x + y * y <= 169 for p in pattern for x, y in p)
    tables = steered_patterns(pattern, 32)
    assert tables[0] == pattern
    for b in range(24):
        assert tables[b + 8] == [((-p[1], p[0]), (-q[1], q[0])) for p, q in tables[b]]
    for table in tables:
        assert all(abs(c) <= 13 for p, q in table for c in p + q)
    t30 = steered_patterns(pattern, 30)
    # The bin of 2 pi / 30 * 5 is 60 degrees.
    c, s = math.cos(math.pi / 3), math.sin(math.pi / 3)
    p = pattern[0][0]
    assert t30[5][0][0] == (round(c * p[0] - s * p[1]), round(s * p[0] + c * p[1]))
    assert angle_bin(2 * math.pi / 30 * 7 + 0.01, 30) == 7 and angle_bin(-0.01, 30) == 0


def test_window_sums():
    rng = random.Random(4)
    img = [[rng.randint(0, 255) for _ in range(12)] for _ in range(12)]
    ii = integral_image(img)
    for v in range(2, 10):
        for u in range(2, 10):
            assert window_sum(ii, u, v) == sum(img[y][x] for y in range(v - 2, v + 3) for x in range(u - 2, u + 3))


def test_rotation_by_90_degrees_gives_the_same_descriptor():
    img = blob_image(7)
    rot = rot90(img)
    tables = steered_patterns(random_pattern(256, seed=0), 32)
    a = orb(img, n_features=20, t=10, bins=32, tables=tables)
    b = {(k[0], k[1]): (k, d) for k, d in orb(rot, n_features=20, t=10, bins=32, tables=tables)}
    assert len(a) >= 8
    plain = []
    for k, d in a:
        k2, d2 = b[(63 - k[1], k[0])]
        assert angle_bin(k2[3], 32) == (angle_bin(k[3], 32) + 8) % 32
        assert hamming(d, d2) == 0
        ii, ir = integral_image(img), integral_image(rot)
        plain.append(hamming(describe(ii, int(k[0]), int(k[1]), tables[0]),
                             describe(ir, int(k2[0]), int(k2[1]), tables[0])))
    # Without steering, the same tests on the turned image disagree on many bits.
    assert sum(plain) / len(plain) > 40


def test_offset_gives_the_same_output():
    img = blob_image(8)
    brighter = [[x + 25 for x in row] for row in img]
    assert orb(img, n_features=15, t=10) == orb(brighter, n_features=15, t=10)


def test_detector_keeps_local_maxima_ranked():
    img = blob_image(9)
    kps = detect(img, n_features=100, t=10)
    assert kps and len(set(kps)) == len(kps)
    for u, v in kps:
        assert is_fast_corner(img, u, v, 10)
    assert len(detect(img, n_features=3, t=10)) == 3
    assert detect(img, n_features=3, t=10) == kps[:3]


def test_hamming_and_correlation():
    rng = random.Random(10)
    for _ in range(100):
        a, b = rng.getrandbits(256), rng.getrandbits(256)
        assert hamming(a, b) == sum(((a >> i) & 1) != ((b >> i) & 1) for i in range(256))
    n = 40
    for _ in range(50):
        a, b = rng.getrandbits(n), rng.getrandbits(n)
        xa = [(a >> i) & 1 for i in range(n)]
        xb = [(b >> i) & 1 for i in range(n)]
        ma, mb = sum(xa) / n, sum(xb) / n
        cov = sum((x - ma) * (y - mb) for x, y in zip(xa, xb)) / n
        sa = math.sqrt(sum((x - ma) ** 2 for x in xa) / n)
        sb = math.sqrt(sum((y - mb) ** 2 for y in xb) / n)
        assert abs(correlation(a, b, n) - cov / (sa * sb)) < 1e-12


def naive_greedy(patches, candidates, n, threshold, step):
    """The greedy search written with lists of 0 and 1."""
    m = len(patches)
    table = []
    for (px, py), (qx, qy) in candidates:
        table.append([1 if sum(p[15 + py + j][15 + px + i] for i in range(-2, 3) for j in range(-2, 3))
                      < sum(p[15 + qy + j][15 + qx + i] for i in range(-2, 3) for j in range(-2, 3)) else 0
                      for p in patches])
    means = [sum(r) / m for r in table]
    order = sorted(range(len(candidates)), key=lambda i: (abs(means[i] - 0.5), i))

    def corr(i, j):
        mi, mj = means[i], means[j]
        si, sj = math.sqrt(mi * (1 - mi)), math.sqrt(mj * (1 - mj))
        if si == 0 or sj == 0:
            return 0.0
        return (sum(x * y for x, y in zip(table[i], table[j])) / m - mi * mj) / (si * sj)

    while True:
        chosen = [order[0]]
        for i in order[1:]:
            if len(chosen) == n:
                break
            if all(abs(corr(i, j)) < threshold for j in chosen):
                chosen.append(i)
        if len(chosen) == n or threshold >= 1.0:
            return [candidates[i] for i in chosen], threshold
        threshold += step


def test_greedy_learning():
    patches = []
    for seed in range(6):
        img = blob_image(100 + seed, 48, 48, 18)
        for u, v in [(16, 16), (31, 16), (16, 31), (31, 31), (24, 24)]:
            patches.append([row[u - 15:u + 16] for row in img[v - 15:v + 16]])
    candidates = random_pattern(150, seed=11)
    chosen, thr = learn_tests(patches, candidates, n=24, threshold=0.1, step=0.05)
    assert (chosen, thr) == naive_greedy(patches, candidates, 24, 0.1, 0.05)
    assert len(chosen) == 24
    bits = bit_table(patches, chosen)
    m = len(patches)
    for i in range(len(chosen)):
        for j in range(i):
            assert abs(correlation(bits[i], bits[j], m)) < thr
