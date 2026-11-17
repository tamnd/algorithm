# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harmonic-coordinates/. The authors are listed in prov/XS2ZCM.jsonl.
import math
import random

from harmonic_coordinates import BandLU, HarmonicCoordinates, gauss_seidel, point_in_polygon

L_SHAPE = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)]
RECT = [(0, 0), (3, 0), (3, 2), (0, 2)]
STAR = [(math.cos(2 * math.pi * k / 10) * (1.0 if k % 2 == 0 else 0.45), math.sin(2 * math.pi * k / 10) * (1.0 if k % 2 == 0 else 0.45)) for k in range(10)]

_CACHE = {}


def hc(cage, n_cells):
    key = (tuple(cage), n_cells)
    if key not in _CACHE:
        _CACHE[key] = HarmonicCoordinates(cage, n_cells)
    return _CACHE[key]


def mvc(p, poly):
    """2D mean value coordinates, for comparison."""
    n = len(poly)
    d = [(c[0] - p[0], c[1] - p[1]) for c in poly]
    r = [math.hypot(*v) for v in d]
    tan_half = []
    for i in range(n):
        a, b = d[i], d[(i + 1) % n]
        cr = a[0] * b[1] - a[1] * b[0]
        tan_half.append(cr / (r[i] * r[(i + 1) % n] + (a[0] * b[0] + a[1] * b[1])))
    w = [(tan_half[i - 1] + tan_half[i]) / r[i] for i in range(n)]
    s = sum(w)
    return [x / s for x in w]


def test_partition_of_unity_and_nonnegative():
    for cage, cells in ((L_SHAPE, 16), (STAR, 20)):
        h = hc(cage, cells)
        for vals in h.values:
            assert abs(sum(vals) - 1) < 1e-12
            assert min(vals) >= -1e-14


def test_linear_precision_at_nodes():
    for cage, cells in ((L_SHAPE, 16), (STAR, 20)):
        h = hc(cage, cells)
        for (i, j), r in h.index.items():
            x, y = h.node(i, j)
            vals = h.values[r]
            px = sum(v * c[0] for v, c in zip(vals, cage))
            py = sum(v * c[1] for v, c in zip(vals, cage))
            assert abs(px - x) < 1e-11 and abs(py - y) < 1e-11


def test_rectangle_gives_bilinear_coordinates():
    h = hc(RECT, 12)
    for (i, j), r in h.index.items():
        x, y = h.node(i, j)
        a, b = x / 3, y / 2
        want = [(1 - a) * (1 - b), a * (1 - b), a * b, (1 - a) * b]
        assert all(abs(u - v) < 1e-12 for u, v in zip(h.values[r], want))


def test_band_lu_matches_gauss_seidel():
    h = hc(L_SHAPE, 10)
    lu = BandLU(h.rows)
    for v in range(len(L_SHAPE)):
        b = [row[v] for row in h.rhs]
        x1 = lu.solve(b)
        x2 = gauss_seidel(h.rows, b)
        assert max(abs(a - c) for a, c in zip(x1, x2)) < 1e-10


def test_band_lu_on_random_m_matrix():
    rng = random.Random(41)
    n = 30
    rows = []
    for i in range(n):
        row = {}
        off = 0.0
        for j in range(max(0, i - 3), min(n, i + 4)):
            if j != i and rng.random() < 0.7:
                row[j] = -rng.uniform(0.1, 1.0)
                off += -row[j]
        row[i] = off + rng.uniform(0.1, 1.0)
        rows.append(row)
    x = [rng.uniform(-1, 1) for _ in range(n)]
    b = [sum(v * x[j] for j, v in row.items()) for row in rows]
    y = BandLU(rows).solve(b)
    assert max(abs(a - c) for a, c in zip(x, y)) < 1e-12


def test_harmonic_stays_nonnegative_where_mean_value_goes_negative():
    h = hc(L_SHAPE, 16)
    worst_mvc = 0.0
    for (i, j), r in h.index.items():
        p = h.node(i, j)
        worst_mvc = min(worst_mvc, min(mvc(p, L_SHAPE)))
        assert min(h.values[r]) >= -1e-14
    assert worst_mvc < -0.009
    # The worked example: at (0.875, 1.375) the mean value weight of the
    # vertex (2, 1) is about -0.0097, and its harmonic coordinate is positive.
    p = (0.875, 1.375)
    assert abs(mvc(p, L_SHAPE)[2] + 0.0097336) < 1e-6
    r = h.index[(round((p[0] - h.x0) / h.h), round((p[1] - h.y0) / h.h))]
    assert 0.003 < h.values[r][2] < 0.0032


def test_interpolation_and_deformation():
    h = hc(L_SHAPE, 16)
    rng = random.Random(42)
    for _ in range(20):
        p = (rng.uniform(0, 2), rng.uniform(0, 2))
        if not point_in_polygon(p, L_SHAPE):
            continue
        w = h.coordinates(p)
        assert abs(sum(w) - 1) < 1e-12
        assert min(w) >= -1e-14
    # The identity cage gives back the node, and a translated cage translates it.
    (i, j) = next(iter(h.index))
    p = h.node(i, j)
    q = h.deform(p, L_SHAPE)
    assert math.dist(p, q) < 1e-11
    moved = [(x + 0.5, y - 0.25) for x, y in L_SHAPE]
    q = h.deform(p, moved)
    assert math.dist((p[0] + 0.5, p[1] - 0.25), q) < 1e-11


def test_vertex_coordinate_peaks_near_its_vertex():
    h = hc(L_SHAPE, 16)
    # The coordinate of the reflex vertex (1, 1) is largest close to it.
    best = max(h.index.items(), key=lambda kv: h.values[kv[1]][3])
    x, y = h.node(*best[0])
    assert math.hypot(x - 1, y - 1) < 0.3
