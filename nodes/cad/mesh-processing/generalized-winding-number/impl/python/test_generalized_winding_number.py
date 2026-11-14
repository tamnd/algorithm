# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-winding-number/. The authors are listed in prov/CVGJTP.jsonl.

import math
import random
from fractions import Fraction

from generalized_winding_number import (
    build_tree,
    exact_ray_winding,
    solid_angle,
    winding_number,
    winding_number_tree,
)

QUADS = [  # the six faces of the unit cube, counterclockwise seen from outside
    ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)),
    ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)),
    ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)),
    ((0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)),
    ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)),
    ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)),
]


def add_cube(points, faces, origin, size, flip=False):
    """Append an axis-aligned cube; its faces point outward unless flip."""
    index = {}
    for q in QUADS:
        ids = []
        for v in q:
            if v not in index:
                index[v] = len(points)
                points.append(tuple(o + size * x for o, x in zip(origin, v)))
            ids.append(index[v])
        a, b, c, d = ids
        tris = [(a, b, c), (a, c, d)]
        faces += [(x, z, y) for x, y, z in tris] if flip else tris


def polycube(rng, k=3, fill=0.5):
    """The boundary of a random union of unit cubes in a k x k x k grid."""
    cells = {(x, y, z) for x in range(k) for y in range(k) for z in range(k) if rng.random() < fill}
    cells.add((1, 1, 1))
    points, index, faces = [], {}, []

    def vid(v):
        if v not in index:
            index[v] = len(points)
            points.append(v)
        return index[v]

    for cell in cells:
        for q in QUADS:
            # the normal of the quad, from its first three corners
            normal = tuple(
                (q[1][(k1 + 1) % 3] - q[0][(k1 + 1) % 3]) * (q[2][(k1 + 2) % 3] - q[0][(k1 + 2) % 3])
                - (q[1][(k1 + 2) % 3] - q[0][(k1 + 2) % 3]) * (q[2][(k1 + 1) % 3] - q[0][(k1 + 1) % 3])
                for k1 in range(3)
            )
            if tuple(c + n for c, n in zip(cell, normal)) in cells:
                continue
            a, b, c, d = (vid(tuple(c0 + x for c0, x in zip(cell, v))) for v in q)
            faces += [(a, b, c), (a, c, d)]
    return points, faces, cells


def random_point(rng, lo, hi):
    return tuple(Fraction(rng.randint(lo * 97, hi * 97) * 2 + 1, 194) for _ in range(3))


def test_cube_is_one_inside_and_zero_outside() -> None:
    points, faces = [], []
    add_cube(points, faces, (0, 0, 0), 1)
    rng = random.Random(1)
    for _ in range(200):
        p = random_point(rng, -1, 2)
        exact = exact_ray_winding(points, faces, p, rng)
        assert exact in (0, 1)
        assert exact == (1 if all(0 < x < 1 for x in p) else 0)
        assert abs(winding_number(points, faces, p) - exact) < 1e-9


def test_polycubes_against_exact_ray_count() -> None:
    rng = random.Random(2013)
    for _ in range(6):
        points, faces, cells = polycube(rng)
        for _ in range(60):
            p = random_point(rng, -1, 4)
            exact = exact_ray_winding(points, faces, p, rng)
            inside = tuple(math.floor(x) for x in p) in cells
            assert exact == (1 if inside else 0)
            assert abs(winding_number(points, faces, p) - exact) < 1e-9


def test_nested_and_reversed_shells() -> None:
    points, faces = [], []
    add_cube(points, faces, (0, 0, 0), 3)
    add_cube(points, faces, (1, 1, 1), 1)
    add_cube(points, faces, (5, 0, 0), 1, flip=True)
    for p, want in (((Fraction(3, 2),) * 3, 2), ((Fraction(1, 2),) * 3, 1), ((Fraction(11, 2), Fraction(1, 2), Fraction(1, 2)), -1), ((Fraction(9, 2), 0, 0), 0)):
        assert exact_ray_winding(points, faces, p) == want
        assert abs(winding_number(points, faces, p) - want) < 1e-9


def test_open_mesh_jumps_by_one_across_a_face() -> None:
    points, faces = [], []
    add_cube(points, faces, (0, 0, 0), 1)
    faces = faces[2:]                         # remove the bottom face z = 0
    rng = random.Random(9)
    for _ in range(20):
        x, y = rng.uniform(0.1, 0.9), rng.uniform(0.1, 0.9)
        eps = 1e-6
        below = winding_number(points, faces, (x, y, 1 - eps))   # inside, behind the top face
        above = winding_number(points, faces, (x, y, 1 + eps))
        assert abs((below - above) - 1) < 1e-5
        assert 0 < below < 1 and -1 < above < 0.5
    # on the missing face the value is between 0 and 1
    w = winding_number(points, faces, (0.5, 0.5, 0.0))
    assert 0.3 < w < 0.7


def test_tree_equals_direct_sum() -> None:
    rng = random.Random(4)
    for _ in range(3):
        points, faces, _ = polycube(rng, k=4)
        holed = [f for i, f in enumerate(faces) if i % 17 != 3]
        for mesh in (faces, holed):
            tree = build_tree(points, mesh, leaf_size=6)
            for _ in range(40):
                p = tuple(rng.uniform(-1, 5) for _ in range(3))
                assert abs(winding_number_tree(points, mesh, tree, p) - winding_number(points, mesh, p)) < 1e-9


def test_solid_angle_of_an_octant() -> None:
    # the triangle with corners on the three axes covers one eighth of the sphere seen from the origin
    omega = solid_angle((1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0))
    assert abs(omega - 4 * math.pi / 8) < 1e-12
    assert abs(solid_angle((1, 0, 0), (0, 0, 1), (0, 1, 0), (0, 0, 0)) + 4 * math.pi / 8) < 1e-12


def test_example_of_the_page() -> None:
    points, faces = [], []
    add_cube(points, faces, (0, 0, 0), 1)
    centre = (0.5, 0.5, 0.5)
    for f in faces:
        assert abs(solid_angle(points[f[0]], points[f[1]], points[f[2]], centre) - math.pi / 3) < 1e-12
    assert abs(winding_number(points, faces, centre) - 1) < 1e-12
    assert abs(winding_number(points, faces, (1.5, 0.5, 0.5))) < 1e-12
    open_box = faces[2:]
    assert abs(winding_number(points, open_box, centre) - 5 / 6) < 1e-12
    assert abs(winding_number(points, open_box, (0.5, 0.5, 0.0)) - 1 / 2) < 1e-12


def test_float_fails_next_to_a_shared_edge() -> None:
    # The point is 1e-20 above the midpoint of the diagonal of the bottom face, inside the cube.
    points, faces = [], []
    add_cube(points, faces, (0, 0, 0), 1)
    p = (0.5, 0.5, 1e-20)
    assert exact_ray_winding(points, faces, p) == 1
    w = winding_number(points, faces, p)
    assert abs(w - 0.5) < 1e-3                # the float value cannot tell inside from outside
    assert abs(winding_number(points, faces, (0.3, 0.7, 1e-20)) - 1) < 1e-9
