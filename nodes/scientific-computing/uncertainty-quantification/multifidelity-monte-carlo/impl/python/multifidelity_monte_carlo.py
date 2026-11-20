# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multifidelity-monte-carlo/. The authors are listed in prov/SQG1XP.jsonl.
"""Multifidelity Monte Carlo (Peherstorfer, Willcox and Gunzburger 2016).

Model 1 is the high fidelity model, and models 2, ..., k are cheaper models of
the same output. Each model is a function of the same random input z. The
estimator is

    s = mean of f_1 over z_1..z_{m_1}
        + sum over i >= 2 of alpha_i (mean of f_i over z_1..z_{m_i}
                                      - mean of f_i over z_1..z_{m_(i-1)}),

with m_1 <= m_2 <= ... <= m_k and nested samples. It is unbiased for
E[f_1]. The sample counts and the weights minimize the variance at a fixed
cost p = sum w_i m_i, where w_i is the cost of one run of model i.

Lists are 0-based in the code: index 0 is model 1 of the text.
"""

import math
import random
from typing import Callable, Sequence

Model = Callable[[object], float]
Draw = Callable[[random.Random], object]


def pilot_statistics(models: Sequence[Model], draw: Draw, n: int, rng: random.Random):
    """Sample standard deviations sigma_i and correlations rho_i = corr(f_1, f_i) from n pilot inputs."""
    zs = [draw(rng) for _ in range(n)]
    ys = [[f(z) for z in zs] for f in models]
    means = [sum(y) / n for y in ys]
    sig = [math.sqrt(sum((v - mu) ** 2 for v in y) / (n - 1)) for y, mu in zip(ys, means)]
    rho = []
    for i, y in enumerate(ys):
        c = sum((a - means[0]) * (b - means[i]) for a, b in zip(ys[0], y)) / (n - 1)
        rho.append(c / (sig[0] * sig[i]))
    return sig, rho


def check_conditions(rho: Sequence[float], w: Sequence[float]) -> None:
    """The conditions of the optimal allocation: |rho_1| > ... > |rho_k| and the cost ratio test."""
    k = len(rho)
    r2 = [x * x for x in rho] + [0.0]
    for i in range(1, k):
        if not r2[i - 1] > r2[i]:
            raise ValueError("the models must be ordered by decreasing |rho|")
        if not w[i - 1] / w[i] > (r2[i - 1] - r2[i]) / (r2[i] - r2[i + 1]):
            raise ValueError(f"model {i + 1} is not cheap enough for its correlation")


def mfmc_allocation(sig: Sequence[float], rho: Sequence[float], w: Sequence[float], budget: float):
    """The optimal real sample counts m_i and weights alpha_i for the budget p."""
    k = len(rho)
    check_conditions(rho, w)  # @line L2
    r2 = [x * x for x in rho] + [0.0]
    ratio = [math.sqrt(w[0] * (r2[i] - r2[i + 1]) / (w[i] * (1.0 - r2[1]))) for i in range(k)]  # @line L3
    m1 = budget / sum(wi * ri for wi, ri in zip(w, ratio))  # @line L4
    m = [m1 * ri for ri in ratio]
    alpha = [rho[i] * sig[0] / sig[i] for i in range(k)]  # @line L5
    return m, alpha


def mfmc_variance(sig: Sequence[float], rho: Sequence[float], m: Sequence[float], alpha: Sequence[float]) -> float:
    """Var(s) = sigma_1^2 / m_1 + sum_{i>=2} (1/m_(i-1) - 1/m_i)(alpha_i^2 sigma_i^2 - 2 alpha_i rho_i sigma_1 sigma_i)."""
    v = sig[0] ** 2 / m[0]
    for i in range(1, len(m)):
        v += (1.0 / m[i - 1] - 1.0 / m[i]) * (alpha[i] ** 2 * sig[i] ** 2 - 2 * alpha[i] * rho[i] * sig[0] * sig[i])
    return v


def optimal_variance(sig: Sequence[float], rho: Sequence[float], w: Sequence[float], budget: float) -> float:
    """The minimum variance sigma_1^2 / p (sum_i sqrt(w_i (rho_i^2 - rho_(i+1)^2)))^2."""
    r2 = [x * x for x in rho] + [0.0]
    return sig[0] ** 2 / budget * sum(math.sqrt(w[i] * (r2[i] - r2[i + 1])) for i in range(len(rho))) ** 2


def integer_counts(m: Sequence[float]) -> list[int]:
    """Round down, keep at least 2 samples of model 1 and keep the counts non-decreasing."""
    out = []
    for x in m:
        c = max(2, int(math.floor(x)))
        if out and c < out[-1]:
            c = out[-1]
        out.append(c)
    return out


def mfmc_estimate(models: Sequence[Model], draw: Draw, m: Sequence[int], alpha: Sequence[float], rng: random.Random) -> float:
    """The multifidelity estimate with nested samples: z_1..z_(m_(i-1)) are the first m_(i-1) of z_1..z_(m_i)."""
    zs = [draw(rng) for _ in range(m[-1])]  # @line L6
    s = sum(models[0](z) for z in zs[: m[0]]) / m[0]  # @line L7
    for i in range(1, len(models)):  # @line L8
        y = [models[i](z) for z in zs[: m[i]]]
        s += alpha[i] * (sum(y) / m[i] - sum(y[: m[i - 1]]) / m[i - 1])
    return s  # @line L9


def mfmc(models: Sequence[Model], w: Sequence[float], budget: float, draw: Draw, rng: random.Random, n_pilot: int = 200) -> dict:
    """The full method: pilot statistics, optimal allocation, then one estimate."""
    sig, rho = pilot_statistics(models, draw, n_pilot, rng)  # @line L1
    m, alpha = mfmc_allocation(sig, rho, w, budget)
    mi = integer_counts(m)
    est = mfmc_estimate(models, draw, mi, alpha, rng)
    return {"estimate": est, "m": mi, "alpha": alpha, "sigma": sig, "rho": rho, "variance": mfmc_variance(sig, rho, mi, alpha)}
