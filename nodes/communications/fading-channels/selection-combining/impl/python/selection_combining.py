# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selection-combining/. The authors are listed in prov/611EDQ.jsonl.

"""Selection combining (SC) of L diversity branches.

Branch l receives y_l = h_l x + w_l with w_l ~ CN(0, N0_l). SC computes the SNR
|h_l|^2 / N0_l of each branch, keeps the branch with the largest one, and
detects x from that branch alone. The output SNR is the maximum of the branch
SNRs.

The distribution functions are for L i.i.d. Rayleigh branches with mean SNR
gamma_bar per branch: the outage (1 - e^(-x / gamma_bar))^L, the mean output
SNR gamma_bar (1 + 1/2 + ... + 1/L) and the BPSK bit error rate.
"""

import math


def select(h: list[complex], y: list[complex], n0: list[float]) -> tuple[complex, int]:
    """The SC estimate of x and the index of the selected branch."""
    if not len(h) == len(y) == len(n0) or not h:
        raise ValueError("need L >= 1 branches with h, y and N0 each")
    snr = [abs(h[l]) ** 2 / n0[l] for l in range(len(h))]  # @line L1
    k = max(range(len(h)), key=lambda l: snr[l])  # @line L2
    if snr[k] == 0.0:
        raise ValueError("all branch gains are zero")
    est = h[k].conjugate() * y[k] / abs(h[k]) ** 2  # @line L3
    return est, k  # @line L4


def outage_rayleigh(branches: int, x: float, gbar: float) -> float:
    """P(max branch SNR < x) = (1 - e^(-x / gamma_bar))^L."""
    return (1.0 - math.exp(-x / gbar)) ** branches


def mean_snr_gain(branches: int) -> float:
    """E[output SNR] / gamma_bar = 1 + 1/2 + ... + 1/L."""
    return sum(1.0 / k for k in range(1, branches + 1))


def ber_bpsk_rayleigh(branches: int, gbar: float) -> float:
    """Exact BPSK bit error rate: (1/2) sum_{k=0}^{L} (-1)^k C(L, k) sqrt(gamma_bar / (gamma_bar + k))."""
    return 0.5 * sum((-1) ** k * math.comb(branches, k) * math.sqrt(gbar / (gbar + k)) for k in range(branches + 1))


def ber_bpsk_rayleigh_integral(branches: int, gbar: float, points: int = 4000) -> float:
    """The same error rate by integration of Q(sqrt(2 g)) against the density of the maximum SNR.

    The density is (L / gamma_bar) e^(-g / gamma_bar) (1 - e^(-g / gamma_bar))^(L - 1).
    The substitution g = u^2 removes the square root at 0, and Simpson's rule
    is used in u on [0, sqrt(50 gamma_bar)].
    """
    umax = math.sqrt(50.0 * gbar)
    h = umax / points

    def f(u):
        g = u * u
        e = math.exp(-g / gbar)
        dens = branches / gbar * e * (1.0 - e) ** (branches - 1)
        return 0.5 * math.erfc(u) * dens * 2.0 * u

    s = f(0.0) + f(umax)
    for k in range(1, points):
        s += (4 if k % 2 else 2) * f(k * h)
    return s * h / 3.0
