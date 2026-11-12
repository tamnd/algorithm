# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilinear-filtering/. The authors are listed in prov/85PFVB.jsonl.

import random
from fractions import Fraction as F

from bilinear_filtering import bilinear_filtering, nearest_filtering, wrap_index

TEX = [
    [(F(0),), (F(10),), (F(20),), (F(30),)],
    [(F(40),), (F(50),), (F(60),), (F(70),)],
    [(F(80),), (F(90),), (F(100),), (F(110),)],
    [(F(120),), (F(130),), (F(140),), (F(150),)],
]


def tent(t):
    return max(F(0), 1 - abs(t))


def extended(tex, i, j, mode):
    """Texel (i, j) of the infinite texture, written out without wrap_index."""
    h, w = len(tex), len(tex[0])
    if mode == "clamp":
        i, j = min(max(i, 0), w - 1), min(max(j, 0), h - 1)
    elif mode == "repeat":
        while i < 0:
            i += w
        while i >= w:
            i -= w
        while j < 0:
            j += h
        while j >= h:
            j -= h
    else:
        period_w, period_h = 2 * w, 2 * h
        while i < 0:
            i += period_w
        while i >= period_w:
            i -= period_w
        while j < 0:
            j += period_h
        while j >= period_h:
            j -= period_h
        if i >= w:
            i = period_w - 1 - i
        if j >= h:
            j = period_h - 1 - j
    return tex[j][i]


def brute(tex, u, v, mode):
    """The tent-filtered texture: sum over a wide window of tent weights times texels."""
    h, w = len(tex), len(tex[0])
    x, y = u * w, v * h
    acc = [F(0)] * len(tex[0][0])
    for j in range(-3 * h, 4 * h):
        wy = tent(y - (j + F(1, 2)))
        if wy == 0:
            continue
        for i in range(-3 * w, 4 * w):
            wx = tent(x - (i + F(1, 2)))
            if wx == 0:
                continue
            acc = [a + wx * wy * c for a, c in zip(acc, extended(tex, i, j, mode))]
    return tuple(acc)


def test_example() -> None:
    assert bilinear_filtering(TEX, F(3, 10), F(3, 5)) == (F(83),)
    assert bilinear_filtering(TEX, F(1, 20), F(5, 8), "clamp") == (F(80),)
    assert bilinear_filtering(TEX, F(1, 20), F(5, 8), "repeat") == (F(89),)
    assert bilinear_filtering(TEX, F(1, 20), F(5, 8), "mirror") == (F(80),)


def test_edges() -> None:
    one = [[(F(7), F(1))]]
    for mode in ("clamp", "repeat", "mirror"):
        assert bilinear_filtering(one, F(1, 3), F(9, 10), mode) == (F(7), F(1))
    # texel centers return the texel
    for t in range(4):
        for s in range(4):
            assert bilinear_filtering(TEX, F(2 * s + 1, 8), F(2 * t + 1, 8)) == TEX[t][s]
    try:
        wrap_index(0, 3, "border")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown mode accepted")
    assert nearest_filtering(TEX, F(3, 10), F(3, 5)) == (F(90),)


def test_against_tent_sum() -> None:
    rng = random.Random(1974)
    for _ in range(600):
        h, w = rng.randint(1, 4), rng.randint(1, 4)
        tex = [[(F(rng.randint(0, 255)), F(rng.randint(0, 9))) for _ in range(w)] for _ in range(h)]
        u = F(rng.randint(-40, 80), 40)
        v = F(rng.randint(-40, 80), 40)
        mode = rng.choice(["clamp", "repeat", "mirror"])
        assert bilinear_filtering(tex, u, v, mode) == brute(tex, u, v, mode)


def test_convex_combination_and_continuity() -> None:
    rng = random.Random(9)
    for _ in range(300):
        u, v = F(rng.randint(0, 400), 400), F(rng.randint(0, 400), 400)
        val = bilinear_filtering(TEX, u, v, "repeat")[0]
        assert 0 <= val <= 150
        # continuity across a texel boundary: a tiny step changes the value a little
        step = F(1, 10 ** 6)
        val2 = bilinear_filtering(TEX, u + step, v, "clamp")[0]
        val1 = bilinear_filtering(TEX, u, v, "clamp")[0]
        assert abs(val2 - val1) <= 4 * 150 * step * 4


def test_float_input() -> None:
    got = bilinear_filtering(TEX, 0.3, 0.6)[0]
    assert abs(got - 83.0) < 1e-9
