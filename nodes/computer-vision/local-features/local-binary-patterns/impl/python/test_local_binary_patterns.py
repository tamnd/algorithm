# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-binary-patterns/. The authors are listed in prov/BQGMR7.jsonl.

import math
import random

from local_binary_patterns import (
    bilinear,
    build_mapping,
    chi_square,
    lbp_codes,
    lbp_histogram,
    min_rotation,
    offsets,
    transitions,
)


def random_image(rng, w, h, hi=255):
    return [[rng.randint(0, hi) for _ in range(w)] for _ in range(h)]


def rot90(img):
    """Turn the image by 90 degrees: the offset (du, dv) goes to (dv, -du)."""
    h, w = len(img), len(img[0])
    return [[img[v][w - 1 - vv] for v in range(h)] for vv in range(w)]


def necklaces(p):
    """Number of binary necklaces of length p, by Burnside's lemma."""
    total = 0
    for d in range(1, p + 1):
        if p % d == 0:
            phi = sum(1 for k in range(1, d + 1) if math.gcd(k, d) == 1)
            total += phi * 2 ** (p // d)
    return total // p


def test_label_counts_for_p8():
    assert build_mapping(8, "u2")[1] == 59
    assert build_mapping(8, "riu2")[1] == 10
    assert build_mapping(8, "ri")[1] == 36
    assert build_mapping(8, "none")[1] == 256


def test_label_counts_general():
    for p in range(3, 13):
        assert build_mapping(p, "u2")[1] == p * (p - 1) + 3
        assert build_mapping(p, "riu2")[1] == p + 2
        assert build_mapping(p, "ri")[1] == necklaces(p)


def test_transitions_and_rotation_brute_force():
    for p in (4, 6, 8):
        for code in range(1 << p):
            bits = [(code >> i) & 1 for i in range(p)]
            u = sum(1 for i in range(p) if bits[i] != bits[i - 1])
            assert transitions(code, p) == u
            rots = []
            for s in range(p):
                b = bits[s:] + bits[:s]
                rots.append(sum(bit << i for i, bit in enumerate(b)))
            assert min_rotation(code, p) == min(rots)


def test_riu2_counts_ones_of_uniform_codes():
    table, _ = build_mapping(8, "riu2")
    assert table[0b00000000] == 0
    assert table[0b00011100] == 3
    assert table[0b11111111] == 8
    assert table[0b01010101] == 9


def test_offsets_on_axes_are_integers():
    offs = offsets(8, 1.0)
    assert offs[0] == (1.0, 0.0)
    assert offs[2] == (0.0, -1.0)
    assert offs[4] == (-1.0, 0.0)
    assert offs[6] == (0.0, 1.0)


def test_codes_match_direct_comparisons_p4():
    rng = random.Random(1)
    img = random_image(rng, 12, 10, hi=5)
    codes = lbp_codes(img, 4, 1.0)
    nbr = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    for v in range(1, 9):
        for u in range(1, 11):
            want = 0
            for p, (du, dv) in enumerate(nbr):
                if img[v + dv][u + du] >= img[v][u]:
                    want |= 1 << p
            assert codes[v - 1][u - 1] == want


def test_bilinear_is_exact_on_constant_cells_and_corners():
    img = [[7, 7], [7, 7]]
    assert bilinear(img, 0.2928932188, 0.7071067812) == 7
    img = [[0, 10], [20, 30]]
    assert bilinear(img, 1.0, 0.0) == 10
    assert abs(bilinear(img, 0.5, 0.5) - 15.0) < 1e-12


def test_monotone_change_keeps_codes_p4():
    rng = random.Random(2)
    img = random_image(rng, 16, 16, hi=40)
    out = [[x * x * x + 3 * x + 11 for x in row] for row in img]
    assert lbp_codes(img, 4, 1.0) == lbp_codes(out, 4, 1.0)


def test_gray_offset_keeps_codes_p8():
    rng = random.Random(3)
    img = random_image(rng, 16, 16)
    shifted = [[x + 37 for x in row] for row in img]
    assert lbp_codes(img, 8, 1.0) == lbp_codes(shifted, 8, 1.0)


def test_rot90_rotates_codes_and_keeps_riu2_and_ri():
    rng = random.Random(4)
    img = random_image(rng, 20, 20)
    r = rot90(img)
    for kind in ("riu2", "ri"):
        assert lbp_histogram(img, 8, 1.0, kind) == lbp_histogram(r, 8, 1.0, kind)
    # Pixel (u, v) of img goes to (v, W - 1 - u) of r; neighbor p goes to p + 2.
    a = lbp_codes(img, 8, 1.0)
    b = lbp_codes(r, 8, 1.0)
    w = 20
    mask = 255
    for v in range(1, 19):
        for u in range(1, 19):
            code = a[v - 1][u - 1]
            turned = ((code << 2) | (code >> 6)) & mask
            assert b[(w - 1 - u) - 1][v - 1] == turned


def test_histogram_total_and_chi_square():
    rng = random.Random(5)
    img = random_image(rng, 18, 14)
    h = lbp_histogram(img, 8, 2.0, "u2")
    assert len(h) == 59
    assert sum(h) == (18 - 4) * (14 - 4)
    assert chi_square(h, h) == 0.0
    assert abs(chi_square([1, 0, 3], [3, 0, 1]) - 2.0) < 1e-12


def test_texture_classes_are_separated():
    rng = random.Random(6)
    stripes = [[(255 if (u // 2) % 2 else 0) + rng.randint(0, 9) for u in range(24)] for v in range(24)]
    stripes2 = [[(255 if (u // 2) % 2 else 0) + rng.randint(0, 9) for u in range(24)] for v in range(24)]
    noise = random_image(rng, 24, 24)
    hs = lbp_histogram(stripes, 8, 1.0, "riu2")
    hs2 = lbp_histogram(stripes2, 8, 1.0, "riu2")
    hn = lbp_histogram(noise, 8, 1.0, "riu2")
    assert chi_square(hs, hs2) < chi_square(hs, hn)
