# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bonferroni-correction/. The authors are listed in prov/DBDQ24.jsonl.
"""The Bonferroni correction for m hypotheses, and the Sidak variant.

Bonferroni rejects H_i when p_i <= alpha / m. By the union bound the
family-wise error rate is at most (m_0 / m) alpha <= alpha under any
dependence. The adjusted p-value is min(1, m p_i), and H_i is rejected
exactly when it is at most alpha. The code works with float or with
fractions.Fraction inputs; with Fractions every result is exact.
"""

from collections.abc import Sequence


def bonferroni_correction(p: Sequence, alpha) -> tuple[list[bool], list]:
    """Return (reject, adjusted) for the p-values p at family-wise level alpha."""
    m = len(p)
    if m == 0:
        return [], []
    if any(not 0 <= v <= 1 for v in p):  # also rejects NaN
        raise ValueError("p-values must lie in [0, 1]")
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must lie in [0, 1]")
    level = alpha / m  # @line L1
    reject, adjusted = [], []
    for v in p:  # @line L2
        reject.append(v <= level)  # @line L3
        adjusted.append(min(1, m * v))  # @line L4
    return reject, adjusted  # @line L5


def sidak_level(alpha: float, m: int) -> float:
    """The per-test level 1 - (1 - alpha)^(1/m) of the Sidak correction.

    Computed as -expm1(log1p(-alpha) / m), which does not cancel for small alpha.
    """
    import math

    if m < 1:
        raise ValueError("m must be at least 1")
    return -math.expm1(math.log1p(-alpha) / m)


def sidak_correction(p: Sequence[float], alpha: float) -> tuple[list[bool], list[float]]:
    """Reject H_i when p_i <= 1 - (1 - alpha)^(1/m); adjusted p-value 1 - (1 - p_i)^m."""
    import math

    m = len(p)
    if m == 0:
        return [], []
    level = sidak_level(alpha, m)
    reject = [v <= level for v in p]
    adjusted = [1.0 if v >= 1 else -math.expm1(m * math.log1p(-v)) for v in p]
    return reject, adjusted
