# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-casting/. The authors are listed in prov/NXDDGG.jsonl.

import math
import random
from fractions import Fraction

from ray_casting import Sphere, Triangle, pixel_ray, ray_cast

F = Fraction
CAM = ((F(0), F(0), F(10)), (1, 0, 0), (0, 1, 0), (0, 0, 1))   # eye on +z, looking down -z


def det3(c0, c1, c2):
    return (c0[0] * (c1[1] * c2[2] - c1[2] * c2[1])
            - c1[0] * (c0[1] * c2[2] - c0[2] * c2[1])
            + c2[0] * (c0[1] * c1[2] - c0[2] * c1[1]))


def exact_t(tri, o, d):
    """Reference: Cramer's rule in Fraction; the hit t > 0 or None."""
    a, b, c = (tuple(F(x) for x in p) for p in (tri.a, tri.b, tri.c))
    e1 = [b[i] - a[i] for i in range(3)]
    e2 = [c[i] - a[i] for i in range(3)]
    md = [-F(x) for x in d]
    r = [F(o[i]) - a[i] for i in range(3)]
    den = det3(e1, e2, md)
    if den == 0:
        return None
    u, v, t = det3(r, e2, md) / den, det3(e1, r, md) / den, det3(e1, e2, r) / den
    return t if u >= 0 and v >= 0 and u + v <= 1 and t > 0 else None


def rand_q(rng, lo, hi):
    return F(rng.randint(lo * 4, hi * 4), 4)


def test_visibility_against_brute_force():
    rng = random.Random(1968)
    for _ in range(6):
        tris = []
        for _ in range(8):
            c = [rand_q(rng, -3, 3), rand_q(rng, -3, 3), rand_q(rng, -4, 4)]
            tris.append(Triangle(*(tuple(c[i] + rand_q(rng, -2, 2) for i in range(3)) for _ in range(3))))
        w = h = 8
        ids, _ = ray_cast(tris, *CAM, w, h, F(1, 2))
        for j in range(h):
            for i in range(w):
                o, d = pixel_ray(*CAM, w, h, F(1, 2), i, j)
                hits = [(exact_t(t, o, d), k) for k, t in enumerate(tris)]
                hits = [x for x in hits if x[0] is not None]
                assert ids[j][i] == (min(hits)[1] if hits else None)


def test_sphere_silhouette():
    # pixel (i, j) is covered when its center ray meets the sphere (exact discriminant)
    s = Sphere((0.0, 0.0, 0.0), 2.0)
    w, h = 21, 15
    cam = ((0.0, 0.0, 10.0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
    ids, _ = ray_cast([s], *cam, w, h, 0.3)
    covered = 0
    for j in range(h):
        for i in range(w):
            o, d = pixel_ray(*cam, w, h, 0.3, i, j)
            f = [F(o[k]) for k in range(3)]
            dd = [F(x) for x in d]
            a = sum(x * x for x in dd)
            b = sum(f[k] * dd[k] for k in range(3))
            k2 = sum(x * x for x in f) - 4
            disc = b * b - a * k2
            if abs(disc) < F(1, 10 ** 9):
                continue
            assert (ids[j][i] == 0) == (disc > 0)
            covered += disc > 0
    assert 0 < covered < w * h


def test_lambert_and_shadow():
    floor = [Triangle((-20.0, -20.0, 0.0), (20.0, -20.0, 0.0), (20.0, 20.0, 0.0)),
             Triangle((-20.0, -20.0, 0.0), (20.0, 20.0, 0.0), (-20.0, 20.0, 0.0))]
    blocker = Triangle((-1.0, -1.0, 2.0), (1.0, -1.0, 2.0), (0.0, 1.5, 2.0))
    light = (0.0, 0.0, 6.0)
    cam = ((0.0, 0.0, 10.0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
    w, h = 31, 31
    ids, shade = ray_cast(floor + [blocker], *cam, w, h, 0.5, light=light, ambient=0.1)
    for j in range(h):
        for i in range(w):
            o, d = pixel_ray(*cam, w, h, 0.5, i, j)
            k = ids[j][i]
            assert k is not None
            if k == 2:
                # the blocker faces the light; cos = (6 - 2) / |light - p|
                t = (2.0 - o[2]) / d[2]
            else:
                t = -o[2] / d[2]
            p = [o[m] + t * d[m] for m in range(3)]
            dist = math.dist(p, light)
            if k == 2:
                want = 0.1 + 0.9 * (light[2] - 2.0) / dist
            else:
                # exact shadow test of the floor point against the blocker
                q = [F(x) for x in p]
                dl = [F(light[m]) - q[m] for m in range(3)]
                s = (2 - q[2]) / dl[2]
                x, y = q[0] + s * dl[0], q[1] + s * dl[1]
                e = (y + 1, F(3, 2) - F(5, 2) * x - y, F(3, 2) + F(5, 2) * x - y)
                inside = min(e) >= 0
                if min(abs(v) for v in e) < 1e-9:
                    continue
                want = 0.1 if inside else 0.1 + 0.9 * light[2] / dist
            assert abs(shade[j][i] - want) < 1e-9
    assert any(shade[j][i] == 0.1 for j in range(h) for i in range(w) if ids[j][i] != 2)
