# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fan-beam-filtered-back-projection/. The authors are listed in prov/2Y6GKS.jsonl.
"""Fan-beam filtered back-projection for an equiangular and a flat detector.

Conventions:
- omega(t) = (cos t, sin t) and omega_perp(t) = (-sin t, cos t). The Radon
  transform is R f(theta, s) = integral f(s omega(theta) + t omega_perp(theta)) dt.
- The source at angle beta is S(beta) = D omega_perp(beta), at the distance D
  from the center of rotation. The ray at the fan angle gamma leaves S(beta)
  in the direction -omega_perp(beta + gamma). It is the line with
  theta = beta + gamma and s = D sin gamma, so its line integral is
  g(beta, gamma) = R f(beta + gamma, D sin gamma).
- Equiangular detector: column j has the fan angle
  gamma_j = (j - (d - 1) / 2) alpha.
- Flat detector: a virtual line detector through the center, normal to the
  central ray. Column j sits at t_j = (j - (d - 1) / 2) tau, and its ray has
  the fan angle atan(t_j / D).
- Full scan: beta_k = 2 pi k / a, k = 0 .. a - 1. Short scan: beta_k = k
  (pi + 2 delta) / a with Parker weights, delta the half fan angle.
- The output is an n x n image on [-1, 1]^2. Pixel (i, j) has its center at
  x_j = -1 + (2 j + 1) / n and y_i = 1 - (2 i + 1) / n, so y goes up.
"""

import math


def ram_lak(m, tau):
    """h(m tau) of the ramp filter |sigma| band-limited to 1 / (2 tau)."""
    if m == 0:
        return 1.0 / (4.0 * tau * tau)
    if m % 2 == 0:
        return 0.0
    return -1.0 / (m * m * math.pi * math.pi * tau * tau)


def fan_kernel(d, alpha):
    """kappa(m alpha) = (1/2) (m alpha / sin(m alpha))^2 h(m alpha), m = -(d - 1) .. d - 1.

    Entry m + d - 1 holds kappa(m alpha): 1 / (8 alpha^2) at m = 0, 0 at even
    m, and -1 / (2 pi^2 sin^2(m alpha)) at odd m.
    """
    out = []
    for m in range(-(d - 1), d):
        if m == 0:
            out.append(1.0 / (8.0 * alpha * alpha))
        elif m % 2 == 0:
            out.append(0.0)
        else:
            out.append(-1.0 / (2.0 * math.pi * math.pi * math.sin(m * alpha) ** 2))
    return out


def flat_kernel(d, tau):
    """h(m tau) / 2 with the Ram-Lak h, m = -(d - 1) .. d - 1."""
    return [0.5 * ram_lak(m, tau) for m in range(-(d - 1), d)]


def convolve(p, kern, step):
    """q_j = step * sum_l kern((j - l) step) p_l, the aperiodic convolution by a direct sum."""
    d = len(p)
    return [step * sum(kern[j - l + d - 1] * p[l] for l in range(d)) for j in range(d)]


def parker_weight(beta, gamma, delta):
    """Parker's short-scan weight for beta in [0, pi + 2 delta] and |gamma| <= delta.

    With the geometry above the ray (beta, gamma) and the ray
    (beta + pi + 2 gamma, -gamma) are the same line, and their weights add to 1.
    """
    if beta < 0.0 or beta > math.pi + 2.0 * delta:
        return 0.0
    if beta < 2.0 * (delta - gamma):
        return math.sin(0.25 * math.pi * beta / (delta - gamma)) ** 2
    if beta <= math.pi - 2.0 * gamma:
        return 1.0
    if delta + gamma <= 0.0:
        return 0.0
    return math.sin(0.25 * math.pi * (math.pi + 2.0 * delta - beta) / (delta + gamma)) ** 2


def source_coordinates(x, y, beta, dist):
    """(L cos gamma', L sin gamma') of the point (x, y) seen from the source S(beta).

    L is the distance from the source and gamma' the fan angle of the ray
    through the point: L cos gamma' = D - x.omega_perp(beta) and
    L sin gamma' = x.omega(beta).
    """
    c, s = math.cos(beta), math.sin(beta)
    return dist - (-x * s + y * c), x * c + y * s


