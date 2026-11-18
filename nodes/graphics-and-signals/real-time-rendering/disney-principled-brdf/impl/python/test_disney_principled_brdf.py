# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disney-principled-brdf/. The authors are listed in prov/X3TDVD.jsonl.

"""Tests of the principled BRDF: GTR normalization, reciprocity, lobes and a white furnace."""

import math
import random

from disney_principled_brdf import (
    burley_diffuse,
    directional_albedo,
    dot,
    furnace_metal,
    gtr1,
    gtr2,
    normalize,
    principled_brdf,
)


def sph(t: float, p: float) -> tuple[float, float, float]:
    return (math.sin(t) * math.cos(p), math.sin(t) * math.sin(p), math.cos(t))


def integrate_d(d, alpha: float, steps: int = 40000) -> float:
    """The integral of D (n.h) over the hemisphere, in u = cos^2 so that peaks are resolved.

    With u = cos^2(theta), 2 pi D cos sin d theta = pi D du.
    """
    du = 1.0 / steps
    return math.pi * du * sum(d(math.sqrt((i + 0.5) * du), alpha) for i in range(steps))


def diffuse_albedo(theta_v: float, r: float, nt: int = 200, npf: int = 64) -> float:
    v = sph(theta_v, 0.0)
    total = 0.0
    dt, dp = (math.pi / 2.0) / nt, 2.0 * math.pi / npf
    for i in range(nt):
        t = (i + 0.5) * dt
        ring = 0.0
        for j in range(npf):
            l = sph(t, (j + 0.5) * dp)
            h = normalize((l[0] + v[0], l[1] + v[1], l[2] + v[2]))
            ring += burley_diffuse(l[2], v[2], dot(l, h), 1.0, r)
        total += ring * math.cos(t) * math.sin(t)
    return total * dt * dp


def test_gtr_normalization() -> None:
    for alpha in (0.05, 0.2, 0.5, 0.9, 1.0):
        assert abs(integrate_d(gtr2, alpha) - 1.0) < 1e-4
        assert abs(integrate_d(gtr1, alpha) - 1.0) < 1e-4
    # GTR1 has the longer tail: at 60 degrees it is far above GTR2 with the same peak width.
    c = math.cos(math.radians(60.0))
    assert gtr1(c, 0.1) > 10.0 * gtr2(c, 0.1)


def test_reciprocity_and_positivity() -> None:
    rng = random.Random(1)
    for _ in range(1000):
        l = sph(rng.uniform(0.0, 1.55), rng.uniform(0.0, 2.0 * math.pi))
        v = sph(rng.uniform(0.0, 1.55), rng.uniform(0.0, 2.0 * math.pi))
        p = dict(
            base=rng.random(),
            metallic=rng.random(),
            specular=rng.random(),
            roughness=rng.uniform(0.05, 1.0),
            sheen=rng.random(),
            clearcoat=rng.random(),
            clearcoat_alpha=rng.uniform(0.01, 0.3),
        )
        a, b = principled_brdf(l, v, **p), principled_brdf(v, l, **p)
        assert a >= 0.0
        assert abs(a - b) <= 1e-9 * max(1.0, a)


def test_metallic_is_linear_blend() -> None:
    rng = random.Random(3)
    for _ in range(500):
        l = sph(rng.uniform(0.0, 1.55), rng.uniform(0.0, 2.0 * math.pi))
        v = sph(rng.uniform(0.0, 1.55), rng.uniform(0.0, 2.0 * math.pi))
        p = dict(base=rng.random(), specular=rng.random(), roughness=rng.uniform(0.05, 1.0), sheen=rng.random())
        m = rng.random()
        blend = (1.0 - m) * principled_brdf(l, v, metallic=0.0, **p) + m * principled_brdf(l, v, metallic=1.0, **p)
        a = principled_brdf(l, v, metallic=m, **p)
        assert abs(a - blend) <= 1e-9 * max(1.0, a)


def test_lobes() -> None:
    l, v = sph(0.5, 0.0), sph(0.7, 2.5)
    # A metal has no diffuse or sheen.
    m = principled_brdf(l, v, base=0.9, metallic=1.0, roughness=0.4, sheen=1.0)
    assert abs(m - principled_brdf(l, v, base=0.9, metallic=1.0, roughness=0.4, sheen=0.0)) < 1e-15
    # Sheen adds sheen (1 - cos theta_d)^5 on a dielectric.
    h = normalize((l[0] + v[0], l[1] + v[1], l[2] + v[2]))
    w = (1.0 - dot(l, h)) ** 5
    d = principled_brdf(l, v, sheen=1.0) - principled_brdf(l, v, sheen=0.0)
    assert abs(d - w) < 1e-12
    # FD90 = 1 gives the Lambertian value base / pi.
    cd = dot(l, h)
    r = 0.5 / (2.0 * cd * cd)
    assert abs(burley_diffuse(l[2], v[2], cd, 0.7, r) - 0.7 / math.pi) < 1e-12


def test_burley_diffuse_albedo() -> None:
    table = {
        0.0: (0.9762, 0.9751, 0.9609, 0.8670, 0.6668),
        0.5: (1.0060, 1.0047, 1.0083, 1.0220, 1.0224),
        1.0: (1.0357, 1.0344, 1.0569, 1.1853, 1.4006),
    }
    for r, vals in table.items():
        for deg, val in zip((0.0, 45.0, 60.0, 75.0, 85.0), vals):
            assert abs(diffuse_albedo(math.radians(deg), r, nt=100, npf=24) - val) < 2e-3


def test_white_dielectric_albedo_above_one() -> None:
    # Diffuse and specular are added with no energy taken from the diffuse,
    # so a white rough dielectric reflects more than all the light.
    for deg, val in ((0.0, 1.0480), (60.0, 1.0756), (80.0, 1.3074)):
        q = directional_albedo(math.radians(deg), nt=100, npf=32, base=1.0, roughness=1.0)
        assert abs(q - val) < 3e-3
        assert q > 1.0


def test_white_furnace_metal() -> None:
    # A white metal reflects at most all light; the single-scattering loss grows with roughness.
    rng = random.Random(5)
    means = []
    for r in (0.2, 0.5, 1.0):
        mean, se = furnace_metal(0.0, r, rng, 20000)
        assert mean <= 1.0 + 4.0 * se
        means.append(mean)
    assert means[0] > means[1] > means[2]
    assert abs(means[0] - 0.998) < 0.003
    assert abs(means[1] - 0.916) < 0.01
    assert abs(means[2] - 0.307) < 0.01
    # Against deterministic quadrature where the lobe is wide enough for the grid.
    for r in (0.5, 1.0):
        for deg in (0.0, 60.0):
            q = directional_albedo(math.radians(deg), nt=120, npf=64, base=1.0, metallic=1.0, roughness=r)
            mean, se = furnace_metal(math.radians(deg), r, rng, 20000)
            assert abs(q - mean) < 4.0 * se + 5e-3


def test_g_remap_darkens_grazing() -> None:
    # For r < 1 the 2012 remap alpha_g = (0.5 + r / 2)^2 is larger than r^2,
    # so it masks more and the grazing specular is lower.
    l, v = sph(1.2, 0.0), sph(1.2, math.pi)
    for r in (0.2, 0.5, 0.8):
        a = principled_brdf(l, v, base=1.0, metallic=1.0, roughness=r, remap_g=False)
        b = principled_brdf(l, v, base=1.0, metallic=1.0, roughness=r, remap_g=True)
        assert b < a
