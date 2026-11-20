# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expectation-propagation-detection/. The authors are listed in prov/R4B3XS.jsonl.

"""Expectation propagation (EP) MIMO detection, in the real-valued form.

The complex model y = H x + w, with H an m by n matrix, x in S^n for a square
QAM constellation S and w ~ CN(0, N0 I), is first written as a real model
y_r = H_r x_r + w_r of size 2m by 2n. Each real symbol takes values in a PAM
alphabet A, and the noise has variance s2 = N0 / 2 per real dimension.

EP replaces the prior factor 1{x_i in A} of each real symbol by a Gaussian
factor exp(gamma_i x_i - Lambda_i x_i^2 / 2). The product with the Gaussian
likelihood is a Gaussian q(x) = N(mu, Sigma) with
    Sigma = (H_r^T H_r / s2 + diag(Lambda))^(-1),  mu = Sigma (H_r^T y_r / s2 + gamma).
Each iteration removes factor i from the marginal of q (the cavity),
multiplies the cavity by the true prior factor, matches the mean and the
variance of the result, and updates (gamma_i, Lambda_i) with damping.
This is the detector of Cespedes, Olmos, Sanchez-Fernandez and Perez-Cruz,
IEEE Trans. Comm. 62(8), 2014.
"""

import math

import cbb


def real_model(y: list[complex], h: list[list[complex]], real_symbols: bool = False) -> tuple[list[float], list[list[float]]]:
    """(y_r, H_r) with y_r = (Re y, Im y) and H_r = [[Re H, -Im H], [Im H, Re H]].

    If the symbols are real (PAM), x has no imaginary part and H_r = [Re H; Im H].
    """
    m, n = len(h), len(h[0])
    yr = [complex(v).real for v in y] + [complex(v).imag for v in y]
    hr = []
    for i in range(m):
        row = [complex(h[i][k]).real for k in range(n)]
        hr.append(row if real_symbols else row + [-complex(h[i][k]).imag for k in range(n)])
    for i in range(m):
        row = [complex(h[i][k]).imag for k in range(n)]
        hr.append(row if real_symbols else row + [complex(h[i][k]).real for k in range(n)])
    return yr, hr


def real_alphabet(points: list[complex]) -> list[float]:
    """The sorted levels of the real part of a square QAM (or real PAM) constellation."""
    return sorted({round(complex(p).real, 12) for p in points})


def tilted_moments(t: float, h2: float, alphabet: list[float]) -> tuple[float, float]:
    """Mean and variance of p(a) proportional to exp(-(a - t)^2 / (2 h2)) on the alphabet."""
    logs = [-(a - t) ** 2 / (2.0 * h2) for a in alphabet]
    top = max(logs)
    ws = [math.exp(v - top) for v in logs]
    tot = sum(ws)
    mean = sum(w * a for w, a in zip(ws, alphabet)) / tot
    var = sum(w * (a - mean) ** 2 for w, a in zip(ws, alphabet)) / tot
    return mean, var


def gaussian_q(gram: list[list[float]], hty: list[float], s2: float, gamma: list[float], lam: list[float]) -> tuple[list[float], list[list[float]]]:
    """(mu, Sigma) of q: Sigma = (G / s2 + diag(Lambda))^(-1), mu = Sigma (H^T y / s2 + gamma)."""
    d = len(gram)
    a = [[gram[i][k] / s2 + (lam[i] if i == k else 0.0) for k in range(d)] for i in range(d)]
    sig = [[v.real for v in row] for row in cbb.inv(a)]
    b = [hty[i] / s2 + gamma[i] for i in range(d)]
    mu = [sum(sig[i][k] * b[k] for k in range(d)) for i in range(d)]
    return mu, sig


def ep_real(yr: list[float], hr: list[list[float]], alphabet: list[float], s2: float, iters: int = 10, damping: float = 0.7, eps: float = 1e-9) -> tuple[list[float], list[float]]:
    """Run EP on a real model. Returns (mu, diag Sigma) of the final Gaussian approximation q."""
    m2, d = len(hr), len(hr[0])
    es = sum(a * a for a in alphabet) / len(alphabet)
    gram = [[sum(hr[r][i] * hr[r][k] for r in range(m2)) for k in range(d)] for i in range(d)]
    hty = [sum(hr[r][i] * yr[r] for r in range(m2)) for i in range(d)]
    gamma = [0.0] * d  # @line L1
    lam = [1.0 / es] * d
    for _ in range(iters):  # @line L2
        mu, sig = gaussian_q(gram, hty, s2, gamma, lam)  # @line L3
        for i in range(d):
            h2 = sig[i][i] / (1.0 - sig[i][i] * lam[i])  # @line L4
            t = h2 * (mu[i] / sig[i][i] - gamma[i])
            mp, vp = tilted_moments(t, h2, alphabet)  # @line L5
            vp = max(vp, eps)
            lam_new = 1.0 / vp - 1.0 / h2  # @line L6
            gam_new = mp / vp - t / h2
            if lam_new > 0.0:  # @line L7
                lam[i] = damping * lam_new + (1.0 - damping) * lam[i]
                gamma[i] = damping * gam_new + (1.0 - damping) * gamma[i]
    mu, sig = gaussian_q(gram, hty, s2, gamma, lam)
    return mu, [sig[i][i] for i in range(d)]


def ep_detect(y: list[complex], h: list[list[complex]], points: list[complex], n0: float, iters: int = 10, damping: float = 0.7) -> list[int]:
    """EP decisions for a complex model with a square QAM (or PAM) constellation, as point indices."""
    n = len(h[0])
    real_only = all(abs(complex(p).imag) < 1e-12 for p in points)
    yr, hr = real_model(y, h, real_only)
    alphabet = real_alphabet(points)
    mu, _ = ep_real(yr, hr, alphabet, n0 / 2.0, iters, damping)
    out = []
    for k in range(n):  # @line L8
        re = min(alphabet, key=lambda a: abs(mu[k] - a))
        im = 0.0 if real_only else min(alphabet, key=lambda a: abs(mu[n + k] - a))
        out.append(min(range(len(points)), key=lambda i: abs(points[i] - complex(re, im))))
    return out  # @line L9
