# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cardano-formula/. The authors are listed in prov/XGZ50G.jsonl.

"""Cardano's formula for the three roots of a cubic, in complex arithmetic."""

import cmath
from typing import Tuple

OMEGA = complex(-0.5, 3 ** 0.5 / 2)  # exp(2 pi i / 3)


def cardano(a: complex, b: complex, c: complex, d: complex) -> Tuple[complex, complex, complex]:
    """Return the three roots, with multiplicity, of a x^3 + b x^2 + c x + d.

    Precondition: a != 0. The coefficients may be real or complex. The
    partner of the cube root u is taken as -p / (3u), and the root of the
    resolvent quadratic of larger modulus is used, so no cancellation to 0
    occurs there. Cost: a fixed number of complex operations, one square
    root and one cube root, O(1) space.
    """
    if a == 0:
        raise ValueError("a must be nonzero")
    s, C, D = b / (3 * a), c / a, d / a  # @line L1
    p, q = C - 3 * s * s, D - s * C + 2 * s ** 3  # @line L2
    r = cmath.sqrt(q * q / 4 + p ** 3 / 27)  # @line L3
    w = -q / 2 + r  # @line L4
    if abs(-q / 2 - r) > abs(w):
        w = -q / 2 - r
    if w == 0:  # @line L5
        return (-s, -s, -s)
    u = complex(w) ** (1 / 3)  # @line L6
    roots = []
    for k in range(3):  # @line L7
        uk = u * OMEGA ** k  # @line L8
        tk = uk - p / (3 * uk)  # @line L9
        roots.append(tk - s)  # @line L10
    return tuple(roots)  # @line L11


def polish(a: complex, b: complex, c: complex, d: complex, x: complex, steps: int = 2) -> complex:
    """A few Newton steps on the cubic from x, to remove rounding errors of the formula."""
    for _ in range(steps):
        fx = ((a * x + b) * x + c) * x + d
        dfx = (3 * a * x + 2 * b) * x + c
        if dfx == 0:
            break
        x = x - fx / dfx
    return x
