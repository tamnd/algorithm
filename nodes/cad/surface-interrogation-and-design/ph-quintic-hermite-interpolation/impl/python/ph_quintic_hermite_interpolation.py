# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ph-quintic-hermite-interpolation/. The authors are listed in prov/XD0FDH.jsonl.

"""Farouki and Neff's PH quintic Hermite interpolation in the complex plane.

Points and vectors of the plane are Python complex numbers x + iy. A PH
quintic is r(t) with r'(t) = w(t)^2, where w is the complex quadratic
w(t) = w0 (1 - t)^2 + w1 2 (1 - t) t + w2 t^2. Given the end points p0, p5
and the end derivatives d0, d1, there are four such quintics, found with
two complex square roots each. The speed |r'(t)| = |w(t)|^2 is a polynomial,
so the arc length is a finite sum.
"""

import cmath
from typing import NamedTuple


class PHQuintic(NamedTuple):
    eps: int  # sign of w2 relative to the principal root of d1
    eta: int  # sign of the square root in w1
    w: tuple  # (w0, w1, w2), Bernstein coefficients of the quadratic w(t)
    points: tuple  # the six control points p0, ..., p5 of the quintic


def control_points(p0: complex, w: tuple) -> tuple:
    """Return the Bezier control points of p0 + integral of w(t)^2."""
    w0, w1, w2 = w
    p1 = p0 + w0 * w0 / 5
    p2 = p1 + w0 * w1 / 5
    p3 = p2 + (2 * w1 * w1 + w0 * w2) / 15
    p4 = p3 + w1 * w2 / 5
    p5 = p4 + w2 * w2 / 5
    return (p0, p1, p2, p3, p4, p5)


def ph_quintic_hermite(p0: complex, p5: complex, d0: complex, d1: complex) -> list:
    """Return the four PH quintics with r(0) = p0, r(1) = p5, r'(0) = d0, r'(1) = d1.

    The end derivatives must be nonzero. The list has the order
    (eps, eta) = (+1, +1), (+1, -1), (-1, +1), (-1, -1). Two entries
    coincide only when the radicand c of their eps is zero.
    """
    p0, p5, d0, d1 = complex(p0), complex(p5), complex(d0), complex(d1)
    if d0 == 0 or d1 == 0:
        raise ValueError("the end derivatives must be nonzero")
    delta = p5 - p0  # @line L1
    w0 = cmath.sqrt(d0)  # @line L2
    out = []
    for eps in (1, -1):  # @line L3
        w2 = eps * cmath.sqrt(d1)  # @line L4
        c = 120 * delta - 15 * (d0 + d1) + 10 * w0 * w2  # @line L5
        root = cmath.sqrt(c)
        for eta in (1, -1):  # @line L6
            w1 = (-3 * (w0 + w2) + eta * root) / 4  # @line L7
            pts = control_points(p0, (w0, w1, w2))  # @line L8
            out.append(PHQuintic(eps, eta, (w0, w1, w2), pts))  # @line L9
    return out  # @line L10


def evaluate(points, t: float) -> complex:
    """Point of the Bezier curve with complex control points, by de Casteljau."""
    b = list(points)
    for r in range(1, len(b)):
        for i in range(len(b) - r):
            b[i] = (1 - t) * b[i] + t * b[i + 1]
    return b[0]


def hodograph(w: tuple, t: float) -> complex:
    """Return w(t)^2, the derivative r'(t)."""
    w0, w1, w2 = w
    s = 1 - t
    wt = w0 * s * s + 2 * w1 * s * t + w2 * t * t
    return wt * wt


def speed_coefficients(w: tuple) -> tuple:
    """Bernstein coefficients of the degree 4 polynomial sigma(t) = |w(t)|^2."""
    w0, w1, w2 = w
    return (
        abs(w0) ** 2,
        (w0 * w1.conjugate()).real,
        (2 * abs(w1) ** 2 + (w0 * w2.conjugate()).real) / 3,
        (w1 * w2.conjugate()).real,
        abs(w2) ** 2,
    )


def speed(w: tuple, t: float) -> float:
    """Return sigma(t) = |r'(t)| from its Bernstein coefficients."""
    s = speed_coefficients(w)
    u = 1 - t
    basis = (u**4, 4 * u**3 * t, 6 * u * u * t * t, 4 * u * t**3, t**4)
    return sum(a * b for a, b in zip(s, basis))


def arc_length(w: tuple, t: float = 1.0) -> float:
    """Arc length from r(0) to r(t), the integral of sigma, in closed form."""
    s = speed_coefficients(w)
    cum = [0.0]
    for a in s:
        cum.append(cum[-1] + a / 5)
    return evaluate([complex(c) for c in cum], t).real


def absolute_rotation_index(w: tuple, samples: int = 1024) -> float:
    """Measured total turning of the tangent, divided by 2 pi.

    The tangent angle is 2 arg w(t). The sum of |change of 2 arg w| over
    `samples` equal steps converges to the absolute rotation index as the
    steps shrink, provided w has no zero on [0, 1].
    """
    w0, w1, w2 = w
    total = 0.0
    prev = w0
    for k in range(1, samples + 1):
        t = k / samples
        s = 1 - t
        cur = w0 * s * s + 2 * w1 * s * t + w2 * t * t
        total += abs(cmath.phase(cur / prev))
        prev = cur
    return total / cmath.pi


def fairest(solutions: list) -> PHQuintic:
    """The solution with the least absolute rotation index."""
    return min(solutions, key=lambda q: absolute_rotation_index(q.w))
