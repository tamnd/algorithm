# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-retrieval/. The authors are listed in prov/YZ4Y3G.jsonl.

"""Exact tools for the ambiguities of 1D Fourier phase retrieval.

A complex number is a pair (re, im) of Fractions, so every identity is exact.
For a finite signal x[0 .. n-1], |X(e^(i w))|^2 = sum_k r[k] e^(-i w k) with the
autocorrelation r[k] = sum_n x[n + k] conj(x[n]), k = -(n-1) .. n-1. Two signals
have the same Fourier magnitude at every w exactly when their autocorrelations
are equal, so all comparisons below are made on r.
"""

from fractions import Fraction
from typing import Iterable, Sequence

C = tuple  # a pair (re, im) of Fractions


def c(re, im=0) -> C:
    return (Fraction(re), Fraction(im))


def add(a: C, b: C) -> C:
    return (a[0] + b[0], a[1] + b[1])


def mul(a: C, b: C) -> C:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conj(a: C) -> C:
    return (a[0], -a[1])


def neg(a: C) -> C:
    return (-a[0], -a[1])


def as_complex(x: Iterable) -> list[C]:
    out = []
    for v in x:
        if isinstance(v, tuple):
            out.append(c(*v))
        elif isinstance(v, complex):
            out.append(c(Fraction(v.real), Fraction(v.imag)))
        else:
            out.append(c(v))
    return out


def trim(x: Sequence[C]) -> list[C]:
    """Drop leading and trailing zeros: the support of the signal."""
    z = c(0)
    lo, hi = 0, len(x)
    while lo < hi and x[lo] == z:
        lo += 1
    while hi > lo and x[hi - 1] == z:
        hi -= 1
    return list(x[lo:hi])


def autocorrelation(x: Sequence) -> list[C]:
    """r[k] for k = -(n-1) .. n-1 of the trimmed signal, as a list of length 2n - 1."""
    x = trim(as_complex(x))
    n = len(x)
    out = []
    for k in range(-(n - 1), n):
        acc = c(0)
        for i in range(n):
            if 0 <= i + k < n:
                acc = add(acc, mul(x[i + k], conj(x[i])))
        out.append(acc)
    return out


def same_magnitude(x: Sequence, y: Sequence) -> bool:
    """True iff |X(e^(i w))| = |Y(e^(i w))| for every w."""
    return autocorrelation(x) == autocorrelation(y)


def shift(x: Sequence, n0: int) -> list[C]:
    """x[n - n0]: n0 zeros in front. The magnitude does not see it."""
    return [c(0)] * n0 + as_complex(x)


def conjugate_flip(x: Sequence) -> list[C]:
    """conj(x[-n]), moved back to start at index 0."""
    return [conj(v) for v in reversed(as_complex(x))]


def global_phase(x: Sequence, u: C) -> list[C]:
    """u x[n] for a unit complex number u, for example (3/5, 4/5)."""
    u = c(*u)
    if u[0] * u[0] + u[1] * u[1] != 1:
        raise ValueError("u must have modulus 1")
    return [mul(u, v) for v in as_complex(x)]


def from_zeros(lead: C, zeros: Sequence[C]) -> list[C]:
    """The signal lead * prod (1 - a z^(-1)), as coefficients of z^0, z^(-1), ..."""
    p = [c(*lead)]
    for a in zeros:
        a = c(*a)
        q = [c(0)] * (len(p) + 1)
        for i, v in enumerate(p):
            q[i] = add(q[i], v)
            q[i + 1] = add(q[i + 1], neg(mul(a, v)))
        p = q
    return p


def flip_zeros(lead: C, zeros: Sequence[C], mask: int) -> list[C]:
    """Replace the factor (1 - a z^(-1)) by (-conj(a) + z^(-1)) for each zero whose bit is set.

    |e^(-i w) - conj(a)| = |1 - a e^(-i w)| on the unit circle, so the magnitude
    is unchanged; the zero a moves to 1 / conj(a).
    """
    p = [c(*lead)]
    for b, a in enumerate(zeros):
        a = c(*a)
        f = [neg(conj(a)), c(1)] if mask >> b & 1 else [c(1), neg(a)]
        q = [c(0)] * (len(p) + 1)
        for i, v in enumerate(p):
            q[i] = add(q[i], mul(f[0], v))
            q[i + 1] = add(q[i + 1], mul(f[1], v))
        p = q
    return p


def trivial_class(x: Sequence) -> set:
    """The real signals that differ from a real x only by sign and reversal (shift removed by trim)."""
    x = trim(as_complex(x))
    out = set()
    for s in (x, list(reversed(x))):
        for sign in (1, -1):
            out.add(tuple(v[0] * sign for v in s))
    return out


def brute_force_same_magnitude(target: Sequence[int], bound: int) -> list[tuple]:
    """All integer signals of the same length, entries in -bound .. bound, ends nonzero, with the target's magnitude."""
    n = len(target)
    want = autocorrelation(target)
    found = []

    def rec(prefix):
        if len(prefix) == n:
            if prefix[0] != 0 and prefix[-1] != 0 and autocorrelation(prefix) == want:
                found.append(tuple(prefix))
            return
        for v in range(-bound, bound + 1):
            rec(prefix + [v])

    rec([])
    return found


def error_reduction(mag: Sequence[float], support: int, x0: Sequence[float], iterations: int) -> tuple[list[float], list[float]]:
    """Fienup's error-reduction iteration for a real signal with known support 0 .. support-1.

    mag is |DFT_L(x)| for a length L >= 2 support - 1. Each step imposes the
    magnitude in frequency and the support in time. Returns the last estimate
    and the squared Fourier-domain error before each step; it does not increase.
    """
    import cmath
    import math

    size = len(mag)

    def dft(a, sign):
        return [sum(a[j] * cmath.exp(sign * 2j * math.pi * j * k / size) for j in range(size)) for k in range(size)]

    g = list(x0) + [0.0] * (size - len(x0))
    history = []
    for _ in range(iterations):
        spec = dft(g, -1)
        history.append(sum((abs(v) - a) ** 2 for v, a in zip(spec, mag)))
        fixed = [a * v / abs(v) if v != 0 else complex(a) for v, a in zip(spec, mag)]
        back = [v / size for v in dft(fixed, 1)]
        g = [back[j].real if j < support else 0.0 for j in range(size)]
    spec = dft(g, -1)
    history.append(sum((abs(v) - a) ** 2 for v, a in zip(spec, mag)))
    return g[:support], history
