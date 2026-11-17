# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gerstner-waves/. The authors are listed in prov/4CGSP7.jsonl.
"""Gerstner (trochoidal) waves on deep water.

One wave in 2D, in Lagrangian form. The water particle with the label (a, b),
b <= 0, is at

    x = a - A e^(k b) sin(theta),   z = b + A e^(k b) cos(theta),
    theta = k a - w t + phase,      w^2 = g k.

The surface is the line of particles with b = 0. The wave runs in the +x
direction, and each particle moves on a circle of radius A e^(k b).

The sum of several waves on a surface in 3D, as used in graphics, moves the
rest point p = (p_x, p_y) to

    p - chop * sum_i d_i A_i sin(theta_i),   height sum_i A_i cos(theta_i),
    theta_i = k_i d_i . p - w_i t + phase_i,

for unit directions d_i. A sum is not an exact solution of the flow
equations; it is a model of this file and of the graphics papers.
"""

import math

G = 9.81


def dispersion(k, g=G, depth=None):
    """The angular frequency w: (g k)^(1/2) in deep water, (g k tanh(k d))^(1/2) at the depth d."""
    if depth is None:
        return math.sqrt(g * k)
    return math.sqrt(g * k * math.tanh(k * depth))


def deep_water(wavelength, g=G):
    """(k, w, period, phase speed) of a deep water wave of the given wavelength (m)."""
    k = 2.0 * math.pi / wavelength
    w = dispersion(k, g)
    return k, w, 2.0 * math.pi / w, w / k


def phase_speed(k, g=G, depth=None):
    """w / k. In deep water (g / k)^(1/2); for k d small at the depth d it tends to (g d)^(1/2)."""
    return dispersion(k, g, depth) / k


def particle(a, b, t, amplitude, k, g=G, phase=0.0, w=None):
    """The position (x, z) of the particle with the label (a, b) at the time t. w defaults to (g k)^(1/2)."""
    if w is None:
        w = dispersion(k, g)
    r = amplitude * math.exp(k * b)
    theta = k * a - w * t + phase
    return a - r * math.sin(theta), b + r * math.cos(theta)


def particle_velocity(a, b, t, amplitude, k, g=G, phase=0.0):
    """The velocity (u, v) of the particle with the label (a, b): the time derivative of particle()."""
    w = dispersion(k, g)
    r = amplitude * math.exp(k * b)
    theta = k * a - w * t + phase
    return r * w * math.cos(theta), r * w * math.sin(theta)


def jacobian(a, b, amplitude, k):
    """det d(x, z) / d(a, b) = 1 - (k A e^(k b))^2. It does not depend on the time."""
    s = k * amplitude * math.exp(k * b)
    return 1.0 - s * s


def vorticity(b, amplitude, k, g=G):
    """The vorticity dv/dx - du/dz at the particle with the depth label b: 2 w s^2 / (1 - s^2), s = k A e^(k b).

    It is positive (counterclockwise), while the particles turn clockwise for a wave that runs in +x.
    """
    s = k * amplitude * math.exp(k * b)
    return 2.0 * dispersion(k, g) * s * s / (1.0 - s * s)


def surface_point(px, py, t, waves, chop=1.0, g=G):
    """The surface point (x, y, z) of the rest point (px, py) for a sum of waves.

    waves is a list of (amplitude, wavelength, (dx, dy), phase) with a unit direction (dx, dy).
    """
    x, y, z = px, py, 0.0
    for amp, wavelength, (dx, dy), phase in waves:
        k = 2.0 * math.pi / wavelength
        theta = k * (dx * px + dy * py) - dispersion(k, g) * t + phase
        s, c = math.sin(theta), math.cos(theta)
        x -= chop * dx * amp * s
        y -= chop * dy * amp * s
        z += amp * c
    return x, y, z


def horizontal_jacobian(px, py, t, waves, chop=1.0, g=G):
    """The 2 by 2 matrix d(x, y) / d(px, py) of surface_point, as ((j11, j12), (j21, j22))."""
    j11, j12, j22 = 1.0, 0.0, 1.0
    for amp, wavelength, (dx, dy), phase in waves:
        k = 2.0 * math.pi / wavelength
        theta = k * (dx * px + dy * py) - dispersion(k, g) * t + phase
        f = chop * k * amp * math.cos(theta)
        j11 -= f * dx * dx
        j12 -= f * dx * dy
        j22 -= f * dy * dy
    return (j11, j12), (j12, j22)


def steepness(waves, chop=1.0):
    """chop * sum_i k_i A_i. If it is below 1, the surface has no loops (see the proof page)."""
    return chop * sum(2.0 * math.pi / wl * amp for amp, wl, _, _ in waves)


def mean_level(amplitude, k, samples=4096):
    """The mean surface height over x of one wave (b = 0, t = 0), by a sum over equally spaced labels a.

    Each label carries the length dx/da da of the surface, so the mean is
    sum z dx/da / sum dx/da. The proof page shows it is -k A^2 / 2 for k A < 1.
    """
    num = 0.0
    den = 0.0
    for i in range(samples):
        theta = 2.0 * math.pi * i / samples
        dxda = 1.0 - k * amplitude * math.cos(theta)
        num += amplitude * math.cos(theta) * dxda
        den += dxda
    return num / den
