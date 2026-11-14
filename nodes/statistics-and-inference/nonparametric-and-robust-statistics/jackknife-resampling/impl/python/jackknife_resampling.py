# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jackknife-resampling/. The authors are listed in prov/DBF7V5.jsonl.

import itertools
import math
from typing import Callable, NamedTuple, Sequence

Statistic = Callable[[Sequence], object]


class JackknifeResult(NamedTuple):
    estimate: object  # theta_hat, the statistic on the full sample
    leave_one_out: list  # theta_(i), i = 1..n
    bias: object  # (n - 1) (theta_(.) - theta_hat)
    corrected: object  # theta_hat - bias
    variance: object  # ((n - 1)/n) sum (theta_(i) - theta_(.))^2


def jackknife(x: Sequence, statistic: Statistic) -> JackknifeResult:
    """The leave-one-out jackknife of Quenouille and Tukey.

    The arithmetic uses + - * / only, so Fraction data give exact results.
    """
    n = len(x)
    if n < 2:
        raise ValueError("the jackknife needs at least two observations")
    theta_hat = statistic(list(x))  # @line L1
    loo = []
    for i in range(n):  # @line L2
        loo.append(statistic(list(x[:i]) + list(x[i + 1 :])))  # @line L3
    theta_dot = sum(loo[1:], loo[0]) / n  # @line L4
    bias = (n - 1) * (theta_dot - theta_hat)  # @line L5
    variance = (n - 1) * sum(((t - theta_dot) ** 2 for t in loo[1:]), (loo[0] - theta_dot) ** 2) / n  # @line L6
    return JackknifeResult(theta_hat, loo, bias, theta_hat - bias, variance)  # @line L7


def pseudo_values(x: Sequence, statistic: Statistic) -> list:
    """Tukey's pseudo-values n theta_hat - (n - 1) theta_(i)."""
    r = jackknife(x, statistic)
    n = len(x)
    return [n * r.estimate - (n - 1) * t for t in r.leave_one_out]


def delete_d_variance(x: Sequence, statistic: Statistic, d: int):
    """The delete-d jackknife variance (n - d)/(d C(n, d)) sum_S (theta_S - mean)^2 over all
    subsets S that leave out d observations. It lists all C(n, d) subsets: small n only."""
    n = len(x)
    if not 1 <= d < n:
        raise ValueError("need 1 <= d < n")
    values = [statistic([x[i] for i in keep]) for keep in itertools.combinations(range(n), n - d)]
    count = len(values)
    mean = sum(values[1:], values[0]) / count
    ss = sum(((v - mean) ** 2 for v in values[1:]), (values[0] - mean) ** 2)
    return (n - d) * ss / (d * count)


def mean(xs: Sequence):
    return sum(xs[1:], xs[0]) / len(xs)


def plugin_variance(xs: Sequence):
    """The plug-in variance with divisor n, a V-statistic of degree 2."""
    m = mean(xs)
    return sum(((v - m) ** 2 for v in xs[1:]), (xs[0] - m) ** 2) / len(xs)


def median(xs: Sequence):
    s = sorted(xs)
    k = len(s)
    if k % 2:
        return s[k // 2]
    return (s[k // 2 - 1] + s[k // 2]) / 2


def jackknife_se(x: Sequence[float], statistic: Statistic) -> float:
    return math.sqrt(jackknife(x, statistic).variance)
