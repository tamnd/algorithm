# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/magsac/. The authors are listed in prov/RA0N0V.jsonl.
"""MAGSAC++, Barath, Noskova, Ivashechkin and Matas 2020 (after MAGSAC, Barath,
Matas and Noskova 2019), for a 2D affine map q = A p + b from 3 correspondences.

No inlier threshold is fixed. The noise scale sigma is taken as uniform on
[0, sigma_max], and the residual r = |A p + b - q| of an inlier, divided by
sigma, follows a chi distribution with n = 2 degrees of freedom, truncated at
k sigma. Marginalizing the inlier density over sigma gives a weight w(r) and a
loss rho(r) = integral_0^r x w(x) dx. A model scores sum_i rho(r_i), lower is
better. Each new best model is polished by iteratively reweighted least squares
with the weights w(r_i) (sigma-consensus++). For n = 2 every incomplete gamma
function reduces to erf and erfc, so w and rho have closed forms here.
Standard library only.
"""

import math
import random

K_CHI2_99 = math.sqrt(-2.0 * math.log(0.01))  # 0.99 quantile of chi with 2 dof, about 3.035


def magsac_weight(r, sigma_max, k=K_CHI2_99):
    """w(r) = (1/sigma_max) C(2) sqrt(2) (Gamma(1/2, r^2/2 sigma_max^2) - Gamma(1/2, k^2/2)), 0 beyond k sigma_max."""
    if r >= k * sigma_max:
        return 0.0
    a = math.sqrt(2.0) * sigma_max
    return math.sqrt(math.pi / 2.0) / sigma_max * (math.erfc(r / a) - math.erfc(k / math.sqrt(2.0)))


def magsac_loss(r, sigma_max, k=K_CHI2_99):
    """rho(r) = integral_0^r x w(x) dx, constant beyond k sigma_max."""
    r = min(r, k * sigma_max)
    a = math.sqrt(2.0) * sigma_max
    e = math.exp(-(r / a) ** 2)
    inner = (0.5 * r * r * math.erfc(r / a) + 0.25 * a * a * math.erf(r / a)
             - a * r * e / (2.0 * math.sqrt(math.pi)) - 0.5 * r * r * math.erfc(k / math.sqrt(2.0)))
    return math.sqrt(math.pi / 2.0) / sigma_max * inner


def solve3(m, v):
    """Solve a 3x3 linear system by Gaussian elimination with partial pivoting; None if singular."""
    a = [list(m[i]) + [v[i]] for i in range(3)]
    for c in range(3):
        p = max(range(c, 3), key=lambda i: abs(a[i][c]))
        if abs(a[p][c]) < 1e-12:
            return None
        a[c], a[p] = a[p], a[c]
        for i in range(c + 1, 3):
            f = a[i][c] / a[c][c]
            for j in range(c, 4):
                a[i][j] -= f * a[c][j]
    x = [0.0, 0.0, 0.0]
    for i in (2, 1, 0):
        x[i] = (a[i][3] - sum(a[i][j] * x[j] for j in range(i + 1, 3))) / a[i][i]
    return x


def fit_affine_weighted(pairs, weights):
    """argmin sum_i w_i |A p_i + b - q_i|^2 as (a11, a12, b1, a21, a22, b2), or None if degenerate."""
    m = [[0.0] * 3 for _ in range(3)]
    vx = [0.0] * 3
    vy = [0.0] * 3
    for (p, q), w in zip(pairs, weights):
        if w <= 0.0:
            continue
        row = (p[0], p[1], 1.0)
        for i in range(3):
            vx[i] += w * row[i] * q[0]
            vy[i] += w * row[i] * q[1]
            for j in range(3):
                m[i][j] += w * row[i] * row[j]
    rx = solve3(m, vx)
    ry = solve3(m, vy)
    if rx is None or ry is None:
        return None
    return (rx[0], rx[1], rx[2], ry[0], ry[1], ry[2])


def fit_affine_minimal(sample):
    """The affine map through 3 correspondences, or None if the 3 source points are collinear."""
    (p1, _), (p2, _), (p3, _) = sample
    area = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
    if abs(area) < 1e-9:
        return None
    return fit_affine_weighted(sample, [1.0, 1.0, 1.0])


def residual(model, pair):
    a11, a12, b1, a21, a22, b2 = model
    (px, py), (qx, qy) = pair
    return math.hypot(a11 * px + a12 * py + b1 - qx, a21 * px + a22 * py + b2 - qy)


def total_loss(model, data, sigma_max, k=K_CHI2_99):
    return sum(magsac_loss(residual(model, x), sigma_max, k) for x in data)


def ransac_trials(p, w, s):
    q = w ** s
    if q >= 1.0:
        return 1
    if q <= 0.0:
        return math.inf
    return math.ceil(math.log(1.0 - p) / math.log1p(-q))


def sigma_consensus_pp(model, data, sigma_max, k=K_CHI2_99, iters=5):
    """IRLS: theta <- argmin sum_i w(r_i(theta_old)) r_i(theta)^2, a fixed number of times."""
    for _ in range(iters):  # @line L13
        w = [magsac_weight(residual(model, x), sigma_max, k) for x in data]  # @line L14
        nxt = fit_affine_weighted(data, w)  # @line L15
        if nxt is None:
            break
        model = nxt
    return model  # @line L16


def marginal_trials(model, data, sigma_max, k, p, s, max_trials, d=10):
    """The RANSAC count averaged over d noise scales sigma_j = j sigma_max / d, each capped at max_trials."""
    res = [residual(model, x) for x in data]
    n = len(data)
    total = 0.0
    for j in range(1, d + 1):
        thr = k * sigma_max * j / d
        w = sum(1 for r in res if r <= thr) / n
        total += min(max_trials, ransac_trials(p, w, s))
    return math.ceil(total / d)


def magsac_pp(data, sigma_max, rng=None, k=K_CHI2_99, p=0.99, max_trials=2000, irls_iters=5, d=10,
              on_model=None):
    """data: list of ((px, py), (qx, qy)). Return (model, loss, trials)."""
    rng = rng if rng is not None else random.Random()
    s, n = 3, len(data)
    if n < s:
        return None, math.inf, 0
    best, best_loss, kk, t = None, math.inf, max_trials, 0  # @line L1
    while t < kk:  # @line L2
        t += 1  # @line L3
        theta = fit_affine_minimal(rng.sample(data, s))  # @line L4
        if theta is None:  # @line L5
            continue
        loss = total_loss(theta, data, sigma_max, k)  # @line L6
        if on_model is not None:
            on_model(theta, loss)
        if loss < best_loss:  # @line L7
            polished = sigma_consensus_pp(theta, data, sigma_max, k, irls_iters)  # @line L8
            pl = total_loss(polished, data, sigma_max, k)
            if pl < loss:  # @line L9
                theta, loss = polished, pl
            best, best_loss = theta, loss  # @line L10
            kk = min(max_trials, marginal_trials(best, data, sigma_max, k, p, s, max_trials, d))  # @line L11
    return best, best_loss, t  # @line L12
