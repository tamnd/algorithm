# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robust-mean-estimation-filter/. The authors are listed in prov/VJ455W.jsonl.

import math
import random


def weighted_mean(xs, w):
    total = sum(w)
    d = len(xs[0])
    return [sum(wi * x[j] for wi, x in zip(w, xs)) / total for j in range(d)]


def weighted_cov(xs, w, mu):
    """sum_i w_i (x_i - mu)(x_i - mu)^T / sum_i w_i, as a list of rows."""
    total = sum(w)
    d = len(mu)
    c = [[0.0] * d for _ in range(d)]
    for wi, x in zip(w, xs):
        if wi == 0:
            continue
        z = [a - b for a, b in zip(x, mu)]
        for a in range(d):
            za = wi * z[a]
            row = c[a]
            for b in range(a, d):
                row[b] += za * z[b]
    for a in range(d):
        for b in range(a, d):
            c[a][b] /= total
            c[b][a] = c[a][b]
    return c


def top_eigen(c, iters=2000, tol=1e-12, seed=0):
    """The largest eigenvalue and a unit eigenvector of a symmetric PSD matrix, by power iteration.

    The Rayleigh quotient of the returned vector is the returned value, so it is a
    lower bound on the largest eigenvalue; the loop runs until it stops changing.
    """
    d = len(c)
    rng = random.Random(seed)
    v = [rng.gauss(0.0, 1.0) for _ in range(d)]
    norm = math.sqrt(sum(t * t for t in v))
    v = [t / norm for t in v]
    lam = 0.0
    for _ in range(iters):
        u = [sum(c[a][b] * v[b] for b in range(d)) for a in range(d)]
        norm = math.sqrt(sum(t * t for t in u))
        if norm == 0.0:
            return 0.0, v
        u = [t / norm for t in u]
        new = sum(u[a] * sum(c[a][b] * u[b] for b in range(d)) for a in range(d))
        v = u
        if abs(new - lam) <= tol * max(1.0, new):
            lam = new
            break
        lam = new
    return lam, v


def default_threshold(eps, c=3.0):
    """1 + c eps log(1/eps), the stopping level for the top eigenvalue."""
    return 1.0 + c * eps * math.log(1.0 / eps)


def filter_mean(xs, eps, threshold=None, max_rounds=None, trace=None):
    """Robust mean of points whose clean part is close to N(mu, I), with an eps fraction corrupted.

    The weighted soft filter: while the top eigenvalue of the weighted covariance
    exceeds the threshold, every weight w_i is multiplied by 1 - tau_i / tau_max,
    where tau_i is the squared projection of x_i - mu_w on the top eigenvector.
    If trace is a list, one dict per round is appended to it.
    """
    n = len(xs)
    if threshold is None:
        threshold = default_threshold(eps)
    if max_rounds is None:
        max_rounds = n
    w = [1.0 / n] * n  # @line L1
    for r in range(max_rounds + 1):  # @line L2
        mu = weighted_mean(xs, w)  # @line L3
        lam, v = top_eigen(weighted_cov(xs, w, mu), seed=r)  # @line L4
        if trace is not None:
            trace.append({"round": r, "lambda": lam, "mean": mu, "weights": list(w)})
        if lam <= threshold:  # @line L5
            return mu
        tau = [(sum(a * (b - m) for a, b, m in zip(v, x, mu))) ** 2 for x in xs]  # @line L6
        tau_max = max(t for t, wi in zip(tau, w) if wi > 0)  # @line L7
        if all(t == tau_max for t, wi in zip(tau, w) if wi > 0):
            return mu  # @line L7
        w = [wi * (1.0 - t / tau_max) if wi > 0 else 0.0 for wi, t in zip(w, tau)]  # @line L8
    return weighted_mean(xs, w)


def sample_mean(xs):
    return weighted_mean(xs, [1.0] * len(xs))


def coordinatewise_median(xs):
    d = len(xs[0])
    out = []
    for j in range(d):
        col = sorted(x[j] for x in xs)
        m = len(col)
        out.append(col[m // 2] if m % 2 else (col[m // 2 - 1] + col[m // 2]) / 2)
    return out


def contaminated_gaussian(n, d, eps, shift, seed=0):
    """n points: (1 - eps) n from N(0, I_d) and eps n from N(shift * u, I_d), u = (1, ..., 1)/sqrt(d).

    The corrupted points have the same spread as the clean ones, so their norms do
    not give them away. Returns (points, is_corrupted).
    """
    rng = random.Random(seed)
    k = int(round(eps * n))
    s = shift / math.sqrt(d)
    xs, bad = [], []
    for i in range(n):
        corrupt = i < k
        xs.append([rng.gauss(s if corrupt else 0.0, 1.0) for _ in range(d)])
        bad.append(corrupt)
    return xs, bad


def norm(v):
    return math.sqrt(sum(t * t for t in v))
