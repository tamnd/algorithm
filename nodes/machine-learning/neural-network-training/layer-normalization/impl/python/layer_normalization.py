# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/layer-normalization/. The authors are listed in prov/0KRVGN.jsonl.
"""Layer normalization (Ba, Kiros and Hinton 2016) and RMSNorm (Zhang and Sennrich 2019) of one
example x with H features, with their backward passes. Both use only the features of that example,
so training and inference compute the same function.
"""

import math

Vec = list[float]


def ln_forward(x: Vec, gamma: Vec, beta: Vec, eps: float = 1e-5) -> tuple[Vec, tuple[Vec, float]]:
    """y = gamma * (x - mu) / sqrt(var + eps) + beta, with mu and var over the H features of x."""
    h = len(x)
    mu = sum(x) / h
    var = sum((v - mu) ** 2 for v in x) / h
    inv = 1 / math.sqrt(var + eps)
    xhat = [(v - mu) * inv for v in x]
    return [g * a + b for g, a, b in zip(gamma, xhat, beta)], (xhat, inv)


def ln_backward(dy: Vec, cache: tuple[Vec, float], gamma: Vec) -> tuple[Vec, Vec, Vec]:
    """dL/dx, dL/dgamma, dL/dbeta. With g = gamma * dy:
    dx_k = inv / H * (H g_k - sum_i g_i - x_hat_k sum_i g_i x_hat_i)."""
    xhat, inv = cache
    h = len(dy)
    g = [a * b for a, b in zip(gamma, dy)]
    sg = sum(g)
    sgx = sum(a * b for a, b in zip(g, xhat))
    dx = [inv / h * (h * gk - sg - xk * sgx) for gk, xk in zip(g, xhat)]
    return dx, [a * b for a, b in zip(dy, xhat)], dy[:]


def rms_forward(x: Vec, gamma: Vec, eps: float = 1e-8) -> tuple[Vec, float]:
    """RMSNorm: y = gamma * x / sqrt(mean(x^2) + eps). No centering and no shift."""
    r = math.sqrt(sum(v * v for v in x) / len(x) + eps)
    return [g * v / r for g, v in zip(gamma, x)], r


def rms_backward(dy: Vec, x: Vec, r: float, gamma: Vec) -> tuple[Vec, Vec]:
    """dL/dx and dL/dgamma: dx_k = g_k / r - x_k / (H r^3) * sum_i g_i x_i, with g = gamma * dy."""
    h = len(x)
    g = [a * b for a, b in zip(gamma, dy)]
    s = sum(a * b for a, b in zip(g, x))
    dx = [gk / r - xk * s / (h * r ** 3) for gk, xk in zip(g, x)]
    return dx, [d * v / r for d, v in zip(dy, x)]


def layer_norm_batch(xs: list[Vec], gamma: Vec, beta: Vec, eps: float = 1e-5) -> list[Vec]:
    """Apply layer normalization to each row on its own; the result of a row does not depend on the others."""
    return [ln_forward(x, gamma, beta, eps)[0] for x in xs]
