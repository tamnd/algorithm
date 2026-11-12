# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/depth-peeling/. The authors are listed in prov/0TEAXT.jsonl.

import random
from fractions import Fraction

from depth_peeling import composite, peel_layers

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


def sorted_fragments(width, height, tris):
    """Brute force: all fragments of each pixel, sorted by (depth, index)."""
    return [[sorted((plane_depth(t, i + HALF, j + HALF), k) for k, t in enumerate(tris)
                    if inside_perturbed(t, i + HALF, j + HALF))
             for i in range(width)] for j in range(height)]


def rand_scene(rng, n, w, h, den):
    return [tuple((Fraction(rng.randint(-den, (w + 1) * den), den),
                   Fraction(rng.randint(-den, (h + 1) * den), den),
                   Fraction(rng.randint(0, 30), den)) for _ in range(3)) for _ in range(n)]


def test_example():
    # Three nested squares at depths 3, 1 and 2, drawn in this order.
    def square(x0, y0, x1, y1, z):
        return [((x0, y0, z), (x1, y0, z), (x1, y1, z)), ((x0, y0, z), (x1, y1, z), (x0, y1, z))]
    tris = square(0, 0, 6, 1, 3) + square(0, 0, 4, 1, 1) + square(2, 0, 6, 1, 2)
    layers = peel_layers(6, 1, tris)
    name = lambda k: "." if k is None else "ABC"[k // 2]
    assert ["".join(name(k) for k in layer[0]) for layer in layers] == ["BBBBCC", "AACCAA", "..AA.."]


def test_layers_against_sorted_fragments():
    rng = random.Random(2001)
    for _ in range(50):
        w, h = rng.randint(1, 7), rng.randint(1, 6)
        tris = rand_scene(rng, rng.randint(0, 7), w, h, rng.choice([1, 2, 3]))
        frags = sorted_fragments(w, h, tris)
        layers = peel_layers(w, h, tris, tie_break=True)
        depth_complexity = max((len(f) for row in frags for f in row), default=0)
        assert len(layers) == depth_complexity
        for j in range(h):
            for i in range(w):
                want = [k for _, k in frags[j][i]]
                got = [layer[j][i] for layer in layers if layer[j][i] is not None]
                assert got == want


def test_composite_against_back_to_front_over():
    rng = random.Random(1989)
    for _ in range(30):
        w, h = rng.randint(1, 6), rng.randint(1, 5)
        tris = rand_scene(rng, rng.randint(0, 6), w, h, 2)
        cols = [(rng.randint(0, 9), rng.randint(0, 9)) for _ in tris]
        alphas = [rng.choice([Fraction(1, 2), Fraction(1, 3), Fraction(1), Fraction(0)]) for _ in tris]
        bg = [[(1, 2)] * w for _ in range(h)]
        got = composite(peel_layers(w, h, tris, tie_break=True), cols, alphas, bg)
        frags = sorted_fragments(w, h, tris)
        for j in range(h):
            for i in range(w):
                c = [Fraction(x) for x in bg[j][i]]
                for _, k in reversed(frags[j][i]):  # back to front, "over"
                    a = Fraction(alphas[k])
                    c = [a * cols[k][t] + (1 - a) * c[t] for t in range(2)]
                assert got[j][i] == tuple(c)


def test_depth_only_peel_loses_coplanar_fragments():
    t = ((0, 0, 1), (4, 0, 1), (0, 4, 1))
    assert len(peel_layers(4, 4, [t, t], tie_break=True)) == 2
    assert len(peel_layers(4, 4, [t, t], tie_break=False)) == 1


def test_max_layers():
    rng = random.Random(3)
    tris = rand_scene(rng, 8, 5, 5, 1)
    full = peel_layers(5, 5, tris, tie_break=True)
    assert peel_layers(5, 5, tris, max_layers=2, tie_break=True) == full[:2]
