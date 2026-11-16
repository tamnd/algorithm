# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/census-transform/. The authors are listed in prov/GZ7T8F.jsonl.

import random

import pytest

from census_transform import (
    census,
    census_cost_volume,
    census_disparity,
    hamming,
    popcount,
    rank,
    window_offsets,
)


def brute_census(img, r):
    """A second implementation: list the bits as characters, then parse."""
    h, w = len(img), len(img[0])
    out = []
    for v in range(h):
        row = []
        for u in range(w):
            bits = []
            for dv in range(-r, r + 1):
                for du in range(-r, r + 1):
                    if du == 0 and dv == 0:
                        continue
                    y = min(max(v + dv, 0), h - 1)
                    x = min(max(u + du, 0), w - 1)
                    bits.append("1" if img[y][x] < img[v][u] else "0")
            row.append(int("".join(bits), 2))
        out.append(row)
    return out


def random_image(rng, w, h, lo=0, hi=255):
    return [[rng.randint(lo, hi) for _ in range(w)] for _ in range(h)]


def test_worked_example():
    left = [[12, 15, 9], [20, 14, 14], [7, 30, 13]]
    right = [[10, 16, 11], [18, 14, 12], [8, 29, 15]]
    cl = census(left, 1)[1][1]
    cr = census(right, 1)[1][1]
    assert cl == 0b10100101 == 165
    assert cr == 0b10101100 == 172
    assert hamming(cl, cr) == 2
    assert rank(left, 1)[1][1] == 4


def test_matches_brute_force():
    rng = random.Random(1)
    for r in (1, 2, 3):
        img = random_image(rng, 11, 8, 0, 9)
        assert census(img, r) == brute_census(img, r)


def test_bit_count_and_constant_image():
    for r in (1, 2, 3):
        offs = window_offsets(r)
        assert len(offs) == (2 * r + 1) ** 2 - 1
        assert len(set(offs)) == len(offs)
    flat = [[7] * 6 for _ in range(5)]
    assert all(c == 0 for row in census(flat, 2) for c in row)
    with pytest.raises(ValueError):
        census(flat, 0)


def test_invariant_to_monotone_change():
    rng = random.Random(2)
    img = random_image(rng, 12, 9)
    for f in (lambda x: 3 * x + 7, lambda x: x * x, lambda x: (x // 1) + 1000):
        img2 = [[f(x) for x in row] for row in img]
        assert census(img2, 2) == census(img, 2)
    # a change that is not monotone does change the string
    img3 = [[255 - x for x in row] for row in img]
    assert census(img3, 2) != census(img, 2)


def test_shift_commutes_in_the_interior():
    rng = random.Random(3)
    img = random_image(rng, 20, 10)
    s = 3
    shifted = [[row[max(u - s, 0)] for u in range(20)] for row in img]
    r = 2
    a, b = census(img, r), census(shifted, r)
    for v in range(10):
        for u in range(s + r, 20 - r):
            assert b[v][u] == a[v][u - s]


def test_rotation_permutes_the_bits():
    rng = random.Random(4)
    h, w, r = 9, 11, 2
    img = random_image(rng, w, h)
    # out[y][x] = img[h - 1 - x][y]: a turn by 90 degrees, w rows and h columns
    rot = [[img[h - 1 - x][y] for x in range(h)] for y in range(w)]
    offs = window_offsets(r)
    n = len(offs)
    pos = {o: n - 1 - i for i, o in enumerate(offs)}
    a, b = census(img, r), census(rot, r)
    for y in range(r, w - r):
        for x in range(r, h - r):
            c = b[y][x]
            u, v = y, h - 1 - x
            for du, dv in offs:
                bit_rot = (c >> pos[(du, dv)]) & 1
                bit_img = (a[v][u] >> pos[(dv, -du)]) & 1
                assert bit_rot == bit_img


def test_hamming_and_popcount():
    assert popcount(0) == 0
    assert popcount(0b1011) == 3
    assert popcount((1 << 48) - 1) == 48
    assert hamming(0b1011, 0b0110) == 3
    rng = random.Random(5)
    for _ in range(100):
        x, y = rng.getrandbits(48), rng.getrandbits(48)
        assert hamming(x, y) == sum(((x >> i) & 1) != ((y >> i) & 1) for i in range(48))


def test_cost_volume_against_brute_force():
    rng = random.Random(6)
    left, right = random_image(rng, 10, 6), random_image(rng, 10, 6)
    D, r = 4, 1
    cv = census_cost_volume(left, right, D, r)
    tl, tr = brute_census(left, r), brute_census(right, r)
    for v in range(6):
        for u in range(10):
            for d in range(D):
                want = bin(tl[v][u] ^ tr[v][u - d]).count("1") if u >= d else 9
                assert cv[v][u][d] == want


def test_disparity_survives_a_gain_and_offset_change():
    rng = random.Random(7)
    w, h, true_d, D = 30, 12, 3, 8
    scene = random_image(rng, w + true_d, h)
    right = [[scene[v][u] for u in range(w)] for v in range(h)]
    left = [[scene[v][u - true_d] if u >= true_d else scene[v][0] for u in range(w)] for v in range(h)]
    # the right camera is brighter and has more gain: a monotone change
    right = [[2 * x + 30 for x in row] for row in right]
    disp = census_disparity(left, right, D, r=2, a=1)
    margin = D + 3
    for v in range(h):
        for u in range(margin, w - 3):
            assert disp[v][u] == true_d
