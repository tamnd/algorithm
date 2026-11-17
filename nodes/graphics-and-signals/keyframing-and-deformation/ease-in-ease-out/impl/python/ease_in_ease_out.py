# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ease-in-ease-out/. The authors are listed in prov/M1V8Y9.jsonl.
"""Ease-in and ease-out curves.

Each function maps the normalized time t in [0, 1] to the fraction s(t) of
the distance travelled, with s(0) = 0, s(1) = 1, s monotone and the slope
s'(0) = s'(1) = 0. The constant acceleration curve has ramps on [0, t1] and
[t2, 1], with 0 < t1 <= t2 < 1, and constant speed in between.
"""

import math


def _clamp(t):
    return 0.0 if t < 0.0 else 1.0 if t > 1.0 else t  # @line L1


def sine_ease(t):
    """Return (sin(pi t - pi / 2) + 1) / 2."""
    t = _clamp(t)
    return (math.sin(math.pi * t - math.pi / 2.0) + 1.0) / 2.0  # @line L2


def smoothstep(t):
    """Return 3 t^2 - 2 t^3, the cubic with zero slope at both ends."""
    t = _clamp(t)
    return t * t * (3.0 - 2.0 * t)  # @line L3


def const_accel(t, t1, t2):
    """Return the distance fraction of the constant acceleration profile."""
    if not 0.0 < t1 <= t2 < 1.0:
        raise ValueError("need 0 < t1 <= t2 < 1")
    t = _clamp(t)
    v0 = 2.0 / (1.0 + t2 - t1)  # @line L4
    if t < t1:
        return v0 * t * t / (2.0 * t1)  # @line L5
    if t <= t2:
        return v0 * t1 / 2.0 + v0 * (t - t1)  # @line L6
    d = t - t2
    return v0 * t1 / 2.0 + v0 * (t2 - t1) + v0 * d * (1.0 - d / (2.0 * (1.0 - t2)))  # @line L7


def sine_speed(t):
    """Return the slope of sine_ease, pi / 2 sin(pi t)."""
    return math.pi / 2.0 * math.sin(math.pi * _clamp(t))


def smoothstep_speed(t):
    """Return the slope of smoothstep, 6 t (1 - t)."""
    t = _clamp(t)
    return 6.0 * t * (1.0 - t)


def const_accel_speed(t, t1, t2):
    """Return the slope of const_accel: a trapezoid with the top v0."""
    t = _clamp(t)
    v0 = 2.0 / (1.0 + t2 - t1)
    if t < t1:
        return v0 * t / t1
    if t <= t2:
        return v0
    return v0 * (1.0 - (t - t2) / (1.0 - t2))


def ease_between(a, b, t, ease=smoothstep):
    """Return the value at the time t between the keys a and b, eased."""
    s = ease(t)
    return tuple(x + s * (y - x) for x, y in zip(a, b))
