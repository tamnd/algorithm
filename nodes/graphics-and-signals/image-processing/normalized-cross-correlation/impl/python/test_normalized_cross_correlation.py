# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normalized-cross-correlation/. The authors are listed in prov/ZSW84C.jsonl.

import math
import random
from fractions import Fraction

import pytest

from normalized_cross_correlation import (
    best_offset,
    cross_term_direct,
    cross_term_fft,
    integral_image,
    match_ncc,
    match_ssd,
    ncc_key,
    ncc_map,
    ncc_parts,
    rect_sum,
    ssd_map,
)


def rand_image(rng, w, h, lo=0, hi=255):
    return [[rng.randint(lo, hi) for _ in range(w)] for _ in range(h)]


def crop(img, u, v, p, q):
    return [row[u:u + p] for row in img[v:v + q]]


def naive_ncc_exact(image, template, u, v):
    """The definition with means, in Fraction: returns (numerator, var_f, var_t) of the mean-centered sums."""
    q, p = len(template), len(template[0])
    n = p * q
    win = [image[v + j][u + i] for j in range(q) for i in range(p)]
    tmp = [template[j][i] for j in range(q) for i in range(p)]
    fm = Fraction(sum(win), n)
    tm = Fraction(sum(tmp), n)
    num = sum((a - fm) * (b - tm) for a, b in zip(win, tmp))
    vf = sum((a - fm) ** 2 for a in win)
    vt = sum((b - tm) ** 2 for b in tmp)
    return num, vf, vt


def naive_ssd(image, template, u, v):
    return sum((image[v + j][u + i] - template[j][i]) ** 2
               for j in range(len(template)) for i in range(len(template[0])))


def test_integral_image_rect_sums_match_direct_sums():
    rng = random.Random(1)
    img = rand_image(rng, 7, 5)
    s = integral_image(img)
    for y0 in range(6):
        for y1 in range(y0, 6):
            for x0 in range(8):
                for x1 in range(x0, 8):
                    direct = sum(img[y][x] for y in range(y0, y1) for x in range(x0, x1))
                    assert rect_sum(s, x0, y0, x1, y1) == direct


@pytest.mark.parametrize("seed", range(6))
def test_ssd_matches_direct_scan_of_every_offset(seed):
    rng = random.Random(100 + seed)
    w, h = rng.randint(4, 9), rng.randint(4, 9)
    p, q = rng.randint(1, w), rng.randint(1, h)
    img = rand_image(rng, w, h)
    tmp = rand_image(rng, p, q)
    table = ssd_map(img, tmp)
    assert len(table) == h - q + 1 and len(table[0]) == w - p + 1
    for v in range(h - q + 1):
        for u in range(w - p + 1):
            assert table[v][u] == naive_ssd(img, tmp, u, v)
    best = min((naive_ssd(img, tmp, u, v), v, u) for v in range(h - q + 1) for u in range(w - p + 1))
    assert match_ssd(img, tmp) == (best[2], best[1])


@pytest.mark.parametrize("seed", range(8))
def test_fast_ncc_parts_equal_naive_window_sums_exactly(seed):
    rng = random.Random(200 + seed)
    w, h = rng.randint(3, 8), rng.randint(3, 8)
    p, q = rng.randint(1, w), rng.randint(1, h)
    img = rand_image(rng, w, h, 0, 9)
    tmp = rand_image(rng, p, q, 0, 9)
    n = p * q
    parts = ncc_parts(img, tmp)
    for v in range(h - q + 1):
        for u in range(w - p + 1):
            num, vf, vt = parts[v][u]
            a, b, c = naive_ncc_exact(img, tmp, u, v)
            # The integer parts are n times the mean-centered sums.
            assert Fraction(num, n) == a
            assert Fraction(vf, n) == b
            assert Fraction(vt, n) == c
            if b != 0 and c != 0:
                exact_sq = a * abs(a) / (b * c)
                assert ncc_key(num, vf, vt) == exact_sq
            else:
                assert ncc_key(num, vf, vt) is None


@pytest.mark.parametrize("seed", range(6))
def test_match_ncc_equals_direct_scan(seed):
    rng = random.Random(300 + seed)
    img = rand_image(rng, 9, 8)
    p, q = 3, 4
    tmp = rand_image(rng, p, q)
    best = None
    for v in range(8 - q + 1):
        for u in range(9 - p + 1):
            a, b, c = naive_ncc_exact(img, tmp, u, v)
            if b == 0 or c == 0:
                continue
            key = a * abs(a) / (b * c)
            if best is None or key > best[0]:
                best = (key, u, v)
    assert match_ncc(img, tmp) == (best[1], best[2])


