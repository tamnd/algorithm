# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-moving-average/. The authors are listed in prov/G9PD69.jsonl.
"""Exponential moving average with the usual starts, bias correction and parameter conversions."""

import math
from typing import Iterable, Iterator, List


def ema(xs: Iterable, alpha, start: str = "first") -> Iterator:
    """Yield s_t = alpha * x_t + (1 - alpha) * s_{t-1}.

    start="first": s_1 = x_1.  start="zero": s_0 = 0, so s_1 = alpha * x_1.
    Works with floats or Fractions.
    """
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")
    s = None
    for x in xs:
        if s is None:
            s = x if start == "first" else alpha * x
        else:
            s = s + alpha * (x - s)
        yield s


def ema_corrected(xs: Iterable, alpha) -> Iterator:
    """Bias-corrected EMA: s_t / (1 - (1 - alpha)^t) with s_0 = 0."""
    keep = 1
    for s in ema(xs, alpha, start="zero"):
        keep *= 1 - alpha
        yield s / (1 - keep)


def weighted_mean_form(xs: List, alpha):
    """The normalized weighted mean sum (1-alpha)^j x_{t-j} / sum (1-alpha)^j."""
    t = len(xs)
    num = sum((1 - alpha) ** j * xs[t - 1 - j] for j in range(t))
    den = sum((1 - alpha) ** j for j in range(t))
    return num / den


def alpha_from_span(n):
    """alpha = 2 / (N + 1): the weights have the same mean age as an N-item window."""
    return 2 / (n + 1)


def alpha_from_com(c):
    """alpha = 1 / (1 + c), where c = (1 - alpha) / alpha is the mean age."""
    return 1 / (1 + c)


def alpha_from_halflife(h: float) -> float:
    """alpha with (1 - alpha)^h = 1/2."""
    return 1 - math.exp(-math.log(2) / h)
