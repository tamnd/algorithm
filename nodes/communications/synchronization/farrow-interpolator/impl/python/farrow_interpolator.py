# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/farrow-interpolator/. The authors are listed in prov/9JVEXY.jsonl.

"""The Farrow interpolator: a polynomial interpolation filter with the fractional delay as one parameter.

The input is a sequence x[n] on a grid of spacing T_s = 1. The output at the
time t = m + mu (basepoint index m, fractional interval 0 <= mu < 1) is

    y(m + mu) = sum_{i=0}^{D} c_i[m] mu^i,   c_i[m] = sum_{n} b[i][n] x[m + n],

where each c_i is the output of a fixed FIR filter b[i]. The polynomial in mu is
evaluated by Horner's rule. Two coefficient sets are given:

- cubic Lagrange (D = 3), taps at n = -1, 0, 1, 2: the polynomial through the
  four samples x[m-1], ..., x[m+2];
- piecewise parabolic (D = 2) of Erup, Gardner and Harris with parameter alpha,
  taps at n = -1, 0, 1, 2.

Both pass through the samples: y(m + 0) = x[m].
"""

import math
from typing import Sequence

# Rows are the filters b[0], ..., b[D]; columns are the taps n = -1, 0, 1, 2.
CUBIC_LAGRANGE: list[list[float]] = [
    [0.0, 1.0, 0.0, 0.0],
    [-1.0 / 3.0, -1.0 / 2.0, 1.0, -1.0 / 6.0],
    [1.0 / 2.0, -1.0, 1.0 / 2.0, 0.0],
    [-1.0 / 6.0, 1.0 / 2.0, -1.0 / 2.0, 1.0 / 6.0],
]


def parabolic(alpha: float = 0.5) -> list[list[float]]:
    """The piecewise parabolic coefficient rows for the parameter alpha."""
    return [
        [0.0, 1.0, 0.0, 0.0],
        [-alpha, alpha - 1.0, alpha + 1.0, -alpha],
        [alpha, -alpha, -alpha, alpha],
    ]


def farrow(x: Sequence[complex], m: int, mu: float, b: list[list[float]] = CUBIC_LAGRANGE) -> complex:
    """The interpolated value at t = m + mu, from the samples x[m - 1], ..., x[m + 2]."""
    window = (x[m - 1], x[m], x[m + 1], x[m + 2])  # @line L1
    c = [sum(row[j] * window[j] for j in range(4)) for row in b]  # @line L2
    y = c[-1]  # @line L3
    for i in range(len(c) - 2, -1, -1):  # @line L4
        y = y * mu + c[i]  # @line L5
    return y  # @line L6


def resample(x: Sequence[complex], times: Sequence[float], b: list[list[float]] = CUBIC_LAGRANGE) -> list[complex]:
    """Values at the given times (in input samples). Each time needs 1 <= t <= len(x) - 3."""
    out: list[complex] = []
    for t in times:
        m = math.floor(t)  # @line L7
        mu = t - m  # @line L8
        out.append(farrow(x, m, mu, b))  # @line L9
    return out


def nco_times(n_in: int, w: float, eta0: float = 0.0) -> list[float]:
    """Output times for the interpolation interval w = T_i / T_s (Gardner 1993 control).

    The first output is at eta0; each next one is w input samples later. Only
    times with a full four-sample window are returned.
    """
    out: list[float] = []
    t = eta0
    while t <= n_in - 3:
        if t >= 1:
            out.append(t)
        t += w
    return out


def impulse_response(t: float, b: list[list[float]] = CUBIC_LAGRANGE) -> float:
    """The continuous impulse response h(t) of the interpolator: y(t) = sum_n x[n] h(t - n)."""
    # y(m + mu) = sum_j sum_i b[i][j] mu^i x[m + j - 1], so h(mu - j + 1) = sum_i b[i][j] mu^i.
    for j in range(4):
        mu = t + j - 1
        if 0.0 <= mu < 1.0:
            return sum(b[i][j] * mu ** i for i in range(len(b)))
    return 0.0
