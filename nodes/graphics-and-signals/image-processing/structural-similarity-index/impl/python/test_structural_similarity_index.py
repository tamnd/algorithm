# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structural-similarity-index/. The authors are listed in prov/N7A0E4.jsonl.

import math
import random
from fractions import Fraction

import pytest

from structural_similarity_index import gaussian_window, ssim

K1, K2 = Fraction(1, 100), Fraction(3, 100)


def reference(x, y, data_range, w):
    """SSIM from the definitions: weighted mean, then weighted central moments per window."""
    k = len(w)
    c1, c2 = (K1 * data_range) ** 2, (K2 * data_range) ** 2
    values = []
    for i in range(len(x) - k + 1):
        for j in range(len(x[0]) - k + 1):
            cells = [(w[a] * w[b], x[i + a][j + b], y[i + a][j + b]) for a in range(k) for b in range(k)]
            mx = sum(q * p for q, p, _ in cells)
            my = sum(q * r for q, _, r in cells)
            vx = sum(q * (p - mx) ** 2 for q, p, _ in cells)
            vy = sum(q * (r - my) ** 2 for q, _, r in cells)
            cxy = sum(q * (p - mx) * (r - my) for q, p, r in cells)
            lum = (2 * mx * my + c1) / (mx * mx + my * my + c1)
            con_str = (2 * cxy + c2) / (vx + vy + c2)
            values.append(lum * con_str)
    return sum(values) / len(values), values


def random_window(rng, k):
    raw = [rng.randint(1, 5) for _ in range(k)]
    s = sum(raw)
    return [Fraction(v, s) for v in raw]


def random_pair(rng, k, data_range):
    w, h = rng.randint(k, k + 3), rng.randint(k, k + 3)
    x = [[rng.randint(0, data_range) for _ in range(w)] for _ in range(h)]
    mode = rng.randrange(3)
    if mode == 0:
        y = [[rng.randint(0, data_range) for _ in range(w)] for _ in range(h)]
    elif mode == 1:
        y = [[min(data_range, max(0, v + rng.randint(-3, 3))) for v in row] for row in x]
    else:
        y = [[data_range - v for v in row] for row in x]
    return x, y


def test_constants_of_the_paper() -> None:
    assert (K1 * 255) ** 2 == Fraction(65025, 10000)
    assert (K2 * 255) ** 2 == Fraction(585225, 10000)
    w = gaussian_window()
    assert len(w) == 11 and math.isclose(sum(w), 1.0)
    assert all(math.isclose(w[i], w[10 - i]) for i in range(11))


def test_exact_against_reference() -> None:
    rng = random.Random(1234)
    for _ in range(500):
        k = rng.randint(1, 3)
        data_range = rng.choice([1, 3, 15, 255])
        x, y = random_pair(rng, k, data_range)
        w = random_window(rng, k)
        mean, smap = ssim(x, y, data_range, w)
        ref_mean, ref_values = reference(x, y, data_range, w)
        assert mean == ref_mean
        assert [v for row in smap for v in row] == ref_values


def test_identity_symmetry_bound() -> None:
    rng = random.Random(99)
    for _ in range(500):
        k = rng.randint(1, 3)
        data_range = rng.choice([1, 15, 255])
        x, y = random_pair(rng, k, data_range)
        w = random_window(rng, k)
        assert ssim(x, x, data_range, w)[0] == 1
        a, amap = ssim(x, y, data_range, w)
        b, bmap = ssim(y, x, data_range, w)
        assert a == b and amap == bmap
        assert all(-1 < v <= 1 for row in amap for v in row)
        if x != y:
            assert a < 1


def test_default_gaussian_window_in_floats() -> None:
    rng = random.Random(7)
    w = gaussian_window()
    for _ in range(5):
        x = [[rng.randint(0, 255) for _ in range(14)] for _ in range(13)]
        y = [[min(255, max(0, v + rng.randint(-20, 20))) for v in row] for row in x]
        mean, smap = ssim(x, y)
        ref_mean, ref_values = reference(x, y, 255, w)
        assert len(smap) == 3 and len(smap[0]) == 4
        assert math.isclose(mean, ref_mean, rel_tol=1e-9, abs_tol=1e-12)
        assert math.isclose(ssim(x, x)[0], 1.0, rel_tol=1e-12)


def test_luminance_only_change() -> None:
    # a constant shift of a constant image: only the luminance term is below 1
    x = [[100] * 3 for _ in range(3)]
    y = [[110] * 3 for _ in range(3)]
    w = [Fraction(1, 3)] * 3
    c1 = (K1 * 255) ** 2
    assert ssim(x, y, 255, w)[0] == (2 * 100 * 110 + c1) / (100**2 + 110**2 + c1)


def test_errors() -> None:
    with pytest.raises(ValueError):
        ssim([[1, 2]], [[1, 2, 3]], 255, [1])
    with pytest.raises(ValueError):
        ssim([[1, 2]], [[1, 2]], 255, [Fraction(1, 2)] * 2)
