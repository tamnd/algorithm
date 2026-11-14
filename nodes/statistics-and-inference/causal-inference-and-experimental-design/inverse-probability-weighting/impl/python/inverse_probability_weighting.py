# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-probability-weighting/. The authors are listed in prov/GVS3R2.jsonl.

"""Inverse probability weighting estimates of the average treatment effect.

Unit i has a treatment t[i] in {0, 1}, an outcome y[i] and a propensity e[i],
the probability that unit i is treated given its covariates. The propensities
are inputs: known from the design, or estimated beforehand (for example by
empirical_propensity for a discrete covariate, or by a logistic regression).
With Fraction or int inputs every result except the interval is exact.
"""

import math
from collections.abc import Hashable, Sequence
from statistics import NormalDist
from typing import NamedTuple


class IPWEstimate(NamedTuple):
    ht: object  # the Horvitz-Thompson form (a1 - a0) / n
    hajek: object  # the normalized (Hajek) form a1 / w1 - a0 / w0
    mu1_ht: object
    mu0_ht: object
    mu1_hajek: object
    mu0_hajek: object


def _check(t: Sequence, y: Sequence, e: Sequence) -> None:
    if not (len(t) == len(y) == len(e)):
        raise ValueError("t, y and e must have the same length")
    if len(t) == 0:
        raise ValueError("no units")
    for ti in t:
        if ti not in (0, 1):
            raise ValueError("every treatment must be 0 or 1")


def ipw_ate(t: Sequence[int], y: Sequence, e: Sequence) -> IPWEstimate:
    """Horvitz-Thompson and Hajek IPW estimates of the ATE. Cost: Theta(n) time, O(1) extra space.

    Precondition: 0 < e[i] < 1 for every unit (positivity). The Hajek form also
    needs at least one treated and one control unit; if an arm is empty its
    Hajek mean is None.
    """
    _check(t, y, e)
    n = len(t)
    a1 = a0 = w1 = w0 = 0  # @line L1
    for ti, yi, ei in zip(t, y, e):  # @line L2
        if ei <= 0 or ei >= 1:  # @line L3
            raise ValueError(f"positivity fails: propensity {ei!r} is not strictly between 0 and 1")
        if ti == 1:  # @line L4
            a1 = a1 + yi / ei
            w1 = w1 + 1 / ei
        else:  # @line L5
            a0 = a0 + yi / (1 - ei)
            w0 = w0 + 1 / (1 - ei)
    mu1_ht, mu0_ht = a1 / n, a0 / n
    tau_ht = (a1 - a0) / n  # @line L6
    mu1_h = a1 / w1 if w1 else None
    mu0_h = a0 / w0 if w0 else None
    tau_h = mu1_h - mu0_h if w1 and w0 else None  # @line L7
    return IPWEstimate(tau_ht, tau_h, mu1_ht, mu0_ht, mu1_h, mu0_h)  # @line L8


def ipw_variance(t: Sequence[int], y: Sequence, e: Sequence) -> tuple:
    """Variance estimates of the two IPW estimates, treating e as known. Cost: Theta(n).

    Returns (v_ht, v_hajek). v_ht is S^2 / n, where S^2 is the sample variance
    (divisor n - 1) of psi_i = t y / e - (1 - t) y / (1 - e); it is unbiased for
    the variance of the HT estimate over iid units with known e. v_hajek is the
    sandwich estimate (divisor n) of the M-estimator that defines the Hajek form.
    With estimated propensities both are approximations (see the page).
    """
    est = ipw_ate(t, y, e)
    n = len(t)
    if n < 2:
        raise ValueError("need at least two units")
    psi = [ti * yi / ei - (1 - ti) * yi / (1 - ei) for ti, yi, ei in zip(t, y, e)]
    v_ht = sum((p - est.ht) ** 2 for p in psi) / ((n - 1) * n)
    if est.hajek is None:
        return v_ht, None
    w1 = sum(ti / ei for ti, ei in zip(t, e))
    w0 = sum((1 - ti) / (1 - ei) for ti, ei in zip(t, e))
    phi = [ti * (yi - est.mu1_hajek) / ei * n / w1 - (1 - ti) * (yi - est.mu0_hajek) / (1 - ei) * n / w0
           for ti, yi, ei in zip(t, y, e)]
    v_h = sum(f * f for f in phi) / (n * n)
    return v_ht, v_h


def ipw_interval(t: Sequence[int], y: Sequence, e: Sequence, alpha: float = 0.05, form: str = "hajek") -> tuple:
    """Normal (Wald) interval tau-hat -/+ z_(1 - alpha/2) sqrt(v). Asymptotic coverage only."""
    est = ipw_ate(t, y, e)
    v_ht, v_h = ipw_variance(t, y, e)
    tau, v = (est.ht, v_ht) if form == "ht" else (est.hajek, v_h)
    if tau is None:
        raise ValueError("an arm is empty")
    z = NormalDist().inv_cdf(1 - alpha / 2)
    half = z * math.sqrt(float(v))
    return float(tau) - half, float(tau) + half


def ipw_att(t: Sequence[int], y: Sequence, e: Sequence):
    """Hajek IPW estimate of the ATT: treated mean minus the control mean weighted by e / (1 - e).

    Needs e[i] < 1 for the controls and at least one unit in each arm. Cost: Theta(n).
    """
    _check(t, y, e)
    s1 = n1 = s0 = w0 = 0
    for ti, yi, ei in zip(t, y, e):
        if ti == 1:
            s1, n1 = s1 + yi, n1 + 1
        else:
            if ei <= 0 or ei >= 1:
                raise ValueError(f"positivity fails: propensity {ei!r} is not strictly between 0 and 1")
            w = ei / (1 - ei)
            s0, w0 = s0 + w * yi, w0 + w
    if n1 == 0 or w0 == 0:
        raise ValueError("an arm is empty")
    return s1 / n1 - s0 / w0


def empirical_propensity(x: Sequence[Hashable], t: Sequence[int]) -> list:
    """For a discrete covariate, e-hat(x) = (treated with value x) / (units with value x), as Fractions.

    Cost: Theta(n) expected with hashing. Values can be 0 or 1 when a stratum has
    only one arm; ipw_ate then reports the failure of positivity.
    """
    from fractions import Fraction

    tot: dict = {}
    tr: dict = {}
    for xi, ti in zip(x, t):
        tot[xi] = tot.get(xi, 0) + 1
        tr[xi] = tr.get(xi, 0) + ti
    return [Fraction(tr[xi], tot[xi]) for xi in x]
