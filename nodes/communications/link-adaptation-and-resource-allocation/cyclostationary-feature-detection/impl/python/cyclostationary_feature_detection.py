# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclostationary-feature-detection/. The authors are listed in prov/XYTR6D.jsonl.

"""Cyclostationary feature detection from the cyclic autocorrelation.

For samples y[0..N-1], a cycle frequency alpha (in cycles per sample) and a lag
tau >= 0, the conjugate cyclic autocorrelation estimate is

    R = (1 / N') sum_{n < N'} y[n + tau] y[n] e^(-j 2 pi alpha n),  N' = N - tau,

and the non-conjugate one uses conj(y[n]) in place of y[n]. With P = (1 / N)
sum |y[n]|^2, the statistic is T = N' |R|^2 / (c P^2), with c = 2 for the
conjugate form at tau = 0 and c = 1 otherwise. Under white circular complex
Gaussian noise of any power, T tends to a unit exponential law as N grows, so
the threshold -ln(P_fa) needs no noise power. A BPSK signal on a carrier f_c
has a conjugate feature at alpha = 2 f_c, tau = 0, which noise does not have.
"""

import cmath
import math

from cbb import dft


def _product(y: list[complex], n: int, tau: int, conjugate: bool) -> complex:
    return y[n + tau] * (y[n] if conjugate else y[n].conjugate())


def _check(y: list[complex], tau: int, conjugate: bool) -> int:
    if tau < 0 or tau >= len(y):
        raise ValueError("need 0 <= tau < len(y)")
    if tau == 0 and not conjugate:
        raise ValueError("the non-conjugate form needs tau >= 1")
    return len(y) - tau


def cyclic_autocorrelation(y: list[complex], alpha: float, tau: int, conjugate: bool = True) -> complex:
    """The estimate R of the cyclic autocorrelation at cycle frequency alpha and lag tau."""
    m = _check(y, tau, conjugate)
    r = 0j  # @line L2
    step = cmath.exp(-2j * math.pi * alpha)
    rot = 1 + 0j  # e^(-j 2 pi alpha n), updated by one multiplication per sample
    for n in range(m):  # @line L3
        r += _product(y, n, tau, conjugate) * rot
        rot *= step
    return r / m  # @line L5


def cyclic_statistic(y: list[complex], alpha: float, tau: int, conjugate: bool = True) -> float:
    """T = N' |R|^2 / (c P^2), where P is the mean power of y. It does not change if y is scaled."""
    m = _check(y, tau, conjugate)
    r = cyclic_autocorrelation(y, alpha, tau, conjugate)
    p = sum(v.real * v.real + v.imag * v.imag for v in y) / len(y)  # @line L4
    if p == 0.0:
        return 0.0
    c = 2.0 if conjugate and tau == 0 else 1.0
    return m * abs(r) ** 2 / (c * p * p)  # @line L6


def cyclic_detect(
    y: list[complex], alpha: float, tau: int, pfa: float, conjugate: bool = True
) -> tuple[bool, float, float]:
    """Test one cycle frequency and lag. Return (signal present, T, threshold)."""
    if not 0.0 < pfa < 1.0:
        raise ValueError("pfa must be in (0, 1)")
    lam = -math.log(pfa)  # @line L1
    t = cyclic_statistic(y, alpha, tau, conjugate)
    if t > lam:  # @line L7
        return True, t, lam
    return False, t, lam  # @line L8


def cyclic_scan(y: list[complex], tau: int, conjugate: bool = True) -> list[complex]:
    """R at all cycle frequencies alpha = k / N' for k = 0..N'-1, from one DFT of the lag products."""
    m = _check(y, tau, conjugate)
    return [v / m for v in dft([_product(y, n, tau, conjugate) for n in range(m)])]


def scan_threshold(pfa: float, bins: int) -> float:
    """The threshold on the largest of `bins` independent unit exponentials with false alarm rate pfa.

    P(max > lam) = 1 - (1 - e^(-lam))^bins, so lam = -ln(1 - (1 - pfa)^(1 / bins)).
    """
    if not 0.0 < pfa < 1.0 or bins < 1:
        raise ValueError("need 0 < pfa < 1 and bins >= 1")
    return -math.log(-math.expm1(math.log1p(-pfa) / bins))


def scan_detect(
    y: list[complex], tau: int, pfa: float, conjugate: bool = True
) -> tuple[bool, int, float, float]:
    """Search all cycle frequencies k / N' for an unknown carrier.

    Return (signal present, best k, largest T, threshold).
    """
    m = _check(y, tau, conjugate)
    rs = cyclic_scan(y, tau, conjugate)
    p = sum(v.real * v.real + v.imag * v.imag for v in y) / len(y)
    c = 2.0 if conjugate and tau == 0 else 1.0
    ts = [m * abs(r) ** 2 / (c * p * p) if p > 0.0 else 0.0 for r in rs]
    k = max(range(m), key=lambda i: ts[i])
    lam = scan_threshold(pfa, m)
    return ts[k] > lam, k, ts[k], lam


def _ncx_tail(mu: float, x: float) -> float:
    """P(|Z|^2 > x) for Z ~ CN(sqrt(mu), 1), as a Poisson mixture of Gamma(j + 1, 1) tails."""
    if x <= 0.0:
        return 1.0
    if mu <= 0.0:
        return math.exp(-x)
    # The Poisson weights outside [jlo, jhi] are negligible. If jlo is far above x, every
    # Gamma(j + 1, 1) tail with j >= jlo is 1 to double precision.
    spread = 12.0 * math.sqrt(mu) + 40.0
    jlo = max(0, int(mu - spread))
    jhi = int(mu + spread)
    if jlo < x + 12.0 * math.sqrt(x) + 40.0:
        jlo = 0
    lmu, lx = math.log(mu), math.log(x)
    total = 0.0
    tail = 1.0 if jlo > 0 else math.exp(-x)  # P(Gamma(jlo + 1, 1) > x)
    for j in range(jlo, jhi + 1):
        total += math.exp(-mu + j * lmu - math.lgamma(j + 1)) * tail
        if tail < 1.0:
            # P(Gamma(j + 2, 1) > x) = P(Gamma(j + 1, 1) > x) + e^(-x) x^(j + 1) / (j + 1)!
            tail = min(1.0, tail + math.exp(-x + (j + 1) * lx - math.lgamma(j + 2)))
    return min(1.0, total)


def pd_bpsk(n: int, snr: float, pfa: float) -> float:
    """The large-N detection probability of the conjugate test at alpha = 2 f_c, tau = 0, for BPSK.

    The BPSK signal sqrt(S) a[n] e^(j (2 pi f_c n + phi)) with a[n] = +-1 has y^2 terms with mean
    S e^(j 2 phi) e^(j 2 pi alpha n). The noise part of the sum has variance N (4 S s2 + 2 s2^2), and
    P tends to S + s2. With gamma = S / s2 this gives T ~ k |Z|^2, Z ~ CN(sqrt(mu), 1), with
    mu = N gamma^2 / (4 gamma + 2) and k = (2 gamma + 1) / (1 + gamma)^2.
    """
    if snr < 0.0 or n < 1:
        raise ValueError("need snr >= 0 and n >= 1")
    mu = n * snr * snr / (4.0 * snr + 2.0)
    k = (2.0 * snr + 1.0) / (1.0 + snr) ** 2
    return _ncx_tail(mu, -math.log(pfa) / k)
