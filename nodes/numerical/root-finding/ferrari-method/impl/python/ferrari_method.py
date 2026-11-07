# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ferrari-method/. The authors are listed in prov/82X66E.jsonl.

"""Ferrari's method for the four roots of a quartic, in complex arithmetic."""

import cmath
from typing import Tuple


def _cardano(a: complex, b: complex, c: complex, d: complex) -> Tuple[complex, complex, complex]:
    """The three roots of a x^3 + b x^2 + c x + d by Cardano's formula (a != 0)."""
    omega = complex(-0.5, 3 ** 0.5 / 2)
    s, cc, dd = b / (3 * a), c / a, d / a
    p, q = cc - 3 * s * s, dd - s * cc + 2 * s ** 3
    rt = cmath.sqrt(q * q / 4 + p ** 3 / 27)
    w = -q / 2 + rt
    if abs(-q / 2 - rt) > abs(w):
        w = -q / 2 - rt
    if w == 0:
        return (-s, -s, -s)
    u = complex(w) ** (1 / 3)
    out = []
    for k in range(3):
        uk = u * omega ** k
        out.append(uk - p / (3 * uk) - s)
    return (out[0], out[1], out[2])


def _quad(beta: complex, gamma: complex) -> Tuple[complex, complex]:
    """The two roots of y^2 + beta y + gamma by the stable quadratic formula."""
    w = cmath.sqrt(beta * beta - 4 * gamma)  # @line L10
    t1, t2 = -(beta + w) / 2, -(beta - w) / 2
    t = t1 if abs(t1) >= abs(t2) else t2
    if t == 0:  # @line L11
        return (0j, 0j)
    return (t, gamma / t)


def ferrari(a: complex, b: complex, c: complex, d: complex, e: complex) -> Tuple[complex, complex, complex, complex]:
    """Return the four roots, with multiplicity, of a x^4 + b x^3 + c x^2 + d x + e.

    Precondition: a != 0. The coefficients may be real or complex. The root
    of the resolvent cubic of largest modulus is used. Cost: a fixed number of
    complex operations, five square roots and one cube root, O(1) space.
    """
    if a == 0:
        raise ValueError("a must be nonzero")
    s, C, D, E = b / (4 * a), c / a, d / a, e / a  # @line L1
    p = C - 6 * s * s  # @line L2
    q = D - 2 * C * s + 8 * s ** 3
    r = E - D * s + C * s * s - 3 * s ** 4
    ms = _cardano(8, 8 * p, 2 * p * p - 8 * r, -q * q)  # @line L3
    m = max(ms, key=abs)  # @line L4
    if m == 0:  # @line L5
        return (complex(-s), complex(-s), complex(-s), complex(-s))
    sigma = cmath.sqrt(2 * m)  # @line L6
    A = p / 2 + m + q / (2 * sigma)  # @line L7
    B = p / 2 + m - q / (2 * sigma)
    y1, y2 = _quad(-sigma, A)  # @line L8
    y3, y4 = _quad(sigma, B)
    return (y1 - s, y2 - s, y3 - s, y4 - s)  # @line L9


def polish(a: complex, b: complex, c: complex, d: complex, e: complex, x: complex, steps: int = 2) -> complex:
    """A few Newton steps on the quartic from x, by Horner's rule, to remove rounding errors."""
    for _ in range(steps):
        f = df = 0j
        for coef in (a, b, c, d, e):
            df = df * x + f
            f = f * x + coef
        if df == 0:
            break
        x = x - f / df
    return x
