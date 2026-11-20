# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mismatched-filter-design/. The authors are listed in prov/T4GZMK.jsonl.

"""Least squares mismatched filter for a phase code, in the manner of Ackroyd and Ghani (1973).

The code is s[0..N-1] and the filter is h[0..L-1]. The filter output is the
linear convolution y[m] = sum over i of h[i] s[m - i], m = 0 .. N + L - 2.
The design asks y to be as close as possible to a unit spike at the center
index c = (N + L - 2) // 2, in the least squares sense:

    minimize || C h - d ||^2,   C[m][i] = s[m - i],   d = the unit vector at c.

The normal equations are R g = e with R[i][j] = r[i - j], where
r[k] = sum over n of s[n + k] conj(s[n]) is the aperiodic autocorrelation of
the code, and e[i] = conj(s[c - i]). The same g, scaled to a unit peak, also
has the least integrated sidelobe level among all filters of length L.

The arithmetic is generic: with int or Fraction codes every step is exact,
with complex codes it is in floating point. With L = N the matched filter
h[i] = conj(s[N - 1 - i]) is the reference.
"""

from fractions import Fraction
from typing import Sequence


def conj(x):
    """Complex conjugate; int and Fraction values are their own conjugate."""
    return x.conjugate()


def autocorrelation(s: Sequence) -> list:
    """r[k] = sum over n of s[n + k] conj(s[n]) for k = 0 .. N - 1. Cost: Theta(N^2)."""
    n = len(s)
    return [sum((s[i + k] * conj(s[i]) for i in range(n - k)), 0) for k in range(n)]


def convolve(h: Sequence, s: Sequence) -> list:
    """y[m] = sum over i of h[i] s[m - i], m = 0 .. len(h) + len(s) - 2."""
    out = [0] * (len(h) + len(s) - 1)
    for i, a in enumerate(h):
        for j, b in enumerate(s):
            out[i + j] += a * b
    return out


def solve(a: list, b: list) -> list:
    """Gaussian elimination with partial pivoting on a copy of a. Exact for Fraction entries."""
    n = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if m[piv][col] == 0:
            raise ValueError("singular system")
        m[col], m[piv] = m[piv], m[col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            if f != 0:
                for k in range(col, n + 1):
                    m[r][k] -= f * m[col][k]
    x = [0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum((m[r][k] * x[k] for k in range(r + 1, n)), 0)) / m[r][r]
    return x


def center(n: int, length: int) -> int:
    """The index c of the main peak in an output of n + length - 1 samples."""
    return (n + length - 2) // 2


def _check(s: Sequence, length: int, c: int | None) -> int:
    n = len(s)
    if n == 0 or length < 1 or not any(x != 0 for x in s):
        raise ValueError("need a nonzero code and a positive length")
    if c is None:
        c = center(n, length)
    if not 0 <= c <= n + length - 2:
        raise ValueError("the peak index is outside the output")
    return c


def _unit(s: Sequence):
    """1 as a Fraction for an exact code, else 1.0."""
    return Fraction(1) if all(isinstance(x, (int, Fraction)) for x in s) else 1.0


def mismatched_filter(s: Sequence, length: int, c: int | None = None) -> list:
    """The least squares mismatched filter of the given length, scaled so that y[c] = 1.

    For int codes the result is a list of Fraction values. Cost: Theta(N^2 + L^3) with
    Gaussian elimination (a Levinson solver for the Toeplitz system would take Theta(L^2)).
    """
    c = _check(s, length, c)
    n = len(s)
    one = _unit(s)
    r = autocorrelation(s)  # @line L1
    rr = [[one * 0] * length for _ in range(length)]
    for i in range(length):  # @line L2
        for j in range(length):
            k = i - j
            if abs(k) < n:
                rr[i][j] = one * (r[k] if k >= 0 else conj(r[-k]))  # @line L2
    e = [one * conj(s[c - i]) if 0 <= c - i < n else one * 0 for i in range(length)]  # @line L3
    g = solve(rr, e)  # @line L4
    peak = sum((conj(e[i]) * g[i] for i in range(length)), 0)  # @line L5
    return [x / peak for x in g]  # @line L6


def matched_filter(s: Sequence) -> list:
    """h[i] = conj(s[N - 1 - i]) / E with E = sum of |s|^2, so that the peak output is 1."""
    energy = sum((x * conj(x) for x in s), 0)
    return [_unit(s) * conj(x) / energy for x in reversed(s)]


def metrics(s: Sequence, h: Sequence, c: int | None = None) -> dict:
    """Measures of the output y = h * s around the peak index c.

    psl2 is the largest |y[m]|^2 / |y[c]|^2 with m != c (a power ratio), isl the sum of these
    ratios, and loss the SNR of the filter over the SNR of the matched filter in white noise,
    |y[c]|^2 / (||h||^2 ||s||^2), a ratio in (0, 1]. All are exact for Fraction input."""
    if c is None:
        c = center(len(s), len(h))
    y = convolve(h, s)

    def p(v):
        return (v * conj(v)).real  # a Fraction stays a Fraction

    p2 = p(y[c])
    side2 = [p(v) for m, v in enumerate(y) if m != c]
    hh = sum((p(v) for v in h), 0)
    ss = sum((p(v) for v in s), 0)
    return {
        "peak": y[c],
        "psl2": max(side2) / p2 if side2 else 0 * p2,
        "isl": sum(side2, 0) / p2,
        "loss": p2 / (hh * ss),
        "output": y,
    }


def min_isl(s: Sequence, length: int, c: int | None = None):
    """The closed form 1 / (e^H R^-1 e) - 1 of the least integrated sidelobe level at unit peak.

    This is computed from the normal equations alone, not from the filter output."""
    c = _check(s, length, c)
    n = len(s)
    one = _unit(s)
    r = autocorrelation(s)
    rr = [[one * (r[i - j] if i >= j else conj(r[j - i])) if abs(i - j) < n else one * 0
           for j in range(length)] for i in range(length)]
    e = [one * conj(s[c - i]) if 0 <= c - i < n else one * 0 for i in range(length)]
    g = solve(rr, e)
    q = sum((conj(e[i]) * g[i] for i in range(length)), 0).real  # e^H R^-1 e is real and positive
    return 1 / q - 1
