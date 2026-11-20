# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moving-target-indication/. The authors are listed in prov/YMQQ6D.jsonl.

"""The L-pulse MTI canceller, a binomial FIR filter in slow time.

X[p][r] is the complex sample of pulse p (slow time, p = 0 .. P-1) at range
bin r (fast time, r = 0 .. M-1). The canceller with L pulses has the weights
w[i] = (-1)^i C(L-1, i), the coefficients of (1 - z^-1)^(L-1), and gives

    y[q][r] = sum over i = 0 .. L-1 of w[i] X[q + L - 1 - i][r],   q = 0 .. P - L.

The two-pulse canceller (L = 2) is X[p] - X[p-1]. Its response to a Doppler
frequency f_d at the pulse repetition frequency PRF has magnitude
(2 |sin(pi f_d / PRF)|)^(L-1). It is zero at f_d = n PRF, so the blind speeds
are v_n = n lambda PRF / 2.

With int input the output is exact.
"""

import cmath
import math
from typing import Sequence


def canceller_weights(n_pulses: int) -> list[int]:
    """w[i] = (-1)^i C(L-1, i) for i = 0 .. L-1. L = 2 gives [1, -1], L = 3 gives [1, -2, 1]."""
    if n_pulses < 1:
        raise ValueError("need L >= 1")
    return [(-1) ** i * math.comb(n_pulses - 1, i) for i in range(n_pulses)]


def mti_cancel(x: Sequence[Sequence], n_pulses: int) -> list[list]:
    """Apply the L-pulse canceller along slow time, in every range bin.

    x is a list of P pulses, each a list of M samples. The output has P - L + 1
    rows (none if P < L). Cost: Theta(L P M) operations, O(L) extra space.
    """
    w = canceller_weights(n_pulses)  # @line L1
    n_rows = len(x)
    m = len(x[0]) if x else 0
    if any(len(row) != m for row in x):
        raise ValueError("every pulse needs the same number of range bins")
    y = []
    for p in range(n_pulses - 1, n_rows):  # @line L2
        out = []
        for r in range(m):  # @line L3
            out.append(sum(w[i] * x[p - i][r] for i in range(n_pulses)))  # @line L4
        y.append(out)
    return y  # @line L5


def response(n_pulses: int, f_norm: float) -> complex:
    """H(f) = sum_i w[i] e^(-j 2 pi f i), with f = f_d / PRF, by the direct sum."""
    w = canceller_weights(n_pulses)
    return sum(c * cmath.exp(-2j * math.pi * f_norm * i) for i, c in enumerate(w))


def response_magnitude(n_pulses: int, f_norm: float) -> float:
    """The closed form |H(f)| = (2 |sin(pi f)|)^(L-1)."""
    return (2.0 * abs(math.sin(math.pi * f_norm))) ** (n_pulses - 1)


def blind_speeds(wavelength: float, prf: float, count: int) -> list[float]:
    """The first count blind speeds v_n = n lambda PRF / 2, n = 1 .. count, in m/s."""
    return [n * wavelength * prf / 2.0 for n in range(1, count + 1)]


def improvement_factor(n_pulses: int, rho: Sequence[float]) -> float:
    """I = (sum of w^2) / (sum over i, k of w[i] w[k] rho[|i - k|]).

    rho[0] = 1, rho[1], ... is the normalized autocorrelation of the clutter
    from pulse to pulse. The numerator is the average gain for a target whose
    Doppler is uniform over one PRF interval.
    """
    w = canceller_weights(n_pulses)
    num = sum(c * c for c in w)
    den = sum(w[i] * w[k] * rho[abs(i - k)] for i in range(n_pulses) for k in range(n_pulses))
    return num / den


def gaussian_clutter_rho(sigma_f: float, prf: float, lags: int) -> list[float]:
    """rho_k = exp(-2 pi^2 sigma_f^2 k^2 / PRF^2) for a Gaussian clutter spectrum of std sigma_f in Hz."""
    return [math.exp(-2.0 * math.pi ** 2 * sigma_f ** 2 * k * k / prf ** 2) for k in range(lags)]
