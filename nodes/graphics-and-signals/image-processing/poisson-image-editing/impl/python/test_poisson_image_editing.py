# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/poisson-image-editing/. The authors are listed in prov/9JM0B6.jsonl.

import random
from fractions import Fraction as F

import pytest

from poisson_image_editing import build_system, check_region, poisson_edit

T = [[10, 10, 10, 10], [10, 50, 50, 30], [10, 50, 50, 30], [30, 30, 30, 30]]
G = [[0, 0, 0, 0], [0, 9, 3, 0], [0, 3, 9, 0], [0, 0, 0, 0]]
M = [[False] * 4, [False, True, True, False], [False, True, True, False], [False] * 4]


def exact_solve(t, g, mask, mixed=False):
    """Write the discrete Poisson system as a dense matrix and solve it by Gaussian elimination in Fractions."""
    h, w = len(t), len(t[0])
    tt = [[F(v) for v in r] for r in t]
    gg = [[F(v) for v in r] for r in g]
    pix = [(x, y) for y in range(h) for x in range(w) if mask[y][x]]
    idx = {p: i for i, p in enumerate(pix)}
    m = len(pix)
    a = [[F(0)] * (m + 1) for _ in range(m)]
    for i, (x, y) in enumerate(pix):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            qx, qy = x + dx, y + dy
            if not (0 <= qx < w and 0 <= qy < h):
                continue
            a[i][i] += 1
            v = gg[y][x] - gg[qy][qx]
            if mixed and abs(tt[y][x] - tt[qy][qx]) > abs(v):
                v = tt[y][x] - tt[qy][qx]
            a[i][m] += v
            if mask[qy][qx]:
                a[i][idx[(qx, qy)]] -= 1
            else:
                a[i][m] += tt[qy][qx]
    for c in range(m):
        piv = next(r for r in range(c, m) if a[r][c] != 0)
        a[c], a[piv] = a[piv], a[c]
        for r in range(m):
            if r != c and a[r][c] != 0:
                k = a[r][c] / a[c][c]
                a[r] = [u - k * v for u, v in zip(a[r], a[c])]
    out = [list(r) for r in tt]
    for i, (x, y) in enumerate(pix):
        out[y][x] = a[i][m] / a[i][i]
    return out


def random_case(rng):
    h, w = rng.randint(1, 5), rng.randint(1, 5)
    t = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
    g = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
    mask = [[rng.random() < 0.5 for _ in range(w)] for _ in range(h)]
    return t, g, mask


def valid(mask):
    try:
        check_region(mask)
        return True
    except ValueError:
        return False


def test_page_example():
    ex = exact_solve(T, G, M)
    assert [ex[1][1], ex[1][2], ex[2][1], ex[2][2]] == [24, 23, 23, 34]
    first = poisson_edit(T, G, M, max_sweeps=1, tol=0)
    assert [first[1][1], first[1][2], first[2][1], first[2][2]] == [37.5, 30.375, 30.375, 37.6875]
    f = poisson_edit(T, G, M)
    for y in range(4):
        assert f[y] == pytest.approx([float(v) for v in ex[y]], abs=1e-8)


def test_against_exact_solve():
    rng = random.Random(2003)
    done = 0
    while done < 500:
        t, g, mask = random_case(rng)
        if not valid(mask):
            continue
        mixed = rng.random() < 0.3
        omega = rng.choice([1.0, 1.5, 1.8])
        ex = exact_solve(t, g, mask, mixed)
        f = poisson_edit(t, g, mask, omega=omega, tol=1e-12, mixed=mixed)
        for y in range(len(t)):
            for x in range(len(t[0])):
                if mask[y][x]:
                    assert abs(f[y][x] - ex[y][x]) <= 1e-7
                else:
                    assert f[y][x] == t[y][x]
        done += 1


def test_invariances():
    rng = random.Random(9)
    done = 0
    while done < 100:
        t, g, mask = random_case(rng)
        if not valid(mask):
            continue
        # cloning the target into itself, or the target plus a constant, gives the target
        for c in (0, 17, -40):
            gc = [[v + c for v in r] for r in t]
            f = poisson_edit(t, gc, mask, tol=1e-12)
            for y in range(len(t)):
                assert f[y] == pytest.approx(t[y], abs=1e-7)
        done += 1


def test_harmonic_fill_1d():
    # zero guidance on a gap in one row gives the straight line between the two ends
    t = [[0, 99, 99, 99, 99, 50]]
    g = [[0] * 6]
    mask = [[False, True, True, True, True, False]]
    f = poisson_edit(t, g, mask, tol=1e-13)
    assert f[0] == pytest.approx([0, 10, 20, 30, 40, 50], abs=1e-8)


def test_system_shape_and_errors():
    pixels, n, b, inner = build_system(T, G, M)
    assert pixels == [(1, 1), (2, 1), (1, 2), (2, 2)]
    assert n[(1, 1)] == 4 and b[(1, 1)] == 10 + 10 + (4 * 9 - 6)
    with pytest.raises(ValueError):
        poisson_edit([[1, 2]], [[1, 2]], [[True, True]])
    with pytest.raises(ValueError):
        poisson_edit([[1, 2]], [[1, 2]], [[True, False]], omega=2.0)
    with pytest.raises(ValueError):
        poisson_edit([[1, 2]], [[1]], [[True, False]])
    # empty region: the target comes back
    assert poisson_edit([[1, 2]], [[5, 6]], [[False, False]]) == [[1.0, 2.0]]
