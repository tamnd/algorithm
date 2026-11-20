# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-diagonalization/. The authors are listed in prov/VCA1WD.jsonl.

"""Block diagonalization (BD) precoding for the multiuser MIMO downlink.

User k has N_k antennas and receives y_k = H_k x + w_k with H_k an N_k by M
matrix and w_k ~ CN(0, N0 I). The transmitter sends x = sum_k W_k d_k. BD
puts the precoder W_k of user k in the null space of the other users'
channels, so H_j W_k = 0 for j != k, and the overall channel becomes block
diagonal. Inside its null space, each user gets SVD precoding, and one
water-filling over the singular values of all users splits the power P.

The SVD here is a one-sided Jacobi method, the same as on the SVD precoding
page; it is repeated so that this file stands alone.
"""

import math

import cbb


def svd(a: list[list[complex]], tol: float = 1e-15, max_sweeps: int = 100):
    """The SVD a = U diag(s) V^H of an m by n complex matrix, by one-sided Jacobi.

    Returns (u, s, v). s has n values in decreasing order. v is n by n and
    unitary. u is m by n; its column i is a_i / s_i for s_i > 0 and the zero
    vector for s_i = 0.
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
                ph = gamma / g
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
    """Powers p_i >= 0 with sum P that maximize sum log2(1 + g_i p_i); a zero gain gets no power."""
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


def null_space(a: list[list[complex]], m: int, rtol: float = 1e-10) -> list[list[complex]]:
    """An M by L matrix whose orthonormal columns span the null space of a (a has M columns, maybe no rows)."""
    if not a:
        return cbb.eye(m)
    _, s, v = svd(a)
    rank = sum(1 for x in s if x > rtol * s[0]) if s[0] > 0 else 0
    return [row[rank:] for row in v]


def bd_precoder(h_list: list[list[list[complex]]], p_total: float, n0: float):
    """The BD precoder for the user channels h_list (H_k is N_k by M).

    Returns (w_list, u_list, s_list, p_list): W_k is M by r_k, U_k holds the
    r_k receive vectors of user k as columns, s_k its gains and p_k its powers.
    """
    m = len(h_list[0][0])
    parts = []
    for k, hk in enumerate(h_list):
        others = [row for j, hj in enumerate(h_list) if j != k for row in hj]  # @line L1
        v0 = null_space(others, m)  # @line L2
        if not v0[0]:
            raise ValueError("user %d has no null space: too few transmit antennas" % k)
        u, s, v1 = svd(cbb.matmul(hk, v0))  # @line L3
        r = sum(1 for x in s if x > 1e-12 * max(s[0], 1e-300))
        parts.append((v0, u, s[:r], v1, r))
    gains = [x * x / n0 for (_, _, s, _, _) in parts for x in s]  # @line L4
    p_all = water_fill(gains, p_total)  # @line L5
    w_list, u_list, s_list, p_list = [], [], [], []
    pos = 0
    for v0, u, s, v1, r in parts:
        p = p_all[pos : pos + r]
        pos += r
        dirs = cbb.matmul(v0, [row[:r] for row in v1])
        w_list.append([[dirs[t][i] * math.sqrt(p[i]) for i in range(r)] for t in range(m)])  # @line L6
        u_list.append([row[:r] for row in u])
        s_list.append(s)
        p_list.append(p)
    return w_list, u_list, s_list, p_list  # @line L7


def rate_from_gains(s_list: list[list[float]], p_list: list[list[float]], n0: float) -> float:
    """sum over users and streams of log2(1 + s^2 p / N0)."""
    return sum(math.log2(1.0 + si * si * pi / n0) for s, p in zip(s_list, p_list) for si, pi in zip(s, p))


def sum_rate(h_list: list[list[list[complex]]], w_list: list[list[list[complex]]], n0: float) -> float:
    """sum_k log2 det(N0 I + sum_j H_k Q_j H_k^H) - log2 det(N0 I + sum_{j != k} H_k Q_j H_k^H), Q_j = W_j W_j^H.

    This is the rate of each user when it treats the other users' signals as noise.
    """
    total = 0.0
    for k, hk in enumerate(h_list):
        nk = len(hk)
        full = [[n0 if i == t else 0j for t in range(nk)] for i in range(nk)]
        intf = [row[:] for row in full]
        for j, wj in enumerate(w_list):
            if not wj[0]:
                continue
            hw = cbb.matmul(hk, wj)
            c = cbb.matmul(hw, cbb.herm(hw))
            full = cbb.add(full, c)
            if j != k:
                intf = cbb.add(intf, c)
        total += math.log2(abs(cbb.det(full))) - math.log2(abs(cbb.det(intf)))
    return total
