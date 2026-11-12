# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a-buffer/. The authors are listed in prov/1XFX5C.jsonl.

import random
from fractions import Fraction

from a_buffer import a_buffer

HALF = Fraction(1, 2)


def inside_perturbed(tri, px, py):
    """Top-left rule as a perturbation: p + (t, t^2) strictly inside for small t > 0."""
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


def brute(width, height, tris, colors, alphas, bg, sx, sy, depth_at_sample):
    """Per subpixel sample: sort all covering triangles by depth, composite
    them front to back, then average the samples of the pixel."""
    out = []
    for j in range(height):
        row = []
        for i in range(width):
            acc = [Fraction(0)] * len(bg)
            for b in range(sy):
                for a in range(sx):
                    px = i + Fraction(2 * a + 1, 2 * sx)
                    py = j + Fraction(2 * b + 1, 2 * sy)
                    qx, qy = (px, py) if depth_at_sample else (i + HALF, j + HALF)
                    hits = sorted((plane_depth(t, qx, qy), k) for k, t in enumerate(tris)
                                  if inside_perturbed(t, px, py))
                    trans = Fraction(1)
                    for _, k in hits:
                        al = Fraction(alphas[k])
                        for c in range(len(bg)):
                            acc[c] += trans * al * colors[k][c]
                        trans *= 1 - al
                    for c in range(len(bg)):
                        acc[c] += trans * bg[c]
            row.append(tuple(x / (sx * sy) for x in acc))
        out.append(row)
    return out


def rand_scene(rng, n, w, h, flat):
    tris, cols, alphas = [], [], []
    for _ in range(n):
        z = Fraction(rng.randint(0, 40), 4)
        tri = tuple((Fraction(rng.randint(-2, 4 * w + 2), 4), Fraction(rng.randint(-2, 4 * h + 2), 4),
                     z if flat else Fraction(rng.randint(0, 40), 4)) for _ in range(3))
        tris.append(tri)
        cols.append((rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255)))
        alphas.append(rng.choice([1, 1, Fraction(1, 2), Fraction(1, 4), Fraction(3, 4)]))
    return tris, cols, alphas


def test_example():
    # A red half-pixel square at depth 1 over a blue triangle at depth 2.
    red = ((0, 0, 1), (Fraction(1, 2), 0, 1), (Fraction(1, 2), 1, 1))
    red2 = ((0, 0, 1), (Fraction(1, 2), 1, 1), (0, 1, 1))
    blue = ((0, 0, 2), (1, 0, 2), (0, 1, 2))
    img = a_buffer(1, 1, [red, red2, blue], [(255, 0, 0)] * 2 + [(0, 0, 255)],
                   [1, 1, 1], (0, 0, 0))
    # Red covers the 16 cells of the left half. Blue covers 16 cells, and 4 of
    # them are in the right half, so 4 blue cells stay visible.
    assert img[0][0] == (Fraction(255 * 16, 32), 0, Fraction(255 * 4, 32))
    # A green fragment with opacity 1/2 in front covers 12 cells: 1 over red,
    # 4 over blue and 7 over the background.
    green = ((Fraction(1, 4), 0, HALF), (1, 0, HALF), (1, 1, HALF))
    img = a_buffer(1, 1, [red, red2, blue, green],
                   [(255, 0, 0)] * 2 + [(0, 0, 255), (0, 255, 0)],
                   [1, 1, 1, HALF], (0, 0, 0))
    assert img[0][0] == (Fraction(7905, 64), Fraction(765, 16), Fraction(255, 16))


def test_against_brute_force_pixel_center_depth():
    rng = random.Random(1984)
    for _ in range(25):
        w, h = rng.randint(1, 4), rng.randint(1, 3)
        tris, cols, alphas = rand_scene(rng, rng.randint(0, 5), w, h, flat=False)
        sx, sy = rng.choice([(1, 1), (2, 2), (4, 2), (8, 4)])
        got = a_buffer(w, h, tris, cols, alphas, (10, 20, 30), sx, sy)
        assert got == brute(w, h, tris, cols, alphas, (10, 20, 30), sx, sy, False)


def test_flat_layers_match_exact_supersampling():
    # For triangles parallel to the screen the one depth per fragment is exact,
    # so the A-buffer equals compositing at each subpixel sample.
    rng = random.Random(84)
    for _ in range(25):
        w, h = rng.randint(1, 4), rng.randint(1, 3)
        tris, cols, alphas = rand_scene(rng, rng.randint(0, 5), w, h, flat=True)
        got = a_buffer(w, h, tris, cols, alphas, (0, 0, 0), 4, 4)
        assert got == brute(w, h, tris, cols, alphas, (0, 0, 0), 4, 4, True)


def test_one_sample_is_a_z_buffer():
    rng = random.Random(5)
    for _ in range(20):
        tris, cols, _ = rand_scene(rng, 5, 4, 4, flat=False)
        got = a_buffer(4, 4, tris, cols, [1] * 5, (0, 0, 0), 1, 1)
        for j in range(4):
            for i in range(4):
                c = (i + HALF, j + HALF)
                hits = [(plane_depth(t, *c), k) for k, t in enumerate(tris) if inside_perturbed(t, *c)]
                want = cols[min(hits)[1]] if hits else (0, 0, 0)
                assert got[j][i] == tuple(Fraction(x) for x in want)


def test_interpenetration_inside_a_pixel_is_approximate():
    # Two opaque squares cross at x = 1/2 inside one pixel. Exact per-sample
    # depth gives half and half; one depth per fragment gives one winner.
    p = ((0, 0, 0), (1, 0, 2), (1, 1, 2)), ((0, 0, 0), (1, 1, 2), (0, 1, 0))
    q = ((0, 0, 2), (1, 0, 0), (1, 1, 0)), ((0, 0, 2), (1, 1, 0), (0, 1, 2))
    tris = [p[0], p[1], q[0], q[1]]
    cols = [(1, 0)] * 2 + [(0, 1)] * 2
    exact = brute(1, 1, tris, cols, [1] * 4, (0, 0), 8, 4, True)[0][0]
    got = a_buffer(1, 1, tris, cols, [1] * 4, (0, 0), 8, 4)[0][0]
    assert exact == (HALF, HALF)
    assert got != exact
