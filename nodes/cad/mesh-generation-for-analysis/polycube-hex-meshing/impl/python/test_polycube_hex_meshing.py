# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polycube-hex-meshing/. The authors are listed in prov/ZACEGX.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from mg4geom import FACES, REF, corner_jacobians, hex_volume, jacobian_bernstein, jacobian_det, trilinear
from polycube_hex_meshing import (
    all_voxels_certified,
    boundary_faces,
    hex_points,
    identity_images,
    polycube_grid,
    voxel_hex,
)


def unchecked_grid(voxels, corner_image, s):
    """The grid hexes of the map without the Bernstein test, for the brute force checks."""
    out = []
    for c in sorted(set(voxels)):
        h = voxel_hex(corner_image, c)
        for q in product(range(s), repeat=3):
            out.append([trilinear(h, *(F(q[t] + r[t], s) for t in range(3))) for r in REF])
    return out


def bernstein_value(coeffs, u, v, w):
    basis = [lambda t: (1 - t) ** 2, lambda t: 2 * t * (1 - t), lambda t: t * t]
    total = 0
    for i, j, k in product(range(3), repeat=3):
        total += coeffs[9 * i + 3 * j + k] * basis[i](u) * basis[j](v) * basis[k](w)
    return total


def check_mesh(voxels, img, s, full=False):
    cells = set(voxels)
    result = polycube_grid(voxels, img, s)
    if full:
        assert (result is not None) == all_voxels_certified(voxels, img)
    if result is None:
        return False
    points, hexes = result
    assert len(hexes) == len(cells) * s**3
    # brute force: the grid points are the keys that lie in some voxel
    lo = [s * min(c[t] for c in cells) for t in range(3)]
    hi = [s * max(c[t] for c in cells) + s for t in range(3)]
    expect = set()
    for k in product(*(range(lo[t], hi[t] + 1) for t in range(3))):
        if any(all(s * c[t] <= k[t] <= s * c[t] + s for t in range(3)) for c in cells):
            expect.add(k)
    assert set(points) == expect
    # conformity: every face of the grid is in one hex on the boundary and two inside
    count = {}
    for hx in hexes:
        for f in FACES:
            key = frozenset(hx[i] for i in f)
            count[key] = count.get(key, 0) + 1
    assert set(count.values()) <= {1, 2}
    assert sum(1 for c in count.values() if c == 1) == s * s * boundary_faces(cells)
    # validity: every hex has positive corner Jacobians, equal to det Dg / s^3 at the grid points
    hp = hex_points(points, hexes)
    for hx, keys in zip(hp, hexes):
        assert all(d > 0 for d in corner_jacobians(hx))
    if full:
        # continuity: a shared grid point has the same image in every voxel that contains it
        for k, p in points.items():
            for c in cells:
                if all(s * c[t] <= k[t] <= s * c[t] + s for t in range(3)):
                    assert trilinear(voxel_hex(img, c), *(F(k[t] - s * c[t], s) for t in range(3))) == p
        # the sub-hex Jacobian is the voxel Jacobian scaled by s^-3
        c = min(cells)
        h = voxel_hex(img, c)
        assert corner_jacobians(hp[0])[0] == jacobian_det(h, 0, 0, 0) / s**3
        # volume: the hexes add up to the volume of the image, for every s
        assert sum(hex_volume(hx) for hx in hp) == sum(hex_volume(voxel_hex(img, c)) for c in cells)
    return True


def test_page_example():
    voxels = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    img = identity_images(voxels)
    for z in (0, 1):
        img[(1, 1, z)] = (F(5, 4), F(5, 4), F(z))
    assert [min(jacobian_bernstein(voxel_hex(img, c))) for c in voxels] == [1, F(3, 4), F(3, 4)]
    assert check_mesh(voxels, img, 2, full=True)
    points, hexes = polycube_grid(voxels, img, 2)
    assert len(points) == 63 and len(hexes) == 24 and boundary_faces(voxels) == 14
    assert points[(2, 2, 0)] == (F(5, 4), F(5, 4), 0)
    assert points[(1, 1, 0)] == (F(9, 16), F(9, 16), 0)
    hp = hex_points(points, hexes)
    assert sum(hex_volume(hx) for hx in hp) == F(13, 4)
    assert min(min(corner_jacobians(hx)) for hx in hp) == F(3, 32)


