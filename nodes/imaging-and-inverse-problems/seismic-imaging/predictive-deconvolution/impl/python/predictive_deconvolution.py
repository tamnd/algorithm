# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/predictive-deconvolution/. The authors are listed in prov/R3R43H.jsonl.
"""Predictive deconvolution with a Wiener prediction error filter.

A prediction filter a_0..a_{n-1} with gap alpha predicts d[t + alpha] from
d[t], d[t - 1], .., d[t - n + 1]. Its least-squares taps solve the Toeplitz
normal equations sum_j a_j r_|i-j| = r_{alpha+i}, i = 0..n-1, with r the
trace autocorrelation. The prediction error filter is
f = (1, 0, .., 0, -a_0, .., -a_{n-1}) with alpha - 1 zeros, and the output is
e = f * d. alpha = 1 is spiking deconvolution. Works with float and with
fractions.Fraction values.
"""


def autocorrelation(d, maxlag):
    """r_k = sum_t d_t d_{t+k} for k = 0..maxlag (zero beyond the trace)."""
    n = len(d)
    return [sum(d[t] * d[t + k] for t in range(n - k)) if k < n else 0 * d[0]
            for k in range(maxlag + 1)]


def levinson(r, g):
    """Solve the symmetric Toeplitz system sum_j x_j r_|i-j| = g_i, i = 0..n-1.

    r has at least n entries and the matrix must be positive definite.
    Levinson recursion: O(n^2) operations and O(n) extra memory.
    """
    n = len(g)
    if r[0] == 0:
        raise ValueError("r_0 must be positive")
    a = [1 + 0 * r[0]]
    err = r[0]
    x = [g[0] / r[0]]
    for m in range(1, n):
        delta = sum(a[j] * r[m - j] for j in range(m))
        k = -delta / err
        ext = a + [0 * r[0]]
        a = [ext[j] + k * ext[m - j] for j in range(m + 1)]
        err = err * (1 - k * k)
        if err <= 0:
            raise ValueError("the Toeplitz matrix is not positive definite")
        eps = sum(x[j] * r[m - j] for j in range(m))
        mu = (g[m] - eps) / err
        x = x + [0 * r[0]]
        x = [x[j] + mu * a[m - j] for j in range(m + 1)]
    return x


def prediction_filter(r, n, gap, prewhitening=0):
    """The n prediction taps for the gap from the autocorrelation r (at least n + gap lags)."""
    rr = [r[0] * (1 + prewhitening)] + list(r[1:n])  # @line L2
    g = [r[gap + i] for i in range(n)]
    return levinson(rr, g)  # @line L3


def prediction_error_filter(a, gap):
    """f = (1, 0 .. 0, -a_0 .. -a_{n-1}) with gap - 1 zeros."""
    one = 1 + 0 * a[0]
    return [one] + [0 * one] * (gap - 1) + [-v for v in a]


def apply_filter(f, d):
    """The causal convolution e_t = sum_k f_k d_{t-k}, t = 0..len(d) - 1."""
    return [sum(f[k] * d[t - k] for k in range(min(len(f), t + 1))) for t in range(len(d))]


def predictive_deconvolution(d, n, gap=1, prewhitening=0, design=None):
    """Design the filter on d[design[0]:design[1]] (default the whole trace) and apply it to d.

    Returns (e, f): the output trace and the prediction error filter.
    """
    lo, hi = (0, len(d)) if design is None else design
    r = autocorrelation(d[lo:hi], n + gap - 1)  # @line L1
    a = prediction_filter(r, n, gap, prewhitening)
    f = prediction_error_filter(a, gap)  # @line L4
    e = apply_filter(f, d)  # @line L5
    return e, f  # @line L6
