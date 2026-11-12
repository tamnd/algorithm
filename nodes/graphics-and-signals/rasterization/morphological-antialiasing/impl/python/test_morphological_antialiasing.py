# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morphological-antialiasing/. The authors are listed in prov/ZVD2J6.jsonl.

import random
from fractions import Fraction as F

from morphological_antialiasing import l_shape_areas, morphological_antialiasing


def clip(poly, inside, inter):
    out = []
    for k in range(len(poly)):
        p, q = poly[k - 1], poly[k]
        if inside(q):
            if not inside(p):
                out.append(inter(p, q))
            out.append(q)
        elif inside(p):
            out.append(inter(p, q))
    return out


def clip_box(poly, x0, x1, y0, y1):
    """Sutherland-Hodgman clipping of a polygon to an axis-aligned box, exact."""
    for axis, bound, keep_ge in ((0, x0, True), (0, x1, False), (1, y0, True), (1, y1, False)):
        if not poly:
            return []

        def inside(p, axis=axis, bound=bound, keep_ge=keep_ge):
            return p[axis] >= bound if keep_ge else p[axis] <= bound

        def inter(p, q, axis=axis, bound=bound):
            t = (bound - p[axis]) / (q[axis] - p[axis])
            return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))

        poly = clip(poly, inside, inter)
    return poly


def area(poly):
    if len(poly) < 3:
        return F(0)
    s = F(0)
    for k in range(len(poly)):
        s += poly[k - 1][0] * poly[k][1] - poly[k][0] * poly[k - 1][1]
    return abs(s) / 2


def triangle_cell_areas(length):
    """Areas of the triangle (0, 0), (length, 0), (0, 1/2) inside the unit cells along the x axis."""
    tri = [(F(0), F(0)), (length, F(0)), (F(0), F(1, 2))]
    out = []
    k = 0
    while k < length:
        out.append(area(clip_box(tri, F(k), F(k + 1), F(0), F(1))))
        k += 1
    return out


def oracle_bw(img):
    """MLAA of a black-and-white image by the closed form o + prod(1 - a) (c - o).

    Shapes are found from the set of separation segments, and the blend areas
    come from clipping the triangle of each L shape to the cells.
    """
    h, w = len(img), len(img[0])
    weights = [[[] for _ in range(w)] for _ in range(h)]

    def shapes(get, w, h, record):
        hseg = {(x, y) for y in range(h - 1) for x in range(w) if get(x, y) != get(x, y + 1)}
        vseg = {(x, y) for y in range(h) for x in range(1, w) if get(x - 1, y) != get(x, y)}
        for (x, y) in sorted(hseg):
            if (x - 1, y) in hseg:
                continue
            b = x
            while (b, y) in hseg:
                b += 1
            ends = []
            for vx in (x, b):
                up, down = (vx, y) in vseg, (vx, y + 1) in vseg
                ends.append(-1 if up and not down else 1 if down and not up else 0)
            n = F(b - x)
            parts = []
            if ends[0] and ends[1]:
                parts = [(x, 1, ends[0], n / 2), (b, -1, ends[1], n / 2)]
            elif ends[0]:
                parts = [(x, 1, ends[0], n)]
            elif ends[1]:
                parts = [(b, -1, ends[1], n)]
            for start, step, side, length in parts:
                row = y if side < 0 else y + 1
                for k, a in enumerate(triangle_cell_areas(length)):
                    col = start + k if step == 1 else start - 1 - k
                    record(col, row, a)

    shapes(lambda x, y: img[y][x], w, h, lambda c, r, a: weights[r][c].append(a))
    shapes(lambda x, y: img[x][y], h, w, lambda c, r, a: weights[c][r].append(a))
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            c = img[y][x]
            o = 1 - c
            keep = F(1)
            for a in weights[y][x]:
                keep *= 1 - a
            row.append(o + keep * (c - o))
        out.append(row)
    return out


def coverage_below(c, slope_den, i, j):
    """Exact area of pixel [i, i+1] x [j, j+1] (y down) on the side y >= c + x / slope_den."""
    poly = [(F(i), F(j)), (F(i + 1), F(j)), (F(i + 1), F(j + 1)), (F(i), F(j + 1))]

    def f(p):
        return p[1] - c - p[0] / slope_den

    def inter(p, q):
        t = f(p) / (f(p) - f(q))
        return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))

    return area(clip(poly, lambda p: f(p) >= 0, inter))


