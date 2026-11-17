# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moderated-t-statistic/. The authors are listed in prov/SC6381.jsonl.
"""The moderated t-statistic of Smyth (2004), as in limma, for two groups.

Each gene g has a sample variance s2_g on d residual degrees of freedom. The
prior is 1 / sigma2_g ~ chi2_{d0} / (d0 s0^2). The hyperparameters d0 and
s0^2 are found by matching the mean and variance of log s2_g (fit_f_dist,
the method of limma's fitFDist without covariate), the posterior variance
is (d0 s0^2 + d s2_g) / (d0 + d), and under the null hypothesis the
moderated t has a t distribution with d0 + d degrees of freedom.

Special functions (digamma, trigamma, tetragamma, the regularized incomplete
beta function) are written here with the standard library only.
"""

from __future__ import annotations

import math
from statistics import NormalDist
from typing import List, Optional, Sequence, Tuple

_NORMAL = NormalDist()


def digamma(x: float) -> float:
    """psi(x) for x > 0, by the recurrence psi(x) = psi(x + 1) - 1 / x and the asymptotic series."""
    if x <= 0:
        raise ValueError("x must be > 0")
    acc = 0.0
    while x < 10.0:
        acc -= 1.0 / x
        x += 1.0
    f = 1.0 / (x * x)
    series = f * (1 / 12 - f * (1 / 120 - f * (1 / 252 - f * (1 / 240 - f / 132))))
    return acc + math.log(x) - 0.5 / x - series


def trigamma(x: float) -> float:
    """psi'(x) for x > 0."""
    if x <= 0:
        raise ValueError("x must be > 0")
    acc = 0.0
    while x < 10.0:
        acc += 1.0 / (x * x)
        x += 1.0
    f = 1.0 / (x * x)
    series = 1.0 + 0.5 / x + f * (1 / 6 - f * (1 / 30 - f * (1 / 42 - f * (1 / 30 - f * 5 / 66))))
    return acc + series / x


def tetragamma(x: float) -> float:
    """psi''(x) for x > 0."""
    if x <= 0:
        raise ValueError("x must be > 0")
    acc = 0.0
    while x < 10.0:
        acc -= 2.0 / (x * x * x)
        x += 1.0
    f = 1.0 / (x * x)
    series = 1.0 + 1.0 / x + f * (0.5 - f * (1 / 6 - f * (1 / 6 - f * (3 / 10 - f * 5 / 6))))
    return acc - f * series


def trigamma_inverse(y: float) -> float:
    """The x > 0 with trigamma(x) = y, by Newton's method from x = 0.5 + 1 / y."""
    if not y > 0:
        raise ValueError("y must be > 0")
    if y > 1e7:
        return 1.0 / math.sqrt(y)
    if y < 1e-6:
        return 1.0 / y
    x = 0.5 + 1.0 / y
    for _ in range(100):
        tri = trigamma(x)
        step = tri * (1.0 - tri / y) / tetragamma(x)
        x += step
        if abs(step) / x < 1e-12:
            break
    return x


def betainc(a: float, b: float, x: float) -> float:
    """The regularized incomplete beta function I_x(a, b), by a continued fraction."""
    if a <= 0 or b <= 0:
        raise ValueError("a and b must be > 0")
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    if x > (a + 1) / (a + b + 2):
        return 1.0 - betainc(b, a, 1.0 - x)
    log_front = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                 + a * math.log(x) + b * math.log1p(-x))
    tiny = 1e-300
    c = 1.0
    d = 1.0 - (a + b) * x / (a + 1)
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for k in range(1, 10000):
        num = k * (b - k) * x / ((a + 2 * k - 1) * (a + 2 * k))
        for _ in range(2):
            d = 1.0 + num * d
            d = 1.0 / (d if abs(d) > tiny else tiny)
            c = 1.0 + num / c
            c = c if abs(c) > tiny else tiny
            h *= d * c
            last = d * c
            num = -(a + k) * (a + b + k) * x / ((a + 2 * k) * (a + 2 * k + 1))
        if abs(last - 1.0) < 1e-15:
            break
    return math.exp(log_front) * h / a


