# SPDX-License-Identifier: MIT
# Shared helper of the biology pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Random variates, exact probability mass functions and test helpers for
the stochastic pages of the biology area.

Every sampler takes a random.Random object as its first argument and never
uses the module-level random functions. Each sampler draws its random
numbers in the order that its docstring gives, so two runs with the same
seed give the same output.

Conventions:
- A reaction network with n species and m reactions is given by `stoich`, a
  list of the m change vectors nu_1, ..., nu_m. So stoich[j][i] is the entry
  S[i][j] of the n by m stoichiometric matrix S.
- `propensity(x)` takes the state as a tuple of n integer counts and returns
  the m propensities a_1(x), ..., a_m(x) as a sequence of floats >= 0.
- nbinom_pmf uses the mean mu and the dispersion alpha, with
  Var = mu + alpha mu^2. The size is r = 1 / alpha; alpha = 0 is Poisson.
- hypergeom_pmf(k, total, good, draws) is the probability of k good items
  in `draws` draws without replacement from `total` items of which `good`
  are good.

Requires Python 3.12 or later (random.Random.binomialvariate).
"""

from __future__ import annotations

import math
from statistics import NormalDist
from typing import Callable, List, Sequence, Tuple

State = Tuple[int, ...]

_POISSON_PART = 30.0


# Random variates

def poisson(rng, lam: float) -> int:
    """A Poisson(lam) variate.

    For lam <= 30, inversion of the cumulative distribution with one
    rng.random() draw. For lam > 30, the sum of p = ceil(lam / 30)
    independent Poisson(lam / p) variates, drawn one after the other by
    inversion (one rng.random() draw each).
    """
    if lam < 0 or math.isnan(lam):
        raise ValueError("lam must be >= 0")
    if lam == 0:
        return 0
    if lam > _POISSON_PART:
        parts = math.ceil(lam / _POISSON_PART)
        part = lam / parts
        return sum(_poisson_inversion(rng, part) for _ in range(parts))
    return _poisson_inversion(rng, lam)


def _poisson_inversion(rng, lam: float) -> int:
    u = rng.random()
    k = 0
    p = math.exp(-lam)
    cdf = p
    while u >= cdf:
        k += 1
        p *= lam / k
        if p == 0.0:
            # Rounding left u above the computed total mass; stop at the tail.
            break
        cdf += p
    return k


def binomial(rng, n: int, p: float) -> int:
    """A Binomial(n, p) variate by rng.binomialvariate (one call)."""
    if n < 0 or not 0.0 <= p <= 1.0:
        raise ValueError("need n >= 0 and 0 <= p <= 1")
    if n == 0 or p == 0.0:
        return 0
    if p == 1.0:
        return n
    return rng.binomialvariate(n, p)


def multinomial(rng, n: int, probs: Sequence[float]) -> List[int]:
    """A Multinomial(n, probs) vector by conditional binomials.

    probs are weights >= 0 with a positive sum; they need not sum to 1. Cell
    i gets Binomial(rest of n, probs[i] / rest of the weight), for i in
    order; the last cell with positive weight gets the rest.
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    w = [float(q) for q in probs]
    if any(q < 0 for q in w):
        raise ValueError("weights must be >= 0")
    total = sum(w)
    if total <= 0:
        raise ValueError("weights must have a positive sum")
    last = max(i for i, q in enumerate(w) if q > 0)
    out = [0] * len(w)
    left = n
    rest = total
    for i in range(last):
        if left == 0:
            break
        if w[i] == 0:
            continue
        x = binomial(rng, left, min(1.0, w[i] / rest))
        out[i] = x
        left -= x
        rest -= w[i]
    out[last] += left
    return out


def categorical(rng, weights: Sequence[float]) -> int:
    """An index i with probability weights[i] / sum(weights).

    One draw u = rng.random() * sum(weights), then a cumulative search from
    index 0. Indices with weight 0 are never returned.
    """
    total = 0.0
    for w in weights:
        if w < 0:
            raise ValueError("weights must be >= 0")
        total += w
    if total <= 0:
        raise ValueError("weights must have a positive sum")
    u = rng.random() * total
    acc = 0.0
    last = -1
    for i, w in enumerate(weights):
        if w > 0:
            acc += w
            last = i
            if u < acc:
                return i
    return last


