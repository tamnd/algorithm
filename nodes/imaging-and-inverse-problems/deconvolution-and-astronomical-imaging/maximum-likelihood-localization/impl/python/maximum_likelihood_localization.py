# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-localization/. The authors are listed in prov/XKDP82.jsonl.
"""Maximum likelihood localization of one emitter in a small image of photon counts.

Model: pixel (v, u) (row v, column u) covers [u - 1/2, u + 1/2] x [v - 1/2, v + 1/2],
in pixel units. The emitter at (x0, y0) sends N photons (expected) through a
symmetric Gaussian PSF of known standard deviation s, and every pixel gets
the expected background b. The expected count is

    mu(u, v) = N Ex(u) Ey(v) + b,
    Ex(u) = (1/2) [erf((u - x0 + 1/2) / (sqrt2 s)) - erf((u - x0 - 1/2) / (sqrt2 s))],

and the counts are independent Poisson. The negative log likelihood, up to
a constant, is L = sum (mu - c log mu). The parameters are
theta = (x0, y0, N, b).
"""

import math

from imgkit import poisson_sample
from imgla import cho_solve, cholesky, solve

_SQRT2 = math.sqrt(2.0)
_SQRT2PI = math.sqrt(2.0 * math.pi)


def _pixel_factor(u, x0, s):
    """(E, dE/dx0, d2E/dx0^2) for the pixel at u and the center x0."""
    t1 = u - x0 + 0.5
    t2 = u - x0 - 0.5
    e = 0.5 * (math.erf(t1 / (_SQRT2 * s)) - math.erf(t2 / (_SQRT2 * s)))
    g1 = math.exp(-t1 * t1 / (2 * s * s)) / (_SQRT2PI * s)
    g2 = math.exp(-t2 * t2 / (2 * s * s)) / (_SQRT2PI * s)
    de = g2 - g1
    d2e = (t2 * g2 - t1 * g1) / (s * s)
    return e, de, d2e


def model(theta, shape, s):
    """The image of expected counts mu for theta = (x0, y0, N, b)."""
    x0, y0, n_ph, b = theta
    n1, n2 = shape
    ex = [_pixel_factor(u, x0, s)[0] for u in range(n2)]
    ey = [_pixel_factor(v, y0, s)[0] for v in range(n1)]
    return [[n_ph * ex[u] * ey[v] + b for u in range(n2)] for v in range(n1)]


def _pixels(theta, shape, s):
    """For each pixel: (mu, the gradient of mu, the Hessian of mu) in theta."""
    x0, y0, n_ph, _ = theta
    n1, n2 = shape
    fx = [_pixel_factor(u, x0, s) for u in range(n2)]
    fy = [_pixel_factor(v, y0, s) for v in range(n1)]
    out = []
    for v in range(n1):
        ey, dey, d2ey = fy[v]
        for u in range(n2):
            ex, dex, d2ex = fx[u]
            mu = n_ph * ex * ey + theta[3]
            grad = [n_ph * dex * ey, n_ph * ex * dey, ex * ey, 1.0]
            hess = [[n_ph * d2ex * ey, n_ph * dex * dey, dex * ey, 0.0],
                    [n_ph * dex * dey, n_ph * ex * d2ey, ex * dey, 0.0],
                    [dex * ey, ex * dey, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0]]
            out.append((v, u, mu, grad, hess))
    return out


def nll(theta, counts, s):
    """L(theta) = sum (mu - c log mu); infinity if some mu <= 0."""
    shape = (len(counts), len(counts[0]))
    total = 0.0
    for row_mu, row_c in zip(model(theta, shape, s), counts):
        for mu, c in zip(row_mu, row_c):
            if mu <= 0:
                return math.inf
            total += mu - c * math.log(mu)
    return total