def t_sf(t: float, df: float) -> float:
    """P(T > t) for T with a t distribution on df degrees of freedom (df = inf is normal)."""
    if not df > 0:
        raise ValueError("df must be > 0")
    if math.isinf(df):
        return _NORMAL.cdf(-t)
    tail = 0.5 * betainc(df / 2, 0.5, df / (df + t * t))
    return tail if t >= 0 else 1.0 - tail


def fit_f_dist(s2: Sequence[float], d: float) -> Tuple[float, float]:
    """(d0, s0^2) by moments of log s2, as fitFDist of limma without covariate.

    Values are floored at 1e-5 times their median, as limma does, so that a
    zero variance does not give log 0.
    """
    if len(s2) < 2:
        raise ValueError("need at least two genes")
    if any(v < 0 for v in s2) or not d > 0:
        raise ValueError("need s2 >= 0 and d > 0")
    srt = sorted(s2)
    n = len(srt)
    med = srt[n // 2] if n % 2 else (srt[n // 2 - 1] + srt[n // 2]) / 2
    if med == 0:
        med = 1.0
    x = [max(v, 1e-5 * med) for v in s2]
    e = [math.log(v) - digamma(d / 2) + math.log(d / 2) for v in x]  # @line L2
    emean = sum(e) / n
    evar = sum((v - emean) ** 2 for v in e) / (n - 1) - trigamma(d / 2)  # @line L3
    if evar > 0:
        d0 = 2.0 * trigamma_inverse(evar)  # @line L4
        s02 = math.exp(emean + digamma(d0 / 2) - math.log(d0 / 2))
    else:
        d0 = math.inf  # @line L5
        s02 = sum(x) / n
    return d0, s02


def squeeze_var(s2: float, d: float, d0: float, s02: float) -> float:
    """The posterior variance (d0 s0^2 + d s2) / (d0 + d); s0^2 when d0 is infinite."""
    if math.isinf(d0):
        return s02
    return (d0 * s02 + d * s2) / (d0 + d)  # @line L6


def group_stats(a: Sequence[float], b: Sequence[float]) -> Tuple[float, float, int, float]:
    """(mean of a - mean of b, pooled variance, its degrees of freedom, 1/n_a + 1/n_b)."""
    na, nb = len(a), len(b)
    d = na + nb - 2
    if na < 1 or nb < 1 or d < 1:
        raise ValueError("need at least three samples in all")
    ma, mb = sum(a) / na, sum(b) / nb
    ss = sum((x - ma) ** 2 for x in a) + sum((x - mb) ** 2 for x in b)
    return ma - mb, ss / d, d, 1.0 / na + 1.0 / nb


def moderated_t(group_a: Sequence[Sequence[float]], group_b: Sequence[Sequence[float]],
                prior: Optional[Tuple[float, float]] = None):
    """Moderated t for each gene; group_a[g] and group_b[g] hold the values of gene g.

    prior = (d0, s0^2) fixes the hyperparameters; otherwise fit_f_dist finds
    them. As in limma's eBayes, the total degrees of freedom are capped at
    the pooled residual degrees of freedom of all genes. Returns
    (t, p, d0, s0^2), with two-sided p-values.
    """
    if len(group_a) != len(group_b) or not group_a:
        raise ValueError("need the same genes in both groups")
    stats = [group_stats(a, b) for a, b in zip(group_a, group_b)]  # @line L1
    d = stats[0][2]
    if any(s[2] != d for s in stats):
        raise ValueError("every gene needs the same number of samples")
    s2 = [s[1] for s in stats]
    d0, s02 = fit_f_dist(s2, d) if prior is None else prior
    df_total = min(d0 + d, d * len(stats))
    ts: List[float] = []
    ps: List[float] = []
    for diff, var, _, v in stats:
        post = squeeze_var(var, d, d0, s02)
        t = diff / math.sqrt(post * v)  # @line L7
        ts.append(t)
        ps.append(min(1.0, 2.0 * t_sf(abs(t), df_total)))  # @line L8
    return ts, ps, d0, s02  # @line L9


def ordinary_t(a: Sequence[float], b: Sequence[float]) -> Tuple[float, float]:
    """The pooled two-sample t and its two-sided p-value."""
    diff, var, d, v = group_stats(a, b)
    t = diff / math.sqrt(var * v)
    return t, min(1.0, 2.0 * t_sf(abs(t), d))
