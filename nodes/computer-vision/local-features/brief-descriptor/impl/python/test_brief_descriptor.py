# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brief-descriptor/. The authors are listed in prov/BQH47W.jsonl.

import random

from brief_descriptor import BINOMIAL9, brief, hamming, match, popcount64, sample_pairs, smooth


def random_image(rng, w, h, hi=255):
    return [[rng.randint(0, hi) for _ in range(w)] for _ in range(h)]


def texture(rng, w, h):
    """A smooth random texture: a coarse random grid, upsampled and summed."""
    coarse = [[rng.randint(0, 255) for _ in range(w // 4 + 2)] for _ in range(h // 4 + 2)]
    return [[coarse[v // 4][u // 4] + coarse[(v + 2) // 4][(u + 2) // 4] for u in range(w)] for v in range(h)]


def test_binomial_kernel_has_variance_two():
    total = sum(BINOMIAL9)
    mean = sum(k * w for k, w in enumerate(BINOMIAL9)) / total
    var = sum((k - mean) ** 2 * w for k, w in enumerate(BINOMIAL9)) / total
    assert total == 256 and mean == 4 and var == 2


def test_smooth_matches_direct_2d_sum():
    rng = random.Random(1)
    img = random_image(rng, 14, 12)
    s = smooth(img)
    h, w = 12, 14
    for v in range(h):
        for u in range(w):
            want = 0
            for a in range(9):
                for b in range(9):
                    uu = min(max(u + b - 4, 0), w - 1)
                    vv = min(max(v + a - 4, 0), h - 1)
                    want += BINOMIAL9[a] * BINOMIAL9[b] * img[vv][uu]
            assert s[v][u] == want


def test_popcount_and_hamming_match_brute_force():
    rng = random.Random(2)
    for _ in range(500):
        x = rng.getrandbits(64)
        assert popcount64(x) == bin(x).count("1")
    for _ in range(200):
        a, b = rng.getrandbits(512), rng.getrandbits(512)
        assert hamming(a, b, 512) == bin(a ^ b).count("1")


def test_pairs_follow_the_patch_and_the_seed():
    p = sample_pairs(256, 32, seed=7)
    assert p == sample_pairs(256, 32, seed=7)
    assert len(p) == 256
    assert all(-16 <= c <= 16 for pair in p for pt in pair for c in pt)
    q = sample_pairs(512, 48, seed=3)
    coords = [c for pair in q for pt in pair for c in pt]
    mean = sum(coords) / len(coords)
    var = sum((c - mean) ** 2 for c in coords) / len(coords)
    assert abs(mean) < 1.0 and 70 < var < 115  # sigma^2 = 48^2 / 25 = 92.16


def test_descriptor_matches_direct_definition():
    rng = random.Random(3)
    img = random_image(rng, 40, 40)
    pairs = sample_pairs(128, 16, seed=1)
    d = brief(img, [(20, 20)], pairs=pairs)[0]
    j = smooth(img)
    for i, ((xu, xv), (yu, yv)) in enumerate(pairs):
        bit = 1 if j[20 + xv][20 + xu] < j[20 + yv][20 + yu] else 0
        assert (d >> i) & 1 == bit


def test_offset_and_positive_gain_give_the_same_descriptor():
    rng = random.Random(4)
    img = random_image(rng, 40, 40)
    kps = [(20, 20), (18, 23), (16, 16)]
    base = brief(img, kps, patch=32)
    for a, b in ((1, 50), (3, 0), (7, -100)):
        assert brief([[a * x + b for x in row] for row in img], kps, patch=32) == base


def test_shift_by_whole_pixels():
    rng = random.Random(5)
    img = random_image(rng, 48, 48)
    shifted = [[img[v][(u + 5) % 48] for u in range(48)] for v in range(48)]
    # Pixel (u, v) of shifted is pixel (u + 5, v) of img; stay 9 pixels from the wrap.
    for u, v in ((22, 24), (21, 26)):
        assert brief(shifted, [(u, v)])[0] == brief(img, [(u + 5, v)])[0]


def test_border_keypoints_get_none():
    rng = random.Random(6)
    img = random_image(rng, 40, 40)
    assert brief(img, [(3, 20), (20, 39)]) == [None, None]


def test_noisy_copy_matches_its_own_keypoints():
    rng = random.Random(7)
    img = texture(rng, 64, 64)
    noisy = [[x + rng.randint(-6, 6) for x in row] for row in img]
    kps = [(u, v) for u in range(18, 47, 7) for v in range(18, 47, 7)]
    d1 = brief(img, kps)
    d2 = brief(noisy, kps)
    m = match(d1, d2)
    right = sum(1 for i, (j, _) in enumerate(m) if j == i)
    assert right >= len(kps) - 2
    same = [hamming(d1[i], d2[i]) for i in range(len(kps))]
    assert max(same) < 64
