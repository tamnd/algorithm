# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joseph-projector/. The authors are listed in prov/YFWYC3.jsonl.

import math
import random
from fractions import Fraction as F

import imgkit as ik
from joseph_projector import (
    bin_centers,
    joseph_back_project,
    joseph_matrix,
    joseph_project,
    joseph_ray,
    ray_weights,
)


def test_worked_example() -> None:
    # n = 4, cos = 4/5, sin = 3/5, s = 0: x = -3 y / 4 in each row
    w = ray_weights(4, F(4, 5), F(3, 5), F(0))
    assert w == [
        (0, 0, F(25, 64)), (0, 1, F(15, 64)),
        (1, 1, F(35, 64)), (1, 2, F(5, 64)),
        (2, 1, F(5, 64)), (2, 2, F(35, 64)),
        (3, 2, F(15, 64)), (3, 3, F(25, 64)),
    ]
    img = [[4 * i + j + 1 for j in range(4)] for i in range(4)]
    assert joseph_ray(img, F(4, 5), F(3, 5), F(0)) == F(85, 4)


def test_axis_aligned_rays() -> None:
    rng = random.Random(1)
    n = 8
    img = [[F(rng.randint(-9, 9)) for _ in range(n)] for _ in range(n)]
    h = F(2, n)
    for j in range(n):
        x = -1 + (2 * j + 1) * h / 2
        assert joseph_ray(img, F(1), F(0), x) == h * sum(img[i][j] for i in range(n))
    for i in range(n):
        y = 1 - (2 * i + 1) * h / 2
        assert joseph_ray(img, F(0), F(1), y) == h * sum(img[i])


def test_adjoint() -> None:
    rng = random.Random(2)
    n, nbins = 16, 23
    angles = [k * math.pi / 7 for k in range(7)]
    x = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    y = [rng.uniform(-1, 1) for _ in range(len(angles) * nbins)]
    ax = joseph_project(x, angles, nbins)
    aty = joseph_back_project(n, angles, nbins, y)
    lhs = sum(a * b for a, b in zip(ax, y))
    rhs = ik.img_dot(x, aty)
    assert abs(lhs - rhs) <= 1e-10 * math.sqrt(sum(a * a for a in ax)) * math.sqrt(sum(b * b for b in y))


def test_matrix_matches_projector() -> None:
    rng = random.Random(3)
    n, nbins = 16, 23
    angles = [0.0, 0.5, 1.0, 2.0]
    x = [[rng.random() for _ in range(n)] for _ in range(n)]
    a = ik.sp_matvec(joseph_matrix(n, angles, nbins), ik.flatten(x))
    b = joseph_project(x, angles, nbins)
    assert max(abs(p - q) for p, q in zip(a, b)) < 1e-12


def test_constant_image() -> None:
    n, nbins = 32, 23
    one = [[1.0] * n for _ in range(n)]
    p = joseph_project(one, [0.0, math.pi / 4], nbins)
    for b, s in enumerate(bin_centers(nbins)):
        if abs(s) < 1 - 1 / n:
            assert abs(p[b] - 2.0) < 1e-12
    assert abs(p[nbins + nbins // 2] - 2.0 * math.sqrt(2.0)) < 1e-12


def test_disk_projection() -> None:
    n, nbins = 32, 23
    angles = [k * math.pi / 8 for k in range(8)]
    img = ik.disk_phantom(n, 0.5)
    p = joseph_project(img, angles, nbins)
    q = ik.sp_matvec(ik.parallel_beam_matrix(n, angles, nbins), ik.flatten(img))
    for k in range(len(angles)):
        for b, s in enumerate(bin_centers(nbins)):
            if abs(s) < 0.35:
                exact = 2.0 * math.sqrt(0.25 - s * s)
                assert abs(p[k * nbins + b] - exact) < 2.0 / n
                assert abs(p[k * nbins + b] - q[k * nbins + b]) < 0.1


def test_gaussian_second_order() -> None:
    errs = []
    nbins = 23
    for n in (16, 32):
        xs, ys = ik.pixel_centers(n)
        g = [[math.exp(-16.0 * (x * x + y * y)) for x in xs] for y in ys]
        p = joseph_project(g, [0.3, 1.1], nbins)
        e = 0.0
        for k in range(2):
            for b, s in enumerate(bin_centers(nbins)):
                e = max(e, abs(p[k * nbins + b] - math.sqrt(math.pi / 16.0) * math.exp(-16.0 * s * s)))
        errs.append(e)
    assert errs[1] < 0.005
    assert errs[0] / errs[1] > 3.0