def derivatives(theta, counts, s):
    """(L, the gradient of L, the Hessian of L, the Fisher information) at theta."""
    shape = (len(counts), len(counts[0]))
    val = 0.0
    g = [0.0] * 4
    h = [[0.0] * 4 for _ in range(4)]
    fi = [[0.0] * 4 for _ in range(4)]
    for v, u, mu, dmu, d2mu in _pixels(theta, shape, s):
        c = counts[v][u]
        val += mu - c * math.log(mu)
        r = 1.0 - c / mu
        w = c / (mu * mu)
        for i in range(4):
            g[i] += r * dmu[i]
            for j in range(4):
                h[i][j] += w * dmu[i] * dmu[j] + r * d2mu[i][j]
                fi[i][j] += dmu[i] * dmu[j] / mu
    return val, g, h, fi


def fisher_information(theta, shape, s):
    """I(theta) = sum dmu dmu^T / mu over the pixels."""
    fi = [[0.0] * 4 for _ in range(4)]
    for _, _, mu, dmu, _ in _pixels(theta, shape, s):
        for i in range(4):
            for j in range(4):
                fi[i][j] += dmu[i] * dmu[j] / mu
    return fi


def crb(theta, shape, s):
    """The Cramer-Rao bound I(theta)^{-1}, a 4 x 4 matrix."""
    fi = fisher_information(theta, shape, s)
    eye = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    return solve(fi, eye)


def initial_guess(counts):
    """Background from the border mean, photons from the excess sum, center from the centroid."""
    n1, n2 = len(counts), len(counts[0])
    border = [counts[v][u] for v in range(n1) for u in range(n2)
              if v in (0, n1 - 1) or u in (0, n2 - 1)]
    b = max(sum(border) / len(border), 1e-3)
    excess = [[max(counts[v][u] - b, 0.0) for u in range(n2)] for v in range(n1)]
    total = sum(sum(row) for row in excess)
    if total <= 0:
        return [(n2 - 1) / 2, (n1 - 1) / 2, 1.0, b]
    x0 = sum(u * excess[v][u] for v in range(n1) for u in range(n2)) / total
    y0 = sum(v * excess[v][u] for v in range(n1) for u in range(n2)) / total
    return [x0, y0, total, b]


def localize(counts, s, theta0=None, max_iter=50, tol=1e-9, max_shift=1.0, callback=None):
    """Maximum likelihood fit of theta = (x0, y0, N, b) to a Poisson image.

    Newton steps with a backtracking line search; when the Hessian of L is
    not positive definite, a Fisher scoring step. A step moves the center by
    at most max_shift pixels, and the center must stay inside the image.
    Returns (theta, crb), with crb the inverse Fisher information at the
    estimate.
    """
    theta = list(theta0) if theta0 is not None else initial_guess(counts)  # @line L1
    shape = (len(counts), len(counts[0]))
    for _ in range(max_iter):  # @line L2
        val, g, h, fi = derivatives(theta, counts, s)  # @line L3
        if callback is not None:
            callback(theta, val)
        try:  # @line L4
            step = cho_solve(cholesky(h), [-gi for gi in g])  # @line L4
        except ValueError:  # @line L5
            step = cho_solve(cholesky(fi), [-gi for gi in g])  # @line L5
        slope = sum(gi * di for gi, di in zip(g, step))
        t = min(1.0, max_shift / max(abs(step[0]), abs(step[1]), 1e-300))  # @line L6
        while True:  # @line L6
            trial = [a + t * d for a, d in zip(theta, step)]  # @line L6
            if (trial[2] > 0 and -0.5 <= trial[0] <= shape[1] - 0.5  # @line L6
                    and -0.5 <= trial[1] <= shape[0] - 0.5  # @line L6
                    and nll(trial, counts, s) <= val + 1e-4 * t * slope):  # @line L6
                break  # @line L6
            t *= 0.5  # @line L6
            if t < 1e-12:  # @line L6
                break  # @line L6
        if t < 1e-12:
            break
        theta = trial  # @line L7
        if max(abs(t * d) for d in step) < tol:  # @line L7
            break  # @line L7
    return theta, crb(theta, shape, s)  # @line L8 L9


def poisson_image(rng, mu):
    """Independent Poisson counts with the means mu (an image)."""
    return [[poisson_sample(rng, m) for m in row] for row in mu]
