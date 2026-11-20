# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-ratio-transmission/. The authors are listed in prov/17KZND.jsonl.

"""Maximum ratio transmission (MRT).

Single user, one receive antenna: the received signal is y = h^H x + w with
h in C^M and w ~ CN(0, N0). MRT sends x = sqrt(P) h / ||h|| s, which gives the
SNR P ||h||^2 / N0, the largest possible for the power P.

Single user, several receive antennas: y = H x + w. MRT sends along the
principal right singular vector v of H (the top eigenvector of H^H H), found
here by power iteration, and the receiver combines with H v. The SNR is
lambda_max(H^H H) P / N0.

Multiuser downlink (conjugate beamforming): y_k = h_k^H x + w_k for K users
and x = sum_k w_k s_k with w_k = sqrt(P / K) h_k / ||h_k||.
"""

import math

import cbb


def mrt_vector(h: list[complex], p_total: float) -> list[complex]:
    """The MRT precoder sqrt(P) h / ||h|| for the channel y = h^H x + w."""
    nrm = math.sqrt(cbb.norm2(h))  # @line L1
    if nrm == 0.0:
        raise ValueError("the channel is zero")
    return [math.sqrt(p_total) * x / nrm for x in h]  # @line L2


def principal_vector(h: list[list[complex]], tol: float = 1e-14, max_iter: int = 10000):
    """The top eigenvalue and a unit eigenvector of G = H^H H, by power iteration.

    Returns (lam, v). The iteration starts once from each nonzero column of G
    and keeps the best result. The columns span the range of G, which holds
    the top eigenvector, so at least one start is not orthogonal to it.
    """
    g = cbb.matmul(cbb.herm(h), h)  # @line L3
    n = len(g)
    best_lam, best_v = -1.0, None
    for k in range(n):
        v = [g[i][k] for i in range(n)]
        nrm = math.sqrt(cbb.norm2(v))
        if nrm == 0.0:
            continue
        v = [x / nrm for x in v]
        for _ in range(max_iter):  # @line L4
            gv = cbb.matvec(g, v)
            nrm = math.sqrt(cbb.norm2(gv))
            if nrm == 0.0:
                break
            v_next = [x / nrm for x in gv]
            # Fix the phase so that the iteration converges as a vector, not only up to a phase.
            ref = max(range(n), key=lambda i: abs(v_next[i]))
            ph = abs(v_next[ref]) / v_next[ref]
            v_next = [x * ph for x in v_next]
            diff = math.sqrt(sum(abs(a - b) ** 2 for a, b in zip(v_next, v)))
            v = v_next
            if diff < tol:
                break
        lam = cbb.dot(v, cbb.matvec(g, v)).real
        if lam > best_lam:
            best_lam, best_v = lam, v
    if best_v is None:
        raise ValueError("the channel is zero")
    return best_lam, best_v


def mrt_mimo(h: list[list[complex]], p_total: float):
    """MRT for y = H x + w. Returns (x_dir, combiner, gain).

    x_dir = sqrt(P) v is the precoder, combiner = H v / ||H v|| is the unit
    receive vector, and gain = lambda_max(H^H H), so the SNR is gain P / N0.
    """
    lam, v = principal_vector(h)  # @line L5
    hv = cbb.matvec(h, v)
    nrm = math.sqrt(cbb.norm2(hv))
    combiner = [x / nrm for x in hv]  # @line L6
    return [math.sqrt(p_total) * x for x in v], combiner, lam


def conjugate_beamforming(hs: list[list[complex]], p_total: float) -> list[list[complex]]:
    """The multiuser MRT precoder. hs[k] is h_k; column k of the M by K result is w_k."""
    k_users = len(hs)
    cols = [mrt_vector(h, p_total / k_users) for h in hs]  # @line L7
    m = len(hs[0])
    return [[cols[k][i] for k in range(k_users)] for i in range(m)]


def sinr(hs: list[list[complex]], w: list[list[complex]], n0: float) -> list[float]:
    """SINR_k = |h_k^H w_k|^2 / (sum over j != k of |h_k^H w_j|^2 + N0), for columns w_j of w."""
    k_users = len(hs)
    cols = [[row[j] for row in w] for j in range(len(w[0]))]
    out = []
    for k in range(k_users):
        gains = [abs(cbb.dot(hs[k], c)) ** 2 for c in cols]
        out.append(gains[k] / (sum(gains) - gains[k] + n0))
    return out
