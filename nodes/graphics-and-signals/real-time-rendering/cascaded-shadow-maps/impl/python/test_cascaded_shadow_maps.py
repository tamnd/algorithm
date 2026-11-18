# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cascaded-shadow-maps/. The authors are listed in prov/SFEHPC.jsonl.

import random
from math import pi, sqrt

from cascaded_shadow_maps import (
    Camera,
    Cascades,
    dot,
    exact_shadowed,
    fit_stable,
    fit_tight,
    light_frame,
    splits,
    to_light,
)

LIGHT = (0.3, -1.0, 0.2)


def scene(rng, k=10):
    out = []
    for _ in range(k):
        r = rng.uniform(0.3, 1.2)
        z = rng.uniform(-30, -3)
        out.append(((rng.uniform(-0.4, 0.4) * -z, r + rng.uniform(0.2, 1.0), z), r))
    return out


def test_split_scheme():
    c = splits(1.0, 100.0, 4, 0.5)
    want = [1.0, 14.456, 30.25, 53.436, 100.0]
    assert all(abs(a - b) < 1e-3 for a, b in zip(c, want))
    log = splits(1.0, 100.0, 4, 1.0)
    assert all(abs(log[i + 1] / log[i] - 100 ** 0.25) < 1e-12 for i in range(4))
    uni = splits(1.0, 100.0, 4, 0.0)
    assert all(abs(uni[i + 1] - uni[i] - 24.75) < 1e-12 for i in range(4))
    rng = random.Random(1)
    for _ in range(200):
        n = rng.uniform(0.05, 2.0)
        f = n * rng.uniform(2.0, 2000.0)
        m = rng.randrange(1, 9)
        lam = rng.uniform(0.0, 1.0)
        c = splits(n, f, m, lam)
        assert abs(c[0] - n) < 1e-12 * f and abs(c[-1] - f) < 1e-9 * f
        assert all(a < b for a, b in zip(c, c[1:]))
        # The practical split lies between the uniform and the logarithmic one.
        lo, hi = splits(n, f, m, 1.0), splits(n, f, m, 0.0)
        assert all(a - 1e-9 <= x <= b + 1e-9 for a, x, b in zip(lo, c, hi))


def test_every_point_of_a_slice_is_inside_its_cascade():
    rng = random.Random(2)
    rows = light_frame(LIGHT)
    for _ in range(20):
        cam = Camera((rng.uniform(-3, 3), rng.uniform(1, 4), 0.0),
                     (rng.uniform(-1, 1), rng.uniform(-0.5, 0.1), -1.0), pi / 3, rng.uniform(1.0, 2.0))
        c = splits(0.5, 40.0, 4, rng.uniform(0, 1))
        for i in range(4):
            for fit in (fit_tight, fit_stable):
                lo, texel = fit(cam, rows, c[i], c[i + 1], 32)
                for _ in range(30):
                    p = cam.point(rng.uniform(c[i], c[i + 1]), rng.uniform(-1, 1), rng.uniform(-1, 1))
                    q = to_light(rows, p)
                    for k in (0, 1):
                        assert lo[k] - 1e-9 <= q[k] <= lo[k] + 32 * texel[k] + 1e-9


def test_lookup_agrees_with_ray_casting_away_from_edges():
    rng = random.Random(3)
    spheres = scene(rng)
    cam = Camera((0.0, 3.0, 0.0), (0.0, -0.3, -1.0), pi / 3, 1.0)
    rows = light_frame(LIGHT)
    for stable in (False, True):
        csm = Cascades(cam, LIGHT, spheres, 0.5, 40.0, 4, 0.5, 64, stable)
        tested = shadowed = 0
        for k in range(3000):
            if k % 2:
                p = (rng.uniform(-12, 12), 0.0, rng.uniform(-40, -1))
            else:
                (cx, cy, cz), r = spheres[k // 2 % len(spheres)]
                p = (cx + 0.3 * cy + rng.uniform(-2 * r, 2 * r), 0.0, cz + 0.2 * cy + rng.uniform(-2 * r, 2 * r))
            d = cam.depth(p)
            i = csm.cascade_of(d)
            v = tuple(a - b for a, b in zip(p, cam.pos))
            if i is None or abs(dot(v, cam.right)) > d * cam.t * cam.aspect or abs(dot(v, cam.up)) > d * cam.t:
                continue
            lo, texel, _ = csm.maps[i]
            q = to_light(rows, p)
            half_diag = 0.5 * sqrt(texel[0] ** 2 + texel[1] ** 2)
            margin = min(abs(sqrt((q[0] - lc[0]) ** 2 + (q[1] - lc[1]) ** 2) - r)
                         for lc, r in ((to_light(rows, c), r) for c, r in spheres))
            if margin <= half_diag:
                continue
            want = exact_shadowed(p, spheres, rows)
            assert csm.shadowed(p) == want
            tested += 1
            shadowed += want
        assert tested > 500 and shadowed > 20


def test_cascade_choice_follows_the_splits():
    cam = Camera((0.0, 3.0, 0.0), (0.0, -0.3, -1.0), pi / 3, 1.0)
    csm = Cascades(cam, LIGHT, [], 0.5, 40.0, 4, 0.5, 4)
    for d in (0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 39.9):
        i = csm.cascade_of(d)
        assert csm.c[i] <= d < csm.c[i + 1]
    assert csm.cascade_of(0.4) is None and csm.cascade_of(40.0) is None


def test_near_cascades_have_smaller_texels():
    cam = Camera((0.0, 3.0, 0.0), (0.0, -0.3, -1.0), pi / 3, 1.0)
    csm = Cascades(cam, LIGHT, [], 0.5, 40.0, 4, 0.5, 4)
    sizes = [max(t) for _, t, _ in csm.maps]
    assert all(a < b for a, b in zip(sizes, sizes[1:]))


def test_stable_fit_keeps_size_and_texel_grid():
    rows = light_frame(LIGHT)
    rng = random.Random(4)
    base = None
    for _ in range(40):
        cam = Camera((rng.uniform(-5, 5), rng.uniform(1, 4), rng.uniform(-5, 5)),
                     (rng.uniform(-1, 1), rng.uniform(-0.5, 0.1), rng.uniform(-1, 1)), pi / 3, 1.5)
        lo, texel = fit_stable(cam, rows, 2.0, 8.0, 32)
        if base is None:
            base = texel
        assert texel == base
        for k in (0, 1):
            t = lo[k] / texel[k]
            assert abs(t - round(t)) < 1e-9
