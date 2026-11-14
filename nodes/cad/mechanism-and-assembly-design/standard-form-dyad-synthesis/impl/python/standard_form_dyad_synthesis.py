# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/standard-form-dyad-synthesis/. The authors are listed in prov/PC7C1B.jsonl.

"""Standard form dyad synthesis for three positions.

A dyad is a grounded link W (from the fixed pivot G to the moving pivot) and a
coupler-side vector Z (from the moving pivot to the precision point). In
position j the link has turned by beta_j and the coupler by alpha_j from
position 1, so

    G + W e^{i beta_j} + Z e^{i alpha_j} = P_j,

and subtracting position 1 gives the standard form

    W (e^{i beta_j} - 1) + Z (e^{i alpha_j} - 1) = delta_j = P_j - P_1.

Rotations are passed as unit numbers u = e^{i angle}, not as angles, so the
same code runs on Python complex numbers and on exact QC numbers (complex
numbers with Fraction parts), with rational points of the unit circle.
"""

import math
from fractions import Fraction


class QC:
    """An exact complex number with Fraction real and imaginary parts."""

    __slots__ = ("re", "im")

    def __init__(self, re, im=0):
        self.re = Fraction(re)
        self.im = Fraction(im)

    @staticmethod
    def of(z):
        return z if isinstance(z, QC) else QC(z)

    def __add__(self, o):
        o = QC.of(o)
        return QC(self.re + o.re, self.im + o.im)

    __radd__ = __add__

    def __sub__(self, o):
        o = QC.of(o)
        return QC(self.re - o.re, self.im - o.im)

    def __rsub__(self, o):
        return QC.of(o) - self

    def __neg__(self):
        return QC(-self.re, -self.im)

    def __mul__(self, o):
        o = QC.of(o)
        return QC(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = QC.of(o)
        n = o.re * o.re + o.im * o.im
        if n == 0:
            raise ZeroDivisionError("division by zero")
        return QC((self.re * o.re + self.im * o.im) / n, (self.im * o.re - self.re * o.im) / n)

    def __eq__(self, o):
        if isinstance(o, (int, Fraction)):
            o = QC(o)
        return isinstance(o, QC) and self.re == o.re and self.im == o.im

    def __hash__(self):
        return hash((self.re, self.im))

    def conj(self):
        return QC(self.re, -self.im)

    def abs2(self):
        return self.re * self.re + self.im * self.im

    def __repr__(self):
        return "QC(%s, %s)" % (self.re, self.im)


def rational_unit(t):
    """The point ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)) of the unit circle, e^{i angle} with tan(angle/2) = t."""
    t = Fraction(t)
    return QC((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))


def unit(angle):
    """e^{i angle} as a Python complex number."""
    return complex(math.cos(angle), math.sin(angle))


def is_zero(z, tol):
    if isinstance(z, QC):
        return z.re == 0 and z.im == 0
    return abs(z) <= tol


def three_position_dyad(p1, p2, p3, a2, a3, b2, b3, tol=1e-12):
    """Solve the 2 x 2 standard form system for (G, W, Z), or None when it is singular.

    p1, p2, p3 are the precision points; a2, a3 the coupler rotations e^{i alpha_j};
    b2, b3 the link rotations e^{i beta_j}. tol is the singularity test for floats.
    """
    d2, d3 = p2 - p1, p3 - p1
    bb2, aa2 = b2 - 1, a2 - 1  # @line L1
    bb3, aa3 = b3 - 1, a3 - 1
    det = bb2 * aa3 - bb3 * aa2  # @line L2
    scale = 1.0 if isinstance(det, QC) else max(1.0, abs(bb2) * abs(aa3) + abs(bb3) * abs(aa2))
    if is_zero(det, tol * scale):  # @line L3
        return None
    w = (d2 * aa3 - d3 * aa2) / det  # @line L4
    z = (bb2 * d3 - bb3 * d2) / det  # @line L5
    g = p1 - w - z  # @line L6
    return g, w, z  # @line L7


def two_position_dyad(p1, p2, a2, b2, z, tol=1e-12):
    """Two positions: with Z and beta_2 chosen, W = (delta_2 - Z (e^{i alpha_2} - 1)) / (e^{i beta_2} - 1)."""
    bb2 = b2 - 1
    if is_zero(bb2, tol):
        return None
    w = (p2 - p1 - z * (a2 - 1)) / bb2
    return p1 - w - z, w, z


def dyad_point(g, w, z, a, b):
    """The precision point of the dyad when the link has turned by b and the coupler by a."""
    return g + w * b + z * a


def free_choices(n):
    """Free real parameters of one dyad for n positions in motion generation: 5 - n."""
    unknowns = 4 + (n - 1)
    equations = 2 * (n - 1)
    return unknowns - equations


def four_bar(dyad_a, dyad_b):
    """Ground pivots and link lengths of the four-bar made of two dyads that share the coupler.

    Returns (G_A, G_B, |W_A|, |W_B|, coupler length |Z_A - Z_B|) for complex dyads.
    """
    ga, wa, za = dyad_a
    gb, wb, zb = dyad_b
    return ga, gb, abs(wa), abs(wb), abs(za - zb)
