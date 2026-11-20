# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dft-based-channel-estimation/. The authors are listed in prov/Q4YZBD.jsonl.

"""DFT-based (transform-domain) channel estimation for OFDM.

The channel has at most L_t taps, so its frequency response H[k] = sum over
l < L_t of h[l] e^(-j 2 pi k l / N) lives in an L_t-dimensional subspace of
the N values. The least squares estimate Y[k] / X[k] has noise on all N
values. The estimator takes the inverse DFT of the least squares estimate,
keeps the first L_t taps, sets the rest to zero and takes the DFT again. This
projects the estimate onto the subspace and keeps only L_t / N of the noise.

dft and idft here are the unnormalized pair of the area (idft has the 1/N),
so idft of H gives the taps h. The comb version uses P = N / D pilots spaced
D apart from k0: an inverse DFT of size P gives h[l] e^(-j 2 pi k0 l / N),
which is exact when the channel has at most P taps.
"""

import cmath
import math

import cbb


def estimate(y: list[complex], x: list[complex], taps: int) -> list[complex]:
    """The estimate of H from a symbol with known values x on all N subcarriers."""
    n = len(y)
    if len(x) != n or not 1 <= taps <= n:
        raise ValueError("need len(x) = N and 1 <= taps <= N")
    h_ls = [a / b for a, b in zip(y, x)]  # @line L1
    g = cbb.idft(h_ls)  # @line L2
    g = g[:taps] + [0j] * (n - taps)  # @line L3
    return cbb.dft(g)  # @line L4


def estimate_comb(y: list[complex], pilot_values: list[complex], spacing: int, taps: int, k0: int = 0) -> list[complex]:
    """The estimate of H on all N subcarriers from comb pilots on k0, k0 + D, ..."""
    n = len(y)
    if spacing < 1 or n % spacing or not 0 <= k0 < spacing:
        raise ValueError("need N a multiple of D and 0 <= k0 < D")
    p = n // spacing
    if len(pilot_values) != p or not 1 <= taps <= p:
        raise ValueError("need one value per pilot and 1 <= taps <= N / D")
    hp = [y[k0 + i * spacing] / pilot_values[i] for i in range(p)]
    g = cbb.idft(hp)
    g = [g[l] * cmath.exp(2j * math.pi * k0 * l / n) for l in range(taps)]
    return cbb.dft(g + [0j] * (n - taps))
