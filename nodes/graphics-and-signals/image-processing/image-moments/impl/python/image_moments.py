# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/image-moments/. The authors are listed in prov/Q8B269.jsonl.

"""Raw, central and normalized central moments, and the seven Hu invariants.

An image is a list of rows; img[y][x] is the value at column x and row y. Two
models of the image are supported:

- points: pixel (x, y) is a point mass f(x, y) at (x, y), and
  m_pq = sum f(x, y) x^p y^q (the usual discrete definition);
- cells: pixel (x, y) is the unit square centered at (x, y) with constant
  value f(x, y), and m_pq is the integral of f x^p y^q over the squares.

A weighted point set [(x, y, w), ...] can also be used directly. All sums are
exact with Fraction. The Hu invariants are computed from complex moments,
which turn a rotation into a phase factor.
"""

import math
from fractions import Fraction
from math import comb
from typing import Dict, List, Sequence, Tuple

Moments = Dict[Tuple[int, int], Fraction]


def image_points(img) -> List[Tuple[Fraction, Fraction, Fraction]]:
    """The pixels with a nonzero value, as weighted points (x, y, f)."""
    return [(Fraction(x), Fraction(y), Fraction(v)) for y, row in enumerate(img) for x, v in enumerate(row) if v]


def raw_moments(points: Sequence[tuple], order: int) -> Moments:
    """m_pq = sum w x^p y^q for p + q <= order."""
    m = {(p, q): Fraction(0) for p in range(order + 1) for q in range(order + 1 - p)}
    for x, y, w in points:
        xp = [Fraction(1)]
        yp = [Fraction(1)]
        for _ in range(order):
            xp.append(xp[-1] * x)
            yp.append(yp[-1] * y)
        for p, q in m:
            m[p, q] += w * xp[p] * yp[q]
    return m


def _cell_power_integral(c: Fraction, p: int) -> Fraction:
    """Integral of t^p over [c - 1/2, c + 1/2]."""
    h = Fraction(1, 2)
    return ((c + h) ** (p + 1) - (c - h) ** (p + 1)) / (p + 1)


def cell_raw_moments(img, order: int) -> Moments:
    """Raw moments of the image as a function that is constant on unit squares."""
    m = {(p, q): Fraction(0) for p in range(order + 1) for q in range(order + 1 - p)}
    for y, row in enumerate(img):
        iy = [_cell_power_integral(Fraction(y), q) for q in range(order + 1)]
        for x, v in enumerate(row):
            if v:
                ix = [_cell_power_integral(Fraction(x), p) for p in range(order + 1)]
                for p, q in m:
                    m[p, q] += Fraction(v) * ix[p] * iy[q]
    return m


def centroid(m: Moments) -> Tuple[Fraction, Fraction]:
    return m[1, 0] / m[0, 0], m[0, 1] / m[0, 0]


def central_moments(m: Moments) -> Moments:
    """mu_pq = sum over r <= p, s <= q of C(p, r) C(q, s) (-xc)^(p-r) (-yc)^(q-s) m_rs,
    the binomial expansion of the moments about the centroid (xc, yc)."""
    xc, yc = centroid(m)
    mu = {}
    for p, q in m:
        mu[p, q] = sum(
            (comb(p, r) * comb(q, s) * (-xc) ** (p - r) * (-yc) ** (q - s) * m[r, s] for r in range(p + 1) for s in range(q + 1)),
            Fraction(0),
        )
    return mu


def normalized_central_moment(mu: Moments, p: int, q: int):
    """eta_pq = mu_pq / mu_00^(1 + (p + q)/2). Exact (a Fraction) when p + q is even,
    a float when p + q is odd, because the power of mu_00 is then a half-integer."""
    if (p + q) % 2 == 0:
        return mu[p, q] / mu[0, 0] ** (1 + (p + q) // 2)
    return float(mu[p, q]) / float(mu[0, 0]) ** (1 + (p + q) / 2)


def _cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def complex_central_moment(mu: Moments, p: int, q: int):
    """c_pq = sum w (x + i y)^p (x - i y)^q about the centroid, as (real, imaginary),
    expanded into the central moments mu."""
    re, im = Fraction(0), Fraction(0)
    for j in range(p + 1):
        for k in range(q + 1):
            coeff = comb(p, j) * comb(q, k) * (-1) ** k
            v = coeff * mu[p + q - j - k, j + k]
            e = (j + k) % 4  # i^(j + k)
            if e == 0:
                re += v
            elif e == 1:
                im += v
            elif e == 2:
                re -= v
            else:
                im -= v
    return re, im


def hu_moments(mu: Moments) -> List[Fraction]:
    """The seven Hu invariants phi_1 .. phi_7, exactly.

    With the complex central moments c_pq, and c_12 the conjugate of c_21:
    phi_1 = c_11, phi_2 = |c_20|^2, phi_3 = |c_30|^2, phi_4 = |c_21|^2,
    phi_5 = Re(c_30 c_12^3), phi_6 = Re(c_20 c_12^2), phi_7 = Im(c_30 c_12^3),
    each divided by the power of mu_00 that makes it scale invariant."""
    n = mu[0, 0]
    c11 = complex_central_moment(mu, 1, 1)
    c20 = complex_central_moment(mu, 2, 0)
    c30 = complex_central_moment(mu, 3, 0)
    c21 = complex_central_moment(mu, 2, 1)
    c12 = complex_central_moment(mu, 1, 2)
    c12_2 = _cmul(c12, c12)
    c12_3 = _cmul(c12_2, c12)
    t5 = _cmul(c30, c12_3)
    t6 = _cmul(c20, c12_2)
    return [
        c11[0] / n**2,
        (c20[0] ** 2 + c20[1] ** 2) / n**4,
        (c30[0] ** 2 + c30[1] ** 2) / n**5,
        (c21[0] ** 2 + c21[1] ** 2) / n**5,
        t5[0] / n**10,
        t6[0] / n**7,
        t5[1] / n**10,
    ]


def orientation(mu: Moments) -> float:
    """The angle of the major axis, 1/2 atan2(2 mu_11, mu_20 - mu_02), in radians."""
    return 0.5 * math.atan2(2 * float(mu[1, 1]), float(mu[2, 0] - mu[0, 2]))


def principal_variances(mu: Moments) -> Tuple[float, float]:
    """The eigenvalues of the covariance matrix [[mu20, mu11], [mu11, mu02]] / mu00, larger first."""
    a, b, c = (float(mu[2, 0] / mu[0, 0]), float(mu[1, 1] / mu[0, 0]), float(mu[0, 2] / mu[0, 0]))
    mid, r = (a + c) / 2, math.hypot((a - c) / 2, b)
    return mid + r, mid - r
