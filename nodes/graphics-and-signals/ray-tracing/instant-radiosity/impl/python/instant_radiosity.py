# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/instant-radiosity/. The authors are listed in prov/H80DBM.jsonl.

"""Instant radiosity (Keller 1997).

Trace N random walks from the lights. Each vertex of each walk becomes a virtual point
light (VPL). Then light each visible point by all the VPLs, as point lights. A VPL on a
Lambertian surface has the radiant intensity beta f cos(theta_y), so it adds

    beta f(y) f_r(x) cos(theta_x) cos(theta_y) / |x - y|^2

to the reflected radiance at x. The geometry term G = cos cos / d^2 is unbounded near the
VPL, so renderers clamp it to G_max. The clamp removes energy, so it adds bias.

Two test scenes, both without occlusion: the inside of an emitting unit sphere (a furnace),
and a point light over a Lambertian floor with a sensor point that faces the floor.
"""

import math
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass

Vec = tuple[float, float, float]


@dataclass
class VPL:
    position: Vec
    normal: Vec | None  # None for an isotropic point light
    beta: float  # the power that arrives at the vertex, or the emitted power at a light vertex
    f: float  # the BRDF or emission factor: rho / pi on a Lambertian surface, 1 / pi on a Lambertian emitter


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cosine_direction(n: Vec, rng: random.Random) -> Vec:
    """A direction about the unit normal n with the density cos(theta) / pi."""
    u1, u2 = rng.random(), rng.random()
    r, phi = math.sqrt(u1), 2.0 * math.pi * u2
    lx, ly, lz = r * math.cos(phi), r * math.sin(phi), math.sqrt(max(0.0, 1.0 - u1))
    if abs(n[0]) > 0.9:
        t = (0.0, 1.0, 0.0)
    else:
        t = (1.0, 0.0, 0.0)
    # b = n x t, normalized; t2 = b x n
    bx, by, bz = n[1] * t[2] - n[2] * t[1], n[2] * t[0] - n[0] * t[2], n[0] * t[1] - n[1] * t[0]
    bl = math.sqrt(bx * bx + by * by + bz * bz)
    bx, by, bz = bx / bl, by / bl, bz / bl
    tx, ty, tz = by * n[2] - bz * n[1], bz * n[0] - bx * n[2], bx * n[1] - by * n[0]
    return (lx * tx + ly * bx + lz * n[0], lx * ty + ly * by + lz * n[1], lx * tz + ly * bz + lz * n[2])


def generate_vpls(
    n_paths: int,
    sample_light: Callable[[random.Random], VPL],
    next_vertex: Callable[[VPL, random.Random], tuple[Vec, Vec, float] | None],
    rng: random.Random,
    max_depth: int = 1000,
) -> list[VPL]:
    """The light pass. sample_light returns a light vertex with beta = (emitted power) / n_paths.
    next_vertex returns the next hit (y, n_y, rho_y) of a walk from a vertex, or None if the ray
    leaves the scene. A walk continues from a surface vertex with probability rho, so beta stays
    the same."""
    vpls: list[VPL] = []  # @line L1
    for _ in range(n_paths):  # @line L2
        v = sample_light(rng)  # @line L3
        for depth in range(max_depth):
            vpls.append(v)  # @line L4
            if depth > 0 and rng.random() >= v.f * math.pi:  # @line L5
                break  # survive with probability rho = pi f
            hit = next_vertex(v, rng)  # @line L6
            if hit is None:
                break
            y, ny, rho = hit
            v = VPL(y, ny, v.beta, rho / math.pi)  # @line L7
    return vpls


