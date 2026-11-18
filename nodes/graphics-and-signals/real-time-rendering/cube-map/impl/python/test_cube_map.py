# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cube-map/. The authors are listed in prov/M0T5ZN.jsonl.

"""Tests of the cube map against ray-plane intersection, a dict model and quadrature.

The face selection is compared with a brute force intersection of the ray
with the six face planes, direction to face and back is a round trip, the
texel of a texel center is that texel, random stores and lookups agree with
a dict model, and the texel solid angles match a direct quadrature and add
up to 4 pi.
"""

import math
import random

from cube_map import CubeMap, face_coords, face_direction, major_axis

AXES = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def rand_dir(rng: random.Random) -> tuple[float, float, float]:
    while True:
        v = (rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))
        r = math.sqrt(sum(c * c for c in v))
        if r > 1e-6:
            return (v[0] / r, v[1] / r, v[2] / r)


def face_by_ray_planes(d) -> int:
    """Brute force: the face plane the ray from the center hits inside the square."""
    best, best_t = -1, math.inf
    for f, a in enumerate(AXES):
        dn = sum(x * y for x, y in zip(d, a))
        if dn <= 0:
            continue
        t = 1.0 / dn
        p = [t * c for c in d]
        others = [p[k] for k in range(3) if a[k] == 0]
        if all(abs(c) <= 1.0 + 1e-12 for c in others) and t < best_t:
            best, best_t = f, t
    return best


def test_face_matches_ray_plane_intersection() -> None:
    rng = random.Random(1)
    for _ in range(3000):
        d = rand_dir(rng)
        assert major_axis(d) == face_by_ray_planes(d)


def test_check_value_of_the_page() -> None:
    face, s, t = face_coords((0.3, -0.8, 0.5))
    assert face == 3 and abs(s - 0.6875) < 1e-15 and abs(t - 0.1875) < 1e-15
    c = CubeMap(4)
    assert c.texel_of((0.3, -0.8, 0.5)) == (3, 2, 0)


def test_direction_round_trip() -> None:
    rng = random.Random(2)
    for _ in range(3000):
        d = rand_dir(rng)
        face, s, t = face_coords(d)
        assert 0.0 <= s <= 1.0 and 0.0 <= t <= 1.0
        back = face_direction(face, s, t)
        assert all(abs(a - b) < 1e-12 for a, b in zip(back, d))
        # Scaling the direction changes nothing.
        assert face_coords((3 * d[0], 3 * d[1], 3 * d[2]))[0] == face


def test_face_centers_and_edges() -> None:
    for f, a in enumerate(AXES):
        assert all(abs(x - y) < 1e-15 for x, y in zip(face_direction(f, 0.5, 0.5), a))
    rng = random.Random(3)
    # A point on the edge of one face lies on the edge of a neighbor face.
    for _ in range(500):
        f = rng.randrange(6)
        u = rng.random()
        for s, t in ((0.0, u), (1.0, u), (u, 0.0), (u, 1.0)):
            d = face_direction(f, s, t)
            g, s2, t2 = face_coords(d)
            assert all(abs(x - y) < 1e-12 for x, y in zip(face_direction(g, s2, t2), d))
            if g != f:
                assert min(s2, 1 - s2, t2, 1 - t2) < 1e-12


def test_texel_center_round_trip() -> None:
    for n in (1, 2, 3, 8):
        c = CubeMap(n)
        for f in range(6):
            for j in range(n):
                for i in range(n):
                    assert c.texel_of(c.texel_direction(f, i, j)) == (f, i, j)


def test_random_operations_against_a_dict() -> None:
    rng = random.Random(4)
    n = 5
    c = CubeMap(n)
    model = {}
    for _ in range(3000):
        if rng.random() < 0.5:
            key = (rng.randrange(6), rng.randrange(n), rng.randrange(n))
            v = rng.uniform(-10, 10)
            c.store(*key, v)
            model[key] = v
        else:
            d = rand_dir(rng)
            assert c.lookup(d) == model.get(c.texel_of(d), 0.0)
            key = (rng.randrange(6), rng.randrange(n), rng.randrange(n))
            assert c.lookup(c.texel_direction(*key)) == model.get(key, 0.0)
        c.check_invariant()


def test_solid_angles() -> None:
    n = 6
    c = CubeMap(n)
    total = sum(c.texel_solid_angle(f, i, j) for f in range(6) for i in range(n) for j in range(n))
    assert abs(total - 4 * math.pi) < 1e-12
    # Direct quadrature of dA / (1 + x^2 + y^2)^(3/2) on the face plane.
    k = 40
    for i, j in ((0, 0), (2, 3), (5, 1)):
        x0, y0, h = 2 * i / n - 1, 2 * j / n - 1, 2 / n
        q = 0.0
        for a in range(k):
            for b in range(k):
                x = x0 + (a + 0.5) * h / k
                y = y0 + (b + 0.5) * h / k
                q += (h / k) ** 2 / (1 + x * x + y * y) ** 1.5
        assert abs(q - c.texel_solid_angle(0, i, j)) < 1e-4 * q
    # A corner texel is smaller than a center texel.
    assert c.texel_solid_angle(0, 0, 0) < c.texel_solid_angle(0, 2, 2)


def test_fill_and_bilinear() -> None:
    c = CubeMap(8)
    c.fill(lambda d: d[0] + 2 * d[1] - d[2])
    for f in range(6):
        for j in range(8):
            for i in range(8):
                d = c.texel_direction(f, i, j)
                assert abs(c.lookup(d) - (d[0] + 2 * d[1] - d[2])) < 1e-12
                assert abs(c.lookup_bilinear(d) - c.lookup(d)) < 1e-12
