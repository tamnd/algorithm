# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-value-representation/. The authors are listed in prov/T0CK84.jsonl.

"""The point-value representation of polynomials over a field.

Fix N distinct points u_0, ..., u_(N-1). A polynomial f of degree less than N
is stored as the list of values [f(u_0), ..., f(u_(N-1))]. Addition and
multiplication are pointwise; conversion to coefficients is interpolation.
Coefficient lists are lowest degree first and normalized (no zero on top).
The elements may be Fraction, a class for Z/pZ, or anything with + - * / and
"== 0". Costs are counted in field operations.
"""

from __future__ import annotations

from typing import Any, List, Sequence

Values = List[Any]


def from_coefficients(a: Sequence[Any], pts: Sequence[Any]) -> Values:
    """The values of a at the points, by Horner's rule. Cost: O(N len(a))."""
    out = []
    for u in pts:
        s: Any = 0
        for c in reversed(a):
            s = s * u + c
        out.append(s)
    return out


def add(y: Sequence[Any], z: Sequence[Any]) -> Values:
    """The values of f + g. Cost: N additions."""
    return [y[i] + z[i] for i in range(len(y))]  # @line L4


def sub(y: Sequence[Any], z: Sequence[Any]) -> Values:
    """The values of f - g. Cost: N subtractions."""
    return [y[i] - z[i] for i in range(len(y))]


def mul(y: Sequence[Any], z: Sequence[Any]) -> Values:
    """The values of f g. Cost: N multiplications.

    The result represents f g only when deg f + deg g < N.
    """
    return [y[i] * z[i] for i in range(len(y))]  # @line L5


def weights(pts: Sequence[Any]) -> List[Any]:
    """The barycentric weights w_i = 1 / prod_(j != i) (u_i - u_j). Cost: O(N^2)."""
    n = len(pts)
    w: List[Any] = []
    for i in range(n):  # @line L1
        p: Any = pts[i] - pts[i] + 1  # the 1 of the field, not the int 1
        for j in range(n):  # @line L2
            if j != i:
                p = p * (pts[i] - pts[j])
        if p == 0:
            raise ValueError("the points must be distinct")
        w.append(1 / p)  # @line L3
    return w


def evaluate_at(y: Sequence[Any], pts: Sequence[Any], w: Sequence[Any], t: Any) -> Any:
    """The value f(t) by the barycentric Lagrange formula. Cost: O(N)."""
    for k in range(len(pts)):  # @line L6
        if t - pts[k] == 0:
            return y[k]
    ell: Any = 1
    for u in pts:  # @line L7
        ell = ell * (t - u)
    s: Any = 0
    for i in range(len(pts)):  # @line L8
        s = s + w[i] * y[i] / (t - pts[i])
    return ell * s


def to_coefficients(y: Sequence[Any], pts: Sequence[Any]) -> List[Any]:
    """The coefficient list of the unique f with deg f < N and f(u_i) = y_i.

    Newton's divided differences, then nested multiplication. Cost: O(N^2).
    """
    n = len(pts)
    if n == 0:
        return []
    d = list(y)  # @line L9
    for k in range(1, n):  # @line L10
        for i in range(n - 1, k - 1, -1):
            d[i] = (d[i] - d[i - 1]) / (pts[i] - pts[i - k])
    c: List[Any] = [d[n - 1]]  # @line L11
    for i in range(n - 2, -1, -1):  # @line L12
        # c <- c (x - u_i) + d_i
        new = [0] * (len(c) + 1)
        for j, cj in enumerate(c):
            new[j + 1] = new[j + 1] + cj
            new[j] = new[j] - cj * pts[i]
        new[0] = new[0] + d[i]
        c = new
    while c and c[-1] == 0:  # @line L13
        c.pop()
    return c


def extend(y: Sequence[Any], pts: Sequence[Any], new_pts: Sequence[Any]) -> Values:
    """The values of the same polynomial at new points. Cost: O(N^2 + N K) for K new points."""
    return from_coefficients(to_coefficients(y, pts), new_pts)
