# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/student-t-test/. The authors are listed in prov/M2JJ9R.jsonl.
"""Student's one-sample, paired and pooled two-sample t-tests.

Each function returns (t, df, p): the statistic, its degrees of freedom and
the p-value for the alternative "two-sided", "greater" (H_1: parameter >
null value) or "less". S^2 uses the divisor n - 1 and the two-pass formula,
which does not cancel like sum x^2 - n xbar^2. Tail areas come from the
upper tail t_sf directly, not from 1 - cdf. The code is in this file and not
in student_t_test.py, because tools treat a file whose name ends in _test.py
as a test file.
"""

import math
from collections.abc import Sequence

from stdist import t_sf

ALTERNATIVES = ("two-sided", "greater", "less")


def t_p_value(t: float, df: float, alternative: str = "two-sided") -> float:
    """The p-value of an observed t when T has the t distribution with df degrees of freedom."""
    if alternative == "two-sided":
        return min(1.0, 2.0 * t_sf(abs(t), df))  # @line L7
    if alternative == "greater":
        return t_sf(t, df)  # @line L8
    if alternative == "less":
        return t_sf(-t, df)  # @line L9
    raise ValueError(f"alternative must be one of {ALTERNATIVES}")


def mean_and_ss(x: Sequence[float]) -> tuple[float, float]:
    """The mean and the sum of squared deviations, by two passes."""
    n = len(x)
    mean = math.fsum(x) / n
    return mean, math.fsum((v - mean) ** 2 for v in x)


def one_sample_t_test(x: Sequence[float], mu0: float = 0.0,
                      alternative: str = "two-sided") -> tuple[float, int, float]:
    """Test H_0: mu = mu0 for iid N(mu, sigma^2) data with sigma unknown."""
    n = len(x)  # @line L1
    if n < 2:
        raise ValueError("need at least 2 observations")
    mean = math.fsum(x) / n  # @line L2
    s2 = math.fsum((v - mean) ** 2 for v in x) / (n - 1)  # @line L3
    if s2 == 0.0:
        raise ValueError("all observations are equal, so S = 0 and t is undefined")
    t = (mean - mu0) / math.sqrt(s2 / n)  # @line L4
    df = n - 1  # @line L5
    return t, df, t_p_value(t, df, alternative)  # @line L6


def paired_t_test(x: Sequence[float], y: Sequence[float], delta0: float = 0.0,
                  alternative: str = "two-sided") -> tuple[float, int, float]:
    """Test H_0: E[X - Y] = delta0 from pairs (x_i, y_i): the one-sample test on x_i - y_i."""
    if len(x) != len(y):
        raise ValueError("paired samples must have the same length")
    return one_sample_t_test([a - b for a, b in zip(x, y)], delta0, alternative)


def pooled_t_test(x: Sequence[float], y: Sequence[float], delta0: float = 0.0,
                  alternative: str = "two-sided") -> tuple[float, int, float]:
    """Test H_0: mu_x - mu_y = delta0 for independent normal samples with a common variance."""
    m, n = len(x), len(y)
    if m < 1 or n < 1 or m + n < 3:
        raise ValueError("need m, n >= 1 and m + n >= 3")
    mx, ssx = mean_and_ss(x)
    my, ssy = mean_and_ss(y)
    df = m + n - 2
    sp2 = (ssx + ssy) / df  # pooled S^2 with divisor m + n - 2
    if sp2 == 0.0:
        raise ValueError("both samples are constant, so the pooled S = 0")
    t = (mx - my - delta0) / math.sqrt(sp2 * (1.0 / m + 1.0 / n))
    return t, df, t_p_value(t, df, alternative)
