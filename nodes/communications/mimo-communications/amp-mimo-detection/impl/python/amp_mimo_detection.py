# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/amp-mimo-detection/. The authors are listed in prov/V4YK5H.jsonl.

"""Approximate message passing (AMP) for MIMO detection, in the LAMA form.

The model is y = H x + w with H an m by n complex matrix, x a vector of n
equally likely points of a constellation, and w ~ CN(0, N0 I). AMP is built
for large i.i.d. channels with entries CN(0, 1/m), so that each column has
squared norm close to 1. beta = n / m is the system ratio.

Each iteration forms the pseudo-observation z = xhat + H^H r. In the large
system limit z behaves like x + CN(0, s2) for each stream, and the tracked
value s2 is the variance of that effective noise. The denoiser F is the
posterior mean of a symbol seen through that scalar channel, and G is the
posterior variance. The residual r carries the Onsager term
(beta mean(G) / s2) r_old, which keeps z close to Gaussian around x.

This is the LAMA iteration of Jeon, Ghods, Maleki and Studer (ISIT 2015;
Algorithm 2 of arXiv:1811.01917), written with s2 = N0 (1 + tau).
The prior "gaussian" replaces the constellation by CN(0, Es); then the
fixed point of the iteration is the linear MMSE estimate.
"""

import math

import cbb


def denoise(z: complex, s2: float, points: list[complex]) -> tuple[complex, float]:
    """(F, G): the posterior mean and variance of X, uniform on points, given z = X + CN(0, s2)."""
    s2 = max(s2, 1e-300)
    logs = [-abs(z - a) ** 2 / s2 for a in points]
    top = max(logs)
    ws = [math.exp(v - top) for v in logs]
    tot = sum(ws)
    mean = sum(w * a for w, a in zip(ws, points)) / tot
    var = sum(w * abs(a - mean) ** 2 for w, a in zip(ws, points)) / tot
    return mean, var


def denoise_gaussian(z: complex, s2: float, es: float) -> tuple[complex, float]:
    """(F, G) for the prior X ~ CN(0, Es): the linear shrinkage Es z / (Es + s2)."""
    return es * z / (es + s2), es * s2 / (es + s2)


def amp(y: list[complex], h: list[list[complex]], points: list[complex] | None, n0: float, iters: int = 20, es: float = 1.0) -> tuple[list[complex], list[complex], float]:
    """Run the AMP iteration. Returns (xhat, z, s2) after the last iteration.

    points=None selects the Gaussian prior CN(0, es). xhat is the posterior
    mean, z the last pseudo-observation and s2 the tracked variance of z - x.
    """
    m, n = len(h), len(h[0])
    beta = n / m
    hh = cbb.herm(h)
    if points is None:
        mu, var0 = 0j, es
    else:
        mu = sum(points) / len(points)
        var0 = sum(abs(a - mu) ** 2 for a in points) / len(points)
    xhat = [mu] * n  # @line L1
    r = cbb.sub(y, cbb.matvec(h, xhat))
    s2 = n0 + beta * var0  # @line L2
    z = xhat
    for _ in range(iters):  # @line L3
        z = cbb.add(xhat, cbb.matvec(hh, r))  # @line L4
        if points is None:
            fg = [denoise_gaussian(v, s2, es) for v in z]
        else:
            fg = [denoise(v, s2, points) for v in z]  # @line L5
        xnew = [f for f, _ in fg]
        gbar = sum(g for _, g in fg) / n
        onsager = beta * gbar / max(s2, 1e-300)
        r = [yi - hx + onsager * ri for yi, hx, ri in zip(y, cbb.matvec(h, xnew), r)]  # @line L6
        s2 = n0 + beta * gbar  # @line L7
        xhat = xnew
    return xhat, z, s2


def amp_detect(y: list[complex], h: list[list[complex]], points: list[complex], n0: float, iters: int = 20) -> list[int]:
    """The AMP decisions: for each stream, the point nearest to the last pseudo-observation z_k."""
    _, z, _ = amp(y, h, points, n0, iters)
    out = []
    for zk in z:  # @line L8
        out.append(min(range(len(points)), key=lambda i: abs(zk - points[i])))
    return out  # @line L9


def state_evolution(points: list[complex], n0: float, beta: float, iters: int, samples: int, rng) -> list[float]:
    """The state evolution s2_(t+1) = N0 + beta E|F(X + sqrt(s2_t) Z, s2_t) - X|^2, by Monte Carlo.

    Returns the list s2_1, ..., s2_(iters+1), with s2_1 = N0 + beta Var[X].
    The same draws of X and Z are reused at every step.
    """
    mu = sum(points) / len(points)
    var0 = sum(abs(a - mu) ** 2 for a in points) / len(points)
    xs = [points[rng.randrange(len(points))] for _ in range(samples)]
    zs = [cbb.cn(rng, 1.0) for _ in range(samples)]
    out = [n0 + beta * var0]
    for _ in range(iters):
        s2 = out[-1]
        sd = math.sqrt(s2)
        mse = sum(abs(denoise(x + sd * g, s2, points)[0] - x) ** 2 for x, g in zip(xs, zs)) / samples
        out.append(n0 + beta * mse)
    return out
