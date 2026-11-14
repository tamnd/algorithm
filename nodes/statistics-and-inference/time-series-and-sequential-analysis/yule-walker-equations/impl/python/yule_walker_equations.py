# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yule-walker-equations/. The authors are listed in prov/Y7J377.jsonl.

"""Yule-Walker estimation of an AR(p) model.

The sample autocovariances use the divisor n. The Toeplitz system Gamma_p phi = gamma_p is
solved by the Durbin-Levinson recursion in O(p^2) operations. The code uses only +, -, * and /,
so it runs unchanged on fractions.Fraction inputs and then gives the exact solution.
"""

from __future__ import annotations

from typing import Sequence


def sample_autocovariance(x: Sequence, max_lag: int, demean: bool = True) -> list:
    """Return gamma_hat(0..max_lag) with the divisor n (not n - h)."""
    n = len(x)
    if n == 0:
        raise ValueError("empty series")
    if not 0 <= max_lag < n:
        raise ValueError("need 0 <= max_lag < n")
    m = sum(x) / n if demean else 0  # @line L1
    d = [xi - m for xi in x]
    gamma = []
    for h in range(max_lag + 1):  # @line L2
        gamma.append(sum(d[t + h] * d[t] for t in range(n - h)) / n)
    return gamma


def levinson_durbin(gamma: Sequence, p: int) -> tuple[list, object, list]:
    """Solve Gamma_p phi = gamma_p by the Durbin-Levinson recursion.

    Returns (phi[1..p] as a list of length p, the innovation variance v_p, the partial
    autocorrelations phi_11, ..., phi_pp). Raises ValueError if some v_k is not positive,
    which happens only when the Toeplitz matrix is singular or not positive definite.
    """
    if p < 0 or len(gamma) < p + 1:
        raise ValueError("need gamma(0..p)")
    v = gamma[0]  # @line L3
    if not v > 0:
        raise ValueError("gamma(0) must be positive")
    phi: list = []
    pacf: list = []
    for k in range(1, p + 1):  # @line L4
        a = (gamma[k] - sum(phi[j - 1] * gamma[k - j] for j in range(1, k))) / v  # @line L5
        new = [phi[j - 1] - a * phi[k - j - 1] for j in range(1, k)]  # @line L6
        new.append(a)  # @line L7
        phi = new
        pacf.append(a)
        v = v * (1 - a * a)  # @line L8
        if not v > 0:
            raise ValueError("the autocovariance matrix is not positive definite")
    return phi, v, pacf  # @line L9


def yule_walker(x: Sequence, p: int, demean: bool = True) -> tuple[list, object]:
    """Yule-Walker estimates (phi_hat[1..p], sigma2_hat) of an AR(p) model."""
    gamma = sample_autocovariance(x, p, demean)
    phi, v, _ = levinson_durbin(gamma, p)
    return phi, v


def sample_pacf(x: Sequence, max_lag: int, demean: bool = True) -> list:
    """Sample partial autocorrelations phi_hat_11, ..., phi_hat_hh from the same recursion."""
    gamma = sample_autocovariance(x, max_lag, demean)
    return levinson_durbin(gamma, max_lag)[2]
