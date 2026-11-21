# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distance-driven-projector/. The authors are listed in prov/MVREDC.jsonl.

import math
import random
from fractions import Fraction as F

import imgkit as ik
from distance_driven_projector import (
    dd_back_project,
    dd_matrix,
    dd_project,
    dd_project_view,
    detector,
    view_weights,
)


def test_worked_example() -> None:
    # n = 2, cos = 4/5, sin = 3/5, four bins of width 1/2 on [-1, 1]
    w = view_weights(2, F(4, 5), F(3, 5), F(-1), F(1, 2), 4)
    assert sorted(w) == sorted([
        (1, 0, 0, F(5, 4)), (2, 0, 0, F(3, 4)), (2, 0, 1, F(1, 2)), (3, 0, 1, F(5, 4)),
        (0, 1, 0, F(5, 4)), (1, 1, 0, F(1, 2)), (1, 1, 1, F(3, 4)), (2, 1, 1, F(5, 4)),
    ])
    p = dd_project_view([[1, 2], [3, 4]], F(4, 5), F(3, 5), F(-1), F(1, 2), 4)
    assert p == [F(15, 4), F(23, 4), F(27, 4), F(5, 2)]
    # the detector misses 1/8 of pixel (0, 1) and 1/8 of pixel (1, 0)
    assert F(1, 2) * sum(p) == 10 - F(2, 8) - F(3, 8)


def test_mass_is_conserved_exactly() -> None:
    rng = random.Random(1)
    n = 6
    img = [[F(rng.randint(0, 9)) for _ in range(n)] for _ in range(n)]
    mass = sum(sum(row) for row in img) * F(2, n) ** 2
    s0, w, nbins = F(-3, 2), F(1, 4), 12
    for c, sn in ((F(4, 5), F(3, 5)), (F(-3, 5), F(4, 5)), (F(12, 13), F(-5, 13)), (F(5, 13), F(12, 13)), (F(1), F(0))):
        p = dd_project_view(img, c, sn, s0, w, nbins)
        assert w * sum(p) == mass


def test_constant_image_has_no_ripple() -> None:
    n, nbins = 32, 23
    angles = [0.0, 0.3, 1.2, 2.0]
    one = [[1.0] * n for _ in range(n)]
    p = dd_project(one, angles, nbins)
    q = ik.sp_matvec(ik.parallel_beam_matrix(n, angles, nbins), ik.flatten(one))
    s0, w = detector(nbins)
    ripple = 0.0
    for k, theta in enumerate(angles):
        c, sn = abs(math.cos(theta)), abs(math.sin(theta))
        for b in range(nbins):
            s = s0 + (b + 0.5) * w
            if abs(s) + w / 2 < max(c, sn) - min(c, sn):
                assert abs(p[k * nbins + b] - 2.0 / max(c, sn)) < 1e-12
                ripple = max(ripple, abs(q[k * nbins + b] - 2.0 / max(c, sn)))
    # the pixel-driven projector of imgkit has a ripple on the same bins
    assert ripple > 1e-3


def test_adjoint() -> None:
    rng = random.Random(2)
    n, nbins = 16, 23
    angles = [k * math.pi / 7 for k in range(7)]
    x = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    y = [rng.uniform(-1, 1) for _ in range(len(angles) * nbins)]
    ax = dd_project(x, angles, nbins)
    aty = dd_back_project(n, angles, nbins, y)
    lhs = sum(a * b for a, b in zip(ax, y))
    rhs = ik.img_dot(x, aty)
    assert abs(lhs - rhs) <= 1e-10 * math.sqrt(sum(a * a for a in ax)) * math.sqrt(sum(b * b for b in y))


def test_matrix_matches_projector() -> None:
    rng = random.Random(3)
    n, nbins = 16, 23
    angles = [0.0, 0.5, 1.0, 2.0, 3.0]
    x = [[rng.random() for _ in range(n)] for _ in range(n)]
    a = ik.sp_matvec(dd_matrix(n, angles, nbins), ik.flatten(x))
    b = dd_project(x, angles, nbins)
    assert max(abs(p - q) for p, q in zip(a, b)) < 1e-12


def test_disk_projection() -> None:
    n, nbins = 32, 23
    angles = [k * math.pi / 8 for k in range(8)]
    p = dd_project(ik.disk_phantom(n, 0.5), angles, nbins)
    s0, w = detector(nbins)
    for k in range(len(angles)):
        for b in range(nbins):
            if abs(s0 + (b + 0.5) * w) < 0.35:
                # the average of the analytic projection 2 sqrt(1/4 - s^2) over the bin
                m = 64
                avg = sum(2.0 * math.sqrt(max(0.0, 0.25 - (s0 + (b + (r + 0.5) / m) * w) ** 2)) for r in range(m)) / m
                assert abs(p[k * nbins + b] - avg) < 2.0 / n
