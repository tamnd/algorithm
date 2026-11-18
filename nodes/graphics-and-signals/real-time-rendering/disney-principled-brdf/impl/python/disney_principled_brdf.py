# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disney-principled-brdf/. The authors are listed in prov/X3TDVD.jsonl.

"""The Disney principled BRDF of Burley (2012, revised 2014), one color channel.

The lobes are the Burley diffuse term, a GGX specular lobe with Schlick's
Fresnel and the Smith G of GGX, a sheen lobe and a clear coat lobe with the
GTR distribution for gamma = 1. One channel means that the tint parameters
have no effect, so they are left out; the subsurface and anisotropic
parameters are also left out. Vectors point away from the surface and the
normal is the z axis.
"""

import math
import random

Vec = tuple[float, float, float]


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def normalize(a: Vec) -> Vec:
    r = math.sqrt(dot(a, a))
    return (a[0] / r, a[1] / r, a[2] / r)


def schlick_weight(c: float) -> float:
    """(1 - c)^5 with c clamped to [0, 1]."""
    m = 1.0 - min(1.0, max(0.0, c))
    return (m * m) * (m * m) * m


def mix(a: float, b: float, t: float) -> float:
    return a * (1.0 - t) + b * t


def gtr2(cos_h: float, alpha: float) -> float:
    """GTR with gamma = 2, which is GGX: alpha^2 / (pi (1 + (alpha^2 - 1) cos^2)^2)."""
    if cos_h <= 0.0:
        return 0.0
    a2 = alpha * alpha
    t = 1.0 + (a2 - 1.0) * cos_h * cos_h
    return a2 / (math.pi * t * t)


def gtr1(cos_h: float, alpha: float) -> float:
    """GTR with gamma = 1: (alpha^2 - 1) / (pi log(alpha^2) (1 + (alpha^2 - 1) cos^2)).

    Burley 2012, Appendix B. At alpha = 1 the limit is 1 / pi.
    """
    if cos_h <= 0.0:
        return 0.0
    if alpha >= 1.0:
        return 1.0 / math.pi
    a2 = alpha * alpha
    return (a2 - 1.0) / (math.pi * math.log(a2) * (1.0 + (a2 - 1.0) * cos_h * cos_h))


def smith_g1_ggx(cos_w: float, alpha: float) -> float:
    """Smith masking for GGX, 2 / (1 + sqrt(1 + alpha^2 tan^2))."""
    if cos_w <= 0.0:
        return 0.0
    c2 = cos_w * cos_w
    return 2.0 / (1.0 + math.sqrt(1.0 + alpha * alpha * (1.0 - c2) / c2))


def burley_diffuse(cos_l: float, cos_v: float, cos_d: float, base: float, roughness: float) -> float:
    """base / pi (1 + (FD90 - 1) FL) (1 + (FD90 - 1) FV), FD90 = 0.5 + 2 r cos^2(theta_d)."""
    fd90 = 0.5 + 2.0 * roughness * cos_d * cos_d
    fl, fv = schlick_weight(cos_l), schlick_weight(cos_v)
    return base / math.pi * (1.0 + (fd90 - 1.0) * fl) * (1.0 + (fd90 - 1.0) * fv)


def principled_brdf(
    l: Vec,
    v: Vec,
    base: float = 0.8,
    metallic: float = 0.0,
    specular: float = 0.5,
    roughness: float = 0.5,
    sheen: float = 0.0,
    clearcoat: float = 0.0,
    clearcoat_alpha: float = 0.1,
    remap_g: bool = False,
) -> float:
    """The BRDF value in 1/sr for one color channel; n = (0, 0, 1).

    remap_g = True uses the 2012 remap alpha_g = (0.5 + r / 2)^2 for the
    specular G; the 2014 revision of the notes dropped it.
    """
    cl, cv = l[2], v[2]
    if cl <= 0.0 or cv <= 0.0:
        return 0.0
    h = normalize((l[0] + v[0], l[1] + v[1], l[2] + v[2]))
    ch = h[2]
    cd = dot(l, h)  # cos(theta_d), the angle between l and h (and v and h)
    fh = schlick_weight(cd)

    diffuse = burley_diffuse(cl, cv, cd, base, roughness)
    sheen_term = sheen * fh  # sheen (1 - cos theta_d)^5 with no tint

    alpha = max(1e-4, roughness * roughness)
    f0 = mix(0.08 * specular, base, metallic)
    ds = gtr2(ch, alpha)
    fs = mix(f0, 1.0, fh)
    ag = (0.5 + roughness / 2.0) ** 2 if remap_g else alpha
    gs = smith_g1_ggx(cl, ag) * smith_g1_ggx(cv, ag)
    spec = ds * fs * gs / (4.0 * cl * cv)

    dr = gtr1(ch, clearcoat_alpha)
    fr = mix(0.04, 1.0, fh)
    gr = smith_g1_ggx(cl, 0.25) * smith_g1_ggx(cv, 0.25)
    coat = 0.25 * clearcoat * dr * fr * gr / (4.0 * cl * cv)

    return (diffuse + sheen_term) * (1.0 - metallic) + spec + coat


def directional_albedo(theta_v: float, nt: int = 160, npf: int = 64, **params: float) -> float:
    """The integral of f (n.l) over the hemisphere of l, by the midpoint rule in theta_l and phi_l."""
    v = (math.sin(theta_v), 0.0, math.cos(theta_v))
    total = 0.0
    dt = (math.pi / 2.0) / nt
    dp = 2.0 * math.pi / npf
    for i in range(nt):
        t = (i + 0.5) * dt
        st, ct = math.sin(t), math.cos(t)
        ring = 0.0
        for j in range(npf):
            p = (j + 0.5) * dp
            l = (st * math.cos(p), st * math.sin(p), ct)
            ring += principled_brdf(l, v, **params)
        total += ring * ct * st
    return total * dt * dp


def sample_ggx_normal(rng: random.Random, alpha: float) -> Vec:
    """A normal m with the density D(m) (n.m) for GGX."""
    u = rng.random()
    phi = 2.0 * math.pi * rng.random()
    tan2 = alpha * alpha * u / (1.0 - u)
    c = 1.0 / math.sqrt(1.0 + tan2)
    s = math.sqrt(max(0.0, 1.0 - c * c))
    return (s * math.cos(phi), s * math.sin(phi), c)


def furnace_metal(theta_v: float, roughness: float, rng: random.Random, n: int) -> tuple[float, float]:
    """Monte Carlo albedo of a white metal (base 1, metallic 1), so F = 1.

    l is the mirror of v about a GGX normal h, with the pdf D (n.h) / (4 v.h).
    The weight f (n.l) / pdf is G (v.h) / ((n.v)(n.h)). Returns the mean and
    its standard error.
    """
    v = (math.sin(theta_v), 0.0, math.cos(theta_v))
    alpha = max(1e-4, roughness * roughness)
    vals = []
    for _ in range(n):
        h = sample_ggx_normal(rng, alpha)
        vh = dot(v, h)
        if vh <= 0.0:
            vals.append(0.0)
            continue
        l = (2.0 * vh * h[0] - v[0], 2.0 * vh * h[1] - v[1], 2.0 * vh * h[2] - v[2])
        if l[2] <= 0.0:
            vals.append(0.0)
            continue
        g = smith_g1_ggx(l[2], alpha) * smith_g1_ggx(v[2], alpha)
        vals.append(g * vh / (v[2] * h[2]))
    mean = sum(vals) / n
    var = sum((x - mean) ** 2 for x in vals) / (n - 1)
    return mean, math.sqrt(var / n)
