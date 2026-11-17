# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/psmc/. The authors are listed in prov/H1EZ3X.jsonl.
"""A small version of PSMC (Li and Durbin 2011).

The two copies of one diploid genome are cut into bins of s bases. A bin
is 1 (heterozygous: at least one site differs), 0 (homozygous) or None
(missing). The hidden state of a bin is the interval that holds the
coalescence time T of the two copies at that bin.

Units. Time is in units of 2 N0 generations. The relative population size
lambda(t) = N(t) / N0 is piecewise constant: lambdas[k] on [t_k, t_{k+1}),
where breaks = [t_0 = 0, t_1, ..., t_{K-1}, t_K = inf]. Two lineages
coalesce at rate 1 / lambda(t). theta = 4 N0 mu s and rho = 4 N0 r s are the
mutation and recombination rates per bin.

Model. T at the first bin has the coalescent law with rate 1 / lambda(t).
Given T = t, a bin is heterozygous with probability 1 - exp(-theta t). Between
two bins, a recombination happens with probability 1 - exp(-rho t); then,
as in the SMC, the cut point u is uniform on (0, t) and the new time is drawn
from the coalescent law started at age u. More than one recombination in a
bin counts as one. With this per-bin probability, the law of T at the first
bin is kept along the chain only up to an error of order rho squared.

Differences from the PSMC program: theta and rho are given, not fitted; the
transition matrix comes from numerical integration (composite Simpson rule)
instead of closed forms; the M step is a coordinate search; the times are not
grouped into shared parameters.
"""

from __future__ import annotations

import bisect
import math
from typing import List, Optional, Sequence, Tuple

Obs = Optional[int]

_TAIL = 40.0  # The last interval is integrated up to t_{K-1} + 40 lambda.


def time_breaks(k: int, t_max: float) -> List[float]:
    """K + 1 breaks spaced like those of PSMC: t_i = 0.1 (exp(i / (K - 1)
    ln(1 + 10 t_max)) - 1) for i < K, so t_{K-1} = t_max, and t_K = inf."""
    if k < 1 or t_max <= 0:
        raise ValueError("need k >= 1 and t_max > 0")
    if k == 1:
        return [0.0, math.inf]
    c = math.log1p(10.0 * t_max)
    out = [0.1 * math.expm1(i * c / (k - 1)) for i in range(k)]
    out.append(math.inf)
    return out


class History:
    """A piecewise-constant size history with its cumulative coalescence
    rate Lambda(t) = integral from 0 to t of 1 / lambda."""

    def __init__(self, breaks: Sequence[float], lambdas: Sequence[float]):
        if len(breaks) != len(lambdas) + 1 or breaks[0] != 0.0 or breaks[-1] != math.inf:
            raise ValueError("need breaks 0 = t_0 < ... < t_K = inf and K sizes")
        if any(b >= c for b, c in zip(breaks, breaks[1:])):
            raise ValueError("breaks must increase")
        if any(x <= 0 for x in lambdas):
            raise ValueError("sizes must be > 0")
        self.t = list(breaks)
        self.lam = [float(x) for x in lambdas]
        self.k = len(lambdas)
        cum = [0.0]
        for j in range(self.k - 1):
            cum.append(cum[-1] + (self.t[j + 1] - self.t[j]) / self.lam[j])
        cum.append(math.inf)
        self.cum = cum
        # ln of G(t_j) = integral from 0 to t_j of exp(Lambda(u)) du.
        self.log_g = [-math.inf] + [self._log_g(self.t[j]) for j in range(1, self.k)]

    def piece(self, t: float) -> int:
        return min(bisect.bisect_right(self.t, t) - 1, self.k - 1)

    def cum_rate(self, t: float) -> float:
        if t == math.inf:
            return math.inf
        j = self.piece(t)
        return self.cum[j] + (t - self.t[j]) / self.lam[j]

    def inverse_cum_rate(self, y: float) -> float:
        j = min(bisect.bisect_right(self.cum, y) - 1, self.k - 1)
        return self.t[j] + self.lam[j] * (y - self.cum[j])

    def _log_g(self, y: float) -> float:
        """ln of the integral from 0 to y of exp(Lambda(u)) du, computed with
        every exponent <= 0."""
        if y <= 0:
            return -math.inf
        top = self.cum_rate(y)
        total = 0.0
        for i in range(self.k):
            lo = self.t[i]
            if lo >= y:
                break
            hi = min(y, self.t[i + 1])
            total += self.lam[i] * (math.exp(self.cum_rate(hi) - top)
                                    - math.exp(self.cum[i] - top))
        return top + math.log(total)

    def interval_probs(self) -> List[float]:
        """pi_k = P(T in [t_k, t_{k+1}))."""
        return [math.exp(-self.cum[k]) - (math.exp(-self.cum[k + 1]) if k + 1 < self.k else 0.0)
                for k in range(self.k)]

    def laplace(self, c: float, k: int) -> float:
        """The integral over [t_k, t_{k+1}) of p(t) exp(-c t), where
        p(t) = exp(-Lambda(t)) / lambda(t) is the density of T."""
        r = 1.0 / self.lam[k] + c
        width = self.t[k + 1] - self.t[k]
        tail = 0.0 if width == math.inf else math.exp(-r * width)
        return math.exp(-self.cum[k] - c * self.t[k]) * (1.0 - tail) / (self.lam[k] * r)


