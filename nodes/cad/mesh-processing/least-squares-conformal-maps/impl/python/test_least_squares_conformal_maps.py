# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-conformal-maps/. The authors are listed in prov/67C616.jsonl.

import math
import random
from fractions import Fraction

import pytest

from least_squares_conformal_maps import dirichlet_energy, image_area, lscm, lscm_energy
from mp3geom import orient2d


def grid(rng, nx, ny, jitter):
    """A planar grid of (nx+1) x (ny+1) vertices with random diagonals and rational jitter."""
    while True:
        pts = {}
        for i in range(nx + 1):
            for j in range(ny + 1):
                dx = Fraction(rng.randint(-jitter, jitter), 4 * jitter + 1) if jitter else 0
                dy = Fraction(rng.randint(-jitter, jitter), 4 * jitter + 1) if jitter else 0
                pts[i * (ny + 1) + j] = (i + dx, j + dy)
        faces = []
        for i in range(nx):
            for j in range(ny):
                a, b, c, d = i * (ny + 1) + j, (i + 1) * (ny + 1) + j, (i + 1) * (ny + 1) + j + 1, i * (ny + 1) + j + 1
                faces += [(a, b, c), (a, c, d)] if rng.random() < 0.5 else [(a, b, d), (b, c, d)]
        if all(orient2d(pts[a], pts[b], pts[c]) > 0 for a, b, c in faces):
            return pts, faces


def similarity(p0, p1, t0, t1):
    """The map z -> a z + b with a p0 + b = t0 and a p1 + b = t1, in exact complex arithmetic."""
    dzr, dzi = p1[0] - p0[0], p1[1] - p0[1]
    dtr, dti = t1[0] - t0[0], t1[1] - t0[1]
    den = dzr * dzr + dzi * dzi
    ar, ai = (dtr * dzr + dti * dzi) / den, (dti * dzr - dtr * dzi) / den
    br, bi = t0[0] - (ar * p0[0] - ai * p0[1]), t0[1] - (ar * p0[1] + ai * p0[0])
    return lambda z: (ar * z[0] - ai * z[1] + br, ar * z[1] + ai * z[0] + bi)


def test_planar_mesh_is_reproduced_up_to_a_similarity_exactly() -> None:
    rng = random.Random(2002)
    for _ in range(12):
        pts, faces = grid(rng, rng.randint(1, 4), rng.randint(1, 4), 3)
        v0, v1 = rng.sample(sorted(pts), 2)
        t0 = (Fraction(rng.randint(-9, 9)), Fraction(rng.randint(-9, 9)))
        t1 = (t0[0] + rng.randint(1, 9), t0[1] + rng.randint(-9, 9))
        uv = lscm(pts, faces, {v0: t0, v1: t1})
        s = similarity(pts[v0], pts[v1], t0, t1)
        for v in pts:
            assert uv[v] == s(pts[v])
        assert lscm_energy(pts, faces, uv) == 0


def strip(turns_quarter):
    """A planar strip around a square, one quarter turn per step; it overlaps itself after 4 steps."""
    inner = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    outer = [(2, 2), (-2, 2), (-2, -2), (2, -2)]
    pts, faces = {}, []
    for t in range(turns_quarter + 1):
        pts[2 * t] = inner[t % 4]
        pts[2 * t + 1] = outer[t % 4]
    for t in range(turns_quarter):
        i0, o0, i1, o1 = 2 * t, 2 * t + 1, 2 * t + 2, 2 * t + 3
        faces += [(i0, o0, o1), (i0, o1, i1)]
    return pts, faces


def test_pins_at_one_point_of_an_immersed_strip_are_singular() -> None:
    pts, faces = strip(6)
    assert pts[0] == pts[8]
    with pytest.raises(ValueError):
        lscm(pts, faces, {0: (0, 0), 8: (1, 0)})
    uv = lscm(pts, faces, {0: (0, 0), 1: (1, 0)})
    s = similarity(pts[0], pts[1], (0, 0), (1, 0))
    assert all(uv[v] == s(pts[v]) for v in pts)


