# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iso-scallop-toolpath/. The authors are listed in prov/MQ38PN.jsonl.

import math
import random

import pytest

from iso_scallop_toolpath import Profile, cylinder_step, iso_scallop, scallop


def convex_cylinder(R, a, b):
    return Profile(lambda x: math.sqrt(R * R - x * x), lambda x: -x / math.sqrt(R * R - x * x), a, b)


def concave_cylinder(R, a, b):
    return Profile(lambda x: -math.sqrt(R * R - x * x), lambda x: x / math.sqrt(R * R - x * x), a, b)


def sine(A, L, b):
    return Profile(lambda x: A * math.sin(x / L), lambda x: A / L * math.cos(x / L), 0.0, b)


def parabola(k, a, b):
    return Profile(lambda x: k * x * x, lambda x: 2 * k * x, a, b)


def ray_thickness(profile, r, t0, t1, samples=800):
    """Brute force: shoot the normal ray from each sample point of the profile between the
    passes, and measure how far it goes before it enters one of the two tool disks.
    The largest such length is the height of the ridge of material left between them.
    The search runs on a grid, then on a finer grid around the best sample, three times."""
    centers = [profile.center(t, r) for t in (t0, t1)]

    def thickness(x):
        p, n = profile.point(x), profile.normal(x)
        hit = math.inf
        for c in centers:
            w = (p[0] - c[0], p[1] - c[1])
            bb = n[0] * w[0] + n[1] * w[1]
            cc = w[0] * w[0] + w[1] * w[1] - r * r
            disc = bb * bb - cc
            if disc >= 0:
                hit = min(hit, max(-bb - math.sqrt(disc), 0.0))
        return hit

    lo, hi = t0, t1
    for _ in range(3):
        xs = [lo + (hi - lo) * i / samples for i in range(samples + 1)]
        k = max(range(len(xs)), key=lambda i: thickness(xs[i]))
        lo, hi = xs[max(k - 1, 0)], xs[min(k + 1, samples)]
    return max(thickness(x) for x in xs)


def test_plane_matches_the_closed_form():
    for r, h in ((5.0, 0.01), (5.0, 0.417424), (3.0, 0.2)):
        passes = iso_scallop(Profile(lambda x: 0.0, lambda x: 0.0, 0.0, 20.0), r, h)
        w = 2 * math.sqrt(r * r - (r - h) ** 2)
        for t0, t1 in zip(passes[:-2], passes[1:-1]):
            assert abs((t1 - t0) - w) < 1e-9
    assert abs(2 * math.sqrt(25 - (5 - 0.417424) ** 2) - 4) < 1e-5


def test_cylinders_match_the_closed_form():
    R, r = 20.0, 5.0
    for h in (0.01, 0.05, 0.3):
        for convex, prof in ((True, convex_cylinder(R, 0.0, 14.0)), (False, concave_cylinder(R, 0.0, 14.0))):
            passes = iso_scallop(prof, r, h)
            theta = cylinder_step(R, r, h, convex)
            angles = [math.asin(t / R) for t in passes]
            for a0, a1 in zip(angles[:-2], angles[1:-1]):
                assert abs((a1 - a0) - theta) < 1e-9
            assert angles[-1] - angles[-2] <= theta + 1e-9


def test_cylinder_closed_form_values():
    R, r = 20.0, 5.0
    # inverse of the forward values for theta = 0.1: convex 0.127393, concave 0.075269
    assert abs(cylinder_step(R, r, 0.127393, True) - 0.1) < 1e-5
    assert abs(cylinder_step(R, r, 0.075269, False) - 0.1) < 1e-5


def test_every_pair_has_the_target_height():
    rng = random.Random(5)
    profiles = [sine(3.0, 4.0, 30.0), parabola(0.05, -10.0, 10.0), sine(1.0, 2.5, 20.0)]
    for prof in profiles:
        r = rng.choice([1.0, 2.0])
        h = rng.choice([0.01, 0.02, 0.05])
        passes = iso_scallop(prof, r, h)
        assert passes[0] == prof.a and passes[-1] == prof.b
        assert all(t0 < t1 for t0, t1 in zip(passes, passes[1:]))
        for t0, t1 in zip(passes[:-2], passes[1:-1]):
            assert abs(scallop(prof, r, t0, t1) - h) < 1e-9
        assert scallop(prof, r, passes[-2], passes[-1]) <= h + 1e-12


def test_scallop_matches_the_ray_brute_force():
    """Measured: the cusp distance and the largest ray thickness agree to 1e-4 of h or better."""
    rng = random.Random(7)
    prof = sine(3.0, 4.0, 30.0)
    for _ in range(12):
        r = rng.choice([1.0, 2.0, 2.5])
        t0 = rng.uniform(0.0, 26.0)
        t1 = t0 + rng.uniform(0.3, 1.5)
        h = scallop(prof, r, t0, t1)
        brute = ray_thickness(prof, r, t0, t1)
        assert abs(h - brute) <= 1e-4 * h + 1e-7, (t0, t1, h, brute)
    for convex, prof2 in ((True, convex_cylinder(20.0, -10.0, 10.0)), (False, concave_cylinder(20.0, -10.0, 10.0))):
        t1 = 20.0 * math.sin(0.2)
        h = scallop(prof2, 5.0, 0.0, t1)
        assert abs(h - ray_thickness(prof2, 5.0, 0.0, t1)) < 1e-6
        assert abs(h - (0.542575 if convex else 0.304456)) < 1e-6


def test_fewer_passes_than_a_constant_worst_case_step():
    """Measured: a constant step equal to the smallest iso-scallop step needs more passes."""
    for prof, r, h in ((sine(3.0, 4.0, 30.0), 2.0, 0.02), (parabola(0.05, -10.0, 10.0), 1.0, 0.01)):
        passes = iso_scallop(prof, r, h)
        smallest = min(t1 - t0 for t0, t1 in zip(passes[:-2], passes[1:-1]))
        constant = math.ceil((prof.b - prof.a) / smallest) + 1
        assert len(passes) < constant


def test_bad_input():
    with pytest.raises(ValueError):
        iso_scallop(sine(1.0, 1.0, 5.0), 0.0, 0.1)
    with pytest.raises(ValueError):
        Profile(lambda x: 0.0, lambda x: 0.0, 1.0, 1.0)
