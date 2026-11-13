# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iir-filter/. The authors are listed in prov/546JYA.jsonl.

"""An IIR filter in the transposed direct form II, and an exact stability test.

The filter is H(z) = B(z) / A(z) with B(z) = b[0] + b[1] z^-1 + ... + b[q] z^-q
and A(z) = 1 + a[1] z^-1 + ... + a[p] z^-p. Pass Fraction coefficients for
exact results.
"""

from typing import Sequence


def iir_filter(b: Sequence, a: Sequence, x: Sequence) -> list:
    """Return y with y[n] = sum b[k] x[n - k] - sum_(k >= 1) a[k] y[n - k], zero initial state."""
    if not a or a[0] == 0:
        raise ValueError("a[0] must be nonzero")
    if a[0] != 1:
        b = [v / a[0] for v in b]
        a = [v / a[0] for v in a]
    n = max(len(a), len(b))
    b = list(b) + [0] * (n - len(b))
    a = list(a) + [0] * (n - len(a))
    z = [0] * (n - 1)  # @line L1: the state, all zero
    y = []
    for v in x:  # @line L2
        out = b[0] * v + (z[0] if n > 1 else 0)  # @line L3
        for i in range(n - 2):  # @line L4
            z[i] = b[i + 1] * v - a[i + 1] * out + z[i + 1]  # @line L5
        if n > 1:
            z[n - 2] = b[n - 1] * v - a[n - 1] * out  # @line L6
        y.append(out)  # @line L7
    return y


def impulse_response(b: Sequence, a: Sequence, length: int) -> list:
    """Return the first length values of the impulse response h[n]."""
    return iir_filter(b, a, [1] + [0] * (length - 1))


def reflection_coefficients(a: Sequence) -> list:
    """Run the Schur-Cohn step-down recursion on A(z) = a[0] + a[1] z^-1 + ... + a[p] z^-p.

    Return the reflection coefficients k_p, ..., k_1, or stop early with a
    last value of modulus at least 1. With Fraction input the result is exact.
    """
    c = list(a)
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    if c[0] != 1:
        c = [v / c[0] for v in c]
    ks = []
    while len(c) > 1:
        k = c[-1]
        ks.append(k)
        if abs(k) >= 1:
            return ks
        p = len(c) - 1
        d = 1 - k * k
        c = [(c[i] - k * c[p - i]) / d for i in range(p)]
    return ks


def is_stable(a: Sequence) -> bool:
    """True if and only if every root of z^p A(z) lies strictly inside the unit circle."""
    return all(abs(k) < 1 for k in reflection_coefficients(a))


def cascade(sections: Sequence, x: Sequence) -> list:
    """Run x through a list of (b, a) sections, one after the other."""
    y = list(x)
    for b, a in sections:
        y = iir_filter(b, a, y)
    return y
