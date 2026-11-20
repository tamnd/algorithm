# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bloch-equations/. The authors are listed in prov/YQ1113.jsonl.

"""The Bloch equation, solved by the classical Runge-Kutta method and in closed form.

State: the magnetization M = (Mx, My, Mz). Field: the angular frequency
vector omega(t) = gamma B(t) in rad/s, given in the frame of the caller (in
the rotating frame, omega = (gamma B1x, gamma B1y, Delta omega)). The
equation is
    dM/dt = M x omega - (Mx / T2, My / T2, (Mz - M0) / T1).
For a proton (gamma > 0) and omega = (0, 0, w0), the transverse part
Mxy = Mx + i My turns clockwise seen from +z: Mxy(t) = Mxy(0) exp(-i w0 t - t / T2).

The Larmor frequency is f = gammabar B0 with gammabar = 42.577478461 MHz/T
for the free proton (the value listed by NIST, physics.nist.gov, constant gammapbar).
"""

import cmath
import math
from typing import Callable, Sequence

GAMMA_BAR_PROTON = 42.577478461e6  # Hz/T
GAMMA_PROTON = 2.0 * math.pi * GAMMA_BAR_PROTON  # rad/s/T

Vec3 = tuple[float, float, float]


def larmor_hz(b0: float) -> float:
    """The proton Larmor frequency in Hz at field b0 in tesla."""
    return GAMMA_BAR_PROTON * b0


def cross(a: Sequence[float], b: Sequence[float]) -> Vec3:
    """The cross product a x b."""
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def bloch_rhs(m: Sequence[float], omega: Sequence[float], t1: float, t2: float, m0: float) -> Vec3:
    """dM/dt of the Bloch equation. Use math.inf for no relaxation."""
    c = cross(m, omega)
    r2 = 0.0 if math.isinf(t2) else 1.0 / t2
    r1 = 0.0 if math.isinf(t1) else 1.0 / t1
    return (c[0] - m[0] * r2, c[1] - m[1] * r2, c[2] - (m[2] - m0) * r1)


def bloch_rk4(
    m: Sequence[float],
    omega: Callable[[float], Sequence[float]],
    t1: float,
    t2: float,
    m0: float,
    h: float,
    steps: int,
) -> Vec3:
    """Integrate the Bloch equation from t = 0 with steps of size h (classical RK4)."""

    def f(t: float, v: Sequence[float]) -> Vec3:
        return bloch_rhs(v, omega(t), t1, t2, m0)  # @line L1

    def add(v: Sequence[float], d: Sequence[float], s: float) -> Vec3:
        return (v[0] + s * d[0], v[1] + s * d[1], v[2] + s * d[2])

    cur: Vec3 = (float(m[0]), float(m[1]), float(m[2]))
    for s in range(steps):  # @line L2
        t = s * h  # @line L3
        a = f(t, cur)  # @line L4
        b = f(t + h / 2, add(cur, a, h / 2))
        c = f(t + h / 2, add(cur, b, h / 2))  # @line L5
        d = f(t + h, add(cur, c, h))
        cur = tuple(cur[i] + h * (a[i] + 2 * b[i] + 2 * c[i] + d[i]) / 6 for i in range(3))  # @line L6
    return cur  # @line L7


def free_precession(m: Sequence[float], w0: float, t1: float, t2: float, m0: float, t: float) -> Vec3:
    """Closed form for omega = (0, 0, w0): Mxy decays by exp(-t/T2) and turns by -w0 t; Mz recovers to M0."""
    mxy = complex(m[0], m[1]) * cmath.exp(-1j * w0 * t) * math.exp(-t / t2)
    mz = m0 + (m[2] - m0) * math.exp(-t / t1)
    return (mxy.real, mxy.imag, mz)


def rotate(v: Sequence[float], axis: Sequence[float], angle: float) -> Vec3:
    """Rodrigues: v turned by angle about the unit axis (right-hand rule)."""
    c, s = math.cos(angle), math.sin(angle)
    k = axis
    kv = cross(k, v)
    kd = k[0] * v[0] + k[1] * v[1] + k[2] * v[2]
    return tuple(v[i] * c + kv[i] * s + k[i] * kd * (1 - c) for i in range(3))
