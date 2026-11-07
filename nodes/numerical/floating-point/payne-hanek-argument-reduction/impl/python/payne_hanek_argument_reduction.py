# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/payne-hanek-argument-reduction/. The authors are listed in prov/H4GFMJ.jsonl.

"""Payne-Hanek reduction of a binary64 argument modulo pi/2.

reduce(x) returns (k, r_hi, r_lo) with k in {0, 1, 2, 3} and
x = (4j + k) * pi/2 + r for some integer j, where r_hi + r_lo approximates
r with |r| <= pi/4 (up to a tiny excess at the boundary).

The bits of 2/pi and pi/2 are computed once with integer arithmetic from
Machin's formula, so the module needs no stored constant.
"""

import math

P = 245          # bits of the product kept after the binary point
Q = 245          # bits of pi/2 used to turn the fraction into radians
N = 971 + P + 8  # bits of 2/pi needed for the largest binary64 exponent

_PI_OVER_4 = 0.7853981633974483  # fl(pi/4), which is below pi/4


def _arctan_inv(n, bits):
    """floor-ish of 2^bits * arctan(1/n) for an integer n >= 2."""
    total = 0
    term = (1 << bits) // n
    n2 = n * n
    k = 1
    sign = 1
    while term:
        total += sign * (term // k)
        term //= n2
        k += 2
        sign = -sign
    return total


def _pi_scaled(bits):
    """An integer within a few units of 2^bits * pi (Machin's formula)."""
    g = 32
    s = 16 * _arctan_inv(5, bits + g) - 4 * _arctan_inv(239, bits + g)
    return s >> g


_EXTRA = 64
_PI_BIG = _pi_scaled(N + _EXTRA)
# TWO_OVER_PI = floor(2^N * 2/pi): bit i of 2/pi (i >= 1) is bit N - i here.
TWO_OVER_PI = (1 << (2 * N + _EXTRA + 1)) // _PI_BIG
# PIO2 = round(2^Q * pi/2).
PIO2 = (_PI_BIG + (1 << (N + _EXTRA - Q))) >> (N + _EXTRA - Q + 1)


def _to_double_double(num, shift):
    """Round num / 2^shift to (hi, lo) with hi = fl(v) and lo = fl(v - hi)."""
    hi = math.ldexp(float(num), -shift) if num else 0.0
    n, d = hi.as_integer_ratio()
    rest = num - (n << shift) // d          # exact: hi * 2^shift is an integer here
    lo = math.ldexp(float(rest), -shift) if rest else 0.0
    return hi, lo


def reduce(x):
    """Return (k, r_hi, r_lo) for a finite binary64 x."""
    if not math.isfinite(x):
        raise ValueError("argument must be finite")
    if abs(x) <= _PI_OVER_4:                               # @line L1
        return 0, x, 0.0
    m, e = math.frexp(abs(x))                              # @line L2
    M = int(math.ldexp(m, 53))
    E = e - 53                                             # |x| = M * 2^E
    i0 = max(1, E - 1)                                     # @line L3
    i1 = E + P
    W = (TWO_OVER_PI >> (N - i1)) & ((1 << (i1 - i0 + 1)) - 1)  # @line L4
    Z = M * W                                              # @line L5
    k = (Z >> P) & 3                                       # @line L6
    F = Z & ((1 << P) - 1)
    if F >= 1 << (P - 1):                                  # @line L7
        k = (k + 1) & 3
        F -= 1 << P
    hi, lo = _to_double_double(F * PIO2, P + Q)            # @line L8
    if x < 0:                                              # @line L9
        k = (-k) & 3
        hi, lo = -hi, -lo
    return k, hi, lo                                       # @line L10


def sin_via_reduction(x):
    """sin(x) from the reduced argument, to show how k is used."""
    k, hi, lo = reduce(x)
    s = math.sin(hi) + math.cos(hi) * lo
    c = math.cos(hi) - math.sin(hi) * lo
    return (s, c, -s, -c)[k]


def naive_reduce(x):
    """The textbook one-constant reduction, which fails for large x."""
    k = round(x * (2 / math.pi))
    return k & 3, x - k * (math.pi / 2)


if __name__ == "__main__":
    for x in (1e22, 6381956970095103 * 2.0 ** 797, 1e300, -5.0):
        k, hi, lo = reduce(x)
        print(repr(x), k, repr(hi), repr(lo), sin_via_reduction(x), math.sin(x))
