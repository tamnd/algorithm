# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-predictive-coding/. The authors are listed in prov/YG23QB.jsonl.

"""Linear predictive coding by the autocorrelation method.

lpc_analyze windows a frame, computes its autocorrelation r[0..p] and runs
Durbin's recursion. It returns the predictor a[1..p] of
x_hat[n] = sum_k a[k] x[n - k], the reflection coefficients k[1..p] and the
prediction error energy E_p. The gain of the synthesis filter is sqrt(E_p).

All functions use only +, -, * and /, apart from lpc_gain and hann_window,
so frames of Fraction give exact results. Frames of int or float give
floating-point results, because the division of line L6 is a true division.
"""

import math
from typing import Optional, Sequence


def hann_window(n: int) -> list[float]:
    """Symmetric Hann window of length n (all ones for n = 1)."""
    if n == 1:
        return [1.0]
    return [0.5 - 0.5 * math.cos(2 * math.pi * i / (n - 1)) for i in range(n)]


def autocorrelation(s: Sequence, p: int) -> list:
    """r[k] = sum_{n=k}^{N-1} s[n] s[n-k] for k = 0..p. Cost O(N p)."""
    n = len(s)
    zero = s[0] - s[0] if n else 0
    return [sum((s[i] * s[i - k] for i in range(k, n)), zero) for k in range(p + 1)]


def durbin(r: Sequence, p: int) -> tuple[list, list, object]:
    """Durbin's recursion for the Toeplitz normal equations of order p.

    Precondition: the Toeplitz matrix of r[0..p] is positive definite (true
    for the autocorrelation of any frame that is not all zero). Returns
    (a, k, err) with sum_j a[j] r[|i - j|] = r[i] for i = 1..p (indices from
    1 in the math, from 0 in the lists) and err = r[0] - sum_j a[j] r[j].
    Cost O(p^2) operations.
    """
    a: list = []
    ks: list = []
    err = r[0]  # @line L4
    for i in range(1, p + 1):  # @line L5
        if err <= 0:
            raise ValueError("the Toeplitz matrix is not positive definite")
        acc = r[i]
        for j in range(1, i):
            acc = acc - a[j - 1] * r[i - j]
        k = acc / err  # @line L6
        a = [a[j - 1] - k * a[i - j - 1] for j in range(1, i)] + [k]  # @line L7
        err = (1 - k * k) * err  # @line L8
        ks.append(k)
    return a, ks, err


def lpc_analyze(x: Sequence, p: int, window: Optional[Sequence] = None) -> tuple[list, list, object]:
    """LPC analysis of one frame by the autocorrelation method.

    window is a sequence of the same length as x, or None for a rectangular
    window. A frame that is zero after the window gives a = 0, k = 0 and
    err = 0. Cost O(N p + p^2) operations for a frame of N samples.
    """
    if p < 1 or not x:
        raise ValueError("need p >= 1 and a frame that is not empty")
    s = list(x) if window is None else [w * v for w, v in zip(window, x)]  # @line L1
    r = autocorrelation(s, p)  # @line L2
    if r[0] == 0:  # @line L3
        zero = 0 * r[0]
        return [zero] * p, [zero] * p, zero
    return durbin(r, p)  # @line L10


def lpc_gain(err) -> float:
    """Gain G = sqrt(E_p) of the synthesis filter G / A(z)."""
    return math.sqrt(err)  # @line L9


def lpc_residual(x: Sequence, a: Sequence) -> list:
    """Prediction error e[n] = x[n] - sum_k a[k] x[n-k] for n = 0..N+p-1.

    x is taken as zero outside the frame, as in the autocorrelation method,
    so sum(e[n]^2) is the error energy that the analysis minimizes.
    """
    n, p = len(x), len(a)
    out = []
    for t in range(n + p):
        acc = x[t] if t < n else 0 * x[0]
        for k in range(1, p + 1):
            if 0 <= t - k < n:
                acc = acc - a[k - 1] * x[t - k]
        out.append(acc)
    return out


def lpc_synthesize(a: Sequence, gain, excitation: Sequence) -> list:
    """All-pole synthesis y[n] = gain * e[n] + sum_k a[k] y[n-k], zero start.

    This is the filter gain / A(z). It is causal, and stable when the zeros
    of A lie inside the unit circle. Cost O(p) per output sample.
    """
    p = len(a)
    y: list = []
    for t, e in enumerate(excitation):  # @line L11
        acc = gain * e
        for k in range(1, p + 1):
            if t - k >= 0:
                acc = acc + a[k - 1] * y[t - k]
        y.append(acc)  # @line L12
    return y
