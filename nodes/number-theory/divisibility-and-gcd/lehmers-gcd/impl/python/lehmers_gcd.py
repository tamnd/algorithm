# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lehmers-gcd/. The authors are listed in prov/RN6MV6.jsonl.


def lehmer_gcd(a: int, b: int, w: int = 64) -> int:
    """Return gcd(a, b) >= 0 by Lehmer's algorithm, with gcd(0, 0) == 0.

    Precondition: a and b are any Python integers (negative values and 0 are
    allowed; signs are dropped first), and w >= 2 is the word size in bits.
    Numbers below 2**w count as single precision.

    The outer loop works on the leading w bits of u and v. It runs Euclid's
    steps on these short numbers while Knuth's test proves that each quotient
    is the true quotient of u by v, then applies all those steps to u and v
    at once with a 2x2 matrix. If no step is proved, it does one ordinary
    division step on u and v. When v fits in w bits, it ends with Euclid's
    algorithm on single-precision numbers.

    Cost: for n-bit inputs, at most O(n) outer iterations, each costing
    O(n / w) word operations plus O(1) per Euclid step on the leading parts,
    so O(n^2) bit operations in the worst case, like Euclid's algorithm; on
    typical inputs each outer iteration replaces many multiprecision steps.
    """
    u, v = abs(a), abs(b)
    if u < v:
        u, v = v, u
    base = 1 << w
    while v >= base:  # @line L1
        s = u.bit_length() - w  # @line L2
        uh, vh = u >> s, v >> s
        A, B, C, D = 1, 0, 0, 1  # @line L3
        while vh + C > 0 and vh + D > 0:  # @line L4
            q = (uh + A) // (vh + C)  # @line L5
            if q == 0 or q != (uh + B) // (vh + D):  # @line L6
                break
            A, B, C, D = C, D, A - q * C, B - q * D  # @line L7
            uh, vh = vh, uh - q * vh  # @line L8
        if B == 0:  # @line L9
            u, v = v, u % v
        else:
            u, v = A * u + B * v, C * u + D * v  # @line L10
    while v != 0:  # @line L11
        u, v = v, u % v
    return u  # @line L12
