# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warnock-algorithm/. The authors are listed in prov/NST03R.jsonl.

import random
from fractions import Fraction

from warnock_algorithm import warnock

HALF = Fraction(1, 2)


def inside_perturbed(tri, px, py):
    a, b, c = [(v[0], v[1]) for v in tri]
    area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if area == 0:
        return False
    if area < 0:
        b, c = c, b
    for (ax, ay), (bx, by) in ((b, c), (c, a), (a, b)):
        e0 = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
        lead = next((x for x in (e0, -(by - ay), bx - ax) if x != 0), 0)
        if lead <= 0:
            return False
    return True


def plane_depth(tri, px, py):
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    return az - Fraction(nx * (px - ax) + ny * (py - ay), nz)


def brute(width, height, tris, background=None):
    out = [[background] * width for _ in range(height)]
    for j in range(height):
        for i in range(width):
            hits = [(plane_depth(t, i + HALF, j + HALF), k) for k, t in enumerate(tris)
                    if inside_perturbed(t, i + HALF, j + HALF)]
            if hits:
                out[j][i] = min(hits)[1]
    return out


def rand_scene(rng, n, w, h, den):
    return [tuple((Fraction(rng.randint(-2 * den, (w + 2) * den), den),
                   Fraction(rng.randint(-2 * den, (h + 2) * den), den),
                   Fraction(rng.randint(0, 30), den)) for _ in range(3)) for _ in range(n)]


def test_example():
    # A far triangle F that surrounds the screen and a near triangle N.
    far = ((-1, -1, 9), (20, -1, 9), (-1, 20, 9))
    near = ((0, 0, 1), (6, 0, 1), (0, 6, 1))
    img, windows = warnock(8, 8, [far, near], ".")
    rows = ["".join("FN"[k] for k in row) for row in img]
    assert rows == ["NNNNNFFF", "NNNNFFFF", "NNNFFFFF", "NNFFFFFF",
                    "NFFFFFFF", "FFFFFFFF", "FFFFFFFF", "FFFFFFFF"]
    assert img == brute(8, 8, [far, near], ".")
    assert windows == 1 + 4 + 12 + 12


def test_against_brute_force():
    rng = random.Random(1969)
    for _ in range(80):
        w, h = rng.randint(1, 11), rng.randint(1, 9)
        tris = rand_scene(rng, rng.randint(0, 6), w, h, rng.choice([1, 2, 3]))
        img, _ = warnock(w, h, tris)
        assert img == brute(w, h, tris)


def test_interpenetrating():
    a = ((0, 0, 0), (8, 0, 0), (4, 6, 12))
    b = ((0, 6, 0), (8, 6, 0), (4, 0, 12))
    img, _ = warnock(8, 6, [a, b])
    assert img == brute(8, 6, [a, b])


def test_empty_and_one_surrounding():
    assert warnock(3, 2, [], 0)[0] == [[0, 0, 0], [0, 0, 0]]
    big = ((-10, -10, 1), (30, -10, 1), (-10, 30, 1))
    img, windows = warnock(5, 5, [big])
    assert img == [[0] * 5 for _ in range(5)] and windows == 1
