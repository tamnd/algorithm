# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gcd-test/. The authors are listed in prov/M4BM5N.jsonl.
"""The GCD dependence test.

A loop nest has depth k. A subscript is a tuple (c0, c1, ..., ck) for the
affine function c0 + c1*i1 + ... + ck*ik of the iteration vector. The source
reference uses the indices i, the sink reference uses the indices j, and a
reference to an array of m dimensions is a list of m subscripts.

gcd_test(src, snk, psi) returns "independent" when no integer vectors i, j
(with any values, the loop bounds are ignored) make all subscripts equal and
match the direction vector psi, and "maybe" otherwise. Only the "=" entries
of psi change the test; "<", ">" and "*" give the same answer as no entry.
"""

from math import gcd


def ext_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with a*x + b*y = g = gcd(a, b) and g >= 0."""
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    if a < 0:
        return -a, -x0, -y0
    return a, x0, y0


def equation(src: tuple[int, ...], snk: tuple[int, ...], psi=None) -> tuple[list[int], int]:
    """The dependence equation of one subscript pair, as (coefficients, c).

    The equation is sum(coef * var) = c over the variables i1, j1, ..., ik, jk,
    except that a level with psi "=" has one variable i_l = j_l.
    """
    k = len(src) - 1
    coefs: list[int] = []
    for l in range(1, k + 1):
        if psi is not None and psi[l - 1] == "=":
            coefs.append(src[l] - snk[l])
        else:
            coefs.append(src[l])
            coefs.append(-snk[l])
    return coefs, snk[0] - src[0]


def solve_linear(coefs: list[int], c: int):
    """Return an integer vector x with sum(coefs[v] * x[v]) == c, or None.

    The vector comes from the extended Euclidean algorithm. It exists exactly
    when gcd(coefs) divides c (with gcd of all zeros equal to 0).
    """
    n = len(coefs)
    g, x = 0, [0] * n  # invariant: sum(coefs[v] * x[v]) == g
    for v in range(n):
        h, s, t = ext_gcd(g, coefs[v])
        x = [s * xv for xv in x]
        x[v] = t
        g = h
    if g == 0:
        return [0] * n if c == 0 else None
    if c % g != 0:
        return None
    q = c // g
    return [q * xv for xv in x]


def gcd_test_subscript(src: tuple[int, ...], snk: tuple[int, ...], psi=None) -> str:
    """The GCD test for one subscript pair."""
    k = len(src) - 1
    c = snk[0] - src[0]  # @line L1
    g = 0  # @line L2
    for l in range(1, k + 1):  # @line L3
        if psi is not None and psi[l - 1] == "=":
            g = gcd(g, src[l] - snk[l])  # @line L4
        else:
            g = gcd(gcd(g, src[l]), snk[l])  # @line L5
    if g == 0:
        return "maybe" if c == 0 else "independent"  # @line L6
    if c % g != 0:
        return "independent"  # @line L7
    return "maybe"  # @line L8


def gcd_test(src: list[tuple[int, ...]], snk: list[tuple[int, ...]], psi=None) -> str:
    """The GCD test for two references, one subscript at a time."""
    for f, g in zip(src, snk):  # @line L9
        if gcd_test_subscript(f, g, psi) == "independent":  # @line L10
            return "independent"
    return "maybe"  # @line L11


if __name__ == "__main__":
    # for i = 1 to n: A[2*i] = A[2*i + 1]
    print(gcd_test([(0, 2)], [(1, 2)]))  # independent
    # for i, j: A[3*i + 2*j] = A[i + 4*j + 1]
    print(gcd_test([(0, 3, 2)], [(1, 1, 4)]))  # maybe
    # with psi = (=, *): gcd(3 - 1, 2, 4) = 2 does not divide 1
    print(gcd_test([(0, 3, 2)], [(1, 1, 4)], ("=", "*")))  # independent
