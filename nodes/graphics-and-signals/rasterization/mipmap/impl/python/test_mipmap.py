# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mipmap/. The authors are listed in prov/6V0FBJ.jsonl.

import math
import random
from fractions import Fraction as F

from mipmap import bilinear, level_of_detail, mipmap, storage, trilinear

EXAMPLE = [
    [(F(0),), (F(4),), (F(8),), (F(12),)],
    [(F(4),), (F(0),), (F(12),), (F(8),)],
    [(F(16),), (F(20),), (F(0),), (F(4),)],
    [(F(20),), (F(16),), (F(4),), (F(0),)],
]


def direct_level(tex, k):
    """Level k computed straight from the base texture: the mean of each block."""
    h, w = len(tex), len(tex[0])
    wk, hk = max(1, w >> k), max(1, h >> k)
    bw, bh = w // wk, h // hk
    out = []
    for t in range(hk):
        row = []
        for s in range(wk):
            cells = [tex[r][c] for r in range(t * bh, (t + 1) * bh) for c in range(s * bw, (s + 1) * bw)]
            row.append(tuple(sum(ch, F(0)) / len(cells) for ch in zip(*cells)))
        out.append(row)
    return out


def tent(x):
    return max(F(0), 1 - abs(x))


def tent_sum(level, u, v):
    """Bilinear lookup written as a sum of tent weights over a wide window, clamp to edge."""
    h, w = len(level), len(level[0])
    x, y = u * w, v * h
    acc = [F(0)] * len(level[0][0])
    for j in range(-2 * h - 2, 3 * h + 2):
        wy = tent(y - j - F(1, 2))
        if wy == 0:
            continue
        for i in range(-2 * w - 2, 3 * w + 2):
            wx = tent(x - i - F(1, 2))
            if wx == 0:
                continue
            texel = level[min(max(j, 0), h - 1)][min(max(i, 0), w - 1)]
            acc = [a + wx * wy * c for a, c in zip(acc, texel)]
    return tuple(acc)


def oracle_trilinear(tex, u, v, lam):
    h, w = len(tex), len(tex[0])
    top = max(w, h).bit_length() - 1
    lam = min(max(lam, F(0)), F(top))
    d = math.floor(lam)
    f = lam - d
    lo = tent_sum(direct_level(tex, d), u, v)
    if f == 0:
        return lo
    hi = tent_sum(direct_level(tex, d + 1), u, v)
    return tuple((1 - f) * p + f * q for p, q in zip(lo, hi))


def random_texture(rng, w, h):
    return [[(F(rng.randint(0, 255)), F(rng.randint(0, 3))) for _ in range(w)] for _ in range(h)]


def test_example() -> None:
    m = mipmap(EXAMPLE)
    assert [len(level) for level in m] == [4, 2, 1]
    assert m[1] == [[(F(2),), (F(10),)], [(F(18),), (F(2),)]]
    assert m[2] == [[(F(8),)]]
    assert storage(m) == 21
    u, v = F(3, 8), F(5, 8)
    assert bilinear(m[0], u, v) == (F(20),)
    assert bilinear(m[1], u, v) == (F(23, 2),)
    assert trilinear(m, u, v, F(3, 2)) == (F(39, 4),)
    assert trilinear(m, u, v, F(1, 2)) == (F(63, 4),)
    assert trilinear(m, u, v, F(-1)) == (F(20),)
    assert trilinear(m, u, v, F(5)) == (F(8),)


def test_levels_are_block_means() -> None:
    rng = random.Random(1983)
    for _ in range(500):
        w, h = 1 << rng.randint(0, 4), 1 << rng.randint(0, 4)
        tex = random_texture(rng, w, h)
        m = mipmap(tex)
        assert len(m) == max(w, h).bit_length()
        for k, level in enumerate(m):
            assert level == direct_level(tex, k)


def test_storage_bound() -> None:
    for a in range(0, 9):
        for b in range(0, 9):
            w, h = 1 << a, 1 << b
            total = sum(max(1, w >> k) * max(1, h >> k) for k in range(max(a, b) + 1))
            ratio = max(w, h) // min(w, h)
            assert 3 * total == 4 * w * h + 2 * ratio - 3
            assert total < 2 * w * h or w * h == 1
            if a == b:
                assert 3 * total == 4 * w * h - 1 and 3 * total < 4 * w * h
    rng = random.Random(4)
    tex = random_texture(rng, 8, 2)
    assert storage(mipmap(tex)) == 16 + 4 + 2 + 1


def test_trilinear_against_direct_sum() -> None:
    rng = random.Random(7)
    for _ in range(500):
        w, h = 1 << rng.randint(0, 3), 1 << rng.randint(0, 3)
        tex = random_texture(rng, w, h)
        m = mipmap(tex)
        u = F(rng.randint(-20, 60), 40)
        v = F(rng.randint(-20, 60), 40)
        lam = F(rng.randint(-8, 40), 8)
        assert trilinear(m, u, v, lam) == oracle_trilinear(tex, u, v, lam)


def test_affine_texture_and_constant_mean() -> None:
    # every level of an affine texture is the same affine function of (u, v)
    w = h = 16
    tex = [[(F(3 * s + 5 * t),) for s in range(w)] for t in range(h)]
    m = mipmap(tex)
    for k, level in enumerate(m[:-1]):
        n = len(level)
        for _ in range(20):
            x = F(random.Random(k).randint(0, 100 * (n - 1)), 100) + F(1, 2)
            u = x / n
            got = bilinear(level, u, u)[0]
            assert got == 3 * (u * w - F(1, 2)) + 5 * (u * h - F(1, 2))
    assert m[-1][0][0] == (F(3 * 15, 2) + F(5 * 15, 2),)
    # the top level is the mean of the whole texture
    rng = random.Random(11)
    tex = random_texture(rng, 8, 4)
    top = mipmap(tex)[-1][0][0]
    assert top == tuple(sum(c, F(0)) / 32 for c in zip(*[t for row in tex for t in row]))


def test_level_of_detail_and_floats() -> None:
    assert level_of_detail(4 / 64, 0, 0, 4 / 64, 64, 64) == 2.0
    assert abs(level_of_detail(1 / 64, 0, 0, 8 / 64, 64, 64) - 3.0) < 1e-12
    assert level_of_detail(0, 0, 0, 0, 8, 8) == -math.inf
    ftex = [[(float(x[0]),) for x in row] for row in EXAMPLE]
    got = trilinear(mipmap(ftex), 0.375, 0.625, 1.5)[0]
    assert abs(got - 9.75) < 1e-12
    try:
        mipmap([[(1,), (2,), (3,)]])
    except ValueError:
        pass
    else:
        raise AssertionError("a side of 3 was accepted")