def test_folded_developable_strip_unfolds() -> None:
    rng = random.Random(5)
    flat, faces = grid(rng, 6, 2, 0)
    folded = {}
    for v, (x, y) in flat.items():
        if x <= 3:
            folded[v] = (x, y, 0)
        else:
            folded[v] = (3 + Fraction(3, 5) * (x - 3), y, Fraction(4, 5) * (x - 3))
    uv = lscm(folded, faces, {0: (0.0, 0.0), 1: (0.0, 1.0)})
    for v in flat:
        assert abs(uv[v][0] - float(flat[v][0])) < 1e-9
        assert abs(uv[v][1] - float(flat[v][1])) < 1e-9


def bump(rng, n):
    pts, faces = grid(rng, n, n, 0)
    out = {}
    for v, (x, y) in pts.items():
        r2 = (float(x) - n / 2) ** 2 + (float(y) - n / 2) ** 2
        out[v] = (float(x), float(y), 1.5 * math.exp(-r2 / 2))
    return out, faces


def test_energy_identity_and_minimality_on_a_curved_mesh() -> None:
    rng = random.Random(77)
    pts, faces = bump(rng, 4)
    pins = {0: (0.0, 0.0), 24: (4.0, 4.0)}
    uv = lscm(pts, faces, pins)
    e = lscm_energy(pts, faces, uv)
    assert e > 1e-3                                      # the bump is not developable
    for trial in range(5):
        u = {v: (rng.uniform(-3, 3), rng.uniform(-3, 3)) for v in pts}
        lhs = lscm_energy(pts, faces, u)
        rhs = 2 * dirichlet_energy(pts, faces, u) - 2 * image_area(faces, u)
        assert abs(lhs - rhs) < 1e-9 * max(1.0, abs(lhs))
    for trial in range(20):
        w = {v: (x + (0 if v in pins else rng.uniform(-1e-3, 1e-3)), y + (0 if v in pins else rng.uniform(-1e-3, 1e-3))) for v, (x, y) in uv.items()}
        assert lscm_energy(pts, faces, w) >= e - 1e-12
    assert all(exact_orient(uv, f) > 0 for f in faces)


def exact_orient(uv, f):
    """ORIENT2D of the computed float points, evaluated exactly."""
    return orient2d(*([Fraction(x) for x in uv[v]] for v in f))


def test_saddle_wheel_folds() -> None:
    # Six triangles around a flat centre, with the rim at heights +2 and -2 in turn.
    # The angle sum at the centre is above 2 pi, and LSCM folds two triangles.
    n, h = 6, 2.0
    pts = {i: (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n), h * (-1) ** i) for i in range(n)}
    pts[n] = (0.0, 0.0, 0.0)
    faces = [(i, (i + 1) % n, n) for i in range(n)]
    uv = lscm(pts, faces, {0: (0.0, 0.0), 3: (1.0, 0.0)})
    signs = [exact_orient(uv, f) for f in faces]
    assert sum(s < 0 for s in signs) == 2
    assert min(signs) < -0.03                       # far from rounding level


def test_example_of_the_page() -> None:
    pts = {0: (-1, -1, 0), 1: (1, -1, 0), 2: (1, 1, 0), 3: (-1, 1, 0), 4: (0, 0, 1)}
    faces = [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]
    uv = lscm(pts, faces, {0: (0.0, 0.0), 2: (2.0, 2.0)})
    assert abs(uv[4][0] - 1) < 1e-12 and abs(uv[4][1] - 1) < 1e-12
    r = 2 * math.sqrt(2) / 3
    assert abs(uv[1][0] - (1 + r)) < 1e-12 and abs(uv[1][1] - (1 - r)) < 1e-12
    assert abs(uv[3][0] - (1 - r)) < 1e-12 and abs(uv[3][1] - (1 + r)) < 1e-12
    assert abs(lscm_energy(pts, faces, uv) - math.sqrt(2) / 3) < 1e-12
    assert abs(image_area(faces, uv) - 8 * math.sqrt(2) / 3) < 1e-12
