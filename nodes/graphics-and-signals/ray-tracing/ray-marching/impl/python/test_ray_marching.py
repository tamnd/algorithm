# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-marching/. The authors are listed in prov/DR3SGB.jsonl.

import math
import random

from ray_marching import march_surface, march_volume


def sphere_sdf(p, c, r):
    return math.dist(p, c) - r


def chord(o, d, c, r):
    """Exact parameter interval where the ray o + t d (|d| = 1) is inside the sphere, or None."""
    oc = [o[i] - c[i] for i in range(3)]
    b = sum(oc[i] * d[i] for i in range(3))
    disc = b * b - (sum(x * x for x in oc) - r * r)
    if disc <= 0:
        return None
    s = math.sqrt(disc)
    return (-b - s, -b + s)


def inside_intervals(o, d, spheres, t0, t1):
    """Merged intervals of [t0, t1] where the union of spheres contains the ray point."""
    ivs = []
    for c, r in spheres:
        iv = chord(o, d, c, r)
        if iv and iv[1] > t0 and iv[0] < t1:
            ivs.append((max(iv[0], t0), min(iv[1], t1)))
    ivs.sort()
    merged = []
    for a, b in ivs:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged


def random_scene(rng, k):
    return [((rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(4, 12)), rng.uniform(0.05, 1.2)) for _ in range(k)]


def random_ray(rng):
    d = (rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), 1.0)
    n = math.sqrt(sum(x * x for x in d))
    return (0.0, 0.0, 0.0), tuple(x / n for x in d)


def test_first_root_against_exact_sphere_chords():
    rng = random.Random(11)
    dt, refine, t1 = 0.05, 30, 20.0
    checked_exact = 0
    for _ in range(150):
        spheres = random_scene(rng, 6)
        o, d = random_ray(rng)

        def F(t):
            p = tuple(o[i] + t * d[i] for i in range(3))
            return min(sphere_sdf(p, c, r) for c, r in spheres)

        ivs = inside_intervals(o, d, spheres, 0.0, t1)
        t, certified = march_surface(F, 0.0, t1, dt, refine, lipschitz=1.0)
        if t is not None:
            assert F(t) <= 0
            assert ivs and t >= ivs[0][0] - 1e-9  # never before the first root
        if ivs and all(b - a >= dt for a, b in ivs):
            # every inside interval is at least one step long: the first root is found
            assert t is not None
            assert ivs[0][0] - 1e-9 <= t <= ivs[0][0] + dt / 2 ** refine + 1e-9
            checked_exact += 1
        if certified and t is not None:
            assert t - ivs[0][0] <= dt + 1e-9
        if certified and t is None:
            assert not ivs
    assert checked_exact > 25


def test_thin_feature_is_missed_by_large_steps():
    # A slab of thickness 0.04 at z in [5, 5.04] between two samples of step 0.1.
    def F(t):
        return abs(t - 5.02) - 0.02

    # Samples at 4.95 and 5.05 are both outside the slab.
    t, certified = march_surface(F, 0.05, 10.0, 0.1, lipschitz=1.0)
    assert t is None
    assert not certified  # the Lipschitz test flags the interval that hides the slab
    t, _ = march_surface(F, 0.05, 10.0, 0.01)
    assert abs(t - 5.0) < 1e-6


def test_dense_sampled_reference_for_a_torus():
    # Torus around the y axis, R = 1, r = 0.3, rays from z = -4 toward it.
    def sdf(p):
        q = math.hypot(p[0], p[2]) - 1.0
        return math.hypot(q, p[1]) - 0.3

    rng = random.Random(12)
    for _ in range(20):
        o = (rng.uniform(-1.5, 1.5), rng.uniform(-0.5, 0.5), -4.0)
        d = (0.0, 0.0, 1.0)

        def F(t):
            return sdf((o[0] + t * d[0], o[1] + t * d[1], o[2] + t * d[2]))

        h = 5e-4
        runs = []  # dense-sampled runs of samples with F <= 0, as (first, last) indices
        for k in range(16001):
            if F(k * h) <= 0:
                if runs and runs[-1][1] == k - 1:
                    runs[-1][1] = k
                else:
                    runs.append([k, k])
        t, _ = march_surface(F, 0.0, 8.0, 0.02, 40)
        if not runs:
            assert t is None or F(t) <= 0
            continue
        first = runs[0][0] * h
        assert t is None or t >= first - h - 1e-9  # never before the first root
        if all((b - a - 2) * h >= 0.02 for a, b in runs):
            assert t is not None and abs(t - first) <= h + 1e-9


def test_volume_midpoint_exact_for_linear_density():
    for a, b in [(0.0, 1.0), (0.5, 0.25), (2.0, 0.0)]:
        def sigma(t):
            return a + b * t

        exact = math.exp(-(a * 3.0 + b * 4.5))  # integral from 0 to 3
        assert abs(march_volume(sigma, 0.0, 3.0, 0.7) - exact) < 1e-12


def test_volume_converges_quadratically():
    def sigma(t):
        return 1.0 + math.sin(t)

    exact = math.exp(-(2.0 + (1 - math.cos(2.0))))
    e1 = abs(march_volume(sigma, 0.0, 2.0, 0.2) - exact)
    e2 = abs(march_volume(sigma, 0.0, 2.0, 0.1) - exact)
    assert 3.5 < e1 / e2 < 4.5


def test_start_inside_returns_start():
    t, _ = march_surface(lambda t: 1.0 - t, 0.0, 5.0, 0.3)
    assert abs(t - 1.0) < 1e-6
    t, _ = march_surface(lambda t: -1.0, 2.0, 5.0, 0.3)
    assert t == 2.0
