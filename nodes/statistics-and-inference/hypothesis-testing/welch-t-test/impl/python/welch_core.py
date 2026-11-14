# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welch-t-test/. The authors are listed in prov/C3KW5Q.jsonl.
"""Welch's two-sample t-test with the Welch-Satterthwaite degrees of freedom.

welch_t_test returns (t, nu, p): the statistic, the approximate degrees of
freedom (a real number) and the p-value for the alternative "two-sided",
"greater" (H_1: mu_x - mu_y > delta0) or "less". Both sample variances use the
divisor n - 1 and the two-pass formula. The code is in this file and not in
welch_t_test.py, because tools treat a file whose name ends in _test.py as a
test file.
"""

import math
from collections.abc import Sequence

from stdist import t_sf

ALTERNATIVES = ("two-sided", "greater", "less")


def welch_df(a: float, m: int, b: float, n: int) -> float:
    """The Welch-Satterthwaite degrees of freedom for the variance estimate a + b.

    a = S_x^2 / m and b = S_y^2 / n are the two estimated variances of the
    means, with m - 1 and n - 1 degrees of freedom.
    """
    if a < 0.0 or b < 0.0 or a + b == 0.0 or m < 2 or n < 2:
        raise ValueError("need a, b >= 0 with a + b > 0, and m, n >= 2")
    return (a + b) ** 2 / (a * a / (m - 1) + b * b / (n - 1))


def _mean_var(x: Sequence[float]) -> tuple[float, float]:
    """The mean and S^2 with divisor len(x) - 1, by two passes."""
    k = len(x)
    mean = math.fsum(x) / k
    return mean, math.fsum((v - mean) ** 2 for v in x) / (k - 1)


def welch_t_test(x: Sequence[float], y: Sequence[float], delta0: float = 0.0,
                 alternative: str = "two-sided") -> tuple[float, float, float]:
    """Test H_0: mu_x - mu_y = delta0 for independent normal samples with unequal variances."""
    m, n = len(x), len(y)
    if m < 2 or n < 2:
        raise ValueError("each sample needs at least 2 observations")
    mx, vx = _mean_var(x)  # @line L1
    my, vy = _mean_var(y)  # @line L2
    a, b = vx / m, vy / n  # @line L3
    if a + b == 0.0:
        raise ValueError("both samples are constant, so the standard error is 0")
    t = (mx - my - delta0) / math.sqrt(a + b)  # @line L4
    nu = welch_df(a, m, b, n)  # @line L5
    if alternative == "two-sided":
        p = min(1.0, 2.0 * t_sf(abs(t), nu))
    elif alternative == "greater":
        p = t_sf(t, nu)
    elif alternative == "less":
        p = t_sf(-t, nu)
    else:
        raise ValueError(f"alternative must be one of {ALTERNATIVES}")
    return t, nu, p  # @line L6
