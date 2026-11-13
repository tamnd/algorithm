# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harris-corner-detector/. The authors are listed in prov/824PAC.jsonl.

import math
import random
from fractions import Fraction

import pytest

from harris_corner_detector import (
    binomial_row,
    gradients,
    harris_corners,
    harris_response,
    local_maxima,
    shi_tomasi_response,
    structure_tensor,
)


def rand_image(rng, w, h, hi=255):
    return [[rng.randint(0, hi) for _ in range(w)] for _ in range(h)]


def pix(img, x, y):
    h, w = len(img), len(img[0])
    return img[min(max(y, 0), h - 1)][min(max(x, 0), w - 1)]


def direct_tensor(img, x, y, radius):
    """The structure tensor at one pixel by a direct double sum over the window."""
    h, w = len(img), len(img[0])
    wts = binomial_row(radius)
    a = b = c = 0
    for j in range(-radius, radius + 1):
        for i in range(-radius, radius + 1):
            # The gradient field is read with the clamp rule too.
            xx = min(max(x + i, 0), w - 1)
            yy = min(max(y + j, 0), h - 1)
            gx = pix(img, xx + 1, yy) - pix(img, xx - 1, yy)
            gy = pix(img, xx, yy + 1) - pix(img, xx, yy - 1)
            wt = wts[i + radius] * wts[j + radius]
            a += wt * gx * gx
            b += wt * gy * gy
            c += wt * gx * gy
    return a, b, c


def rot90(img):
    """Counterclockwise: r[i][j] = img[j][W - 1 - i]."""
    return [list(r) for r in zip(*img)][::-1]


def test_binomial_rows():
    assert binomial_row(0) == [1]
    assert binomial_row(1) == [1, 2, 1]
    assert binomial_row(2) == [1, 4, 6, 4, 1]


@pytest.mark.parametrize("seed,radius", [(1, 1), (2, 1), (3, 2), (4, 2)])
def test_response_matches_direct_formula(seed, radius):
    rng = random.Random(seed)
    img = rand_image(rng, 7, 6)
    k = Fraction(1, 25)
    a, b, c = structure_tensor(img, radius)
    resp = harris_response(img, k, radius)
    for y in range(6):
        for x in range(7):
            da, db, dc = direct_tensor(img, x, y, radius)
            assert (a[y][x], b[y][x], c[y][x]) == (da, db, dc)
            assert resp[y][x] == da * db - dc * dc - k * (da + db) ** 2


def test_response_matches_eigenvalue_form():
    rng = random.Random(5)
    img = rand_image(rng, 8, 8)
    k = Fraction(3, 50)
    a, b, c = structure_tensor(img)
    resp = harris_response(img, k)
    st = shi_tomasi_response(img)
    for y in range(8):
        for x in range(8):
            aa, bb, cc = a[y][x], b[y][x], c[y][x]
            disc = math.sqrt(((aa - bb) / 2) ** 2 + cc * cc)
            l1, l2 = (aa + bb) / 2 + disc, (aa + bb) / 2 - disc
            assert l1 >= l2 >= -1e-9  # M is positive semidefinite
            want = l1 * l2 - float(k) * (l1 + l2) ** 2
            assert abs(float(resp[y][x]) - want) <= 1e-6 * max(1.0, abs(want))
            assert abs(st[y][x] - l2) <= 1e-9 * max(1.0, l1)


def square_image():
    img = [[0] * 12 for _ in range(12)]
    for y in range(3, 9):
        for x in range(3, 9):
            img[y][x] = 10
    return img


def test_square_corners_are_found():
    assert harris_corners(square_image()) == [(3, 3), (8, 3), (3, 8), (8, 8)]


def test_signs_corner_edge_flat():
    resp = harris_response(square_image())
    assert resp[3][3] == 520400          # corner: both eigenvalues large
    assert resp[3][5] == -57600          # edge: A = 0, B = 1200, so R = -k B^2
    assert resp[5][5] == 0               # flat inside
    assert resp[0][11] == 0              # flat outside


def test_small_l_corner_example():
    s = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 9, 9, 9], [0, 0, 9, 9, 9], [0, 0, 9, 9, 9]]
    a, b, c = structure_tensor(s)
    assert (a[2][2], b[2][2], c[2][2]) == (729, 729, 324)
    resp = harris_response(s)
    assert resp[2][2] == Fraction(8535861, 25)
    assert resp[1][4] == Fraction(-944784, 25)
    assert resp[4][4] == 0
    assert harris_corners(s) == [(2, 2)]
    # The eigenvalues at (2, 2) are 729 + 324 and 729 - 324.
    assert 1053 * 405 == 729 * 729 - 324 * 324


@pytest.mark.parametrize("seed", range(3))
def test_rotation_by_90_degrees_rotates_the_response(seed):
    rng = random.Random(30 + seed)
    img = rand_image(rng, 7, 5)
    r1 = harris_response(img)
    r2 = harris_response(rot90(img))
    assert r2 == rot90(r1)
    c1 = set(harris_corners(img))
    w = len(img[0])
    c2 = set(harris_corners(rot90(img)))
    # Pixel (x, y) moves to (y, W - 1 - x).
    assert c2 == {(y, w - 1 - x) for x, y in c1}


@pytest.mark.parametrize("c", [2, 3, Fraction(1, 2)])
def test_response_scales_with_fourth_power_of_contrast(c):
    rng = random.Random(40)
    img = rand_image(rng, 6, 6)
    r1 = harris_response(img)
    r2 = harris_response([[c * v for v in row] for row in img])
    assert all(b == c ** 4 * a for ra, rb in zip(r1, r2) for a, b in zip(ra, rb))


def test_added_constant_changes_nothing():
    rng = random.Random(41)
    img = rand_image(rng, 6, 7)
    assert harris_response(img) == harris_response([[v + 77 for v in row] for row in img])


def test_gradients_clamp_border():
    img = [[1, 4, 9]]
    gx, gy = gradients(img)
    assert gx == [[3, 8, 5]]
    assert gy == [[0, 0, 0]]


def test_local_maxima_are_strict():
    resp = [[0, 5, 5], [0, 1, 0], [9, 0, 0]]
    assert local_maxima(resp) == [(0, 2)]
