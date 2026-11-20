# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-forcing-precoding/. The authors are listed in prov/3A1WH4.jsonl.

"""Zero-forcing precoding for the multiuser MISO downlink.

User k has one antenna and receives y_k = h_k^H x + w_k with w_k ~ CN(0, N0).
The K by M matrix H has row k equal to h_k^H, with K <= M and full row rank.
The transmitter sends x = W s with E[s s^H] = I and the power tr(W^H W) = P.

B = H^H (H H^H)^(-1) is the pseudoinverse of H, so H B = I. Column k of W is
b_k sqrt(q_k / c_k) with c_k = ||b_k||^2 = [(H H^H)^(-1)]_kk, so user k gets
h_k^H w_k = sqrt(q_k / c_k), no interference, and the SNR q_k / (c_k N0).
The powers q_k come from one of three rules:
- "waterfill": water-filling over the gains 1 / (c_k N0), the best sum rate;
- "equal": q_k = P / K;
- "inversion": the same SNR P / (N0 tr((H H^H)^(-1))) for every user.
"""

import math

import cbb


def water_fill(gains: list[float], p_total: float) -> list[float]:
    """Powers p_i >= 0 with sum P that maximize sum log2(1 + g_i p_i)."""
    idx = sorted(range(len(gains)), key=lambda i: -gains[i])
    inv = [1.0 / gains[i] for i in idx]
    k = len(idx)
    while k > 1 and (p_total + sum(inv[:k])) / k <= inv[k - 1]:
        k -= 1
    mu = (p_total + sum(inv[:k])) / k
    p = [0.0] * len(gains)
    for t in range(k):
        p[idx[t]] = mu - inv[t]
    return p


def zf_precoder(h: list[list[complex]], p_total: float, n0: float, mode: str = "waterfill"):
    """The ZF precoder of the K by M channel h. Returns (w, q, c).

    w is M by K (column k serves user k), q holds the user powers and c the
    noise gains c_k = [(H H^H)^(-1)]_kk.
    """
    k_users = len(h)
    hh = cbb.herm(h)  # M by K
    g = cbb.matmul(h, hh)  # @line L1
    b = cbb.herm(cbb.solve(g, h))  # @line L2
    # cbb.solve(g, h) is G^(-1) H, and its conjugate transpose is H^H G^(-1), since G is Hermitian.
    c = [sum(abs(b[i][k]) ** 2 for i in range(len(b))) for k in range(k_users)]  # @line L3
    if mode == "waterfill":
        q = water_fill([1.0 / (ck * n0) for ck in c], p_total)  # @line L4
    elif mode == "equal":
        q = [p_total / k_users] * k_users
    elif mode == "inversion":
        q = [p_total * ck / sum(c) for ck in c]
    else:
        raise ValueError("unknown mode")
    w = [[b[i][k] * math.sqrt(q[k] / c[k]) for k in range(k_users)] for i in range(len(b))]  # @line L5
    return w, q, c  # @line L6


def sinr(h: list[list[complex]], w: list[list[complex]], n0: float) -> list[float]:
    """SINR_k = |h_k^H w_k|^2 / (sum over j != k of |h_k^H w_j|^2 + N0)."""
    e = cbb.matmul(h, w)
    out = []
    for k in range(len(h)):
        sig = abs(e[k][k]) ** 2
        out.append(sig / (sum(abs(x) ** 2 for x in e[k]) - sig + n0))
    return out


def sum_rate(h: list[list[complex]], w: list[list[complex]], n0: float) -> float:
    """The sum rate sum log2(1 + SINR_k) in bits per channel use."""
    return sum(math.log2(1.0 + s) for s in sinr(h, w, n0))
