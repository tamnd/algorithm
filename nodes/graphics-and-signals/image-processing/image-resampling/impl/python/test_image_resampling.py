# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/image-resampling/. The authors are listed in prov/ZHSZ9B.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from image_resampling import box, keys, resample_row, resize, tent, weights


def clamp(i, n):
    return min(max(i, 0), n - 1)


def direct(img, new_w, new_h, kern, support, antialias=True):
    """The double sum of the definition, evaluated pixel by pixel in exact fractions."""
    h, w = len(img), len(img[0])
    sx, sy = F(w, new_w), F(h, new_h)
    ax = sx if antialias and sx > 1 else F(1)
    ay = sy if antialias and sy > 1 else F(1)
    out = []
    for j in range(new_h):
        y = (j + F(1, 2)) * sy - F(1, 2)
        row = []
        for i in range(new_w):
            x = (i + F(1, 2)) * sx - F(1, 2)
            num = den = F(0)
            for v in range(math.floor(y - support * ay) - 1, math.ceil(y + support * ay) + 2):
                for u in range(math.floor(x - support * ax) - 1, math.ceil(x + support * ax) + 2):
                    wt = kern((x - u) / ax) * kern((y - v) / ay)
                    num += wt * img[clamp(v, h)][clamp(u, w)]
                    den += wt
            row.append(num / den)
        out.append(row)
    return out


def test_against_direct_sum():
    rng = random.Random(1981)
    table = [("nearest", box, F(1, 2)), ("linear", tent, F(1)), ("cubic", keys, F(2))]
    for _ in range(500):
        w, h = rng.randint(1, 5), rng.randint(1, 5)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        nw, nh = rng.randint(1, 6), rng.randint(1, 6)
        name, kern, sup = rng.choice(table)
        aa = rng.random() < 0.7
        assert resize(img, nw, nh, name, aa) == direct(img, nw, nh, kern, sup, aa)


def test_linear_and_cubic_formulas_when_enlarging():
    rng = random.Random(4)
    for _ in range(500):
        n = rng.randint(1, 7)
        m = rng.randint(n, 3 * n)
        row = [rng.randint(-50, 300) for _ in range(n)]
        lin = resample_row(row, m, "linear")
        cub = resample_row(row, m, "cubic")
        for j in range(m):
            x = (j + F(1, 2)) * F(n, m) - F(1, 2)
            i0 = math.floor(x)
            f = x - i0
            p = [row[clamp(i0 + d, n)] for d in (-1, 0, 1, 2)]
            assert lin[j] == (1 - f) * p[1] + f * p[2]
            # the Catmull-Rom form of the Keys a = -1/2 cubic
            c = (2 * p[1] + (p[2] - p[0]) * f + (2 * p[0] - 5 * p[1] + 4 * p[2] - p[3]) * f ** 2
                 + (3 * p[1] - p[0] - 3 * p[2] + p[3]) * f ** 3) / 2
            assert cub[j] == c


def test_page_examples():
    assert resample_row([0, 0, 80, 80], 8, "nearest") == [0, 0, 0, 0, 80, 80, 80, 80]
    assert resample_row([0, 0, 80, 80], 8, "linear") == [0, 0, 0, 20, 60, 80, 80, 80]
    assert resample_row([0, 0, 80, 80], 8, "cubic") == [
        0, F(-15, 8), F(-45, 8), F(65, 4), F(255, 4), F(685, 8), F(655, 8), 80]
    assert weights(8, 4, "linear")[1] == {1: F(1, 8), 2: F(3, 8), 3: F(3, 8), 4: F(1, 8)}
    stripe = [0, 100] * 6
    assert resample_row(stripe, 5, "nearest", antialias=False) == [100, 100, 0, 0, 0]
    assert [round(float(v), 2) for v in resample_row(stripe, 5, "linear", antialias=False)] == [70, 90, 50, 10, 30]
    assert [round(float(v), 2) for v in resample_row(stripe, 5, "linear")] == [38.6, 52.54, 50, 47.46, 61.4]


def test_identity_and_box_average():
    rng = random.Random(8)
    for _ in range(100):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        for k in ("nearest", "linear", "cubic"):
            assert resize(img, w, h, k) == img
        # halving with the widened box averages pairs
        row = [rng.randint(0, 255) for _ in range(2 * w)]
        assert resample_row(row, w, "nearest") == [F(row[2 * j] + row[2 * j + 1], 2) for j in range(w)]


def test_constant_image_stays_constant():
    rng = random.Random(12)
    for _ in range(200):
        w, h, c = rng.randint(1, 6), rng.randint(1, 6), rng.randint(0, 255)
        nw, nh = rng.randint(1, 9), rng.randint(1, 9)
        for k in ("nearest", "linear", "cubic"):
            for aa in (True, False):
                out = resize([[c] * w for _ in range(h)], nw, nh, k, aa)
                assert out == [[c] * nw for _ in range(nh)]


def test_errors():
    with pytest.raises(ValueError):
        resize([], 2, 2)
    with pytest.raises(ValueError):
        resize([[1, 2], [3]], 2, 2)
    with pytest.raises(ValueError):
        resample_row([1, 2], 0)
