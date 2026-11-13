# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/savitzky-golay-filter/. The authors are listed in prov/WPM8SW.jsonl.

"""The Savitzky-Golay filter: a least squares polynomial fit in each window, read at one point.

The window holds the 2m + 1 samples at offsets i = -m .. m around the output
sample. The fit has degree p <= 2m. The weights are computed exactly with
Fraction, from the polynomials that are orthogonal on the points -m .. m
(Gram polynomials), so no linear system is solved.
"""

from fractions import Fraction
from typing import Sequence


def _poly_eval(c: list, x) -> Fraction:
    v = Fraction(0)
    for a in reversed(c):
        v = v * x + a
    return v


def _poly_deriv(c: list, d: int) -> list:
    for _ in range(d):
        c = [k * c[k] for k in range(1, len(c))]
    return c


def gram_polynomials(m: int, p: int) -> list[list[Fraction]]:
    """Monic polynomials P_0 .. P_p, orthogonal for the sum over i = -m .. m, as ascending coefficient lists."""
    pts = range(-m, m + 1)
    polys: list[list[Fraction]] = []
    for k in range(p + 1):
        q = [Fraction(0)] * k + [Fraction(1)]  # @line L1: start from x^k
        for r in polys:  # @line L2: remove the parts along the earlier polynomials
            num = sum(_poly_eval(q, i) * _poly_eval(r, i) for i in pts)
            den = sum(_poly_eval(r, i) ** 2 for i in pts)
            f = num / den
            q = [a - f * (r[j] if j < len(r) else 0) for j, a in enumerate(q)]
        polys.append(q)
    return polys


def _weights(polys: list, m: int, t: int, d: int) -> list[Fraction]:
    pts = range(-m, m + 1)
    c = [Fraction(0)] * (2 * m + 1)
    for q in polys:
        vals = [_poly_eval(q, i) for i in pts]
        norm = sum(v * v for v in vals)  # @line L3
        at_t = _poly_eval(_poly_deriv(q, d), t)  # @line L4
        for idx, v in enumerate(vals):
            c[idx] += v * at_t / norm  # @line L5: c_i = sum_k P_k(i) P_k^(d)(t) / ||P_k||^2
    return c


def sg_coefficients(m: int, p: int, t: int = 0, d: int = 0) -> list[Fraction]:
    """Weights c[-m .. m] (as a list) such that sum c_i y_i is the d-th derivative of the fit at offset t."""
    if m < 0 or not 0 <= p <= 2 * m:
        raise ValueError("need m >= 0 and 0 <= p <= 2m")
    return _weights(gram_polynomials(m, p), m, t, d)


def savitzky_golay(x: Sequence, m: int, p: int, d: int = 0) -> list[Fraction]:
    """Smooth (d = 0) or differentiate x with a window of 2m + 1 and degree p.

    Interior samples use the center weights. The first and last m samples use
    the fit of the first or last full window, read at the offset of the sample.
    """
    n = len(x)
    if n < 2 * m + 1:
        raise ValueError("the signal is shorter than one window")
    if not 0 <= p <= 2 * m:
        raise ValueError("need 0 <= p <= 2m")
    polys = gram_polynomials(m, p)
    center = _weights(polys, m, 0, d)
    out = []
    for k in range(n):  # @line L6
        if k < m:
            c, base = _weights(polys, m, k - m, d), 0
        elif k >= n - m:
            c, base = _weights(polys, m, k - (n - 1 - m), d), n - 2 * m - 1
        else:
            c, base = center, k - m
        out.append(sum(ci * x[base + j] for j, ci in enumerate(c)))  # @line L7
    return out
