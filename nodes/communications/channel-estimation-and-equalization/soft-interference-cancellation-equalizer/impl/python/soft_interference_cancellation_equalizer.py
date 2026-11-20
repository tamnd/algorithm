# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soft-interference-cancellation-equalizer/. The authors are listed in prov/G8QTJ4.jsonl.

"""The MMSE turbo equalizer with soft interference cancellation (Tuchler, Koetter and Singer).

BPSK symbols x_k = 1 - 2 b_k in {+1, -1} pass a real channel h of L taps:
y_m = sum_l h_l x_(m-l) + w_m, w_m ~ N(0, sigma2), for m = 0, ..., K + L - 2.
The prior LLRs La_k = ln P(b_k = 0) / P(b_k = 1) give the soft symbols
xbar_k = tanh(La_k / 2) with variances v_k = 1 - xbar_k^2.

For symbol n, the window Y = (y_(n-N2), ..., y_(n+N1)) of W = N1 + N2 + 1
samples is H X + noise, with X = (x_(n-N2-L+1), ..., x_(n+N1)) and
H[i][j] = h[i - j + L - 1]. The column of H for x_n is s, with s_i = h[i - N2].
The estimate treats x_n as unknown (mean 0, variance 1), so that its own
prior does not enter, and uses the priors of all other symbols:
    C = H V H^T + sigma2 I + (1 - v_n) s s^T,  f = C^-1 s,
    xhat = f^T (Y - H xbar + xbar_n s),        mu = s^T f,
    Le_n = 2 xhat / (1 - mu).
The approximate form replaces V by the average variance vbar times I, so f
is computed once per block.

Samples outside 0..K+L-2 are 0, and symbols outside 0..K-1 are known zeros
(mean 0, variance 0); then such samples carry no signal and get weight 0.
"""

import math

import cbb


def soft_symbols(la: list[float]) -> tuple[list[float], list[float]]:
    """The means tanh(La / 2) and variances 1 - mean^2 of BPSK symbols with prior LLRs La."""
    xbar = [math.tanh(v / 2.0) for v in la]
    return xbar, [1.0 - m * m for m in xbar]


def window_matrix(h: list[float], w: int) -> list[list[float]]:
    """The W by (W + L - 1) matrix H with H[i][j] = h[i - j + L - 1]."""
    taps = len(h)
    return [[float(h[i - j + taps - 1]) if 0 <= i - j + taps - 1 < taps else 0.0 for j in range(w + taps - 1)] for i in range(w)]


def _real_solve(a: list[list[float]], b: list[float]) -> list[float]:
    return [v.real for v in cbb.solve(a, b)]


def siso_equalize(
    y: list[float], h: list[float], la: list[float], sigma2: float, n1: int, n2: int, approx: bool = False
) -> list[float]:
    """Extrinsic LLRs Le_n for n = 0, ..., K-1, where K = len(la) and len(y) = K + L - 1."""
    taps, k = len(h), len(la)
    if taps < 1 or sigma2 <= 0 or n1 < taps - 1 or n2 < 0 or len(y) != k + taps - 1:
        raise ValueError("need L >= 1, sigma2 > 0, N1 >= L - 1, N2 >= 0 and len(y) = K + L - 1")
    w = n1 + n2 + 1
    hm = window_matrix(h, w)
    j0 = n2 + taps - 1
    s = [hm[i][j0] for i in range(w)]
    xbar, var = soft_symbols(la)  # @line L1

    def sym(t: int) -> tuple[float, float]:
        return (xbar[t], var[t]) if 0 <= t < k else (0.0, 0.0)

    def sample(m: int) -> float:
        return float(y[m]) if 0 <= m < len(y) else 0.0

    f_fixed = None
    if approx:
        vbar = sum(var) / k
        c = [[vbar * sum(hm[i][j] * hm[r][j] for j in range(w + taps - 1)) + (sigma2 if i == r else 0.0) + (1 - vbar) * s[i] * s[r] for r in range(w)] for i in range(w)]  # @line L4
        f_fixed = _real_solve(c, s)  # @line L5
    out = []
    for n in range(k):  # @line L2
        yw = [sample(n - n2 + i) for i in range(w)]  # @line L3
        xs = [sym(n - n2 - taps + 1 + j) for j in range(w + taps - 1)]  # @line L3
        mx = [m for m, _ in xs]  # @line L3
        if approx:
            f = f_fixed
        else:
            vn = xs[j0][1]
            c = [
                [sum(hm[i][j] * xs[j][1] * hm[r][j] for j in range(w + taps - 1)) + (sigma2 if i == r else 0.0) + (1 - vn) * s[i] * s[r] for r in range(w)]
                for i in range(w)
            ]  # @line L4
            f = _real_solve(c, s)  # @line L5
        resid = [yw[i] - sum(hm[i][j] * mx[j] for j in range(w + taps - 1)) + mx[j0] * s[i] for i in range(w)]  # @line L6
        xhat = sum(fi * ri for fi, ri in zip(f, resid))  # @line L6
        mu = sum(si * fi for si, fi in zip(s, f))  # @line L7
        out.append(2.0 * xhat / (1.0 - mu))  # @line L8
    return out  # @line L9
