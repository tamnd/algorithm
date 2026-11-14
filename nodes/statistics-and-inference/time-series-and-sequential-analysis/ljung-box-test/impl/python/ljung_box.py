# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ljung-box-test/. The authors are listed in prov/NPBB3C.jsonl.

"""The Ljung-Box portmanteau test, with the Box-Pierce statistic as an option.

The sample autocorrelations use the divisor-n autocovariances, as in Ljung and Box (1978).
The p-value is the upper tail of the chi-square law with h - fitted degrees of freedom,
from the shared helper module.
"""

from __future__ import annotations

import math
from typing import Sequence

from stdist import chi2_sf


def residual_autocorrelations(e: Sequence[float], h: int) -> list[float]:
    """r_1, ..., r_h of the series e, centred at its mean, with the divisor-n convention."""
    n = len(e)
    if not 1 <= h < n:
        raise ValueError("need 1 <= h < n")
    m = math.fsum(e) / n  # @line L1
    d = [x - m for x in e]
    c0 = math.fsum(x * x for x in d)  # @line L2
    if c0 == 0.0:
        raise ValueError("the series is constant")
    return [math.fsum(d[t] * d[t - k] for t in range(k, n)) / c0 for k in range(1, h + 1)]  # @line L3


def ljung_box(e: Sequence[float], h: int, fitted: int = 0,
              statistic: str = "ljung-box") -> tuple[float, int, float]:
    """Return (Q, df, p) for the first h residual autocorrelations.

    fitted is the number of ARMA coefficients p + q estimated before the residuals were
    formed (0 for a raw series). statistic is "ljung-box" or "box-pierce".
    """
    n = len(e)
    r = residual_autocorrelations(e, h)
    if statistic == "ljung-box":
        q = n * (n + 2) * math.fsum(r[k - 1] ** 2 / (n - k) for k in range(1, h + 1))  # @line L4
    elif statistic == "box-pierce":
        q = n * math.fsum(rk * rk for rk in r)
    else:
        raise ValueError("statistic must be 'ljung-box' or 'box-pierce'")
    df = h - fitted  # @line L5
    if df < 1:
        raise ValueError("need h > fitted")
    return q, df, chi2_sf(q, df)  # @line L6
