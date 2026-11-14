# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/freudenstein-equation/. The authors are listed in prov/Z9SNZM.jsonl.

"""Three-point function generation with Freudenstein's equation.

Four-bar notation (Norton): ground d from O2 = (0, 0) to O4 = (d, 0), input a,
coupler b, output c. phi is the input angle theta2 and psi the output angle
theta4, both counterclockwise from the ground line. The equation is

    K1 cos(psi) - K2 cos(phi) + K3 = cos(phi - psi),
    K1 = d/a,  K2 = d/c,  K3 = (a^2 - b^2 + c^2 + d^2) / (2 a c).

It is linear in K1, K2, K3, so three pairs (phi_j, psi_j) give a 3 x 3 linear
system. A precision point is passed as (cos phi, sin phi, cos psi, sin psi).
With Fraction values (rational points on the unit circle) every step is exact.
A negative a or c is a signed length: the link points the other way, which is
the same as length |a| at the angle phi + pi.
"""

import math
from fractions import Fraction


def solve_linear(m, rhs, tol=1e-12):
    """Solve m x = rhs by Gaussian elimination with partial pivoting.

    m is a list of n rows of n numbers (int, Fraction or float). Returns the
    list x, or None when the matrix is singular: an exact zero pivot for exact
    numbers, a pivot below tol times the largest entry for floats. O(n^3).
    """
    n = len(m)
    a = [list(row) + [r] for row, r in zip(m, rhs)]
    exact = all(isinstance(v, (int, Fraction)) for row in a for v in row)
    big = max((abs(v) for row in m for v in row), default=0)
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(a[r][col]))
        if a[piv][col] == 0 or (not exact and abs(a[piv][col]) <= tol * big):
            return None
        a[col], a[piv] = a[piv], a[col]
        for r in range(col + 1, n):
            f = a[r][col] / a[col][col]
            if f:
                for k in range(col, n + 1):
                    a[r][k] -= f * a[col][k]
    x = [0] * n
    for r in range(n - 1, -1, -1):
        s = a[r][n] - sum(a[r][k] * x[k] for k in range(r + 1, n))
        x[r] = s / a[r][r]
    return x


def three_point_synthesis(points, d):
    """The four-bar whose input and output angles pass the three precision points.

    points: three tuples (cos phi, sin phi, cos psi, sin psi). d: the ground
    length. Returns (a, b_squared, c, (K1, K2, K3)), or None when the system is
    singular or a K is zero. b_squared <= 0 means that no real coupler exists.
    Exact for Fraction input. O(1).
    """
    rows, rhs = [], []
    for cphi, sphi, cpsi, spsi in points:
        rows.append([cpsi, -cphi, 1])  # @line L1
        rhs.append(cphi * cpsi + sphi * spsi)
    k = solve_linear(rows, rhs)  # @line L2
    if k is None or k[0] == 0 or k[1] == 0:  # @line L3
        return None
    k1, k2, k3 = k
    a, c = d / k1, d / k2  # @line L4
    b_squared = a * a + c * c + d * d - 2 * a * c * k3  # @line L5
    return a, b_squared, c, (k1, k2, k3)  # @line L6


def unit_point(phi, psi):
    """(cos phi, sin phi, cos psi, sin psi) for float angles in radians."""
    return math.cos(phi), math.sin(phi), math.cos(psi), math.sin(psi)


def rational_unit(t):
    """The exact point ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)) of the unit circle, t = tan(angle/2)."""
    t = Fraction(t)
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def function_generator(f, x0, x1, xs, phi0, dphi, psi0, dpsi, d=1.0):
    """Three-point synthesis of a four-bar for y = f(x) on [x0, x1].

    The input angle is phi = phi0 + dphi (x - x0)/(x1 - x0) and the output angle
    is psi = psi0 + dpsi (f(x) - f(x0))/(f(x1) - f(x0)), in radians. xs holds the
    three precision points. Returns the result of three_point_synthesis.
    """
    y0, y1 = f(x0), f(x1)
    pts = []
    for x in xs:
        phi = phi0 + dphi * (x - x0) / (x1 - x0)
        psi = psi0 + dpsi * (f(x) - y0) / (y1 - y0)
        pts.append(unit_point(phi, psi))
    return three_point_synthesis(pts, d)
