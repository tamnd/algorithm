# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-entropy-deconvolution/. The authors are listed in prov/FDWZTR.jsonl.
"""Minimum entropy deconvolution (MED) by Wiggins' fixed-point iteration.

The filter f has L taps. For each trace x_i the output is the full
convolution y_i = f * x_i, of length len(x_i) + L - 1. The varimax norm of
an output is V(y) = sum_t y_t^4 / (sum_t y_t^2)^2, a number in [1/T, 1]
that is large for a spiky output. MED looks for the f that makes
sum_i V(y_i) stationary. With E_i = sum y_it^2, F_i = sum y_it^4,
b_ik = sum_t y_it^3 x_i(t - k) and R_i the autocorrelation matrix of x_i,
the gradient is zero exactly when

    sum_i (F_i / E_i^3) R_i f = sum_i b_i / E_i^2,

and the iteration solves this linear system for f with the right-hand side
and the weights taken from the current output.
"""

import math

import imgla as la


def convolve_full(f, x):
    """The full convolution y_t = sum_k f_k x_{t-k}, t = 0..len(x) + len(f) - 2."""
    n = len(x) + len(f) - 1
    y = [0.0] * n
    for k, fk in enumerate(f):
        if fk == 0:
            continue
        for t, xt in enumerate(x):
            y[t + k] += fk * xt
    return y


def varimax(y):
    """V(y) = sum y^4 / (sum y^2)^2 (0 for a zero signal)."""
    e = sum(v * v for v in y)
    if e == 0:
        return 0.0
    return sum(v ** 4 for v in y) / (e * e)


def total_varimax(f, traces):
    """sum_i V(f * x_i)."""
    return sum(varimax(convolve_full(f, x)) for x in traces)


def autocorrelation_matrix(x, length):
    """R[k][j] = sum_t x_{t-j} x_{t-k} = r_|k-j| (full convolution, so R is Toeplitz)."""
    r = [sum(x[t] * x[t + k] for t in range(len(x) - k)) for k in range(length)]
    return [[r[abs(k - j)] for j in range(length)] for k in range(length)]


def cross_term(y, x, length):
    """b_k = sum_t y_t^3 x_{t-k}, k = 0..length - 1."""
    y3 = [v ** 3 for v in y]
    return [sum(y3[t + k] * x[t] for t in range(len(x))) for k in range(length)]


def gradient(f, traces):
    """The gradient of sum_i V(f * x_i) with respect to f."""
    length = len(f)
    g = [0.0] * length
    for x in traces:
        y = convolve_full(f, x)
        e = sum(v * v for v in y)
        fq = sum(v ** 4 for v in y)
        b = cross_term(y, x, length)
        rf = [sum(y[t + k] * x[t] for t in range(len(x))) for k in range(length)]
        for k in range(length):
            g[k] += 4.0 * (b[k] * e - fq * rf[k]) / e ** 3
    return g


def med(traces, length, iters=30, f0=None, tol=1e-12):
    """Run the MED iteration. Returns (f, history of sum_i V)."""
    rs = [autocorrelation_matrix(x, length) for x in traces]
    if f0 is None:  # @line L1
        f = [0.0] * length
        f[length // 2] = 1.0
    else:
        f = list(f0)
    history = [total_varimax(f, traces)]
    for _ in range(iters):  # @line L2
        a = la.zeros(length, length)
        c = [0.0] * length
        for x, r in zip(traces, rs):
            y = convolve_full(f, x)  # @line L3
            e = sum(v * v for v in y)  # @line L4
            fq = sum(v ** 4 for v in y)
            w = fq / e ** 3
            for k in range(length):  # @line L5
                rowa, rowr = a[k], r[k]
                for j in range(length):
                    rowa[j] += w * rowr[j]
            b = cross_term(y, x, length)  # @line L6
            for k in range(length):
                c[k] += b[k] / (e * e)
        new = la.solve(a, c)  # @line L7
        nrm = math.sqrt(sum(v * v for v in new))
        new = [v / nrm for v in new]
        step = min(math.sqrt(sum((p - q) ** 2 for p, q in zip(new, f))),
                   math.sqrt(sum((p + q) ** 2 for p, q in zip(new, f))))
        f = new
        history.append(total_varimax(f, traces))
        if step < tol:
            break
    return f, history  # @line L8