def test_planted_template_has_score_one_and_is_found():
    rng = random.Random(7)
    img = rand_image(rng, 12, 10)
    tmp = crop(img, 5, 3, 4, 3)
    parts = ncc_parts(img, tmp)
    assert ncc_key(*parts[3][5]) == 1
    assert match_ncc(img, tmp) == (5, 3)
    assert match_ssd(img, tmp) == (5, 3)
    assert ssd_map(img, tmp)[3][5] == 0


@pytest.mark.parametrize("a,b", [(2, 0), (3, -40), (Fraction(1, 3), 7), (Fraction(5, 2), Fraction(-9, 4))])
def test_ncc_invariant_under_affine_brightness(a, b):
    rng = random.Random(11)
    img = rand_image(rng, 8, 7)
    tmp = rand_image(rng, 3, 3)
    img2 = [[a * val + b for val in row] for row in img]
    k1 = [[ncc_key(*c) for c in row] for row in ncc_parts(img, tmp)]
    k2 = [[ncc_key(*c) for c in row] for row in ncc_parts(img2, tmp)]
    assert k1 == k2
    # The template can change too.
    tmp2 = [[a * val + b for val in row] for row in tmp]
    k3 = [[ncc_key(*c) for c in row] for row in ncc_parts(img2, tmp2)]
    assert k1 == k3


def test_negative_gain_flips_the_sign():
    rng = random.Random(12)
    img = rand_image(rng, 6, 6)
    tmp = rand_image(rng, 2, 3)
    img2 = [[-val + 255 for val in row] for row in img]
    k1 = [[ncc_key(*c) for c in row] for row in ncc_parts(img, tmp)]
    k2 = [[ncc_key(*c) for c in row] for row in ncc_parts(img2, tmp)]
    assert all(x == -y for r1, r2 in zip(k1, k2) for x, y in zip(r1, r2))


def test_ssd_is_not_invariant_under_brightness():
    rng = random.Random(13)
    img = rand_image(rng, 8, 8, 0, 100)
    tmp = crop(img, 2, 2, 3, 3)
    brighter = [[val + 60 for val in row] for row in img]
    assert ssd_map(brighter, tmp)[2][2] == 9 * 60 * 60


def test_scores_lie_in_minus_one_one_by_cauchy_schwarz():
    rng = random.Random(14)
    for _ in range(20):
        img = rand_image(rng, 6, 5, 0, 5)
        tmp = rand_image(rng, 3, 2, 0, 5)
        for row in ncc_parts(img, tmp):
            for num, vf, vt in row:
                assert num * num <= vf * vt
                assert vf >= 0 and vt >= 0


def test_flat_window_or_template_is_undefined():
    img = [[5, 5, 5, 1], [5, 5, 5, 2], [5, 5, 5, 3]]
    tmp = [[1, 2], [3, 4]]
    scores = ncc_map(img, tmp)
    assert scores[0][0] is None and scores[1][1] is None
    assert scores[0][2] is not None
    flat_tmp = [[4, 4], [4, 4]]
    assert all(s is None for row in ncc_map(img, flat_tmp) for s in row)


@pytest.mark.parametrize("seed", range(4))
def test_fft_cross_term_matches_direct(seed):
    rng = random.Random(400 + seed)
    w, h = rng.randint(5, 13), rng.randint(5, 11)
    p, q = rng.randint(1, w), rng.randint(1, h)
    img = rand_image(rng, w, h)
    tmp = rand_image(rng, p, q)
    d = cross_term_direct(img, tmp)
    f = cross_term_fft(img, tmp)
    for rd, rf in zip(d, f):
        for x, y in zip(rd, rf):
            assert abs(x - y) <= 1e-6 * max(1.0, abs(x))
    s1 = ncc_map(img, tmp, use_fft=False)
    s2 = ncc_map(img, tmp, use_fft=True)
    for r1, r2 in zip(s1, s2):
        for x, y in zip(r1, r2):
            assert (x is None) == (y is None)
            if x is not None:
                assert abs(x - y) < 1e-9


def test_worked_example_from_the_page():
    img = [
        [1, 2, 3, 4, 5],
        [2, 9, 2, 6, 2],
        [3, 2, 9, 3, 8],
        [4, 5, 2, 6, 1],
    ]
    tmp = [[9, 2], [2, 9]]
    parts = ncc_parts(img, tmp)
    assert parts[1][1] == (196, 196, 196)
    assert ncc_key(*parts[1][1]) == 1
    assert ssd_map(img, tmp)[1][1] == 0
    bright = [[2 * val + 10 for val in row] for row in img]
    assert ncc_key(*ncc_parts(bright, tmp)[1][1]) == 1
    assert match_ncc(bright, tmp) == (1, 1)
    sb = ssd_map(bright, tmp)
    assert best_offset(sb, False) != (1, 1)
