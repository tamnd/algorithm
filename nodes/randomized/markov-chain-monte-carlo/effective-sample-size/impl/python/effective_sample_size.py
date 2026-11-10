# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/effective-sample-size/. The authors are listed in prov/KEPQ21.jsonl.

import operator
from typing import Callable, Optional, Sequence


def _centered(xs: Sequence[float]) -> list[float]:
    m = sum(xs) / len(xs)
    return [x - m for x in xs]


def _acov(c: list[float], k: int) -> float:
    return sum(map(operator.mul, c, c[k:])) / len(c)


def autocovariance(xs: Sequence[float], k: int) -> float:
    """Sample autocovariance at lag k, with divisor n and the sample mean removed."""
    return _acov(_centered(xs), k)


def _tau_from_rho(rho: Callable[[int], Optional[float]]) -> float:
    """Geyer's initial monotone sequence: tau = -1 + 2 * sum of the pair sums Gamma_m.

    rho(k) returns the estimated autocorrelation at lag k (None past the end); rho(0) = 1.
    Pairs are summed while they stay positive and are forced to be non-increasing.
    """
    tau = -1.0
    prev = float("inf")
    k = 0
    while True:
        r0, r1 = rho(k), rho(k + 1)
        if r0 is None or r1 is None:
            break
        g = r0 + r1
        if g <= 0:
            break
        g = min(g, prev)
        tau += 2 * g
        prev = g
        k += 2
    return tau


def integrated_autocorrelation_time(xs: Sequence[float]) -> float:
    """Estimate tau = 1 + 2 sum rho_k for one chain (Geyer 1992, initial monotone sequence)."""
    n = len(xs)
    if n < 4:
        raise ValueError("need at least 4 draws")
    c = _centered(xs)
    g0 = _acov(c, 0)
    if g0 == 0:
        raise ValueError("the chain is constant")
    return _tau_from_rho(lambda k: _acov(c, k) / g0 if k < n else None)


def effective_sample_size(xs: Sequence[float]) -> float:
    """ESS = n / tau for one chain."""
    return len(xs) / integrated_autocorrelation_time(xs)


def multichain_effective_sample_size(chains: Sequence[Sequence[float]]) -> float:
    """ESS for m chains of equal length n, combining within- and between-chain variance.

    rho_k = 1 - (W - mean_j gamma_{k,j}) / var_plus for k >= 1, as in Gelman et al. (BDA3)
    and Vehtari et al. (2021), where gamma_{k,j} uses divisor n, W is the mean of the
    chain variances, and var_plus = (n - 1) / n * W + B / n. Returns m n / tau.
    """
    m = len(chains)
    if m < 1:
        raise ValueError("need at least one chain")
    n = len(chains[0])
    if n < 4 or any(len(ch) != n for ch in chains):
        raise ValueError("need chains of equal length, at least 4")
    cs = [_centered(ch) for ch in chains]
    means = [sum(ch) / n for ch in chains]
    grand = sum(means) / m
    w = sum(_acov(c, 0) * n / (n - 1) for c in cs) / m
    b = n * sum((mu - grand) ** 2 for mu in means) / (m - 1) if m > 1 else 0.0
    var_plus = (n - 1) / n * w + b / n
    if var_plus == 0:
        raise ValueError("all chains are constant")

    def rho(k: int) -> Optional[float]:
        if k >= n:
            return None
        if k == 0:
            return 1.0
        mean_gamma = sum(_acov(c, k) for c in cs) / m
        return 1 - (w - mean_gamma) / var_plus

    return m * n / _tau_from_rho(rho)
