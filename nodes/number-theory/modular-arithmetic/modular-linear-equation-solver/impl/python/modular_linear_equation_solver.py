# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modular-linear-equation-solver/. The authors are listed in prov/XRMYSW.jsonl.

"""Modular linear equation solver.

Solves a*x = b (mod n) for integers a, b and a modulus n >= 1. With
d = gcd(a, n), the equation has no solution when d does not divide b, and
otherwise exactly d solutions in 0..n-1, spaced n/d apart. The solver runs
the extended Euclidean algorithm once, O(log n) loop passes, and then lists
the d solutions in increasing order, so its time is O(log n + d) arithmetic
operations. Python integers have arbitrary precision; on inputs of k binary
digits the cost is O(k^2 + d*k) bit operations.
"""


def extended_euclid(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with g = gcd(a, b) and a*x + b*y = g, for a, b >= 0."""
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return r0, s0, t0


def modular_linear_equation_solver(a: int, b: int, n: int) -> list[int]:
    """Return all x in 0..n-1 with a*x = b (mod n), in increasing order.

    The precondition is n >= 1. The list is empty when there is no solution.
    It has gcd(a, n) entries otherwise, which can be as many as n.
    """
    if n < 1:
        raise ValueError("the modulus must be at least 1")
    a, b = a % n, b % n  # @line L1
    d, x1, _ = extended_euclid(a, n)  # @line L2
    if b % d != 0:  # @line L3
        return []
    m = n // d  # @line L4
    x0 = (x1 * (b // d)) % m  # @line L5
    xs: list[int] = []  # @line L6
    for i in range(d):  # @line L7
        xs.append(x0 + i * m)  # @line L8
    return xs  # @line L9


def solve_compact(a: int, b: int, n: int) -> tuple[int, int] | None:
    """Return (x0, m) such that the solutions are exactly the x = x0 (mod m),
    with 0 <= x0 < m = n / gcd(a, n), or None when there is no solution.

    This is lines L1 to L5 without the list, so it runs in O(log n)
    arithmetic operations even when the number of solutions is huge.
    """
    if n < 1:
        raise ValueError("the modulus must be at least 1")
    a, b = a % n, b % n
    d, x1, _ = extended_euclid(a, n)
    if b % d != 0:
        return None
    m = n // d
    return (x1 * (b // d)) % m, m
