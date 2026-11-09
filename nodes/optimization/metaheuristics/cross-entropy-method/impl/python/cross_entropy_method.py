# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cross-entropy-method/. The authors are listed in prov/HK9SF5.jsonl.

"""The cross-entropy method for optimization, with a Bernoulli family on {0, 1}^n
and a Gaussian family with a diagonal covariance on R^n."""

import math
import random
from typing import Callable, Sequence


def elite_count(n_samples: int, rho: float) -> int:
    return max(1, math.ceil(rho * n_samples))


def ce_bernoulli(
    score: Callable[[Sequence[int]], float],
    p0: Sequence[float],
    n_samples: int,
    rho: float,
    alpha: float,
    iterations: int,
    rng: random.Random,
    trace: list | None = None,
) -> tuple[list[int], float, list[float]]:
    """Maximize score over {0, 1}^n. Return (best x, best score, final p).

    Each iteration draws n_samples vectors with independent bits, P(x_j = 1) = p_j,
    keeps the ceil(rho * n_samples) best, and moves p toward the bit frequencies of
    this elite with the smoothing factor alpha. If trace is a list, append
    (gamma, p) after each iteration, where gamma is the worst elite score.
    """
    p = list(p0)  # @line L1
    best, best_s = None, -math.inf
    k = elite_count(n_samples, rho)
    for _ in range(iterations):  # @line L2
        xs = [[1 if rng.random() < pj else 0 for pj in p] for _ in range(n_samples)]  # @line L3
        ss = [score(x) for x in xs]
        order = sorted(range(n_samples), key=lambda i: -ss[i])[:k]  # @line L4
        if ss[order[0]] > best_s:
            best, best_s = xs[order[0]], ss[order[0]]
        w = [sum(xs[i][j] for i in order) / k for j in range(len(p))]  # @line L5
        p = [alpha * wj + (1 - alpha) * pj for wj, pj in zip(w, p)]  # @line L6
        if trace is not None:
            trace.append((ss[order[-1]], p[:]))
    return best, best_s, p  # @line L7


def ce_gaussian(
    f: Callable[[Sequence[float]], float],
    mu0: Sequence[float],
    sigma0: Sequence[float],
    n_samples: int,
    rho: float,
    alpha: float,
    iterations: int,
    rng: random.Random,
    trace: list | None = None,
) -> tuple[list[float], float, list[float], list[float]]:
    """Minimize f over R^n with a Gaussian of diagonal covariance.

    Return (best x, best value, final mean, final standard deviations). The update
    is the maximum likelihood fit of the elite, the sample mean and the sample
    standard deviation, smoothed with alpha. If trace is a list, append
    (gamma, mu, sigma) after each iteration.
    """
    mu, sigma = list(mu0), list(sigma0)
    best, best_f = None, math.inf
    k = elite_count(n_samples, rho)
    n = len(mu)
    for _ in range(iterations):
        xs = [[rng.gauss(mu[j], sigma[j]) for j in range(n)] for _ in range(n_samples)]
        fs = [f(x) for x in xs]
        order = sorted(range(n_samples), key=lambda i: fs[i])[:k]
        if fs[order[0]] < best_f:
            best, best_f = xs[order[0]], fs[order[0]]
        m = [sum(xs[i][j] for i in order) / k for j in range(n)]
        s = [math.sqrt(sum((xs[i][j] - m[j]) ** 2 for i in order) / k) for j in range(n)]
        mu = [alpha * a + (1 - alpha) * b for a, b in zip(m, mu)]
        sigma = [alpha * a + (1 - alpha) * b for a, b in zip(s, sigma)]
        if trace is not None:
            trace.append((fs[order[-1]], mu[:], sigma[:]))
    return best, best_f, mu, sigma


def cut_value(w: Sequence[Sequence[float]], x: Sequence[int]) -> float:
    """Total weight of the edges between the sides x_i = 0 and x_i = 1."""
    n = len(x)
    return sum(w[i][j] for i in range(n) for j in range(i + 1, n) if x[i] != x[j])


def random_graph(n: int, rng: random.Random) -> list[list[float]]:
    """Symmetric weights: each pair gets weight 0 with probability 1/2, else an integer in 1..5."""
    w = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.5:
                w[i][j] = w[j][i] = float(rng.randint(1, 5))
    return w


def max_cut_brute_force(w: Sequence[Sequence[float]]) -> float:
    n = len(w)
    best = 0.0
    for mask in range(1 << (n - 1)):  # vertex n - 1 is fixed on side 0
        x = [(mask >> i) & 1 for i in range(n)]
        best = max(best, cut_value(w, x))
    return best
