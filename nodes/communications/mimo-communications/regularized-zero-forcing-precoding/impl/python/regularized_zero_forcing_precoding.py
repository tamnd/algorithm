# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regularized-zero-forcing-precoding/. The authors are listed in prov/E77HBP.jsonl.

"""Regularized zero-forcing (RZF) precoding for the multiuser MISO downlink.

User k receives y_k = h_k^H x + w_k with w_k ~ CN(0, N0). The K by M matrix H
has row k equal to h_k^H. The transmitter sends x = W s with E[s s^H] = I and
tr(W^H W) = P, where

    F = H^H (H H^H + alpha I)^(-1),   W = beta F,   beta = sqrt(P / ||F||_F^2),

and alpha = K N0 / P by default. Every user scales its signal by 1 / beta.
With this alpha, F minimizes the sum MSE ||I - H F||_F^2 + (K N0 / P) ||F||_F^2
(the transmit Wiener filter). alpha -> 0 gives the zero-forcing channel
inversion and alpha -> infinity gives a precoder along H^H.
"""

import math

import cbb


def rzf_precoder(h: list[list[complex]], p_total: float, n0: float, alpha: float | None = None):
    """The RZF precoder of the K by M channel h. Returns (w, beta, f)."""
    k_users = len(h)
    if alpha is None:
        alpha = k_users * n0 / p_total  # @line L1
    g = cbb.matmul(h, cbb.herm(h))  # @line L2
    for i in range(k_users):
        g[i][i] += alpha  # @line L3
    f = cbb.herm(cbb.solve(g, h))  # @line L4
    # solve(g, h) = (H H^H + alpha I)^(-1) H, and its conjugate transpose is F.
    beta = math.sqrt(p_total / cbb.norm2(f))  # @line L5
    w = cbb.scale(beta, f)
    return w, beta, f  # @line L6


def sum_mse(h: list[list[complex]], f: list[list[complex]], p_total: float, n0: float) -> float:
    """E||s - y / beta||^2 = ||I - H F||_F^2 + (K N0 / P) ||F||_F^2 for W = beta F with tr(W^H W) = P."""
    k_users = len(h)
    e = cbb.sub(cbb.eye(k_users), cbb.matmul(h, f))
    return cbb.norm2(e) + k_users * n0 / p_total * cbb.norm2(f)


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