def lin_interp(q, u):
    """The linear interpolation of q at the fractional index u, and 0 outside [0, len(q) - 1]."""
    b = math.floor(u)
    w = u - b
    val = 0.0
    if 0 <= b < len(q):
        val += (1.0 - w) * q[b]
    if 0 <= b + 1 < len(q):
        val += w * q[b + 1]
    return val


def _angles(a, scan, delta):
    if scan == "full":
        return [2.0 * math.pi * k / a for k in range(a)], 2.0 * math.pi / a, 1.0
    if scan == "short":
        span = math.pi + 2.0 * delta
        return [span * k / a for k in range(a)], span / a, 2.0
    raise ValueError("scan must be 'full' or 'short'")


def fan_beam_fbp(sino, dist, alpha, n, scan="full", delta=None):
    """Reconstruct an n x n image from equiangular fan-beam data.

    sino[k][j] = g(beta_k, gamma_j). For scan = "short" the angles cover
    [0, pi + 2 delta) and delta must be at least the largest |gamma_j|.
    """
    a, d = len(sino), len(sino[0])  # @line L1
    betas, dbeta, factor = _angles(a, scan, delta)
    kern = fan_kernel(d, alpha)  # @line L2
    c0 = (d - 1) / 2.0
    gammas = [(j - c0) * alpha for j in range(d)]
    qs = []
    for k in range(a):  # @line L3
        w = [1.0] * d
        if scan == "short":
            w = [parker_weight(betas[k], gm, delta) for gm in gammas]
        p = [dist * math.cos(gm) * wj * v for gm, wj, v in zip(gammas, w, sino[k])]  # @line L4
        qs.append(convolve(p, kern, alpha))  # @line L5
    xs = [-1.0 + (2 * j + 1) / n for j in range(n)]
    ys = [1.0 - (2 * i + 1) / n for i in range(n)]
    img = [[0.0] * n for _ in range(n)]
    for k in range(a):
        q, beta = qs[k], betas[k]
        for i, y in enumerate(ys):  # @line L6
            row = img[i]
            for j, x in enumerate(xs):
                lc, ls = source_coordinates(x, y, beta, dist)  # @line L7
                gam = math.atan2(ls, lc)
                row[j] += lin_interp(q, gam / alpha + c0) / (lc * lc + ls * ls)  # @line L8
    w = factor * dbeta
    return [[w * v for v in row] for row in img]  # @line L9


def fan_beam_fbp_flat(sino, dist, tau, n, scan="full", delta=None):
    """Reconstruct an n x n image from fan-beam data on a flat detector.

    sino[k][j] = g(beta_k, atan(t_j / D)) with t_j = (j - (d - 1) / 2) tau on
    the virtual detector through the center.
    """
    a, d = len(sino), len(sino[0])
    betas, dbeta, factor = _angles(a, scan, delta)
    kern = flat_kernel(d, tau)
    c0 = (d - 1) / 2.0
    ts = [(j - c0) * tau for j in range(d)]
    qs = []
    for k in range(a):
        w = [1.0] * d
        if scan == "short":
            w = [parker_weight(betas[k], math.atan(t / dist), delta) for t in ts]
        p = [dist / math.sqrt(dist * dist + t * t) * wj * v for t, wj, v in zip(ts, w, sino[k])]
        qs.append(convolve(p, kern, tau))
    xs = [-1.0 + (2 * j + 1) / n for j in range(n)]
    ys = [1.0 - (2 * i + 1) / n for i in range(n)]
    img = [[0.0] * n for _ in range(n)]
    for k in range(a):
        q, beta = qs[k], betas[k]
        for i, y in enumerate(ys):
            row = img[i]
            for j, x in enumerate(xs):
                lc, ls = source_coordinates(x, y, beta, dist)
                u = lc / dist
                row[j] += lin_interp(q, (dist * ls / lc) / tau + c0) / (u * u)
    w = factor * dbeta
    return [[w * v for v in row] for row in img]
