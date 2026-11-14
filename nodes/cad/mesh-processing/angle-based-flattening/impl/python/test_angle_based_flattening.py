# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/angle-based-flattening/. The authors are listed in prov/1YT62Y.jsonl.

import math
import random
from fractions import Fraction

from angle_based_flattening import (
    abf_angles,
    constraints,
    corner_angles_3d,
    corners_at,
    inner_vertices,
    layout,
    layout_residual,
    objective,
    target_angles,
)
from mp3geom import orient2d


def grid(rng, nx, ny, jitter):
    """A planar grid with random diagonals and rational jitter, all triangles counterclockwise."""
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


def bump(rng, n, height=1.5):
    pts, faces = grid(rng, n, n, 0)
    out = {}
    for v, (x, y) in pts.items():
        r2 = (float(x) - n / 2) ** 2 + (float(y) - n / 2) ** 2
        out[v] = (float(x), float(y), height * math.exp(-r2 / 2))
    return out, faces


def exact_orient(x, f):
    """ORIENT2D of the computed float points, evaluated exactly."""
    return orient2d(*([Fraction(c) for c in x[v]] for v in f))


def similarity_error(pts, x, v0, v1):
    p = {v: complex(float(a), float(b)) for v, (a, b) in pts.items()}
    q = {v: complex(*x[v]) for v in x}
    a = (q[v1] - q[v0]) / (p[v1] - p[v0])
    b = q[v0] - a * p[v0]
    return max(abs(a * p[v] + b - q[v]) for v in p)


def test_flat_mesh_maps_to_a_similar_copy() -> None:
    rng = random.Random(2001)
    for _ in range(10):
        pts, faces = grid(rng, rng.randint(1, 4), rng.randint(1, 4), 3)
        alpha, _ = abf_angles(pts, faces)
        x = layout(pts, faces, alpha)
        assert similarity_error(pts, x, faces[0][0], faces[0][1]) < 1e-9
        assert objective(alpha, target_angles(pts, faces)) < 1e-20


def test_constraints_layout_and_orientation_on_a_bump() -> None:
    rng = random.Random(11)
    for n, height in ((3, 1.0), (4, 1.5), (5, 2.5)):
        pts, faces = bump(rng, n, height)
        alpha, iters = abf_angles(pts, faces)
        c, _ = constraints(faces, alpha, inner_vertices(faces), corners_at(faces))
        assert max(abs(v) for v in c) < 1e-10
        assert iters <= 20
        x = layout(pts, faces, alpha)
        assert layout_residual(faces, alpha, x) < 1e-9
        assert all(exact_orient(x, f) > 0 for f in faces)


def test_without_the_wheel_condition_the_layout_does_not_close() -> None:
    rng = random.Random(11)
    pts, faces = bump(rng, 4, 1.5)
    alpha, _ = abf_angles(pts, faces, wheel=False)
    x = layout(pts, faces, alpha)
    assert layout_residual(faces, alpha, x) > 1e-3


def test_objective_not_above_other_valid_flattenings() -> None:
    # Measured, not proved: the angles of other valid flat meshes with the same
    # connectivity satisfy the constraints, and ABF finds a lower objective.
    rng = random.Random(23)
    pts, faces = bump(rng, 4, 1.5)
    beta = target_angles(pts, faces)
    best = objective(abf_angles(pts, faces)[0], beta)
    for _ in range(10):
        flat, _ = grid(random.Random(rng.random()), 4, 4, 3)
        flat_faces_ok = all(orient2d(flat[a], flat[b], flat[c]) > 0 for a, b, c in faces)
        if not flat_faces_ok:
            continue
        other = corner_angles_3d(flat, faces)
        assert best <= objective(other, beta) + 1e-12
    proj = {v: (p[0], p[1]) for v, p in pts.items()}
    assert best < objective(corner_angles_3d(proj, faces), beta)


def test_saddle_wheel_does_not_fold() -> None:
    n, h = 6, 2.0
    pts = {i: (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n), h * (-1) ** i) for i in range(n)}
    pts[n] = (0.0, 0.0, 0.0)
    faces = [(i, (i + 1) % n, n) for i in range(n)]
    alpha, _ = abf_angles(pts, faces)
    assert all(abs(a - math.pi / 3) < 1e-12 for a in alpha)
    x = layout(pts, faces, alpha)
    assert all(exact_orient(x, f) > 0 for f in faces)


def test_example_of_the_page() -> None:
    pts = {0: (-1, -1, 0), 1: (1, -1, 0), 2: (1, 1, 0), 3: (-1, 1, 0), 4: (0, 0, 1)}
    faces = [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]
    beta3 = corner_angles_3d(pts, faces)
    assert abs(beta3[2] - math.acos(1 / 3)) < 1e-12
    assert abs(beta3[0] - math.atan(math.sqrt(2))) < 1e-12
    beta = target_angles(pts, faces)
    assert abs(beta[2] - math.pi / 2) < 1e-12
    alpha, iters = abf_angles(pts, faces)
    assert iters == 2
    for f in range(4):
        assert abs(alpha[3 * f] - math.pi / 4) < 1e-12
        assert abs(alpha[3 * f + 1] - math.pi / 4) < 1e-12
        assert abs(alpha[3 * f + 2] - math.pi / 2) < 1e-12
    b = math.atan(math.sqrt(2))
    assert abs(objective(alpha, beta) - 8 * ((math.pi / 4 - b) / b) ** 2) < 1e-12
    x = layout(pts, faces, alpha)
    want = {0: (0, 0), 1: (2, 0), 2: (2, 2), 3: (0, 2), 4: (1, 1)}
    for v, (u, w) in want.items():
        assert abs(x[v][0] - u) < 1e-12 and abs(x[v][1] - w) < 1e-12
