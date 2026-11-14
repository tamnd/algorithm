# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/storey-q-value/. The authors are listed in prov/WKCJWX.jsonl.
"""Storey's estimate of the proportion of true nulls, q-values, and the
Storey-Taylor-Siegmund adaptive step-up procedure.

pi0_hat(lambda) = #{p_i > lambda} / (m (1 - lambda)) estimates pi_0 = m_0 / m.
The estimated FDR of the rule "reject p_i <= t" is pi0_hat m t / max(#{p_i <= t}, 1),
and the q-value of p_i is the smallest estimated FDR over the rules that reject it.

sts_reject is the version with finite-sample FDR control under independence
(Storey, Taylor and Siegmund 2004): it uses (1 + #{p_i > lambda}) in the
numerator and only thresholds t <= lambda.
"""

from collections.abc import Sequence
from fractions import Fraction


def _check(p: Sequence, lam) -> None:
    if any(not 0 <= v <= 1 for v in p):
        raise ValueError("p-values must lie in [0, 1]")
    if not 0 <= lam < 1:
        raise ValueError("lambda must lie in [0, 1)")


def pi0_estimate(p: Sequence, lam=0.5, plus_one: bool = False):
    """#{p_i > lam} / (m (1 - lam)), with 1 added to the count if plus_one; capped at 1 unless plus_one."""
    m = len(p)
    _check(p, lam)
    w = sum(1 for v in p if v > lam) + (1 if plus_one else 0)  # @line L1
    one = Fraction(1) if isinstance(lam, Fraction) else 1
    est = one * w / (m * (1 - lam))  # @line L2
    return est if plus_one else min(est, one)


def q_values(p: Sequence, lam=0.5) -> list:
    """Storey's q-values: q_(k) = min over j >= k of min(1, pi0_hat m p_(j) / j)."""
    m = len(p)
    if m == 0:
        return []
    pi0 = pi0_estimate(p, lam)
    order = sorted(range(m), key=lambda i: p[i])  # @line L3
    q = [0] * m
    running = 1
    for r in range(m - 1, -1, -1):  # @line L4
        running = min(running, pi0 * m * p[order[r]] / (r + 1))  # @line L5
        q[order[r]] = running  # @line L6
    return q  # @line L7


def sts_reject(p: Sequence, alpha, lam=0.5) -> list[bool]:
    """Reject p_i <= t, for the largest t <= lam with (1 + #{p_j > lam}) t / ((1 - lam) max(#{p_j <= t}, 1)) <= alpha.

    Equivalently, BH at level alpha / pi0_star on the p-values, keeping only ranks with p_(k) <= lam.
    """
    m = len(p)
    if m == 0:
        return []
    if not 0 < alpha <= 1:
        raise ValueError("alpha must lie in (0, 1]")
    pi0 = pi0_estimate(p, lam, plus_one=True)
    order = sorted(range(m), key=lambda i: p[i])
    k = m
    while k >= 1 and (p[order[k - 1]] > lam or pi0 * m * p[order[k - 1]] > k * alpha):
        k -= 1
    reject = [False] * m
    for r in range(k):
        reject[order[r]] = True
    return reject
