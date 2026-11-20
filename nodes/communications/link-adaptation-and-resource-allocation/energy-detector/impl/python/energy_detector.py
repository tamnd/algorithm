# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/energy-detector/. The authors are listed in prov/T2T7RR.jsonl.

"""The energy detector (radiometer) for complex baseband samples.

The receiver takes N samples y[0..N-1] with complex Gaussian noise CN(0, s2)
of known power s2. It computes T = sum |y[n]|^2 / s2 and declares a signal
present when T > lam. Under noise only, T is a sum of N independent unit
exponentials, so T ~ Gamma(N, 1) and

    P_fa = P(T > lam) = e^(-lam) sum_{k < N} lam^k / k!.

The threshold lam is the root of this equation for the target P_fa. With a
complex Gaussian signal of SNR snr, T / (1 + snr) ~ Gamma(N, 1). With a fixed
signal of total energy mu * s2, T is a noncentral gamma variable, a Poisson
mixture of Gamma(N + j, 1) laws with weights Poisson(j; mu).
"""

import math

from cbb import qinv


def gamma_tail(n: int, x: float) -> float:
    """P(Gamma(n, 1) > x) = e^(-x) sum_{k < n} x^k / k!.

    The terms x^k / k! grow while k < x and then shrink, so the sum starts at the
    largest term k = min(n - 1, floor(x)), computed in the log domain, and walks away
    from it in both directions with the ratio x / k until the terms are negligible.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if x <= 0.0:
        return 1.0
    m = min(n - 1, int(x))
    log_top = -x + m * math.log(x) - math.lgamma(m + 1)
    s, t = 1.0, 1.0
    for k in range(m + 1, n):
        t *= x / k
        s += t
        if t < 1e-18 * s:
            break
    t = 1.0
    for k in range(m, 0, -1):
        t *= k / x
        s += t
        if t < 1e-18 * s:
            break
    return min(1.0, math.exp(log_top) * s)


def threshold(n: int, pfa: float) -> float:
    """The lam with gamma_tail(n, lam) = pfa, by bisection (gamma_tail decreases in lam)."""
    if not 0.0 < pfa < 1.0:
        raise ValueError("pfa must be in (0, 1)")
    lo, hi = 0.0, n + 40.0 * math.sqrt(n) + 100.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if gamma_tail(n, mid) > pfa:
            lo = mid
        else:
            hi = mid
        if hi - lo <= 1e-13 * hi:
            break
    return 0.5 * (lo + hi)


def statistic(y: list[complex], noise_var: float) -> float:
    """T = sum |y[n]|^2 / noise_var."""
    if noise_var <= 0.0:
        raise ValueError("noise_var must be positive")
    t = 0.0  # @line L2
    for v in y:  # @line L3
        t += v.real * v.real + v.imag * v.imag
    return t / noise_var  # @line L4


def energy_detect(y: list[complex], noise_var: float, pfa: float) -> tuple[bool, float, float]:
    """Run the detector. Return (signal present, T, lam)."""
    lam = threshold(len(y), pfa)  # @line L1
    t = statistic(y, noise_var)
    if t > lam:  # @line L5
        return True, t, lam
    return False, t, lam  # @line L6


def pd_gaussian(n: int, snr: float, lam: float) -> float:
    """P_d for a complex Gaussian signal of SNR snr per sample: P(Gamma(n, 1) > lam / (1 + snr))."""
    return gamma_tail(n, lam / (1.0 + snr))


def pd_deterministic(n: int, mu: float, lam: float) -> float:
    """P_d for a fixed signal with sum |s[n]|^2 / noise_var = mu, as a Poisson mixture of gamma tails.

    2T is noncentral chi-square with 2n degrees of freedom and noncentrality 2 mu, and
    P(T > lam) = sum_j e^(-mu) mu^j / j! * gamma_tail(n + j, lam).
    """
    if mu < 0.0:
        raise ValueError("mu must be nonnegative")
    if mu == 0.0:
        return gamma_tail(n, lam)
    jmax = int(mu + 12.0 * math.sqrt(mu) + 40.0)
    tail = gamma_tail(n, lam)
    total = 0.0
    lx, lm = math.log(lam) if lam > 0 else -math.inf, math.log(mu)
    for j in range(jmax + 1):
        total += math.exp(-mu + j * lm - math.lgamma(j + 1)) * tail
        # gamma_tail(n + j + 1, lam) = gamma_tail(n + j, lam) + e^(-lam) lam^(n + j) / (n + j)!
        if lam > 0:
            tail = min(1.0, tail + math.exp(-lam + (n + j) * lx - math.lgamma(n + j + 1)))
    return min(1.0, total)


def clt_samples(snr: float, pfa: float, pd: float) -> float:
    """The normal-approximation sample count for a complex Gaussian signal.

    Under H0, T has mean N and variance N; under H1, mean N (1 + snr) and variance N (1 + snr)^2.
    Equating the threshold N + sqrt(N) Q^-1(pfa) = N (1 + snr) + sqrt(N) (1 + snr) Q^-1(pd)
    gives N = ((Q^-1(pfa) - (1 + snr) Q^-1(pd)) / snr)^2.
    """
    if snr <= 0.0:
        raise ValueError("snr must be positive")
    return ((qinv(pfa) - (1.0 + snr) * qinv(pd)) / snr) ** 2


def snr_wall(uncertainty_db: float) -> float:
    """The SNR wall rho - 1 / rho (linear) for noise power known within a factor rho = 10^(x / 10)."""
    rho = 10.0 ** (uncertainty_db / 10.0)
    return rho - 1.0 / rho
