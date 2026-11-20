# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-ratio-combining/. The authors are listed in prov/5E6BSS.jsonl.

"""Maximal ratio combining (MRC) of L diversity branches.

Branch l receives y_l = h_l x + w_l with w_l ~ CN(0, N0_l), independent. MRC
weights branch l by conj(h_l) / N0_l and adds the branches. The result,
divided by g = sum |h_l|^2 / N0_l, is x plus noise of variance 1 / g, so the
output SNR is E_s g = sum of the branch SNRs. No other linear combiner has a
higher output SNR (Cauchy-Schwarz).

The error rate functions are for coherent BPSK and L i.i.d. Rayleigh branches
with mean SNR gamma_bar per branch.
"""

import math


def mrc(h: list[complex], y: list[complex], n0: list[float]) -> tuple[complex, float]:
    """The MRC estimate of x and the gain g = sum |h_l|^2 / N0_l (the output SNR per unit symbol energy)."""
    if not len(h) == len(y) == len(n0) or not h:
        raise ValueError("need L >= 1 branches with h, y and N0 each")
    w = [h[l] / n0[l] for l in range(len(h))]  # @line L1
    z = sum(w[l].conjugate() * y[l] for l in range(len(h)))  # @line L2
    g = sum(abs(h[l]) ** 2 / n0[l] for l in range(len(h)))  # @line L3
    if g == 0.0:
        raise ValueError("all branch gains are zero")
    return z / g, g  # @line L4


def output_snr(weights: list[complex], h: list[complex], n0: list[float], es: float = 1.0) -> float:
    """The SNR of z = sum conj(c_l) y_l for any weights c: E_s |sum conj(c_l) h_l|^2 / sum |c_l|^2 N0_l."""
    sig = abs(sum(c.conjugate() * g for c, g in zip(weights, h))) ** 2 * es
    noise = sum(abs(c) ** 2 * v for c, v in zip(weights, n0))
    return sig / noise


def ber_bpsk_rayleigh(branches: int, gbar: float) -> float:
    """Exact BPSK bit error rate of MRC over L i.i.d. Rayleigh branches with mean SNR gamma_bar each."""
    mu = math.sqrt(gbar / (1.0 + gbar))
    return ((1.0 - mu) / 2.0) ** branches * sum(
        math.comb(branches - 1 + k, k) * ((1.0 + mu) / 2.0) ** k for k in range(branches)
    )


def ber_bpsk_rayleigh_craig(branches: int, gbar: float, points: int = 400) -> float:
    """The same error rate by the MGF method: (1 / pi) integral over (0, pi / 2) of (1 + gamma_bar / sin^2 t)^(-L) dt.

    The integrand, a function of sin^2 t, is smooth and even around both ends,
    so the midpoint rule converges very fast.
    """
    h = (math.pi / 2.0) / points
    s = 0.0
    for k in range(points):
        t = (k + 0.5) * h
        s += (1.0 + gbar / math.sin(t) ** 2) ** (-branches)
    return s * h / math.pi


def outage_rayleigh(branches: int, x: float, gbar: float) -> float:
    """P(output SNR < x) for MRC of L i.i.d. Rayleigh branches: 1 - e^(-x / gamma_bar) sum_{k<L} (x / gamma_bar)^k / k!."""
    u = x / gbar
    return 1.0 - math.exp(-u) * sum(u ** k / math.factorial(k) for k in range(branches))
