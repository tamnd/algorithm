# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/focal-loss/. The authors are listed in prov/05AH1D.jsonl.
"""Focal loss (Lin, Goyal, Girshick, He and Dollar 2017): FL(p_t) = -alpha_t (1 - p_t)^gamma log(p_t).
Binary form on a logit x with labels y in {+1, -1}, where p_t = sigmoid(y x), and softmax form on logits z.
With gamma = 0 it is the (alpha-balanced) cross-entropy.
"""

import math


def log_sigmoid(t: float) -> float:
    """log(1 / (1 + e^-t)), stable for large |t|."""
    return -math.log1p(math.exp(-t)) if t >= 0 else t - math.log1p(math.exp(t))


def sigmoid(t: float) -> float:
    return math.exp(log_sigmoid(t))


def alpha_t(y: int, alpha) -> float:
    if alpha is None:
        return 1.0
    return alpha if y == 1 else 1 - alpha


def focal_loss(x: float, y: int, gamma: float, alpha=None) -> float:
    """Binary focal loss of the logit x for the label y in {+1, -1}."""
    log_pt = log_sigmoid(y * x)
    pt = math.exp(log_pt)
    return -alpha_t(y, alpha) * (1 - pt) ** gamma * log_pt


def focal_grad(x: float, y: int, gamma: float, alpha=None) -> float:
    """d FL / d x = alpha_t y (1 - p_t)^gamma (gamma p_t log p_t + p_t - 1)  (Lin et al., Appendix B)."""
    log_pt = log_sigmoid(y * x)
    pt = math.exp(log_pt)
    return alpha_t(y, alpha) * y * (1 - pt) ** gamma * (gamma * pt * log_pt + pt - 1)


def log_softmax(z: list[float]) -> list[float]:
    m = max(z)
    lse = m + math.log(sum(math.exp(v - m) for v in z))
    return [v - lse for v in z]


def focal_loss_softmax(z: list[float], y: int, gamma: float) -> float:
    """-(1 - p_y)^gamma log p_y with p = softmax(z)."""
    lp = log_softmax(z)[y]
    return -(1 - math.exp(lp)) ** gamma * lp


def focal_grad_softmax(z: list[float], y: int, gamma: float) -> list[float]:
    """d/dz_j = [gamma (1 - p_y)^(gamma - 1) p_y log p_y - (1 - p_y)^gamma] (delta_jy - p_j)."""
    lps = log_softmax(z)
    p = [math.exp(v) for v in lps]
    py, lpy = p[y], lps[y]
    lead = gamma * (1 - py) ** (gamma - 1) * py * lpy if gamma != 0 else 0.0
    c = lead - (1 - py) ** gamma
    return [c * ((1 if j == y else 0) - pj) for j, pj in enumerate(p)]


def expected_focal(p: float, q: float, gamma: float) -> float:
    """The expected binary focal loss of the prediction p when the label is +1 with probability q."""
    return -q * (1 - p) ** gamma * math.log(p) - (1 - q) * p ** gamma * math.log(1 - p)


def best_prediction(q: float, gamma: float) -> float:
    """The p in (0, 1) that minimizes the expected focal loss, by golden-section search
    (the expected loss is unimodal in p for these cases)."""
    lo, hi = 1e-12, 1 - 1e-12
    r = (math.sqrt(5) - 1) / 2
    a, b = hi - r * (hi - lo), lo + r * (hi - lo)
    fa, fb = expected_focal(a, q, gamma), expected_focal(b, q, gamma)
    for _ in range(200):
        if fa < fb:
            hi, b, fb = b, a, fa
            a = hi - r * (hi - lo)
            fa = expected_focal(a, q, gamma)
        else:
            lo, a, fa = a, b, fb
            b = lo + r * (hi - lo)
            fb = expected_focal(b, q, gamma)
    return (lo + hi) / 2


def prior_bias(pi: float) -> float:
    """The bias b = -log((1 - pi) / pi) of the last layer, so that every anchor starts with p = pi."""
    return -math.log((1 - pi) / pi)
