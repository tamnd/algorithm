# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/guided-filter/. The authors are listed in prov/4HSCV2.jsonl.

import random
from fractions import Fraction as F

from guided_filter import box_mean, guided_filter


def window(h, w, y, x, r):
    return [(j, i) for j in range(max(0, y - r), min(h, y + r + 1))
            for i in range(max(0, x - r), min(w, x + r + 1))]


def ridge_fit(guide, src, cells, eps):
    """Minimize sum over the window of (a I + b - p)^2 + eps a^2 by the normal equations.

    a (sum I^2 + n eps) + b sum I = sum I p and a sum I + b n = sum p, solved by Cramer's rule.
    """
    n = len(cells)
    si = sum(F(guide[j][i]) for j, i in cells)
    sp = sum(F(src[j][i]) for j, i in cells)
    sii = sum(F(guide[j][i]) ** 2 for j, i in cells)
    sip = sum(F(guide[j][i]) * src[j][i] for j, i in cells)
    m11, m12, m21, m22 = sii + n * eps, si, si, F(n)
    det = m11 * m22 - m12 * m21
    a = (sip * m22 - m12 * sp) / det
    b = (m11 * sp - m21 * sip) / det
    return a, b


def direct(guide, src, r, eps):
    """Fit every window, then average over the windows that hold each pixel."""
    h, w = len(guide), len(guide[0])
    fits = {(y, x): ridge_fit(guide, src, window(h, w, y, x, r), eps) for y in range(h) for x in range(w)}
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            ks = [k for k in fits if abs(k[0] - y) <= r and abs(k[1] - x) <= r]
            row.append(sum(fits[k][0] * guide[y][x] + fits[k][1] for k in ks) / len(ks))
        out.append(row)
    return out


def test_example_row() -> None:
    img = [[10, 12, 10, 50, 48, 50]]
    assert box_mean(img, 1) == [[11, F(32, 3), 24, 36, F(148, 3), 49]]
    q = guided_filter(img, img, 1, F(100))
    want = [10.8254, 12.1413, 13.2598, 46.7402, 47.8587, 49.1746]
    assert all(abs(float(a) - b) < 1e-4 for a, b in zip(q[0], want))


def test_edges() -> None:
    assert guided_filter([], [], 2, 1) == []
    assert guided_filter([[5]], [[9]], 3, F(1, 2)) == [[9]]
    for bad in (0, -1):
        try:
            guided_filter([[1]], [[1]], 1, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("eps must be positive")
    try:
        guided_filter([[1, 2]], [[1]], 1, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("sizes must match")


def test_exact_against_window_ridge_regression() -> None:
    rng = random.Random(2010)
    for _ in range(120):
        h, w, r = rng.randint(1, 5), rng.randint(1, 5), rng.randint(0, 2)
        eps = F(rng.randint(1, 50), rng.randint(1, 4))
        guide = [[rng.randint(0, 30) for _ in range(w)] for _ in range(h)]
        src = guide if rng.random() < 0.4 else [[rng.randint(0, 30) for _ in range(w)] for _ in range(h)]
        assert guided_filter(guide, src, r, eps) == direct(guide, src, r, eps)


def test_constant_guide_gives_box_mean_of_box_mean() -> None:
    rng = random.Random(3)
    guide = [[F(4)] * 5 for _ in range(4)]
    src = [[rng.randint(0, 9) for _ in range(5)] for _ in range(4)]
    assert guided_filter(guide, src, 1, F(1)) == box_mean(box_mean(src, 1), 1)


def test_linear_source_is_almost_kept_for_small_eps() -> None:
    rng = random.Random(11)
    guide = [[rng.randint(0, 50) for _ in range(6)] for _ in range(5)]
    src = [[3 * v + 7 for v in row] for row in guide]
    q = guided_filter(guide, src, 1, F(1, 10 ** 9))
    assert all(abs(float(a - b)) < 1e-5 for ra, rb in zip(q, src) for a, b in zip(ra, rb))


def test_float_inputs_match_exact() -> None:
    rng = random.Random(12)
    guide = [[rng.randint(0, 255) for _ in range(7)] for _ in range(6)]
    src = [[rng.randint(0, 255) for _ in range(7)] for _ in range(6)]
    exact = guided_filter(guide, src, 2, F(25))
    fl = guided_filter([[float(v) for v in row] for row in guide], [[float(v) for v in row] for row in src], 2, 25.0)
    assert all(abs(float(a) - b) < 1e-7 for ra, rb in zip(exact, fl) for a, b in zip(ra, rb))