def _h_values(h: History, t: float) -> List[float]:
    """H(t, t_l) for l = 0 .. K, where H(t, x) is the integral over u in
    (0, t) of P(T' >= x | start at u), and T' is drawn from the coalescent
    law started at age u."""
    log_gt = h._log_g(t)
    out = []
    for l in range(h.k + 1):
        x = h.t[l]
        if x == math.inf:
            out.append(0.0)
        elif x >= t:
            out.append(math.exp(log_gt - h.cum[l]) if log_gt > -math.inf else 0.0)
        else:
            g = math.exp(h.log_g[l] - h.cum[l]) if h.log_g[l] > -math.inf else 0.0
            out.append(g + (t - x))
    return out


def transition_joint(h: History, rho: float, steps: int = 64) -> List[List[float]]:
    """J[k][l] = P(T in interval k and T' in interval l) for the times T and
    T' of two neighbouring bins, with T from the stationary law."""
    if rho < 0:
        raise ValueError("need rho >= 0")
    k_n = h.k
    joint = [[0.0] * k_n for _ in range(k_n)]
    for k in range(k_n):
        joint[k][k] += h.laplace(rho, k)
        if rho == 0:
            continue
        lo = h.t[k]
        hi = h.t[k + 1]
        m = steps
        if hi == math.inf:
            hi = lo + _TAIL * h.lam[k]
            m = 4 * steps
        step = (hi - lo) / m
        acc = [0.0] * k_n
        for i in range(m + 1):
            t = lo + i * step
            if t == 0.0:
                continue  # The integrand is 0 at t = 0.
            w = 1.0 if i in (0, m) else (4.0 if i % 2 else 2.0)
            dens = math.exp(-h.cum_rate(t)) / h.lam[k]
            front = w * dens * (-math.expm1(-rho * t)) / t
            hv = _h_values(h, t)
            for l in range(k_n):
                acc[l] += front * (hv[l] - hv[l + 1])
        for l in range(k_n):
            joint[k][l] += acc[l] * step / 3.0
    return joint


def model_matrices(breaks: Sequence[float], lambdas: Sequence[float], theta: float,
                   rho: float, steps: int = 64):
    """(pi, A, e): the initial law, the K x K transition matrix (rows scaled
    to sum to 1) and e[k] = P(heterozygous bin | T in interval k)."""
    h = History(breaks, lambdas)
    pi = h.interval_probs()
    joint = transition_joint(h, rho, steps)
    a = []
    for row in joint:
        total = sum(row)
        a.append([x / total for x in row])
    e = [1.0 - h.laplace(theta, k) / pi[k] for k in range(h.k)]
    return pi, a, e


def _emit(e: Sequence[float], o: Obs) -> List[float]:
    if o is None:
        return [1.0] * len(e)
    if o == 1:
        return list(e)
    return [1.0 - x for x in e]


def forward_backward(obs: Sequence[Obs], pi, a, e):
    """Scaled forward-backward pass.

    Returns (loglik, post, xi, het, hom, first): the log-likelihood, the
    posterior of the state at each bin, the expected number of transitions
    k -> l, the expected numbers of heterozygous and homozygous bins in each
    state, and the posterior of the first state.
    """
    n = len(obs)
    k_n = len(pi)
    if n == 0:
        raise ValueError("empty sequence")
    alpha = []
    scale = []
    b = _emit(e, obs[0])
    cur = [pi[k] * b[k] for k in range(k_n)]  # @line L3
    for i in range(n):
        if i > 0:
            b = _emit(e, obs[i])
            prev = alpha[-1]
            cur = [sum(prev[k] * a[k][l] for k in range(k_n)) * b[l] for l in range(k_n)]
        c = sum(cur)
        if c <= 0:
            raise ValueError("observations have probability 0")
        scale.append(c)
        alpha.append([x / c for x in cur])
    loglik = sum(math.log(c) for c in scale)
    beta = [1.0] * k_n  # @line L4
    post = [None] * n
    xi = [[0.0] * k_n for _ in range(k_n)]
    het = [0.0] * k_n
    hom = [0.0] * k_n
    for i in range(n - 1, -1, -1):
        g = [alpha[i][k] * beta[k] for k in range(k_n)]
        post[i] = g
        if obs[i] == 1:
            for k in range(k_n):
                het[k] += g[k]  # @line L5
        elif obs[i] == 0:
            for k in range(k_n):
                hom[k] += g[k]
        if i == 0:
            break
        b = _emit(e, obs[i])
        nxt = [b[l] * beta[l] / scale[i] for l in range(k_n)]
        for k in range(k_n):
            ak = alpha[i - 1][k]
            for l in range(k_n):
                xi[k][l] += ak * a[k][l] * nxt[l]
        beta = [sum(a[k][l] * nxt[l] for l in range(k_n)) for k in range(k_n)]
    return loglik, post, xi, het, hom, post[0]


