# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/statistical-model-checking/. The authors are listed in prov/HY0E25.jsonl.

"""Statistical model checking: decide or estimate the probability of a path
property from independent simulated runs.

A sampler is a function of no arguments that returns True when a fresh random
run satisfies the property and False otherwise. The two methods are

  estimate(sample, eps, delta): Hoeffding's fixed sample size; the estimate is
      within eps of the true probability p with probability at least 1 - delta.

  sprt(sample, theta, eps, alpha, beta): Wald's sequential probability ratio
      test, as used by Younes and Simmons, for the question "is p >= theta?".
      It tests H0: p >= theta + eps against H1: p <= theta - eps. It returns
      (True, m) when it accepts H0 and (False, m) when it accepts H1, after m
      samples.

A small simulator of discrete-time Markov chains gives samplers for bounded
until formulas, in the format of the PCTL model checking page: P[s] is a dict
from successor states to probabilities, and phi, psi are sets of states.
"""

import math


def hoeffding_samples(eps, delta):
    """The least N with 2 exp(-2 N eps^2) <= delta."""
    if not (0 < eps < 1 and 0 < delta < 1):
        raise ValueError("need 0 < eps < 1 and 0 < delta < 1")
    n = math.ceil(math.log(2 / delta) / (2 * eps * eps))
    while n > 1 and 2 * math.exp(-2 * (n - 1) * eps * eps) <= delta:
        n -= 1  # guard against rounding in the logarithm
    while 2 * math.exp(-2 * n * eps * eps) > delta:
        n += 1
    return n


def estimate(sample, eps, delta):
    """Return (k / N, N), where k counts the successes among N samples."""
    n = hoeffding_samples(eps, delta)  # @line L10
    k = sum(1 for _ in range(n) if sample())  # @line L11
    return k / n, n  # @line L12


def sprt_parameters(p0, p1, alpha, beta, strict=False):
    """The step sizes and thresholds of the log likelihood ratio for
    H0: p >= p0 against H1: p <= p1.

    lambda = d * up + (m - d) * down after m samples with d successes.
    Wald's thresholds are A = (1 - beta) / alpha and B = beta / (1 - alpha).
    With strict=True they are A = 1 / alpha and B = beta, which bound the
    error probabilities by alpha and beta themselves.
    """
    if not (0 < p1 < p0 < 1):
        raise ValueError("need 0 < p1 < p0 < 1")
    if not (0 < alpha < 1 and 0 < beta < 1 and alpha + beta < 1):
        raise ValueError("need 0 < alpha, beta and alpha + beta < 1")
    up = math.log(p1 / p0)  # a success: evidence for H0, so lambda goes down
    down = math.log((1 - p1) / (1 - p0))  # a failure: evidence for H1
    if strict:
        log_a, log_b = math.log(1 / alpha), math.log(beta)
    else:
        log_a, log_b = math.log((1 - beta) / alpha), math.log(beta / (1 - alpha))
    return up, down, log_a, log_b


def sprt_verdict(d, m, params):
    """None while the test continues; True for H0 and False for H1."""
    up, down, log_a, log_b = params
    lam = d * up + (m - d) * down  # @line L7
    if lam >= log_a:  # @line L8
        return False
    if lam <= log_b:  # @line L9
        return True
    return None


def sprt(sample, theta, eps, alpha, beta, strict=False, max_samples=None):
    """Return (verdict, m). verdict is True when the test accepts p >= theta + eps,
    False when it accepts p <= theta - eps, and None when max_samples ran out."""
    p0, p1 = theta + eps, theta - eps  # @line L1
    params = sprt_parameters(p0, p1, alpha, beta, strict)  # @line L2
    m = d = 0  # @line L3
    while max_samples is None or m < max_samples:  # @line L4
        x = 1 if sample() else 0  # @line L5
        m += 1
        d += x  # @line L6
        verdict = sprt_verdict(d, m, params)
        if verdict is not None:
            return verdict, m
    return None, m


def step(chain, s, rng):
    """One random transition of the chain from state s."""
    u = rng.random()
    acc = 0.0
    last = None
    for t, p in chain["P"][s].items():
        if p <= 0:
            continue
        acc += float(p)
        last = t
        if u < acc:
            return t
    return last  # rounding: the probabilities summed to slightly below 1


def bounded_until_sampler(chain, start, phi, psi, k, rng):
    """A sampler for phi U<=k psi from start: simulate at most k steps."""

    def sample():
        s = start
        for i in range(k + 1):
            if s in psi:
                return True
            if s not in phi or i == k:
                return False
            s = step(chain, s, rng)
        return False

    return sample
