# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/katsevich-algorithm/. The authors are listed in prov/KKE2E7.jsonl.

import math
import random

from katsevich_algorithm import Geometry, derivative_view, helix_ray, kappa_psi, kappa_v, katsevich, pi_interval, project

R, P, DIST = 3.0, 2.0, 3.0
D_COLS, M_ROWS = 41, 41
CENTER, ALPHA = (0.1, 0.05, 0.0), 10.0
POINTS = [(0.1, 0.05, 0.0), (0.2, 0.05, 0.0), (0.1, 0.05, 0.15), (0.0, 0.0, 0.0), (-0.2, 0.1, -0.1), (0.6, 0.0, 0.0)]
DS = 2.0 * math.pi / 64
GEO = Geometry(R, P, DIST, -2.2, DS, 2.2 / (D_COLS - 1), 2.0 / (M_ROWS - 1))
VIEWS = 48


def gauss3(src, v, c=CENTER, alpha=ALPHA):
    """Line integral of exp(-alpha |x - c|^2) along the line src + t v, with v a unit vector."""
    w = [c[i] - src[i] for i in range(3)]
    t = sum(w[i] * v[i] for i in range(3))
    d2 = sum(w[i] ** 2 for i in range(3)) - t * t
    return math.sqrt(math.pi / alpha) * math.exp(-alpha * d2)


def helix_data(geo=GEO, views=VIEWS):
    return [
        [
            [gauss3(*helix_ray(geo, geo.s0 + k * geo.ds, (j - (D_COLS - 1) / 2.0) * geo.du, (r - (M_ROWS - 1) / 2.0) * geo.dv)) for j in range(D_COLS)]
            for r in range(M_ROWS)
        ]
        for k in range(views)
    ]


DATA = helix_data()


def test_pi_interval() -> None:
    sb, st = pi_interval(GEO, (0.0, 0.0, 0.0))
    assert abs(sb + math.pi / 2.0) < 1e-9 and abs(st - math.pi / 2.0) < 1e-9
    rng = random.Random(5)
    h = P / (2.0 * math.pi)
    for _ in range(30):
        x = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))
        sb, st = pi_interval(GEO, x)
        assert 0.0 < st - sb < 2.0 * math.pi
        a = (R * math.cos(sb), R * math.sin(sb), h * sb)
        b = (R * math.cos(st), R * math.sin(st), h * st)
        # x is on the segment from a to b
        lam = sum((x[i] - a[i]) * (b[i] - a[i]) for i in range(3)) / sum((b[i] - a[i]) ** 2 for i in range(3))
        assert 0.0 < lam < 1.0
        assert max(abs(a[i] + lam * (b[i] - a[i]) - x[i]) for i in range(3)) < 1e-9


def test_kappa_line_through_helix_points() -> None:
    # The kappa-line with the angle psi at the view s passes through the projections of y(s + psi) and y(s + 2 psi).
    h = P / (2.0 * math.pi)
    for s in (0.0, 0.7):
        for psi in (-1.2, -0.4, 0.3, 1.0):
            for t in (psi, 2.0 * psi):
                y = (R * math.cos(s + t), R * math.sin(s + t), h * (s + t))
                u, v, _ = project(GEO, y, s)
                assert abs(kappa_v(GEO, u, psi) - v) < 1e-12
                if abs(u) < 1.2:
                    # on the detector the height grows with psi, so bisection finds psi again
                    assert abs(kappa_psi(GEO, u, v) - psi) < 1e-9


def test_derivative_at_fixed_direction() -> None:
    # Compare g1 with the derivative of the line integral along the source path for a fixed ray direction.
    k, eps = 30, 1e-5
    g2 = derivative_view(GEO, DATA, k)
    s = GEO.s0 + k * GEO.ds
    for r, j in ((20, 20), (15, 26), (24, 12), (18, 30)):
        u, v = (j - (D_COLS - 1) / 2.0) * GEO.du, (r - (M_ROWS - 1) / 2.0) * GEO.dv
        _, direction = helix_ray(GEO, s, u, v)
        h = P / (2.0 * math.pi)

        def line_from(sp):
            return gauss3((R * math.cos(sp), R * math.sin(sp), h * sp), direction)

        g1 = (line_from(s + eps) - line_from(s - eps)) / (2.0 * eps)
        want = DIST / math.sqrt(u * u + v * v + DIST * DIST) * g1
        assert abs(g2[r][j] - want) < 0.02 * max(1.0, abs(want))


def test_gaussian_values() -> None:
    vals = katsevich(GEO, DATA, POINTS)
    for x, val in zip(POINTS, vals):
        want = math.exp(-ALPHA * sum((x[i] - CENTER[i]) ** 2 for i in range(3)))
        assert abs(val - want) < 0.05


def test_rows_far_from_the_kappa_lines_are_not_used() -> None:
    # Every kappa-line with |psi| < pi/2 and |u| <= 1.1 stays within |v| < (D P / (2 pi R)) (pi/2 + 1.1 / D) < 0.62.
    rng = random.Random(9)
    changed = [[row if abs((r - (M_ROWS - 1) / 2.0) * GEO.dv) < 0.75 else [rng.uniform(-9, 9) for _ in row] for r, row in enumerate(p)] for p in DATA]
    assert katsevich(GEO, changed, POINTS[:3]) == katsevich(GEO, DATA, POINTS[:3])
