# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-diophantine-solution/. The authors are listed in prov/747E8M.jsonl.


def solve_linear_diophantine(a: int, b: int, c: int) -> tuple[int, int] | None:
    """Return one integer pair (x, y) with a*x + b*y == c, or None if there is none.

    Precondition: a, b and c are any Python integers; negative values and 0
    are allowed. If a == b == 0, the answer is (0, 0) when c == 0 and None
    otherwise. Otherwise a solution exists exactly when gcd(a, b) divides c,
    and the pair returned is (s * c/g, t * c/g) for the Bezout coefficients
    s and t that the extended Euclidean algorithm finds.

    Cost: O(1 + log min(|a|, |b|)) loop iterations. Python integers have
    arbitrary precision; for inputs of at most n bits the loop takes O(n^2)
    bit operations and the final products O(n^2) more.
    """
    if a == 0 and b == 0:  # @line L1
        return (0, 0) if c == 0 else None  # @line L2
    r0, s0, t0, r1, s1, t1 = abs(a), 1, 0, abs(b), 0, 1  # @line L3
    while r1 != 0:  # @line L4
        q = r0 // r1  # @line L5
        r0, r1 = r1, r0 - q * r1  # @line L6
        s0, s1 = s1, s0 - q * s1  # @line L7
        t0, t1 = t1, t0 - q * t1  # @line L8
    g = r0  # @line L9: g == |a|*s0 + |b|*t0 == gcd(a, b) > 0
    if c % g != 0:  # @line L10
        return None
    m = c // g
    x = s0 * m if a >= 0 else -s0 * m  # @line L11
    y = t0 * m if b >= 0 else -t0 * m
    return (x, y)  # @line L12
