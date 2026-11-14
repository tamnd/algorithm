# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plastering/. The authors are listed in prov/ZETKKR.jsonl.

import random
from fractions import Fraction as F

from mg4geom import FACES, bernstein_certified, corner_jacobians, hex_volume, jacobian_det
from plastering import box_front, box_normals, plaster_layer, safe_thickness


def layer(xs, ys, zs, h):
    points, quads = box_front(xs, ys, zs)
    normals = box_normals(points, (xs[0], ys[0], zs[0]), (xs[-1], ys[-1], zs[-1]))
    new_points, hexes, ok = plaster_layer(points, quads, normals, h)
    return points, quads, new_points, hexes, ok


def faces_by_coordinates(hexes):
    count = {}
    for hx in hexes:
        for f in FACES:
            key = frozenset(hx[i] for i in f)
            count[key] = count.get(key, 0) + 1
    return count


def check_layer(xs, ys, zs, h, full=False):
    points, quads, new_points, hexes, ok = layer(xs, ys, zs, h)
    nx, ny, nz = len(xs) - 1, len(ys) - 1, len(zs) - 1
    assert len(quads) == len(hexes) == 2 * (nx * ny + ny * nz + nz * nx)
    g = safe_thickness(xs, ys, zs)
    # brute force: corner Jacobians of every hex
    assert ok == all(d > 0 for hx in hexes for d in corner_jacobians(hx))
    # oracle: a corner Jacobian is h times the product of two in-plane widths, outer or inner
    ws = [inner_widths(grid, h) for grid in (xs, ys, zs)]
    expect = h > 0 and all(p * q > 0 for b in range(3) for c in range(b + 1, 3) for p in ws[b] for q in ws[c])
    assert ok == expect
    # the layer is a valid mesh of the shell exactly when 0 < h < g
    assert (0 < h < g) == (h > 0 and all(w > 0 for wl in ws for w in wl))
    if 0 < h < g:
        assert ok
        lo = [xs[0] + h, ys[0] + h, zs[0] + h]
        hi = [xs[-1] - h, ys[-1] - h, zs[-1] - h]
        # the new front is the boundary of the inner box
        for p in new_points:
            assert all(lo[t] <= p[t] <= hi[t] for t in range(3))
            assert any(p[t] in (lo[t], hi[t]) for t in range(3))
        # conformity: outer and inner quads are free, every other face is shared by two hexes
        count = faces_by_coordinates(hexes)
        outer = {frozenset(points[v] for v in q) for q in quads}
        inner = {frozenset(new_points[v] for v in q) for q in quads}
        for key, c in count.items():
            assert c == (1 if key in outer or key in inner else 2)
        if full:
            vol = sum(hex_volume(hx) for hx in hexes)
            big = (xs[-1] - xs[0]) * (ys[-1] - ys[0]) * (zs[-1] - zs[0])
            small = (hi[0] - lo[0]) * (hi[1] - lo[1]) * (hi[2] - lo[2])
            assert vol == big - small
            assert all(bernstein_certified(hx) for hx in hexes)
    return points, quads, new_points, hexes, ok


def test_page_example():
    xs = ys = zs = [0, 1, 3, 4]
    points, quads, new_points, hexes, ok = check_layer(xs, ys, zs, F(1, 2), full=True)
    assert len(points) == 56 and len(quads) == 54 and ok
    assert safe_thickness(xs, ys, zs) == 1
    corner = points.index((0, 0, 0))
    assert new_points[corner] == (F(1, 2), F(1, 2), F(1, 2))
    edge_pt = points.index((1, 0, 0))
    assert new_points[edge_pt] == (1, F(1, 2), F(1, 2))
    face_pt = points.index((1, 1, 0))
    assert new_points[face_pt] == (1, 1, F(1, 2))
    assert sum(hex_volume(hx) for hx in hexes) == 64 - 27
    kinds = {}
    for hx in hexes:
        key = (tuple(sorted(set(corner_jacobians(hx)))), hex_volume(hx))
        kinds[key] = kinds.get(key, 0) + 1
    assert kinds == {((F(1, 8), F(1, 2)), F(7, 24)): 24, ((F(1, 2), 1), F(3, 4)): 24, ((2,), 2): 6}


def test_thickness_at_the_limit_fails():
    xs = ys = zs = [0, 1, 3, 4]
    for h in (F(0), F(1), F(3, 2), F(-1, 2)):
        assert not layer(xs, ys, zs, h)[4]


def test_one_cell_box_and_half_length():
    xs, ys, zs = [0, 4], [0, 2], [0, 6]
    assert safe_thickness(xs, ys, zs) == 1
    assert check_layer(xs, ys, zs, F(99, 100), full=True)[4]
    _, _, _, hexes, ok = layer(xs, ys, zs, F(3, 2))
    assert not ok
    # past half the length in y the inner box is turned over in y only, and hexes invert near it
    assert any(jacobian_det(hx, F(1, 2), F(1, 2), F(1, 4)) < 0 for hx in hexes)


def test_box_turned_inside_out_passes_the_corner_check():
    # h is past half of every length, so the inner box is reflected in all three axes:
    # every hex keeps positive corner Jacobians, but the layer folds over itself
    xs, ys, zs = [0, 4], [0, 2], [0, 6]
    points, quads, new_points, hexes, ok = layer(xs, ys, zs, F(7, 2))
    assert ok and safe_thickness(xs, ys, zs) == 1
    # the signed volumes add up to the box minus the signed volume of the reflected inner box
    assert sum(hex_volume(hx) for hx in hexes) == 48 - (4 - 7) * (2 - 7) * (6 - 7)
    corner = points.index((0, 0, 0))
    assert new_points[corner] == (F(7, 2), F(7, 2), F(7, 2))  # outside the box in y


def inner_widths(grid, h):
    widths = [b - a for a, b in zip(grid, grid[1:])]
    if len(widths) == 1:
        return [widths[0] - 2 * h]
    return [widths[0] - h] + widths[1:-1] + [widths[-1] - h]


def test_second_layer_on_the_new_front():
    xs = ys = zs = [0, 2, 4, 6]
    points, quads, p1, hexes1, ok1 = check_layer(xs, ys, zs, F(1, 2))
    normals = box_normals(p1, (F(1, 2),) * 3, (F(11, 2),) * 3)
    p2, hexes2, ok2 = plaster_layer(p1, quads, normals, F(1, 2))
    assert ok1 and ok2
    assert all(hx[4:] == hy[:4] for hx, hy in zip(hexes2, hexes1))
    # the void that remains is the box [1, 5]^3 with the breakpoints 1, 2, 4, 5
    assert {c for p in p2 for c in p} == {1, 2, 4, 5}


def test_random_boxes():
    rng = random.Random(1993)
    passed = 0
    for trial in range(500):
        grids = []
        for _ in range(3):
            n = rng.randint(1, 3)
            grids.append(sorted(rng.sample(range(0, 10), n + 1)))
        g = safe_thickness(*grids)
        h = rng.choice([g * F(rng.randint(1, 15), 10), F(rng.randint(-2, 12), 4)])
        ok = check_layer(*grids, h, full=(trial % 50 == 0))[4]
        passed += ok
    assert 100 < passed < 450