def gather(x: Vec, nx: Vec, rho_x: float, vpls: Sequence[VPL], g_max: float = math.inf) -> float:
    """The reflected radiance at x with normal nx and reflectance rho_x from all the VPLs.
    The geometry term of a surface VPL is clamped to g_max. Visibility is 1 in the test scenes."""
    total = 0.0
    for v in vpls:  # @line L8
        d = (v.position[0] - x[0], v.position[1] - x[1], v.position[2] - x[2])
        d2 = _dot(d, d)
        if d2 == 0.0:
            continue
        dist = math.sqrt(d2)
        cx = _dot(nx, d) / dist
        if cx <= 0.0:
            continue
        if v.normal is None:  # an isotropic point light: intensity beta / (4 pi)
            total += v.beta / (4.0 * math.pi) * cx / d2
            continue
        cy = -_dot(v.normal, d) / dist
        if cy <= 0.0:
            continue
        g = min(cx * cy / d2, g_max)  # @line L9
        total += v.beta * v.f * g  # @line L10
    return rho_x / math.pi * total  # @line L11


# The furnace: the inside of the unit sphere, emitting the exitance b_e, with reflectance rho.


def furnace_scene(b_e: float, rho: float, n_paths: int):
    def sample_light(rng: random.Random) -> VPL:
        z = 1.0 - 2.0 * rng.random()
        a = 2.0 * math.pi * rng.random()
        s = math.sqrt(max(0.0, 1.0 - z * z))
        p = (s * math.cos(a), s * math.sin(a), z)
        return VPL(p, (-p[0], -p[1], -p[2]), 4.0 * math.pi * b_e / n_paths, 1.0 / math.pi)

    def next_vertex(v: VPL, rng: random.Random):
        w = cosine_direction(v.normal, rng)
        t = -2.0 * _dot(v.position, w)  # the second root of |p + t w| = 1
        q = tuple(v.position[k] + t * w[k] for k in range(3))
        ln = math.sqrt(_dot(q, q))
        q = (q[0] / ln, q[1] / ln, q[2] / ln)
        return q, (-q[0], -q[1], -q[2]), rho

    return sample_light, next_vertex


def furnace_exact(b_e: float, rho: float) -> float:
    """The reflected radiance in the furnace: rho E / pi with the irradiance E = b_e / (1 - rho)."""
    return rho * b_e / (math.pi * (1.0 - rho))


# A point light of power phi at height h over the floor z = 0 with reflectance rho.


def floor_scene(phi: float, h: float, rho: float, n_paths: int):
    def sample_light(rng: random.Random) -> VPL:
        return VPL((0.0, 0.0, h), None, phi / n_paths, 1.0 / math.pi)

    def next_vertex(v: VPL, rng: random.Random):
        if v.normal is None:  # from the point light, an isotropic direction
            z = 1.0 - 2.0 * rng.random()
            a = 2.0 * math.pi * rng.random()
            if z >= 0.0:
                return None
            s = math.sqrt(max(0.0, 1.0 - z * z))
            t = -h / z
            return (t * s * math.cos(a), t * s * math.sin(a), 0.0), (0.0, 0.0, 1.0), rho
        return None  # light that leaves the floor goes to the sky

    return sample_light, next_vertex


def simpson(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    if n % 2:
        n += 1
    hstep = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * hstep)
    return s * hstep / 3.0


def floor_sensor_exact(phi: float, h: float, rho: float, a: float, rho_x: float, g_max: float = math.inf) -> float:
    """The reflected radiance at the point (0, 0, a) that faces the floor, from one bounce off the
    floor, with the geometry term clamped to g_max. The integral is over the distance r on the
    floor, by Simpson's rule after the change of variables r = a tan(t)."""

    def integrand(t: float) -> float:
        r = a * math.tan(t)
        e_floor = phi * h / (4.0 * math.pi * (h * h + r * r) ** 1.5)
        g = min(a * a / (a * a + r * r) ** 2, g_max)
        dr = a / math.cos(t) ** 2
        return rho / math.pi * e_floor * g * 2.0 * math.pi * r * dr

    top = math.pi / 2.0 - 1e-9
    cut = None
    if g_max < 1.0 / (a * a):
        rc = math.sqrt(a / math.sqrt(g_max) - a * a)  # where the clamp ends
        cut = math.atan(rc / a)
    if cut is None:
        value = simpson(integrand, 0.0, top, 4000)
    else:
        value = simpson(integrand, 0.0, cut, 2000) + simpson(integrand, cut, top, 4000)
    return rho_x / math.pi * value
