# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/siddon-algorithm/. The authors are listed in prov/3SDE4K.jsonl.

import math
import random
from fractions import Fraction as F

import imgkit as ik
from siddon_algorithm import (
    parallel_rays,
    siddon_back_project,
    siddon_matrix,
    siddon_project,
    siddon_ray,
)


def clip_length(p0, p1, box):
    """Brute force: the length of the segment p0 -> p1 inside an axis-aligned box (Liang-Barsky)."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    lo, hi = F(0), F(1)
    for c0, dc, cmin, cmax in ((x0, dx, box[0], box[1]), (y0, dy, box[2], box[3])):
        if dc == 0:
            if not cmin <= c0 <= cmax:
                return F(0)
            continue
        a, b = (cmin - c0) / dc, (cmax - c0) / dc
        lo, hi = max(lo, min(a, b)), min(hi, max(a, b))
    if hi <= lo:
        return F(0)
    q = dx * dx + dy * dy
    return (hi - lo) * F(math.isqrt(q.numerator), math.isqrt(q.denominator))


def pixel_box(n, i, j):
    return (F(2 * j, n) - 1, F(2 * j + 2, n) - 1, 1 - F(2 * i + 2, n), 1 - F(2 * i, n))


def test_worked_example() -> None:
    out = siddon_ray(4, (F(-1), F(-1, 2)), (F(1), F(1)))
    assert out == [
        (2, 0, F(5, 8)),
        (2, 1, F(5, 24)),
        (1, 1, F(5, 12)),
        (1, 2, F(5, 12)),
        (0, 2, F(5, 24)),
        (0, 3, F(5, 8)),
    ]


def test_exact_against_brute_force() -> None:
    rng = random.Random(1)
    n = 8
    dirs = [(3, 4), (4, -3), (-5, 12), (12, 5), (8, -15), (1, 0), (0, 1), (-1, 0)]
    for trial in range(40):
        u, v = dirs[trial % len(dirs)]
        x0, y0 = F(rng.randint(-24, 24), 16), F(rng.randint(-24, 24), 16)
        t = F(rng.randint(1, 8), 4)
        p0, p1 = (x0, y0), (x0 + t * u, y0 + t * v)
        got = {}
        for i, j, w in siddon_ray(n, p0, p1):
            assert (i, j) not in got
            got[(i, j)] = w
        want = {}
        for i in range(n):
            for j in range(n):
                w = clip_length(p0, p1, pixel_box(n, i, j))
                if w > 0:
                    want[(i, j)] = w
        if u == 0 or v == 0:
            # a ray on a grid line touches two pixels; Siddon gives it to one of them
            assert sum(got.values()) == clip_length(p0, p1, (F(-1), F(1), F(-1), F(1)))
            assert all(want.get(key) == w for key, w in got.items())
        else:
            assert got == want


def test_total_length_is_the_chord() -> None:
    for u, v in ((3, 4), (5, -12), (7, 24)):
        p0, p1 = (F(-3, 2), F(-1, 3)), (F(-3, 2) + 3 * u, F(-1, 3) + 3 * v)
        total = sum(w for _, _, w in siddon_ray(16, p0, p1))
        assert total == clip_length(p0, p1, (F(-1), F(1), F(-1), F(1)))


def test_axis_parallel_ray() -> None:
    n = 8
    x = F(-1) + F(2 * 3 + 1, n)  # the center of column 3
    out = siddon_ray(n, (x, F(-2)), (x, F(2)))
    assert out == [(i, 3, F(2, n)) for i in range(n - 1, -1, -1)]
    assert siddon_ray(n, (F(1), F(-2)), (F(1), F(2))) == []
    assert siddon_ray(n, (F(-3), F(3)), (F(3), F(5))) == []


def test_adjoint() -> None:
    rng = random.Random(2)
    n, nbins = 16, 23
    rays = parallel_rays([k * math.pi / 6 for k in range(6)], nbins)
    x = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    y = [rng.uniform(-1, 1) for _ in rays]
    ax = siddon_project(x, rays)
    aty = siddon_back_project(n, rays, y)
    lhs = sum(a * b for a, b in zip(ax, y))
    rhs = ik.img_dot(x, aty)
    assert abs(lhs - rhs) <= 1e-10 * math.sqrt(sum(a * a for a in ax)) * math.sqrt(sum(b * b for b in y))


def test_matrix_matches_projector() -> None:
    n, nbins = 16, 23
    rays = parallel_rays([0.0, 0.4, 1.3], nbins)
    rng = random.Random(3)
    x = [[rng.random() for _ in range(n)] for _ in range(n)]
    rows = siddon_matrix(n, rays)
    a = ik.sp_matvec(rows, ik.flatten(x))
    b = siddon_project(x, rays)
    assert max(abs(p - q) for p, q in zip(a, b)) < 1e-12


def test_disk_projection() -> None:
    n, nbins = 32, 23
    angles = [k * math.pi / 8 for k in range(8)]
    img = ik.disk_phantom(n, 0.5)
    p = siddon_project(img, parallel_rays(angles, nbins))
    q = ik.sp_matvec(ik.parallel_beam_matrix(n, angles, nbins), ik.flatten(img))
    width = 2.0 * math.sqrt(2.0) / nbins
    for k in range(len(angles)):
        for b in range(nbins):
            s = -math.sqrt(2.0) + (b + 0.5) * width
            exact = 2.0 * math.sqrt(0.25 - s * s) if abs(s) < 0.5 else 0.0
            # the pixelated disk differs from the true disk by at most one pixel (2 / n = 0.0625) along a chord
            if abs(s) < 0.35:
                assert abs(p[k * nbins + b] - exact) < 2.0 / n
                assert abs(p[k * nbins + b] - q[k * nbins + b]) < 0.1


def test_gaussian_second_order() -> None:
    errs = []
    angles = [0.3, 1.1]
    nbins = 23
    width = 2.0 * math.sqrt(2.0) / nbins
    for n in (16, 32):
        xs, ys = ik.pixel_centers(n)
        g = [[math.exp(-16.0 * (x * x + y * y)) for x in xs] for y in ys]
        p = siddon_project(g, parallel_rays(angles, nbins))
        e = 0.0
        for k in range(len(angles)):
            for b in range(nbins):
                s = -math.sqrt(2.0) + (b + 0.5) * width
                e = max(e, abs(p[k * nbins + b] - math.sqrt(math.pi / 16.0) * math.exp(-16.0 * s * s)))
        errs.append(e)
    assert errs[1] < 0.003
    assert errs[0] / errs[1] > 3.0
