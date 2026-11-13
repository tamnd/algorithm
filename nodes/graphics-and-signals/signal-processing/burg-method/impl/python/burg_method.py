# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burg-method/. The authors are listed in prov/CXSG6S.jsonl.

"""Burg's method: an AR(p) model fitted by forward-backward lattice prediction.

The model is A(z) = 1 + a[1] z^-1 + ... + a[p] z^-p, the prediction error
filter, and the spectrum estimate is S(w) = E / |A(e^(iw))|^2 with w in
radians per sample.
"""

import cmath
from typing import Sequence


def _conj(v):
    return v.conjugate() if isinstance(v, complex) else v


def _abs2(v):
    return v.real * v.real + v.imag * v.imag if isinstance(v, complex) else v * v


def burg(x: Sequence, p: int) -> tuple[list, list, object]:
    """Return (a, k, E): the coefficients a[0] = 1, ..., a[p], the reflection
    coefficients k[1..p] (as a list of length p) and the error power E.

    Each k[m] minimizes the sum of the squared forward and backward
    prediction errors of order m over the samples where both are defined,
    so |k[m]| <= 1. With int or Fraction input the arithmetic is exact.
    Precondition: 0 <= p < N. Cost: about 5 N p multiplies.
    """
    a, ks, e, _, _ = burg_with_errors(x, p)
    return a, ks, e


def burg_with_errors(x: Sequence, p: int) -> tuple[list, list, object, list, list]:
    """burg, plus the final forward errors f[t] and backward errors b[t] (valid for t >= p)."""
    n = len(x)
    if not 0 <= p < n:
        raise ValueError("need 0 <= p < N")
    f = list(x)  # @line L1
    b = list(x)
    e = sum(_abs2(v) for v in x) / n
    a = [1]
    ks = []
    for m in range(1, p + 1):  # @line L2
        num = 0
        den = 0
        for t in range(m, n):  # @line L3
            num += f[t] * _conj(b[t - 1])
            den += _abs2(f[t]) + _abs2(b[t - 1])
        k = -2 * num / den if den != 0 else 0  # @line L4
        ext = a + [0]
        a = [ext[i] + k * _conj(ext[m - i]) for i in range(m + 1)]  # @line L5
        new_f = list(f)
        new_b = list(b)
        for t in range(m, n):  # @line L6
            new_f[t] = f[t] + k * b[t - 1]
            new_b[t] = b[t - 1] + _conj(k) * f[t]
        f, b = new_f, new_b
        e = (1 - _abs2(k)) * e  # @line L7
        ks.append(k)
    return a, ks, e, f, b  # @line L8


def burg_psd(a: Sequence[complex], e: float, w: float) -> float:
    """S(w) = E / |sum of a[i] e^(-iwi)|^2."""
    s = sum(c * cmath.exp(-1j * w * i) for i, c in enumerate(a))
    return float(e) / abs(s) ** 2


def step_down(a: Sequence) -> list:
    """Recover k[1..p] from a by the inverse Levinson recursion. Raises if some |k| = 1."""
    a = list(a)
    p = len(a) - 1
    ks = [0] * p
    for m in range(p, 0, -1):
        k = a[m]
        ks[m - 1] = k
        den = 1 - _abs2(k)
        if den == 0:
            raise ValueError("|k| = 1: the filter has a zero on the unit circle")
        a = [(a[i] - k * _conj(a[m - i])) / den for i in range(m)]
    return ks