def test_paper_figure_3() -> None:
    assert l_shape_areas(F(3, 2)) == [F(1, 3), F(1, 24)]
    # a Z shape of length 3 between a white row and a black row
    img = [[(F(0),), (F(1),), (F(1),), (F(1),), (F(1),)],
           [(F(0),), (F(0),), (F(0),), (F(0),), (F(1),)]]
    out = morphological_antialiasing(img, 0, "h")
    assert out[0][1:4] == [(F(2, 3),), (F(23, 24),), (F(1),)]
    assert out[1][1:4] == [(F(0),), (F(1, 24),), (F(1, 3),)]


def test_areas_against_clipping() -> None:
    for m in range(1, 41):
        length = F(m, 2)
        got = l_shape_areas(length)
        assert got == triangle_cell_areas(length)
        assert sum(got) == length / 4


def test_bw_images_against_oracle() -> None:
    rng = random.Random(2009)
    for _ in range(500):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        p = rng.random()
        img = [[(F(1) if rng.random() < p else F(0),) for _ in range(w)] for _ in range(h)]
        got = morphological_antialiasing(img)
        want = oracle_bw([[px[0] for px in row] for row in img])
        assert [[px[0] for px in row] for row in got] == want


def test_shallow_lines_horizontal_pass_is_exact() -> None:
    # a line through the middles of the secondary edges: the reconstruction is the line itself
    for den in range(1, 9):
        for shift in range(-den, den + 1):
            c = F(1, 2) + F(shift, den)
            w, h = 4 * den, 7
            img = [[(F(1) if j + F(1, 2) > c + (i + F(1, 2)) / den else F(0),) for i in range(w)] for j in range(h)]
            out = morphological_antialiasing(img, 0, "h")
            for j in range(h):
                for i in range(den, w - den):
                    assert out[j][i][0] == coverage_below(c, den, i, j)
            # the same image turned by a quarter turn needs the vertical pass
            turned = [list(col) for col in zip(*img)]
            out_t = morphological_antialiasing(turned, 0, "v")
            for j in range(h):
                for i in range(den, w - den):
                    assert out_t[i][j][0] == coverage_below(c, den, i, j)
            # the full method adds a blend of 1/8 on each side of every step,
            # and 1/4 where the step touches the top or bottom border
            if den == 1:
                continue
            full = morphological_antialiasing(img)
            for j in range(h):
                for i in range(den, w - den):
                    err = abs(full[j][i][0] - coverage_below(c, den, i, j))
                    assert err <= (F(1, 8) if 0 < j < h - 1 else F(1, 4))


def test_invariants_on_color_images() -> None:
    rng = random.Random(3)
    for _ in range(100):
        h, w = rng.randint(1, 5), rng.randint(1, 5)
        img = [[(F(rng.randint(0, 255)), F(rng.randint(0, 3))) for _ in range(w)] for _ in range(h)]
        out = morphological_antialiasing(img, threshold=rng.choice([0, 16, 64]))
        for ch in range(2):
            lo = min(px[ch] for row in img for px in row)
            hi = max(px[ch] for row in img for px in row)
            assert all(lo <= px[ch] <= hi for row in out for px in row)
        # a threshold above every difference leaves the image alone
        assert morphological_antialiasing(img, threshold=255) == img
    flat = [[(F(5), F(1))] * 4 for _ in range(3)]
    assert morphological_antialiasing(flat) == flat
    halves = [[(F(0),)] * 5, [(F(0),)] * 5, [(F(1),)] * 5]
    assert morphological_antialiasing(halves) == halves


def test_isolated_pixel() -> None:
    img = [[(F(0),)] * 3, [(F(0),), (F(1),), (F(0),)], [(F(0),)] * 3]
    out = morphological_antialiasing(img)
    assert out[1][1] == (F(7, 8) ** 8,)
    assert out[0][1] == (F(0),) and out[0][0] == (F(0),)