def ssa_direct(rng, x0: Sequence[int], stoich: Sequence[Sequence[int]],
               propensity: Callable[[State], Sequence[float]], t_end: float,
               max_events: int = 10 ** 6):
    """Gillespie's direct method from state x0 at time 0 up to time t_end.

    Each step computes a = propensity(x) and a0 = sum(a). If a0 = 0 the run
    stops. Otherwise it draws tau = rng.expovariate(a0) first. If
    t + tau > t_end the run stops, and no second number is drawn. Else it
    draws u = rng.random() * a0 and fires the first reaction j with
    a_1 + ... + a_j > u (a linear search), then adds stoich[j] to x.

    Returns (times, states, complete). times[0] = 0.0 and states[0] =
    tuple(x0); entry k > 0 is the time and the state just after event k.
    The state at t_end is states[-1]. complete is False only when the run
    stopped because max_events events had fired before t_end.
    """
    x = tuple(int(v) for v in x0)
    times = [0.0]
    states = [x]
    t = 0.0
    m = len(stoich)
    for _ in range(max_events):
        a = propensity(x)
        a0 = 0.0
        for v in a:
            if v < 0:
                raise ValueError("propensities must be >= 0")
            a0 += v
        if a0 <= 0.0:
            return times, states, True
        t += rng.expovariate(a0)
        if t > t_end:
            return times, states, True
        u = rng.random() * a0
        acc = 0.0
        j = -1
        for i in range(m):
            if a[i] > 0:
                acc += a[i]
                j = i
                if u < acc:
                    break
        nu = stoich[j]
        x = tuple(x[i] + nu[i] for i in range(len(x)))
        times.append(t)
        states.append(x)
    return times, states, False


# Sample statistics and test helpers

def mean_var(xs) -> Tuple[float, float]:
    """The mean and the unbiased sample variance (divisor n - 1) by the
    Welford method. The variance is 0.0 for fewer than two values."""
    n = 0
    mean = 0.0
    m2 = 0.0
    for x in xs:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
    if n == 0:
        raise ValueError("empty sample")
    return mean, (m2 / (n - 1) if n > 1 else 0.0)


def check_mean(m: float, mu: float, var: float, n: int, z: float = 4.0) -> bool:
    """True when |m - mu| <= z sqrt(var / n): a sample mean m of n
    independent values with exact mean mu and exact variance var."""
    return abs(m - mu) <= z * math.sqrt(var / n)


# Exact probability mass functions

def log_choose(n: int, k: int) -> float:
    """ln C(n, k), or -inf when k < 0 or k > n."""
    if k < 0 or k > n:
        return -math.inf
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def binom_pmf(k: int, n: int, p: float) -> float:
    """P(K = k) for K ~ Binomial(n, p)."""
    if k < 0 or k > n:
        return 0.0
    if p == 0.0:
        return 1.0 if k == 0 else 0.0
    if p == 1.0:
        return 1.0 if k == n else 0.0
    return math.exp(log_choose(n, k) + k * math.log(p) + (n - k) * math.log1p(-p))


def poisson_pmf(k: int, lam: float) -> float:
    """P(K = k) for K ~ Poisson(lam)."""
    if k < 0:
        return 0.0
    if lam == 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))


def nbinom_pmf(k: int, mu: float, alpha: float) -> float:
    """P(K = k) for the negative binomial with mean mu and Var = mu + alpha mu^2."""
    if k < 0:
        return 0.0
    if alpha == 0:
        return poisson_pmf(k, mu)
    if mu == 0:
        return 1.0 if k == 0 else 0.0
    r = 1.0 / alpha
    return math.exp(math.lgamma(k + r) - math.lgamma(r) - math.lgamma(k + 1)
                    + r * math.log(r / (r + mu)) + k * math.log(mu / (r + mu)))


def hypergeom_pmf(k: int, total: int, good: int, draws: int) -> float:
    """P(K = k) for k good items in `draws` draws without replacement from
    `total` items of which `good` are good."""
    if k < 0 or k > good or draws - k < 0 or draws - k > total - good:
        return 0.0
    return math.exp(log_choose(good, k) + log_choose(total - good, draws - k)
                    - log_choose(total, draws))


def logsumexp(xs) -> float:
    """ln(sum of exp(x)) without overflow; -inf for an empty input."""
    xs = list(xs)
    if not xs:
        return -math.inf
    top = max(xs)
    if top == -math.inf:
        return -math.inf
    if top == math.inf:
        return math.inf
    return top + math.log(sum(math.exp(x - top) for x in xs))


# Tail probabilities

def _gamma_q(a: float, x: float) -> float:
    """The regularized upper incomplete gamma function Q(a, x)."""
    if a <= 0:
        raise ValueError("a must be > 0")
    if x <= 0:
        return 1.0
    log_front = -x + a * math.log(x) - math.lgamma(a)
    if x < a + 1.0:
        # Series for P(a, x).
        ap = a
        term = 1.0 / a
        total = term
        for _ in range(100000):
            ap += 1.0
            term *= x / ap
            total += term
            if abs(term) < abs(total) * 1e-16:
                break
        return max(0.0, 1.0 - total * math.exp(log_front))
    # Continued fraction for Q(a, x), by the modified Lentz method.
    tiny = 1e-300
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, 100000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-16:
            break
    return math.exp(log_front) * h


def chi2_sf(x: float, df: float) -> float:
    """P(X > x) for X chi-squared with df degrees of freedom."""
    if df <= 0:
        raise ValueError("df must be > 0")
    if x <= 0:
        return 1.0
    return _gamma_q(df / 2.0, x / 2.0)


_STD_NORMAL = NormalDist()


def normal_sf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """P(X > x) for X ~ Normal(mu, sigma^2), by statistics.NormalDist."""
    return _STD_NORMAL.cdf(-(x - mu) / sigma)
