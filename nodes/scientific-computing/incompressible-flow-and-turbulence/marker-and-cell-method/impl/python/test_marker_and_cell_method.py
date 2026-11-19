# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marker-and-cell-method/. The authors are listed in prov/B1FT13.jsonl.

import math
import random
from fractions import Fraction as Fr

import scisparse as sp
from marker_and_cell_method import Box, divergence, gradient, interpolate, mac, move_markers, project


def _err(a, b):
    return max(abs(a[k] - b[k]) for k in range(len(a)))


def test_minus_div_grad_is_the_neumann_5_point_matrix_exactly():
    b = Box(3, 2, Fr(3), Fr(1))  # dx = 1, dy = 1/2
    A = sp.poisson2d(3, 2, Fr(1), Fr(1, 2), bc="neumann")
    for m in range(6):
        e = [Fr(int(k == m)) for k in range(6)]
        gx, gy = gradient(b, e)
        col = [-x for x in divergence(b, gx, gy)]
        assert col == [A[k].get(m, 0) for k in range(6)]


def test_no_checkerboard_mode():
    # G p = 0 only for constant p; the checkerboard has a nonzero MAC gradient
    b = Box(4, 4, 1.0, 1.0)
    cb = [(-1) ** (i + j) for j in range(4) for i in range(4)]
    gx, gy = gradient(b, cb)
    assert max(abs(x) for x in gx + gy) == 8.0
    # a collocated central gradient (p[i+1] - p[i-1]) / (2 dx) of the checkerboard is zero
    assert all(cb[i + 1 + 4 * j] - cb[i - 1 + 4 * j] == 0 for j in range(4) for i in range(1, 3))
    gx, gy = gradient(b, [2.5] * 16)
    assert max(abs(x) for x in gx + gy) == 0


def test_projection_on_random_data():
    rng = random.Random(5)
    b = Box(6, 5, 1.0, 1.2)
    us = [rng.uniform(-1, 1) if 0 < k % 7 < 6 else 0.0 for k in range(7 * 5)]
    vs = [rng.uniform(-1, 1) if 0 < k // 6 < 5 else 0.0 for k in range(6 * 6)]
    u, v, _, _ = project(b, us, vs, 0.1)
    assert max(abs(x) for x in divergence(b, u, v)) < 1e-10
    u2, v2, _, _ = project(b, u, v, 0.1)
    assert _err(u, u2) < 1e-10 and _err(v, v2) < 1e-10
    inner = sum((us[k] - u[k]) * u[k] for k in range(len(u))) + sum((vs[k] - v[k]) * v[k] for k in range(len(v)))
    assert abs(inner) < 1e-10


def test_free_slip_taylor_green_order():
    # u = sin x cos y, v = -cos x sin y, p = (cos 2x + cos 2y) / 4 times e^(-2 nu t), e^(-4 nu t) on [0, pi]^2
    nu, T = 0.1, 0.2
    eu, ep = [], []
    for n in (8, 16, 32):
        b = Box(n, n, math.pi, math.pi)
        u, v = b.sample(lambda x, y: math.sin(x) * math.cos(y), lambda x, y: -math.cos(x) * math.sin(y))
        steps = max(1, round(T / (0.4 * b.dx**2)))
        u, v, p, _, _ = mac(b, u, v, T / steps, nu, steps)
        assert max(abs(x) for x in divergence(b, u, v)) < 1e-10
        a = math.exp(-2 * nu * T)
        ue, ve = b.sample(lambda x, y: math.sin(x) * math.cos(y) * a, lambda x, y: -math.cos(x) * math.sin(y) * a)
        pe = b.sample_p(lambda x, y: (math.cos(2 * x) + math.cos(2 * y)) / 4 * a * a)
        m, me = sum(p) / len(p), sum(pe) / len(pe)
        eu.append(max(_err(u, ue), _err(v, ve)))
        ep.append(max(abs(p[k] - m - pe[k] + me) for k in range(len(p))))
    for e in (eu, ep):
        assert all(abs(math.log2(e[i] / e[i + 1]) - 2) < 0.2 for i in range(2)), e
    assert abs(eu[0] - 2.349e-4) < 1e-6  # 8 by 8 cells, 3 steps of dt = 1/15


def test_bilinear_interpolation_is_exact_for_linear_fields():
    b = Box(5, 4, 1.0, 2.0)
    u, v = b.sample(lambda x, y: 1 + 2 * x - 3 * y, lambda x, y: -0.5 + x + 4 * y)
    rng = random.Random(9)
    for _ in range(50):
        # stay at least half a cell from the walls, where both fields have unknowns on both sides
        x, y = rng.uniform(0.1, 0.9), rng.uniform(0.25, 1.75)
        uu, vv = interpolate(b, u, v, x, y)
        assert abs(uu - (1 + 2 * x - 3 * y)) < 1e-12 and abs(vv - (-0.5 + x + 4 * y)) < 1e-12


def test_markers_follow_streamlines():
    # in the frozen free-slip vortex the stream function sin x sin y is constant along paths
    b = Box(16, 16, math.pi, math.pi)
    u, v = b.sample(lambda x, y: math.sin(x) * math.cos(y), lambda x, y: -math.cos(x) * math.sin(y))
    start = [(0.8, 1.0), (1.5, 0.6), (2.2, 2.0), (1.2, 2.5)]
    pts = list(start)
    for _ in range(100):
        pts = move_markers(b, u, v, pts, 0.05)
    drift = max(abs(math.sin(x) * math.sin(y) - math.sin(x0) * math.sin(y0)) for (x, y), (x0, y0) in zip(pts, start))
    assert drift < 1e-3, drift  # measured 1.9e-4
    assert all(0 < x < math.pi and 0 < y < math.pi for x, y in pts)


def test_lid_driven_cavity_runs_divergence_free():
    # no-slip box with a lid moving at speed 1, Re = 1 / nu = 100, a short start-up run
    b = Box(8, 8, 1.0, 1.0, slip="no", lid=1.0)
    u, v, _ = b.zeros()
    rng = random.Random(2)
    markers = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(40)]
    u, v, p, markers, cells = mac(b, u, v, 0.01, 0.01, 60, markers=markers)
    assert max(abs(x) for x in divergence(b, u, v)) < 1e-10
    assert all(0 <= x <= 1 and 0 <= y <= 1 for x, y in markers)
    assert cells <= set(range(64))
    # the lid drags the top row of fluid to the right, and the return flow below goes left
    assert min(u[b.iu(i, 7)] for i in range(1, 8)) > 0
    assert min(u[b.iu(4, j)] for j in range(8)) < 0
