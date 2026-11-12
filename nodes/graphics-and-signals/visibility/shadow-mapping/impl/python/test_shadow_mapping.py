# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shadow-mapping/. The authors are listed in prov/4VKYK3.jsonl.

import random
from fractions import Fraction

from shadow_mapping import FAR, pcf, shadow_map, shadowed, to_light

HALF = Fraction(1, 2)
ORTHO = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
# A light at the origin that looks along +z: x' = 4x/z + 4, y' = 4y/z + 4,
# depth = 2 - 2/z, which grows with z.
PERSP = [[4, 0, 4, 0], [0, 4, 4, 0], [0, 0, 2, -2], [0, 0, 1, 0]]


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


def light_hits(tris, m, px, py):
    """All depths, over all triangles, on the light ray through (px, py)."""
    out = []
    for t in tris:
        lt = [to_light(m, v) for v in t]
        if inside_perturbed(lt, px, py):
            out.append(plane_depth(lt, px, py))
    return out


def inverse(m):
    a = [[Fraction(v) for v in row] + [Fraction(int(r == c)) for c in range(4)] for r, row in enumerate(m)]
    for c in range(4):
        p = next(r for r in range(c, 4) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        a[c] = [v / a[c][c] for v in a[c]]
        for r in range(4):
            if r != c:
                a[r] = [u - a[r][c] * v for u, v in zip(a[r], a[c])]
    return [row[4:] for row in a]


def from_light(minv, q):
    h = [sum(minv[r][k] * v for k, v in enumerate((*q, 1))) for r in range(4)]
    return tuple(h[r] / h[3] for r in range(3))


def rand_scene(rng, n, m):
    tris = []
    for _ in range(n):
        if m is ORTHO:
            tris.append(tuple((Fraction(rng.randint(-4, 36), 4), Fraction(rng.randint(-4, 36), 4),
                               Fraction(rng.randint(1, 40), 4)) for _ in range(3)))
        else:
            tris.append(tuple((Fraction(rng.randint(-20, 20), 4), Fraction(rng.randint(-20, 20), 4),
                               Fraction(rng.randint(4, 40), 4)) for _ in range(3)))
    return tris


def quad(x0, y0, x1, y1, z):
    return [((x0, y0, z), (x1, y0, z), (x1, y1, z)), ((x0, y0, z), (x1, y1, z), (x0, y1, z))]


def test_example():
    # A floor at depth 5 under an orthographic light, and a box top at depth 2.
    scene = quad(0, 0, 8, 8, 5) + quad(2, 2, 6, 6, 2)
    smap = shadow_map(8, 8, scene, ORTHO)
    assert [smap[j][i] for i, j in ((0, 0), (2, 2), (5, 5), (6, 6))] == [5, 2, 2, 5]
    assert shadowed(smap, ORTHO, (4, 4, 5))
    assert not shadowed(smap, ORTHO, (1, 1, 5))  # 5 > 5 is false: no self-shadow
    assert not shadowed(smap, ORTHO, (4, 4, 2))  # the box top itself is lit
    assert pcf(smap, ORTHO, (Fraction(5, 2), Fraction(5, 2), 5)) == Fraction(4, 9)


def test_map_against_brute_force():
    rng = random.Random(1978)
    for m in (ORTHO, PERSP):
        for _ in range(15):
            tris = rand_scene(rng, rng.randint(0, 5), m)
            smap = shadow_map(8, 8, tris, m)
            for j in range(8):
                for i in range(8):
                    hits = light_hits(tris, m, i + HALF, j + HALF)
                    assert smap[j][i] == (min(hits) if hits else FAR)


def test_shadow_test_is_exact_at_texel_centers():
    # With bias 0 and a point on a texel center, the test equals brute-force
    # occlusion: some surface on the light ray lies strictly nearer.
    rng = random.Random(1987)
    for m in (ORTHO, PERSP):
        minv = inverse(m)
        for _ in range(20):
            tris = rand_scene(rng, rng.randint(1, 5), m)
            smap = shadow_map(8, 8, tris, m)
            for _ in range(20):
                i, j = rng.randrange(8), rng.randrange(8)
                z = Fraction(rng.randint(1, 40), 4) if m is ORTHO else Fraction(rng.randint(0, 39), 20)
                p = from_light(minv, (i + HALF, j + HALF, z))
                assert to_light(m, p) == (i + HALF, j + HALF, z)
                want = any(d < z for d in light_hits(tris, m, i + HALF, j + HALF))
                assert shadowed(smap, m, p) == want


def test_pcf_is_the_mean_of_binary_tests():
    rng = random.Random(37435)
    for _ in range(20):
        tris = rand_scene(rng, 4, PERSP)
        smap = shadow_map(8, 8, tris, PERSP)
        for _ in range(10):
            p = (Fraction(rng.randint(-20, 20), 7), Fraction(rng.randint(-20, 20), 7), Fraction(rng.randint(4, 40), 4))
            x, y, z = to_light(PERSP, p)
            for r in (0, 1, 2):
                n = 0
                for jj in range(int(y // 1) - r, int(y // 1) + r + 1):
                    for ii in range(int(x // 1) - r, int(x // 1) + r + 1):
                        if 0 <= ii < 8 and 0 <= jj < 8 and z > smap[jj][ii]:
                            n += 1
                assert pcf(smap, PERSP, p, r=r) == Fraction(n, (2 * r + 1) ** 2)
            assert pcf(smap, PERSP, p, r=0) == int(shadowed(smap, PERSP, p))


def test_acne_without_bias_and_none_with_bias():
    # A floor tilted along x: depth 5 + x/2. A texel stores the depth at its
    # center, so a point right of the center looks behind the stored depth.
    floor = [((0, 0, 5), (8, 0, 9), (8, 8, 9)), ((0, 0, 5), (8, 8, 9), (0, 8, 5))]
    smap = shadow_map(8, 8, floor, ORTHO)
    rng = random.Random(5)
    pts = []
    for _ in range(200):
        x, y = Fraction(rng.randint(0, 799), 100), Fraction(rng.randint(0, 799), 100)
        pts.append((x, y, 5 + x / 2))
    acne = sum(shadowed(smap, ORTHO, p) for p in pts)
    assert acne > 0
    # The depth slope is 1/2 per texel and a point is at most 1/2 texel from
    # the center, so a bias of 1/4 removes all self-shadowing.
    assert sum(shadowed(smap, ORTHO, p, bias=Fraction(1, 4)) for p in pts) == 0
    assert shadowed(smap, ORTHO, (Fraction(19, 10), Fraction(6, 5), Fraction(119, 20)))


def test_too_much_bias_loses_a_contact_shadow():
    # A thin sheet just above the floor: a large bias hides its shadow.
    scene = quad(0, 0, 8, 8, 6) + quad(2, 2, 6, 6, Fraction(47, 8))
    smap = shadow_map(8, 8, scene, ORTHO)
    assert shadowed(smap, ORTHO, (4, 4, 6))
    assert not shadowed(smap, ORTHO, (4, 4, 6), bias=Fraction(1, 4))
