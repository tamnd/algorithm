# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blinn-phong-reflection-model/. The authors are listed in prov/3J4E53.jsonl.

"""Tests of the Blinn-Phong model: normalization, albedo, reciprocity and the Phong match."""

import math
import random

from blinn_phong_reflection_model import (
    blinn_lobe,
    blinn_phong_brdf,
    blinn_phong_d,
    dot,
    half_vector,
    normalize,
    phong_lobe,
    phong_to_blinn_exponent,
    reflect,
    shade_classic,
    specular_albedo,
    specular_albedo_normal,
)

N = (0.0, 0.0, 1.0)


def random_up(rng: random.Random) -> tuple[float, float, float]:
    """A random unit vector in the upper hemisphere, by rejection."""
    while True:
        x, y, z = rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(0, 1)
        r2 = x * x + y * y + z * z
        if 1e-6 < r2 <= 1.0 and z > 1e-3:
            return normalize((x, y, z))


def test_half_vector_and_mirror() -> None:
    rng = random.Random(1)
    for _ in range(500):
        l, v = random_up(rng), random_up(rng)
        h = half_vector(l, v)
        assert abs(dot(h, l) - dot(h, v)) < 1e-12
        # When v is the mirror of l, h is n and both lobes peak.
        r = reflect(l, N)
        assert abs(dot(half_vector(l, r), N) - 1.0) < 1e-12
        assert abs(blinn_lobe(N, l, r, 50.0) - 1.0) < 1e-9
        assert abs(phong_lobe(N, l, r, 50.0) - 1.0) < 1e-9


def test_d_is_normalized() -> None:
    # The integral of D (n.h) over the hemisphere is 1 for every s; midpoint rule in theta.
    for s in (0.0, 1.0, 10.0, 100.0, 1000.0):
        k = 20000
        dt = (math.pi / 2.0) / k
        total = 0.0
        for i in range(k):
            t = (i + 0.5) * dt
            total += blinn_phong_d(math.cos(t), s) * math.cos(t) * math.sin(t)
        assert abs(total * 2.0 * math.pi * dt - 1.0) < 1e-4


def test_reciprocity() -> None:
    rng = random.Random(2)
    for _ in range(1000):
        l, v = random_up(rng), random_up(rng)
        s = rng.uniform(1.0, 200.0)
        a = blinn_phong_brdf(N, l, v, 0.5, 0.5, s)
        b = blinn_phong_brdf(N, v, l, 0.5, 0.5, s)
        assert abs(a - b) <= 1e-12 * max(1.0, a)
        # The Phong lobe is also symmetric: r(l).v = r(v).l.
        assert abs(phong_lobe(N, l, v, 10.0) - phong_lobe(N, v, l, 10.0)) < 1e-12


def test_albedo_at_normal_incidence() -> None:
    expected = {1.0: 1.0243, 4.0: 1.0625, 16.0: 1.0669, 64.0: 1.0267, 256.0: 1.0075}
    for s, val in expected.items():
        assert abs(specular_albedo_normal(s) - val) < 5e-5
        assert abs(specular_albedo(0.0, s) - specular_albedo_normal(s)) < 5e-4
    # The largest value over s is 1.0752, near s = 8.76; it tends to 1 at both ends.
    best = max(specular_albedo_normal(i / 100.0) for i in range(1, 5001))
    assert abs(best - 1.0752) < 5e-5
    assert abs(specular_albedo_normal(1e-6) - 1.0) < 1e-4
    assert abs(specular_albedo_normal(1e6) - 1.0) < 1e-4


def test_albedo_at_sixty_degrees() -> None:
    expected = {1.0: 0.8388, 4.0: 0.5938, 16.0: 0.3702, 64.0: 0.2811, 256.0: 0.2578}
    for s, val in expected.items():
        assert abs(specular_albedo(math.radians(60.0), s) - val) < 5e-4


def test_phong_to_blinn_match() -> None:
    # At v = n, n.h = cos(t / 2) and r.v = cos t for the angle t between l and n.
    for p in (10.0, 50.0, 200.0):
        s = phong_to_blinn_exponent(p)
        for t in (0.02, 0.05, 0.1):
            l = (math.sin(t), 0.0, math.cos(t))
            ph = phong_lobe(N, l, N, p)
            bl = blinn_lobe(N, l, N, s)
            assert abs(math.log(bl) - math.log(ph)) < 0.02 * p * t * t + 1e-12
    # Away from normal view the Blinn lobe gets narrow across the plane of incidence.
    def sph(t: float, p: float) -> tuple[float, float, float]:
        return (math.sin(t) * math.cos(p), math.sin(t) * math.sin(p), math.cos(t))

    tv = math.radians(75.0)
    v = sph(tv, 0.0)
    d = 0.2
    in_plane = sph(tv - d, math.pi)
    dphi = 2.0 * math.asin(math.sin(d / 2.0) / math.sin(tv))
    across = sph(tv, math.pi + dphi)
    assert abs(math.acos(dot(across, reflect(v, N))) - d) < 1e-12
    assert abs(phong_lobe(N, in_plane, v, 10.0) - 0.818) < 5e-4
    assert abs(blinn_lobe(N, in_plane, v, 40.0) - 0.818) < 5e-4
    assert abs(phong_lobe(N, across, v, 10.0) - 0.818) < 5e-4
    assert abs(blinn_lobe(N, across, v, 40.0) - 0.062) < 5e-4


def test_classic_shading() -> None:
    l = normalize((1.0, 0.0, 1.0))
    v = normalize((-1.0, 0.0, 1.0))
    # Mirror configuration: n.l = 0.7071 and n.h = 1.
    val = shade_classic(N, l, v, 0.1, 0.6, 0.3, 32.0)
    assert abs(val - (0.1 + 0.6 * math.sqrt(0.5) + 0.3)) < 1e-12
    # Light behind the surface: only ambient.
    assert shade_classic(N, (0.0, 0.0, -1.0), v, 0.1, 0.6, 0.3, 32.0) == 0.1
