# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multisample-antialiasing/. The authors are listed in prov/X9CB9D.jsonl.

import random
from fractions import Fraction as F

from multisample_antialiasing import ROTATED_GRID_4, multisample_antialiasing

BLACK = (F(0),)


def lex_sign(*terms):
    for t in terms:
        if t != 0:
            return 1 if t > 0 else -1
    return 0


def owns(tri, px, py):
    """Ownership by symbolic perturbation: is p + (eps, eps^2) strictly inside the triangle?"""
    (ax, ay, _), (bx, by, _), (cx, cy, _), _ = tri
    area = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    if area == 0:
        return False
    want = 1 if area > 0 else -1
    for (sx, sy), (ex, ey) in (((ax, ay), (bx, by)), ((bx, by), (cx, cy)), ((cx, cy), (ax, ay))):
        e = (ex - sx) * (py - sy) - (ey - sy) * (px - sx)
        gx, gy = -(ey - sy), ex - sx  # gradient of e in (px, py)
        if lex_sign(e, gx, gy) != want:
            return False
    return True


def plane_depth(tri, px, py):
    """Depth of the plane through the three vertices, by Cramer's rule."""
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2), _ = tri
    det = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    s = ((px - x0) * (y2 - y0) - (x2 - x0) * (py - y0)) / det
    t = ((x1 - x0) * (py - y0) - (px - x0) * (y1 - y0)) / det
    return z0 + s * (z1 - z0) + t * (z2 - z0)


def visible(tris, px, py):
    best, best_z = None, None
    for k, tri in enumerate(tris):
        if owns(tri, px, py):
            z = plane_depth(tri, px, py)
            if best is None or z < best_z:
                best, best_z = k, z
    return best


def random_scene(rng, w, h, count):
    tris = []
    for k in range(count):
        verts = tuple((F(rng.randint(-4, 8 * w + 4), 8), F(rng.randint(-4, 8 * h + 4), 8), F(rng.randint(0, 20), 4)) for _ in range(3))
        tris.append(verts + ((F(k + 1), F(rng.randint(0, 9))),))
    return tris


def random_pattern(rng):
    n = rng.choice([1, 2, 4, 8])
    if n == 4 and rng.random() < 0.5:
        return ROTATED_GRID_4
    return [(F(rng.randint(0, 15), 16), F(rng.randint(0, 15), 16)) for _ in range(n)]


def test_example() -> None:
    tri = ((F(3, 5), F(2, 5), F(0)), (F(7, 2), F(1), F(0)), (F(1), F(3), F(0)), (F(1),))
    image, _, calls = multisample_antialiasing([tri], 4, 3, ROTATED_GRID_4, BLACK)
    got = [[int(p[0] * 4) for p in row] for row in image]
    assert got == [[0, 2, 1, 0], [1, 4, 3, 0], [0, 2, 0, 0]]
    assert calls == 6
    # two planes that cross inside one pixel: the samples split by depth
    red = ((F(0), F(0), F(0)), (F(2), F(0), F(4)), (F(0), F(2), F(0)), (F(1), F(0)))
    blue = ((F(0), F(0), F(1)), (F(2), F(0), F(1)), (F(0), F(2), F(1)), (F(0), F(1)))
    image, samples, calls = multisample_antialiasing([red, blue], 1, 1, ROTATED_GRID_4, (F(0), F(0)))
    assert calls == 2
    assert samples[0][0] == [(F(1), F(0)), (F(0), F(1)), (F(1), F(0)), (F(0), F(1))]
    assert image[0][0] == (F(1, 2), F(1, 2))


def test_samples_match_brute_force_visibility() -> None:
    rng = random.Random(1993)
    for _ in range(500):
        w, h = rng.randint(1, 4), rng.randint(1, 3)
        tris = random_scene(rng, w, h, rng.randint(1, 4))
        pattern = random_pattern(rng)
        image, samples, calls = multisample_antialiasing(tris, w, h, pattern, BLACK + (F(0),))
        touched = 0
        for j in range(h):
            for i in range(w):
                expect = []
                for ox, oy in pattern:
                    k = visible(tris, i + ox, j + oy)
                    expect.append(BLACK + (F(0),) if k is None else tris[k][3])
                assert samples[j][i] == expect
                n = len(pattern)
                assert image[j][i] == tuple(sum(c[q] for c in expect) / F(n) for q in range(2))
                touched += sum(1 for tri in tris if any(owns(tri, i + ox, j + oy) for ox, oy in pattern))
        assert calls == touched


def test_shading_once_per_pixel_at_the_center() -> None:
    rng = random.Random(5)
    for _ in range(200):
        w, h = rng.randint(1, 4), rng.randint(1, 3)
        tris = random_scene(rng, w, h, rng.randint(1, 3))
        log = []

        def shade(t, x, y):
            log.append((t, x, y))
            return (x + 10 * y + 100 * t,)

        _, samples, calls = multisample_antialiasing(tris, w, h, ROTATED_GRID_4, (F(-1),), shade)
        assert calls == len(log) == len(set(log))
        for j in range(h):
            for i in range(w):
                for m, (ox, oy) in enumerate(ROTATED_GRID_4):
                    k = visible(tris, i + ox, j + oy)
                    want = (F(-1),) if k is None else (i + F(1, 2) + 10 * (j + F(1, 2)) + 100 * k,)
                    assert samples[j][i][m] == want


def test_top_left_rule_on_a_fan() -> None:
    # a fan around an interior vertex tiles the square [0, 4] x [0, 4]: every sample belongs to one triangle
    rng = random.Random(8)
    for _ in range(60):
        cx, cy = F(rng.randint(1, 15), 4), F(rng.randint(1, 15), 4)
        ring = [(F(0), F(0)), (F(2), F(0)), (F(4), F(0)), (F(4), F(2)), (F(4), F(4)), (F(2), F(4)), (F(0), F(4)), (F(0), F(2))]
        tris = []
        for k in range(len(ring)):
            (ax, ay), (bx, by) = ring[k], ring[(k + 1) % len(ring)]
            if rng.random() < 0.5:
                (ax, ay), (bx, by) = (bx, by), (ax, ay)
            tris.append(((cx, cy, F(0)), (ax, ay, F(0)), (bx, by, F(0)), (F(k + 1),)))
        pattern = [(F(a, 4), F(b, 4)) for a in range(1, 4) for b in range(1, 4)]
        _, samples, _ = multisample_antialiasing(tris, 4, 4, pattern, (F(0),))
        for j in range(4):
            for i in range(4):
                for m, (ox, oy) in enumerate(pattern):
                    owners = [k for k, tri in enumerate(tris) if owns(tri, i + ox, j + oy)]
                    assert len(owners) == 1
                    assert samples[j][i][m] == tris[owners[0]][3]


def test_degenerate_and_float() -> None:
    flat = ((F(0), F(0), F(0)), (F(1), F(1), F(0)), (F(2), F(2), F(0)), (F(1),))
    image, _, calls = multisample_antialiasing([flat], 2, 2, ROTATED_GRID_4, (F(0),))
    assert calls == 0 and image == [[(F(0),)] * 2] * 2
    tri = ((0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 2.0, 0.0), (1.0,))
    image, _, _ = multisample_antialiasing([tri], 2, 2, ROTATED_GRID_4, (0.0,))
    assert image[0][0] == (1.0,) and image[1][1] == (0.0,)