def log_likelihood(obs: Sequence[Obs], pi, a, e) -> float:
    return forward_backward(obs, pi, a, e)[0]


def expected_complete_loglik(stats, breaks, lambdas, theta, rho, steps=64) -> float:
    """Q(lambda) for the expected counts stats = (xi, het, hom, first)."""
    xi, het, hom, first = stats
    pi, a, e = model_matrices(breaks, lambdas, theta, rho, steps)
    q = 0.0
    for k in range(len(pi)):
        q += first[k] * math.log(pi[k])
        q += het[k] * math.log(e[k]) + hom[k] * math.log1p(-e[k])
        for l in range(len(pi)):
            if xi[k][l] > 0:
                q += xi[k][l] * math.log(a[k][l])
    return q


def _golden_max(f, lo, hi, iters):
    g = (math.sqrt(5.0) - 1.0) / 2.0
    x1 = hi - g * (hi - lo)
    x2 = lo + g * (hi - lo)
    f1, f2 = f(x1), f(x2)
    for _ in range(iters):
        if f1 < f2:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + g * (hi - lo)
            f2 = f(x2)
        else:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - g * (hi - lo)
            f1 = f(x1)
    return (x1, f1) if f1 >= f2 else (x2, f2)


def psmc_fit(obs: Sequence[Obs], breaks: Sequence[float], theta: float, rho: float,
             lambdas0: Sequence[float], iterations: int = 5, steps: int = 64,
             search: float = 2.0, golden_iters: int = 16):
    """EM for the sizes lambda with theta and rho fixed.

    Returns (lambdas, logliks), where logliks[i] is the log-likelihood of
    the sizes before iteration i, and the last entry that of the result.
    The M step changes one ln(lambda_j) at a time by golden-section search
    on [ln lambda_j - search, ln lambda_j + search] and keeps a change only
    if it raises Q, so the log-likelihood never decreases.
    """
    lam = [float(x) for x in lambdas0]
    logliks = []
    for _ in range(iterations):  # @line L1
        pi, a, e = model_matrices(breaks, lam, theta, rho, steps)  # @line L2
        loglik, _, xi, het, hom, first = forward_backward(obs, pi, a, e)
        logliks.append(loglik)
        stats = (xi, het, hom, first)
        best = expected_complete_loglik(stats, breaks, lam, theta, rho, steps)
        for j in range(len(lam)):  # @line L6
            def q_of(x, j=j):
                trial = lam[:]
                trial[j] = math.exp(x)
                return expected_complete_loglik(stats, breaks, trial, theta, rho, steps)
            x0 = math.log(lam[j])
            x, val = _golden_max(q_of, x0 - search, x0 + search, golden_iters)
            if val > best:
                lam[j] = math.exp(x)
                best = val
    pi, a, e = model_matrices(breaks, lam, theta, rho, steps)
    logliks.append(log_likelihood(obs, pi, a, e))
    return lam, logliks  # @line L7


def simulate_pair(rng, length: int, breaks: Sequence[float], lambdas: Sequence[float],
                  theta: float, rho: float) -> Tuple[List[float], List[int]]:
    """Coalescence times and observations of `length` bins under the
    continuous model. For each bin: one random() for the observation, then,
    except after the last bin, one random() for recombination and, if there
    is one, one random() for u and one expovariate for the new time."""
    h = History(breaks, lambdas)
    t = h.inverse_cum_rate(rng.expovariate(1.0))
    times, obs = [], []
    for i in range(length):
        times.append(t)
        obs.append(1 if rng.random() < -math.expm1(-theta * t) else 0)
        if i + 1 < length and rng.random() < -math.expm1(-rho * t):
            u = rng.random() * t
            t = h.inverse_cum_rate(h.cum_rate(u) + rng.expovariate(1.0))
    return times, obs


def to_real_units(breaks: Sequence[float], lambdas: Sequence[float], theta: float,
                  mu: float, bin_size: int, generation_time: float):
    """Scale the result: N0 = theta / (4 mu s); time t_k becomes 2 N0 t_k
    generations, or years with the generation time; size k is N0 lambda_k."""
    n0 = theta / (4.0 * mu * bin_size)
    years = [2.0 * n0 * t * generation_time for t in breaks]
    sizes = [n0 * x for x in lambdas]
    return n0, years, sizes
