# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shewchuk-expansion-sum/. The authors are listed in prov/A734Z5.jsonl.

"""Shewchuk's expansion arithmetic for exact summation.

An expansion is a list of nonzero binary64 numbers, smallest magnitude first,
whose bits do not overlap. Its value is the exact sum of its components.
grow_expansion adds one float exactly; shewchuk_sum adds a sequence exactly
and rounds the result correctly, which is the method behind math.fsum.
"""

import math


def two_sum(a, b):
    """s = fl(a + b) and t = a + b - s exactly (Knuth, Moller)."""
    s = a + b
    bv = s - a
    av = s - bv
    t = (a - av) + (b - bv)
    return s, t


def fast_two_sum(a, b):
    """Requires |a| >= |b| (or a == 0); then s + t = a + b exactly."""
    s = a + b
    t = b - (s - a)
    return s, t


def grow_expansion(e, x):
    """Return the expansion of value(e) + x (Shewchuk, Grow-Expansion)."""
    Q = x                                                  # @line L3
    h = []
    for y in e:                                            # @line L4
        Q, t = two_sum(Q, y)                               # @line L5
        if t != 0.0:                                       # @line L6
            h.append(t)
    if Q != 0.0:                                           # @line L7
        h.append(Q)
    return h


def expansion_sum(e, f):
    """Exact sum of two expansions, by growing e with each component of f."""
    for y in f:
        e = grow_expansion(e, y)
    return e


def round_expansion(e):
    """Correctly rounded (to nearest, ties to even) value of an expansion."""
    if not e:
        return 0.0
    j = len(e) - 1
    s = e[j]                                               # @line L8
    t = 0.0
    while j > 0:                                           # @line L9
        j -= 1
        s, t = fast_two_sum(s, e[j])
        if t != 0.0:
            break
    if t != 0.0 and j > 0 and (t < 0) == (e[j - 1] < 0):  # @line L10
        y = 2.0 * t
        x = s + y
        if x - s == y and math.isfinite(x):
            s = x
    return s                                               # @line L11


def shewchuk_sum(xs):
    """Correctly rounded sum of finite or special floats, like math.fsum."""
    e = []                                                 # @line L1
    special = 0.0
    inf_seen = False
    for x in xs:                                           # @line L2
        if not math.isfinite(x):
            inf_seen = True
            special += x
            continue
        e = grow_expansion(e, x)
        if e and not math.isfinite(e[-1]):
            raise OverflowError("intermediate overflow in shewchuk_sum")
    if inf_seen:
        return special
    return round_expansion(e)


def value(e):
    """Exact value of an expansion as a Fraction (for checking)."""
    from fractions import Fraction
    return sum((Fraction(c) for c in e), Fraction(0))


if __name__ == "__main__":
    for xs in ([0.1] * 10, [1e100, 1.0, -1e100], [1.0, 2.0 ** -53, 2.0 ** -106]):
        print(xs, sum(xs), shewchuk_sum(xs), math.fsum(xs))
    e = []
    for x in [0.1] * 10:
        e = grow_expansion(e, x)
    print(e)
