# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wiener-filter/. The authors are listed in prov/F5ZCZM.jsonl.

"""Wiener filters: the FIR Wiener-Hopf solution and the noncausal DFT gain.

wiener_fir solves R w = p for the M-tap causal FIR filter that estimates
d[n] from x[n], ..., x[n - M + 1] with the least mean-square error, and
returns w and the minimum error J_min = var_d - p^T w. With int or Fraction
inputs the result is exact.

wiener_dft applies the gain H[m] = S_x[m] / (S_x[m] + S_n[m]) to each DFT
bin of a block y = x + n. It is the exact linear MMSE estimate of x when x
and n are independent, zero-mean and circularly stationary with power
spectra S_x and S_n on the DFT grid.
"""

import cmath
from typing import Sequence


def solve_linear(a: Sequence[Sequence], b: Sequence) -> list:
    """Solve a x = b by Gaussian elimination with partial pivoting. O(M^3)."""
    n = len(a)
    m = [list(row) + [bb] for row, bb in zip(a, b)]
    for c in range(n):
        piv = max(range(c, n), key=lambda i: abs(m[i][c]))
        if m[piv][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[piv] = m[piv], m[c]
        for i in range(c + 1, n):
            f = m[i][c] / m[c][c]
            if f != 0:
                m[i] = [u - f * v for u, v in zip(m[i], m[c])]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        acc = m[i][n]
        for j in range(i + 1, n):
            acc = acc - m[i][j] * x[j]
        x[i] = acc / m[i][i]
    return x


def wiener_fir(rx: Sequence, rdx: Sequence, var_d, m: int) -> tuple[list, object]:
    """Taps w[0..m-1] and J_min of the FIR Wiener filter.

    rx[k] = E[x[n] x[n-k]] for k = 0..m-1, rdx[k] = E[d[n] x[n-k]] for
    k = 0..m-1, var_d = E[d[n]^2]. Precondition: the Toeplitz matrix of rx
    is positive definite. Cost O(m^3) here; a Levinson solver gives O(m^2).
    """
    r = [[rx[abs(i - j)] for j in range(m)] for i in range(m)]  # @line L1
    p = list(rdx[:m])  # @line L2
    w = solve_linear(r, p)  # @line L3
    jmin = var_d - sum(pk * wk for pk, wk in zip(p, w))  # @line L4
    return w, jmin  # @line L5


def apply_fir(w: Sequence, x: Sequence) -> list:
    """Causal output d_hat[n] = sum_k w[k] x[n-k], zero before the start. O(M) per sample."""
    out = []
    for n in range(len(x)):  # @line L6
        acc = 0 * w[0]
        for k, wk in enumerate(w):
            if n - k >= 0:
                acc = acc + wk * x[n - k]
        out.append(acc)
    return out


def dft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """DFT by radix-2 FFT for powers of two, by the defining sum otherwise.

    The inverse includes the factor 1/N.
    """
    n = len(a)
    sign = 1 if inverse else -1
    if n & (n - 1) == 0 and n > 1:
        out = _fft(list(map(complex, a)), sign)
    else:
        out = [sum(complex(a[t]) * cmath.exp(sign * 2j * cmath.pi * k * t / n) for t in range(n))
               for k in range(n)]
    return [v / n for v in out] if inverse else out


def _fft(a: list[complex], sign: int) -> list[complex]:
    n = len(a)
    if n == 1:
        return a
    even, odd = _fft(a[0::2], sign), _fft(a[1::2], sign)
    out = [0j] * n
    for k in range(n // 2):
        t = cmath.exp(sign * 2j * cmath.pi * k / n) * odd[k]
        out[k], out[k + n // 2] = even[k] + t, even[k] - t
    return out


def wiener_gain(sx: Sequence[float], sn: Sequence[float]) -> list[float]:
    """H[m] = S_x[m] / (S_x[m] + S_n[m]), and 0 where both spectra are 0."""
    return [a / (a + b) if a + b > 0 else 0.0 for a, b in zip(sx, sn)]


def wiener_dft(y: Sequence[float], sx: Sequence[float], sn: Sequence[float]) -> list[float]:
    """Noncausal Wiener estimate of x from one block y, by DFT bins.

    sx and sn are the power spectra on the N-point DFT grid; they must be
    even in the bin index (sx[m] = sx[N - m]) for a real output.
    Cost O(N log N) for N a power of two.
    """
    spec = dft(y)
    h = wiener_gain(sx, sn)  # @line L7
    est = [hm * ym for hm, ym in zip(h, spec)]  # @line L8
    return [v.real for v in dft(est, inverse=True)]  # @line L9
