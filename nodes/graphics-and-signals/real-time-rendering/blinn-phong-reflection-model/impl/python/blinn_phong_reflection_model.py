# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blinn-phong-reflection-model/. The authors are listed in prov/3J4E53.jsonl.

"""The Blinn-Phong reflection model, its classic shading form, its
normalized BRDF form, and the Phong lobe it replaces.

All vectors point away from the surface. n, l and v are unit vectors.
Colors are single linear channels here.
"""

import math

Vec = tuple[float, float, float]


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def normalize(a: Vec) -> Vec:
    r = math.sqrt(dot(a, a))
    return (a[0] / r, a[1] / r, a[2] / r)


def half_vector(l: Vec, v: Vec) -> Vec:
    """h = (l + v) / |l + v|; undefined when l = -v."""
    return normalize((l[0] + v[0], l[1] + v[1], l[2] + v[2]))


def reflect(l: Vec, n: Vec) -> Vec:
    """The mirror direction r = 2 (n.l) n - l."""
    c = 2.0 * dot(n, l)
    return (c * n[0] - l[0], c * n[1] - l[1], c * n[2] - l[2])


def phong_lobe(n: Vec, l: Vec, v: Vec, p: float) -> float:
    """The Phong specular factor max(0, r.v)^p."""
    return max(0.0, dot(reflect(l, n), v)) ** p


def blinn_lobe(n: Vec, l: Vec, v: Vec, s: float) -> float:
    """The Blinn specular factor max(0, n.h)^s."""
    return max(0.0, dot(n, half_vector(l, v))) ** s


def shade_classic(n: Vec, l: Vec, v: Vec, ka: float, kd: float, ks: float, s: float, light: float = 1.0) -> float:
    """The classic intensity ka + light (kd max(0, n.l) + ks max(0, n.h)^s).

    The specular term is set to zero when the light is behind the surface.
    """
    nl = dot(n, l)
    if nl <= 0.0:
        return ka
    return ka + light * (kd * nl + ks * blinn_lobe(n, l, v, s))


def blinn_phong_d(cos_h: float, s: float) -> float:
    """The normalized distribution (s + 2) / (2 pi) (n.h)^s, a valid microfacet D."""
    if cos_h <= 0.0:
        return 0.0
    return (s + 2.0) / (2.0 * math.pi) * cos_h ** s


def blinn_phong_brdf(n: Vec, l: Vec, v: Vec, kd: float, ks: float, s: float) -> float:
    """The normalized BRDF kd / pi + ks (s + 8) / (8 pi) (n.h)^s, in 1/sr."""
    if dot(n, l) <= 0.0 or dot(n, v) <= 0.0:
        return 0.0
    return kd / math.pi + ks * (s + 8.0) / (8.0 * math.pi) * blinn_lobe(n, l, v, s)


def specular_albedo(theta_v: float, s: float, nt: int = 400, npf: int = 96) -> float:
    """The directional albedo of the specular term (s + 8) / (8 pi) (n.h)^s.

    It integrates f (n.l) over the hemisphere of l by a change of variables to
    the half vector, d omega_l = 4 (v.h) d omega_h, with the midpoint rule in
    theta_h and phi_h. The frame has n = z and v in the xz plane.
    """
    n = (0.0, 0.0, 1.0)
    v = (math.sin(theta_v), 0.0, math.cos(theta_v))
    k = (s + 8.0) / (8.0 * math.pi)
    tmax = math.pi / 2.0
    total = 0.0
    dt = tmax / nt
    dp = 2.0 * math.pi / npf
    for i in range(nt):
        t = (i + 0.5) * dt
        st, ct = math.sin(t), math.cos(t)
        lobe = k * ct ** s
        if lobe == 0.0:
            continue
        ring = 0.0
        for j in range(npf):
            p = (j + 0.5) * dp
            h = (st * math.cos(p), st * math.sin(p), ct)
            vh = dot(v, h)
            if vh <= 0.0:
                continue
            l = (2.0 * vh * h[0] - v[0], 2.0 * vh * h[1] - v[1], 2.0 * vh * h[2] - v[2])
            nl = dot(n, l)
            if nl <= 0.0:
                continue
            ring += nl * 4.0 * vh
        total += lobe * ring * st
    return total * dt * dp


def specular_albedo_normal(s: float) -> float:
    """The exact albedo of the specular term at v = n.

    There l is the mirror of v about h, so n.l = cos(2 theta_h), v.h = cos(theta_h),
    and the integral over cos(theta_h) from 1/sqrt(2) to 1 has a closed form.
    """
    c0 = 1.0 / math.sqrt(2.0)
    return (s + 8.0) * (2.0 * (1.0 - c0 ** (s + 4.0)) / (s + 4.0) - (1.0 - c0 ** (s + 2.0)) / (s + 2.0))


def phong_to_blinn_exponent(p: float) -> float:
    """s = 4 p makes the two lobes match near the mirror direction at normal view."""
    return 4.0 * p
