# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matched-filter/. The authors are listed in prov/3Q26KM.jsonl.

"""The matched filter for a known pulse s[0..N-1] in white noise, and its Neyman-Pearson detector.

The filter is h[n] = c conj(s[N-1-n]); filtering x with h is cross-correlating x with s.
For real white Gaussian noise of variance sigma^2, the output at the end of the pulse is
N(0, sigma^2 E) without the pulse and N(E, sigma^2 E) with it, where E = sum of |s[n]|^2.
"""

import math
from typing import Sequence


def matched_filter(s: Sequence, c=1) -> list:
    """Impulse response h[n] = c conj(s[N - 1 - n]). Cost: Theta(N)."""
    return [c * (v.conjugate() if isinstance(v, complex) else v) for v in reversed(s)]


def fir(h: Sequence, x: Sequence) -> list:
    """y[n] = sum over k of h[k] x[n - k] for n = 0 .. len(x) - 1 (x is zero before 0). Cost: Theta(N M)."""
    return [sum(h[k] * x[n - k] for k in range(len(h)) if n - k >= 0) for n in range(len(x))]


def output_snr(h: Sequence, s: Sequence, sigma2) -> object:
    """|sum of h[k] s[N-1-k]|^2 / (sigma^2 sum of |h[k]|^2): the peak signal power over the noise power
    at the output sample n = N - 1, for white noise of variance sigma2. Exact for Fraction input."""
    n = len(s)
    peak = sum(h[k] * s[n - 1 - k] for k in range(n))
    power = sum(abs(v) ** 2 if isinstance(v, complex) else v * v for v in h)
    num = abs(peak) ** 2 if isinstance(peak, complex) else peak * peak
    return num / (sigma2 * power)


def colored_snr(w: Sequence, s: Sequence, cov: Sequence[Sequence]) -> object:
    """(w . s)^2 / (w^T C w) for real w, s and noise covariance C: the SNR of the statistic w . x."""
    m = len(s)
    peak = sum(w[i] * s[i] for i in range(m))
    var = sum(w[i] * cov[i][j] * w[j] for i in range(m) for j in range(m))
    return peak * peak / var


def solve(a: Sequence[Sequence], b: Sequence) -> list:
    """Gaussian elimination with partial pivoting (exact for Fraction)."""
    n = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if m[piv][col] == 0:
            raise ValueError("singular system")
        m[col], m[piv] = m[piv], m[col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            for c in range(col, n + 1):
                m[r][c] -= f * m[col][c]
    y = [0] * n
    for r in range(n - 1, -1, -1):
        y[r] = (m[r][n] - sum(m[r][c] * y[c] for c in range(r + 1, n))) / m[r][r]
    return y


def whitened_template(s: Sequence, cov: Sequence[Sequence]) -> list:
    """w = C^{-1} s, the matched filter for noise with covariance C (read as a correlator)."""
    return solve(cov, s)


def q_function(x: float) -> float:
    """Q(x) = P(Z > x) for a standard normal Z."""
    return 0.5 * math.erfc(x / math.sqrt(2))


def q_inverse(p: float) -> float:
    """The x with Q(x) = p, for 0 < p < 1, by bisection on the decreasing function Q."""
    if not 0 < p < 1:
        raise ValueError("need 0 < p < 1")
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if q_function(mid) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def threshold(s: Sequence[float], sigma2: float, pfa: float) -> float:
    """gamma = sqrt(sigma^2 E) Q^{-1}(P_FA) for real white Gaussian noise."""
    energy = sum(v * v for v in s)
    return math.sqrt(sigma2 * energy) * q_inverse(pfa)


def detection_probability(energy: float, sigma2: float, pfa: float) -> float:
    """P_D = Q(Q^{-1}(P_FA) - sqrt(E / sigma^2))."""
    return q_function(q_inverse(pfa) - math.sqrt(energy / sigma2))


def detect(x: Sequence[float], s: Sequence[float], sigma2: float, pfa: float) -> list[int]:
    """Start times t at which the pulse s is declared present in x (real data, white noise).

    Precondition: sigma2 > 0, 0 < pfa < 1, s not all zero. Each test has false alarm
    probability pfa. Cost: Theta(N M) for M = len(x) and N = len(s).
    """
    n = len(s)
    h = matched_filter(s)  # @line L1
    y = fir(h, x)  # @line L2
    gamma = threshold(s, sigma2, pfa)  # @line L3
    found = []
    for t in range(n - 1, len(x)):  # @line L4
        if y[t] > gamma:  # @line L5
            found.append(t - n + 1)
    return found  # @line L6
