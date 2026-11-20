# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/van-de-beek-estimator/. The authors are listed in prov/9K7QSC.jsonl.

"""The van de Beek, Sandell and Borjesson estimator of symbol timing and
carrier frequency offset from the cyclic prefix of an OFDM signal.

The prefix of L samples repeats the last L samples of the symbol, N samples
later. A carrier offset epsilon (in subcarrier spacings) multiplies sample k
by e^(j 2 pi epsilon k / N), so r(k) conj(r(k + N)) has the angle
-2 pi epsilon on the prefix. For each candidate start theta:

    gamma(theta) = sum for k = theta .. theta + L - 1 of r(k) conj(r(k + N))
    Phi(theta)   = (1/2) sum for k = theta .. theta + L - 1 of |r(k)|^2 + |r(k + N)|^2
    Lambda(theta) = |gamma(theta)| - rho Phi(theta),  rho = SNR / (SNR + 1)

theta_hat maximizes Lambda and epsilon_hat = -angle(gamma(theta_hat)) / (2 pi).
This is the maximum likelihood estimate when the OFDM samples are modeled as
complex Gaussian, in a channel with additive white Gaussian noise only.
gamma and Phi are running sums, so each new theta costs O(1).
"""

import cmath
import math


def statistics(r: list[complex], n: int, l: int) -> tuple[list[complex], list[float]]:
    """gamma(theta) and Phi(theta) for theta = 0, ..., len(r) - n - l."""
    count = len(r) - n - l + 1
    if count < 1:
        raise ValueError("need at least N + L samples")
    g = sum(r[k] * r[k + n].conjugate() for k in range(l))
    p = 0.5 * sum(abs(r[k]) ** 2 + abs(r[k + n]) ** 2 for k in range(l))
    gs, phis = [], []
    for t in range(count):  # @line L1
        if t > 0:
            a, b = t - 1, t - 1 + l
            g += r[b] * r[b + n].conjugate() - r[a] * r[a + n].conjugate()  # @line L2
            p += 0.5 * (abs(r[b]) ** 2 + abs(r[b + n]) ** 2 - abs(r[a]) ** 2 - abs(r[a + n]) ** 2)  # @line L3
        gs.append(g)
        phis.append(p)
    return gs, phis


def estimate(r: list[complex], n: int, l: int, snr: float) -> tuple[int, float]:
    """(theta_hat, epsilon_hat) from the samples r, for N subcarriers and a prefix of L samples.

    snr is the ratio of signal power to noise power per sample (not in dB).
    theta_hat is the index in r of the first prefix sample; epsilon_hat is in [-1/2, 1/2).
    """
    if snr <= 0:
        raise ValueError("snr must be positive")
    rho = snr / (snr + 1.0)
    gs, phis = statistics(r, n, l)
    lam = [abs(g) - rho * p for g, p in zip(gs, phis)]  # @line L4
    theta = max(range(len(lam)), key=lam.__getitem__)  # @line L5
    eps = -cmath.phase(gs[theta]) / (2 * math.pi)  # @line L6
    if eps >= 0.5:
        eps -= 1.0
    return theta, eps  # @line L7
