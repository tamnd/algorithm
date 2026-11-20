# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svd-precoding/. The authors are listed in prov/8XKR8Q.jsonl.

"""SVD precoding for a single-user MIMO channel.

The model is y = H x + w, with H an m by n complex matrix (m receive antennas,
n transmit antennas), w ~ CN(0, N0 I) and the power constraint E[x^H x] <= P.
The transmitter knows H. It computes H = U S V^H, sends stream i along the
right singular vector v_i with power p_i, and chooses the powers by
water-filling over the gains s_i^2 / N0. The receiver applies U^H, which
turns the channel into parallel scalar channels z_i = s_i sqrt(p_i) d_i + noise.
"""

import math

import cbb


def svd(a: list[list[complex]], tol: float = 1e-15, max_sweeps: int = 100):
    """The SVD a = U diag(s) V^H of an m by n complex matrix, by one-sided Jacobi.

    Returns (u, s, v). s has n values in decreasing order. v is n by n and
    unitary. u is m by n; its column i is a_i / s_i for s_i > 0 and the zero
    vector for s_i = 0. Each sweep rotates every pair of columns of a so that
    the pair becomes orthogonal; the same rotations applied to I give V.
    """
    m, n = len(a), len(a[0])
    cols = [[complex(a[i][k]) for i in range(m)] for k in range(n)]
    vcols = [[1 + 0j if i == k else 0j for i in range(n)] for k in range(n)]
    # A column with a squared norm below this is zero to rounding; rotating it only adds noise.
    small = (1e-15) ** 2 * sum(abs(x) ** 2 for col in cols for x in col)
    for _ in range(max_sweeps):
        rotated = False
        for p in range(n - 1):
            for q in range(p + 1, n):
                ap, aq = cols[p], cols[q]
                alpha = sum(abs(x) ** 2 for x in ap)
                beta = sum(abs(x) ** 2 for x in aq)
                if alpha <= small or beta <= small:
                    continue
                gamma = sum(x.conjugate() * y for x, y in zip(ap, aq))
                g = abs(gamma)
                if g <= tol * math.sqrt(alpha * beta):
                    continue
                rotated = True
                ph = gamma / g  # e^(j phi)
                ph /= abs(ph)
                zeta = (beta - alpha) / (2.0 * g)
                t = (1.0 if zeta >= 0 else -1.0) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                e = ph.conjugate()
                cols[p] = [c * x - s * e * y for x, y in zip(ap, aq)]
                cols[q] = [s * x + c * e * y for x, y in zip(ap, aq)]
                vp, vq = vcols[p], vcols[q]
                vcols[p] = [c * x - s * e * y for x, y in zip(vp, vq)]
                vcols[q] = [s * x + c * e * y for x, y in zip(vp, vq)]
        if not rotated:
            break
    norms = [math.sqrt(sum(abs(x) ** 2 for x in col)) for col in cols]
    order = sorted(range(n), key=lambda k: -norms[k])
    s = [norms[k] for k in order]
    big = s[0] if s else 0.0
    ucols = []
    for k in order:
        if norms[k] > 1e-13 * max(big, 1e-300):
            ucols.append([x / norms[k] for x in cols[k]])
        else:
            ucols.append([0j] * m)
    u = [[ucols[k][i] for k in range(n)] for i in range(m)]
    v = [[vcols[k][i] for k in order] for i in range(n)]
    return u, s, v


def water_fill(gains: list[float], p_total: float) -> list[float]:
    """Powers p_i >= 0 with sum P that maximize sum log2(1 + g_i p_i).

    A channel with gain 0 gets no power. The water level mu solves
    sum (mu - 1/g_i)^+ = P.
    """
    idx = sorted((i for i in range(len(gains)) if gains[i] > 0), key=lambda i: -gains[i])
    p = [0.0] * len(gains)
    if not idx or p_total <= 0:
        return p
    inv = [1.0 / gains[i] for i in idx]
    k = len(idx)
    while k > 1:
        mu = (p_total + sum(inv[:k])) / k
        if mu > inv[k - 1]:
            break
        k -= 1
    mu = (p_total + sum(inv[:k])) / k
    for t in range(k):
        p[idx[t]] = mu - inv[t]
    return p


def svd_precode(h: list[list[complex]], p_total: float, n0: float):
    """The SVD precoder of H for the power P and the noise level N0.

    Returns (f, u, s, p): f is the n by r precoder (column i is sqrt(p_i) v_i),
    u holds the r receive vectors as columns, s the r nonzero singular values
    and p the powers. The transmitter sends x = f d for r unit-energy symbols d.
    """
    u, s, v = svd(h)  # @line L1
    r = sum(1 for x in s if x > 1e-12 * s[0])  # @line L2
    p = water_fill([s[i] ** 2 / n0 for i in range(r)], p_total)  # @line L3
    f = [[v[t][i] * math.sqrt(p[i]) for i in range(r)] for t in range(len(v))]  # @line L4
    ur = [row[:r] for row in u]
    return f, ur, s[:r], p  # @line L5


def receive(y: list[complex], u: list[list[complex]]) -> list[complex]:
    """The receiver step z = U^H y, one output per stream."""
    return cbb.matvec(cbb.herm(u), y)  # @line L6


def rate(s: list[float], p: list[float], n0: float) -> float:
    """The rate sum log2(1 + s_i^2 p_i / N0) of the parallel channels, in bits per channel use."""
    return sum(math.log2(1.0 + si * si * pi / n0) for si, pi in zip(s, p))


def logdet_rate(h: list[list[complex]], q: list[list[complex]], n0: float) -> float:
    """log2 det(I + H Q H^H / N0) for an input covariance Q."""
    hq = cbb.matmul(cbb.matmul(h, q), cbb.herm(h))
    m = len(h)
    a = [[(1.0 if i == k else 0.0) + hq[i][k] / n0 for k in range(m)] for i in range(m)]
    return math.log2(abs(cbb.det(a)))
