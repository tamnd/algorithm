# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-smoothing/. The authors are listed in prov/HVTX47.jsonl.

"""Randomized smoothing with Gaussian noise: PREDICT and CERTIFY of Cohen, Rosenfeld and Kolter (2019).

The smoothed classifier is g(x) = the label c that maximizes P(f(x + eta) = c), with
eta drawn from N(0, sigma^2 I). CERTIFY estimates the top label from n0 noisy samples,
then counts it in n fresh samples and takes a one-sided Clopper-Pearson lower bound
pA of its probability. If pA > 1/2, then with probability at least 1 - alpha over the
samples, g is constant on the open l2 ball of radius sigma * PhiInv(pA) around x.
The certificate is about g, not about the base classifier f.

The base classifiers in the tests are synthetic models built from a fixed seed.
"""

import math
import random
from statistics import NormalDist
from typing import Callable, Optional, Sequence

Classifier = Callable[[list[float]], int]
ABSTAIN = -1
_STD = NormalDist()


def binomial_upper_tail(k: int, n: int, p: float) -> float:
    """P(K >= k) for K ~ Binomial(n, p). Cost O(n - k)."""
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    if p <= 0.0:
        return 0.0
    if p >= 1.0:
        return 1.0
    log_term = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * math.log(p) + (n - k) * math.log1p(-p)
    term = math.exp(log_term)
    total = term
    ratio = p / (1.0 - p)
    for i in range(k, n):
        term *= (n - i) / (i + 1) * ratio
        total += term
    return min(total, 1.0)


def lower_confidence_bound(k: int, n: int, alpha: float) -> float:
    """The one-sided Clopper-Pearson lower bound of a binomial proportion at level 1 - alpha.

    It is the p with P(K >= k) = alpha under Binomial(n, p), and 0 when k = 0. For every
    p, P_p(bound > p) <= alpha. Found by bisection, so it is exact to about 1e-12.
    Cost O(n) per step of the bisection.
    """
    if k <= 0:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(45):
        mid = (lo + hi) / 2.0
        if binomial_upper_tail(k, n, mid) < alpha:
            lo = mid
        else:
            hi = mid
    return lo


def binomial_p_value(k: int, n: int) -> float:
    """Two-sided p-value of the test of p = 1/2 for k successes in n trials. Cost O(n)."""
    if n == 0:
        return 1.0
    m = max(k, n - k)
    return min(1.0, 2.0 * binomial_upper_tail(m, n, 0.5))


def sample_under_noise(f: Classifier, x: Sequence[float], n: int, sigma: float, rng: random.Random) -> dict[int, int]:
    """Counts of the labels of f(x + eta) for n independent draws of eta from N(0, sigma^2 I). Cost n calls of f."""
    counts: dict[int, int] = {}
    for _ in range(n):  # @line L8
        noisy = [a + rng.gauss(0.0, sigma) for a in x]  # @line L9
        c = f(noisy)  # @line L10
        counts[c] = counts.get(c, 0) + 1  # @line L10
    return counts  # @line L11


def top_two(counts: dict[int, int]) -> tuple[int, int, int, int]:
    """(cA, nA, cB, nB): the two labels with the most counts, ties to the smaller label."""
    order = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ca, na = order[0]
    cb, nb = order[1] if len(order) > 1 else (ABSTAIN, 0)
    return ca, na, cb, nb


def certify(f: Classifier, sigma: float, x: Sequence[float], n0: int, n: int, alpha: float,
            rng: random.Random) -> tuple[int, float]:
    """(cA, R) with an l2 radius R > 0 for the smoothed classifier, or (ABSTAIN, 0.0).

    With probability at least 1 - alpha over the noise, if the answer is (cA, R), then
    g(x + delta) = cA for every delta with ||delta||_2 < R.
    Precondition: sigma > 0, n0 >= 1, n >= 1, 0 < alpha < 1. Cost n0 + n calls of f.
    """
    counts0 = sample_under_noise(f, x, n0, sigma, rng)  # @line L1
    ca = top_two(counts0)[0]  # @line L2
    counts = sample_under_noise(f, x, n, sigma, rng)  # @line L3
    pa = lower_confidence_bound(counts.get(ca, 0), n, alpha)  # @line L4
    if pa > 0.5:  # @line L5
        return ca, sigma * _STD.inv_cdf(pa)  # @line L6
    return ABSTAIN, 0.0  # @line L7


def predict(f: Classifier, sigma: float, x: Sequence[float], n: int, alpha: float, rng: random.Random) -> int:
    """The label of the smoothed classifier, or ABSTAIN. A wrong label has probability at most alpha.

    Cost n calls of f.
    """
    counts = sample_under_noise(f, x, n, sigma, rng)  # @line L12
    ca, na, _, nb = top_two(counts)  # @line L13
    if binomial_p_value(na, na + nb) <= alpha:  # @line L14
        return ca  # @line L14
    return ABSTAIN  # @line L15


def radius_from_probabilities(sigma: float, pa: float, pb: float) -> float:
    """The radius (sigma / 2) (PhiInv(pA) - PhiInv(pB)) of Theorem 1 of Cohen et al., for 0 < pB <= pA < 1."""
    return sigma / 2.0 * (_STD.inv_cdf(pa) - _STD.inv_cdf(pb))


def linear_classifier(w: Sequence[float], b: float) -> Classifier:
    """The base classifier x -> 1 if w.x + b > 0 else 0."""
    def f(x: list[float]) -> int:
        return 1 if math.fsum(wi * xi for wi, xi in zip(w, x, strict=True)) + b > 0 else 0
    return f


def exact_top_probability(w: Sequence[float], b: float, x: Sequence[float], sigma: float) -> tuple[int, float]:
    """For the linear classifier, the label of g at x and its exact probability under the noise.

    w.(x + eta) + b is normal with mean w.x + b and standard deviation sigma ||w||, so the
    probability of the label 1 is Phi((w.x + b) / (sigma ||w||)).
    """
    s = math.fsum(wi * xi for wi, xi in zip(w, x, strict=True)) + b
    p1 = _STD.cdf(s / (sigma * math.sqrt(math.fsum(wi * wi for wi in w))))
    return (1, p1) if p1 > 0.5 else (0, 1.0 - p1)


def distance_to_boundary(w: Sequence[float], b: float, x: Sequence[float]) -> float:
    """The l2 distance from x to the hyperplane w.x + b = 0."""
    s = math.fsum(wi * xi for wi, xi in zip(w, x, strict=True)) + b
    return abs(s) / math.sqrt(math.fsum(wi * wi for wi in w))


def certified_accuracy(results: Sequence[tuple[int, float]], labels: Sequence[int], radius: float) -> float:
    """Fraction of points with a correct certified label and a certified radius above the given one."""
    if not labels:
        return 0.0
    good = sum(1 for (c, r), y in zip(results, labels, strict=True) if c == y and r > radius)
    return good / len(labels)


def smoothed_label_estimate(f: Classifier, sigma: float, x: Sequence[float], n: int,
                            rng: random.Random) -> Optional[int]:
    """The most frequent label of f(x + eta) over n samples, with no confidence claim. For tests only."""
    counts = sample_under_noise(f, x, n, sigma, rng)
    return top_two(counts)[0] if counts else None
