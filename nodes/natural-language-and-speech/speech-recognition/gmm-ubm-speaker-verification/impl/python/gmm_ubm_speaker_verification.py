# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gmm-ubm-speaker-verification/. The authors are listed in prov/AXV6G0.jsonl.

"""GMM-UBM speaker verification (Reynolds, Quatieri and Dunn 2000).

A universal background model (UBM) is a Gaussian mixture with diagonal
covariances, given as a tuple (weights, means, variances), trained elsewhere
on many speakers. Enrollment MAP-adapts the UBM means to the speaker's frames
with the relevance factor r; the weights and variances are kept. A test
utterance y_1 ... y_T is scored by the average log likelihood ratio per frame

    Lambda = (1/T) sum_t [log p(y_t | speaker) - log p(y_t | UBM)],

and the claim is accepted when Lambda >= theta. Every log is the natural log,
and every mixture density is summed in log space.

score_top_c is the fast scoring of Reynolds et al.: for each frame it keeps the
C UBM components with the largest weighted log density, and sums only those
components in both models. With C = M it equals score.
"""

import math
from typing import List, Sequence, Tuple

from nlslog import log_sum

Vector = List[float]
Matrix = List[List[float]]
GMM = Tuple[Sequence[float], Sequence[Sequence[float]], Sequence[Sequence[float]]]

LOG_2PI = math.log(2.0 * math.pi)


def log_gauss_diag(x: Sequence[float], mu: Sequence[float], var: Sequence[float]) -> float:
    """Return log N(x; mu, diag(var))."""
    s = 0.0
    for xi, mi, vi in zip(x, mu, var):
        s += LOG_2PI + math.log(vi) + (xi - mi) * (xi - mi) / vi
    return -0.5 * s


def component_logs(x: Sequence[float], gmm: GMM) -> Vector:
    """Return log(c_m N(x; mu_m, Sigma_m)) for every component m."""
    weights, means, variances = gmm
    return [math.log(w) + log_gauss_diag(x, mu, v) if w > 0 else float("-inf")
            for w, mu, v in zip(weights, means, variances)]


def frame_loglik(x: Sequence[float], gmm: GMM) -> float:
    """Return log p(x | gmm)."""
    return log_sum(component_logs(x, gmm))


def enroll(frames: Sequence[Sequence[float]], ubm: GMM, r: float = 16.0) -> GMM:
    """Return the speaker model: the UBM with MAP-adapted means (relevance factor r > 0)."""
    if not r > 0:
        raise ValueError("the relevance factor must be positive")
    weights, means, variances = ubm
    M, d = len(means), len(means[0])
    n = [0.0] * M
    s = [[0.0] * d for _ in range(M)]
    for x in frames:
        lp = component_logs(x, ubm)
        z = log_sum(lp)
        for m in range(M):
            g = math.exp(lp[m] - z)  # @line L1
            if g > 0.0:
                n[m] += g  # @line L2
                for i in range(d):
                    s[m][i] += g * x[i]
    new_means = []
    for m in range(M):
        alpha = n[m] / (n[m] + r)  # @line L3
        if n[m] > 0.0:
            E = [v / n[m] for v in s[m]]
            new_means.append([alpha * E[i] + (1.0 - alpha) * means[m][i] for i in range(d)])  # @line L4
        else:
            new_means.append(list(means[m]))
    return (list(weights), new_means, [list(v) for v in variances])  # @line L5


def frame_llrs(frames: Sequence[Sequence[float]], spk: GMM, ubm: GMM) -> Vector:
    """Return log p(y_t | speaker) - log p(y_t | UBM) for every frame."""
    return [frame_loglik(y, spk) - frame_loglik(y, ubm) for y in frames]


def score(frames: Sequence[Sequence[float]], spk: GMM, ubm: GMM) -> float:
    """Return the average log likelihood ratio per frame."""
    if not frames:
        raise ValueError("no test frames")
    return math.fsum(frame_llrs(frames, spk, ubm)) / len(frames)  # @line L6


def decide(llr: float, theta: float) -> bool:
    """Accept the identity claim when the score reaches the threshold."""
    return llr >= theta  # @line L7


def score_top_c(frames: Sequence[Sequence[float]], spk: GMM, ubm: GMM, C: int = 5) -> float:
    """Return the fast top-C score: both mixtures summed over the C best UBM components of each frame.

    The speaker model must be MAP-adapted from this UBM, so that component m
    of both models describes the same region. Ties keep the lower index.
    """
    if not frames:
        raise ValueError("no test frames")
    total = []
    for y in frames:
        lu = component_logs(y, ubm)
        top = sorted(range(len(lu)), key=lambda m: (-lu[m], m))[:C]
        ls = component_logs(y, spk)
        total.append(log_sum(ls[m] for m in top) - log_sum(lu[m] for m in top))
    return math.fsum(total) / len(frames)


def bayes_threshold(p_target: float, c_miss: float = 1.0, c_fa: float = 1.0) -> float:
    """Return the Bayes threshold log(c_fa (1 - p_target) / (c_miss p_target)) for a calibrated LLR."""
    return math.log(c_fa * (1.0 - p_target) / (c_miss * p_target))