def twisted_voxel():
    img = {}
    for a, b in product((0, 1), repeat=2):
        img[(a, b, 0)] = (F(2 * a - 1), F(2 * b - 1), F(0))
        img[(a, b, 1)] = (F(1 - 2 * a), F(3 - 6 * b), F(1))
    return img


def test_twisted_voxel_is_rejected_although_its_corners_are_positive():
    img = twisted_voxel()
    h = voxel_hex(img, (0, 0, 0))
    assert sorted(set(corner_jacobians(h))) == [4, 12]
    assert min(jacobian_bernstein(h)) == -8
    # det Dg = 4 (1 - 2 w)(1 - 4 w), negative for 1/4 < w < 1/2
    for w in (0, F(1, 4), F(1, 3), F(1, 2), 1):
        assert jacobian_det(h, F(1, 2), F(1, 2), w) == 4 * (1 - 2 * w) * (1 - 4 * w)
    for s in (1, 2, 3, 4):
        assert polycube_grid([(0, 0, 0)], img, s) is None
    # without the test the grid of resolution 3 has inverted hexes
    mins = {s: min(min(corner_jacobians(hx)) for hx in unchecked_grid([(0, 0, 0)], img, s)) for s in (1, 2, 3)}
    assert mins == {1: 4, 2: 0, 3: F(-4, 243)}


def test_affine_maps():
    rng = random.Random(11)
    for _ in range(12):
        while True:
            a = [[F(rng.randint(-3, 3), 2) for _ in range(3)] for _ in range(3)]
            d = (
                a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
                - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
            )
            if d > 0:
                break
        voxels = random_polycube(rng, 3)
        img = {}
        for c in voxels:
            for r in REF:
                k = tuple(c[t] + r[t] for t in range(3))
                img[k] = tuple(sum(a[i][j] * k[j] for j in range(3)) + i for i in range(3))
        s = rng.randint(1, 2)
        points, hexes = polycube_grid(voxels, img, s)
        for hx in hex_points(points, hexes):
            assert set(corner_jacobians(hx)) == {d / s**3}
        assert check_mesh(voxels, img, s)


def random_polycube(rng, size):
    cells = {(rng.randint(0, 2), rng.randint(0, 2), rng.randint(0, 1))}
    while len(cells) < size:
        c = list(rng.choice(sorted(cells)))
        t = rng.randrange(3)
        c[t] += rng.choice((-1, 1))
        cells.add(tuple(c))
    return sorted(cells)


def test_random_polycubes():
    rng = random.Random(2016)
    meshed = 0
    for trial in range(500):
        voxels = random_polycube(rng, rng.choice((1, 1, 1, 2, 2, 3)))
        # integer images: the identity scaled by 8 plus a random move, which keeps the arithmetic fast
        img = identity_images(voxels)
        spread = rng.choice((1, 2, 3))
        for k in img:
            img[k] = tuple(8 * k[t] + rng.randint(-spread, spread) for t in range(3))
        s = rng.choice((1, 1, 2, 2, 3))
        ok = check_mesh(voxels, img, s, full=(trial % 100 == 0))
        meshed += ok
        if trial % 20 == 0:
            # the 27 coefficients reproduce det J at a random point (checks the Bernstein form)
            h = voxel_hex(img, voxels[0])
            u, v, w = (F(rng.randint(0, 12), 12) for _ in range(3))
            coeffs = jacobian_bernstein(h)
            assert bernstein_value(coeffs, u, v, w) == jacobian_det(h, u, v, w)
            if ok:
                assert jacobian_det(h, u, v, w) >= min(coeffs) > 0
    assert 100 < meshed < 500
